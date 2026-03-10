# ocr_utils.py - Prescription OCR and text extraction utilities

import re
import json
import logging

logger = logging.getLogger(__name__)

# Try to import optional OCR libraries
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("pytesseract or Pillow not installed. OCR will use mock mode.")

# Try to import rapidfuzz for fuzzy matching
try:
    from rapidfuzz import process, fuzz
    FUZZ_AVAILABLE = True
except ImportError:
    FUZZ_AVAILABLE = False
    logger.warning("rapidfuzz not installed. Fuzzy matching disabled.")

# Try to import ollama for LLM support
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("ollama not installed. AI extraction will use rule-based fallback.")

# Path to Tesseract executable (Windows – adjust if needed)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def configure_tesseract(path=None):
    """Set the Tesseract executable path."""
    if OCR_AVAILABLE:
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = path or TESSERACT_PATH


def extract_text_from_image(image_file):
    """
    Extract raw text from an uploaded prescription image using Tesseract OCR.
    Returns extracted text string.
    """
    if not OCR_AVAILABLE:
        return "[OCR not available – install pytesseract and Pillow]"
    try:
        configure_tesseract()
        image = Image.open(image_file)
        # Pre-process: convert to grayscale for better OCR accuracy
        image = image.convert("L")
        text = pytesseract.image_to_string(image, config="--psm 6")
        return text.strip()
    except Exception as e:
        logger.error(f"OCR extraction error: {e}")
        return f"[OCR Error: {str(e)}]"


def find_medicine_fuzzy(name, medicine_names, threshold=75):
    """
    Use fuzzy matching to find the closest medicine name from the database.
    Returns matched name or None.
    """
    if not name:
        return None
    if not FUZZ_AVAILABLE:
        # Simple case-insensitive fallback
        name_lower = name.lower().strip()
        for med in medicine_names:
            if med.lower() == name_lower:
                return med
        return None

    # Clean the input
    cleaned = (
        name.lower()
        .replace("+", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("/", " ")
        .strip()
    )
    # Remove dosage numbers (e.g., "500mg", "10mg")
    cleaned = re.sub(r"\d+\s*(mg|ml|mcg|g|iu)\b", "", cleaned, flags=re.IGNORECASE).strip()

    if not cleaned:
        return None

    match, score, _ = process.extractOne(cleaned, medicine_names, scorer=fuzz.WRatio)
    if score >= threshold:
        return match
    return None


def parse_ocr_text_rule_based(raw_text, medicine_names):
    """
    Rule-based extraction of medicine names from raw OCR text.
    Returns a list of dicts with medicine and matched_db_name.
    """
    results = []
    lines = raw_text.split("\n")

    # Patterns that suggest a medicine line (e.g., starts with Tab, Cap, Inj, Syp)
    med_pattern = re.compile(
        r"^\s*(tab\.?|cap\.?|inj\.?|syp\.?|oint\.?|drops?|gel|cream|spray|susp\.?)?\s*([a-zA-Z][a-zA-Z0-9\s\-\+\/\.]+)",
        re.IGNORECASE,
    )

    seen = set()
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        m = med_pattern.match(line)
        if m:
            raw_name = m.group(2).strip()
            matched = find_medicine_fuzzy(raw_name, medicine_names)
            key = matched or raw_name.lower()
            if key not in seen:
                results.append(
                    {
                        "raw": raw_name,
                        "matched": matched,
                        "type": (m.group(1) or "").strip().upper() or "UNKNOWN",
                    }
                )
                seen.add(key)

    return results


def extract_medicines_with_llm(raw_text):
    """
    Use Ollama LLM (LLaMA 3) to extract medicines and their active salts from OCR text.
    Returns a list of dicts: {medicine, salt, type} or falls back to rule-based.
    """
    if not OLLAMA_AVAILABLE:
        return None  # Caller should fall back to rule-based

    prompt = f"""You are a medical data extraction assistant.
Given the following raw prescription text extracted via OCR, extract all medicine names and their active drug/salt components.

Return ONLY a valid JSON array with objects having these keys:
- "type": dosage form (e.g., TAB, CAP, SYP, INJ) or empty string
- "medicine": the medicine/brand name
- "salt": the active drug or salt name; use "None" if unknown

Do NOT include any explanation, markdown, or text outside the JSON array.

Prescription text:
\"\"\"
{raw_text}
\"\"\"

JSON output:"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.message.content.strip()
        # Extract JSON array from response
        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        # Try parsing the whole response as JSON
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"LLM JSON parse error: {e}")
        return None
    except Exception as e:
        logger.error(f"LLM extraction error: {e}")
        return None


def explain_interaction_with_llm(med1, med2, warning_text):
    """
    Use Ollama LLM to generate a patient-friendly explanation of a drug interaction.
    """
    if not OLLAMA_AVAILABLE:
        return None

    prompt = f"""You are a medical safety assistant providing educational (non-diagnostic) information.
Explain the following drug interaction between {med1} and {med2} in simple, clear language for a patient.
Keep the response to 2–3 sentences. Focus on what the patient should know and do.
Do not provide a diagnosis. End with: 'Always consult your doctor before making any changes.'

Interaction warning: {warning_text}"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.message.content.strip()
    except Exception as e:
        logger.error(f"LLM interaction explanation error: {e}")
        return None


def generate_symptom_explanation_with_llm(symptoms_text, basic_advice):
    """
    Use Ollama LLM to generate an enhanced, friendly educational response for symptoms.
    """
    if not OLLAMA_AVAILABLE:
        return None

    advice_summary = "; ".join(basic_advice[:5]) if basic_advice else "Follow general health guidelines."

    prompt = f"""You are a friendly, caring health educator providing non-diagnostic educational content.
A user has described the following symptoms: "{symptoms_text}"

Basic advice available: {advice_summary}

Write a warm, helpful 2–3 paragraph response that:
1. Acknowledges their symptoms with empathy
2. Provides practical home care tips, lifestyle suggestions, and simple breathing or yoga exercises
3. Mentions dietary tips for recovery
4. Includes a clear "Warning sign to watch" sentence at the end

Keep the tone friendly and reassuring. Do NOT diagnose. End with: 'Remember: if you experience severe or persistent symptoms, be sure to consult with a healthcare professional.'"""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.message.content.strip()
    except Exception as e:
        logger.error(f"LLM symptom explanation error: {e}")
        return None


def generate_side_effect_explanation_with_llm(age, gender, medicines, dosages, experience):
    """
    Use Ollama LLM to analyze a reported side-effect experience.
    """
    if not OLLAMA_AVAILABLE:
        return None

    prompt = f"""You are a medical safety educator providing non-diagnostic, educational information.
A user has reported the following post-medication experience:

- Age: {age}
- Gender: {gender}
- Medicines taken: {', '.join(medicines)}
- Dosages: {', '.join(str(d) for d in dosages)} mg
- Reported experience: {experience}

Provide a brief, empathetic educational response (2–3 sentences) that:
1. Acknowledges their experience
2. Highlights one possible contributing factor (educational, not diagnostic)
3. States one clear precaution they should watch for

End with: 'Please consult your doctor if symptoms persist or worsen.'
Do NOT diagnose. Keep it non-alarming and educational."""

    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.message.content.strip()
    except Exception as e:
        logger.error(f"LLM side-effect explanation error: {e}")
        return None
