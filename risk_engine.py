# risk_engine.py - Emergency risk scoring and safety rules

# ---------------------------------------------------------------------------
# HIGH-RISK SYMPTOM INDICATORS
# Each entry: keyword/phrase → risk contribution points + reason
# ---------------------------------------------------------------------------

HIGH_RISK_SYMPTOMS = {
    "chest pain": {"points": 35, "reason": "Chest pain may indicate a cardiac emergency."},
    "chest tightness": {"points": 30, "reason": "Chest tightness can signal heart or lung problems."},
    "heart attack": {"points": 50, "reason": "Suspected heart attack – requires immediate emergency care."},
    "stroke": {"points": 50, "reason": "Suspected stroke – call emergency services immediately."},
    "shortness of breath": {"points": 30, "reason": "Severe breathing difficulty is a medical emergency."},
    "difficulty breathing": {"points": 30, "reason": "Breathing difficulty can be life-threatening."},
    "cant breathe": {"points": 35, "reason": "Inability to breathe requires immediate attention."},
    "unconscious": {"points": 50, "reason": "Loss of consciousness is always an emergency."},
    "fainted": {"points": 35, "reason": "Fainting may indicate a serious underlying condition."},
    "seizure": {"points": 45, "reason": "Seizures require immediate medical evaluation."},
    "convulsion": {"points": 45, "reason": "Convulsions are a medical emergency."},
    "paralysis": {"points": 45, "reason": "Sudden paralysis may indicate stroke or spinal injury."},
    "vomiting blood": {"points": 40, "reason": "Hematemesis (vomiting blood) is a medical emergency."},
    "blood in stool": {"points": 35, "reason": "Blood in stool may indicate serious GI bleeding."},
    "severe bleeding": {"points": 40, "reason": "Uncontrolled bleeding requires emergency intervention."},
    "high fever": {"points": 25, "reason": "Very high fever (>104°F/40°C) can be dangerous."},
    "stiff neck": {"points": 20, "reason": "Stiff neck with fever may indicate meningitis."},
    "sudden headache": {"points": 25, "reason": "Thunderclap headache can signal brain emergency."},
    "worst headache": {"points": 25, "reason": "Sudden severe headache needs urgent assessment."},
    "vision loss": {"points": 35, "reason": "Sudden vision loss may indicate a serious eye or brain event."},
    "double vision": {"points": 20, "reason": "New-onset double vision requires urgent evaluation."},
    "sudden weakness": {"points": 30, "reason": "Sudden limb weakness may indicate stroke."},
    "arm pain": {"points": 15, "reason": "Arm pain combined with chest symptoms may signal heart attack."},
    "jaw pain": {"points": 15, "reason": "Jaw pain with chest symptoms may signal heart attack."},
    "blue lips": {"points": 40, "reason": "Cyanosis (blue lips) indicates low oxygen – emergency."},
    "allergic reaction": {"points": 30, "reason": "Anaphylaxis / severe allergic reaction is an emergency."},
    "anaphylaxis": {"points": 50, "reason": "Anaphylaxis requires immediate epinephrine and emergency care."},
    "swollen throat": {"points": 35, "reason": "Throat swelling can block airway – emergency."},
    "throat closing": {"points": 40, "reason": "Throat closing is an airway emergency."},
    "poisoning": {"points": 45, "reason": "Suspected poisoning – call Poison Control and emergency services."},
    "overdose": {"points": 45, "reason": "Drug overdose requires immediate emergency attention."},
    "suicidal": {"points": 50, "reason": "Mental health crisis – contact emergency services or helpline now."},
    "self harm": {"points": 50, "reason": "Self-harm crisis – seek immediate mental health emergency support."},
    "severe abdominal pain": {
        "points": 25,
        "reason": "Severe abdominal pain may indicate appendicitis or other serious condition.",
    },
    "appendix": {"points": 25, "reason": "Possible appendicitis – seek immediate medical evaluation."},
    "diabetic coma": {"points": 45, "reason": "Diabetic emergency – requires immediate medical care."},
    "hypoglycemia": {"points": 25, "reason": "Very low blood sugar can be dangerous; treat immediately."},
    "severe dehydration": {
        "points": 25,
        "reason": "Severe dehydration, especially in infants/elderly, requires medical attention.",
    },
    "burn": {"points": 20, "reason": "Significant burns require immediate medical evaluation."},
    "head injury": {"points": 25, "reason": "Head trauma with symptoms needs urgent evaluation."},
}

# Moderate risk indicators
MODERATE_RISK_SYMPTOMS = {
    "fever": {"points": 10, "reason": "Persistent fever may need medical evaluation."},
    "high temperature": {"points": 10, "reason": "Elevated temperature – monitor and consult if prolonged."},
    "persistent cough": {"points": 10, "reason": "Persistent cough lasting > 2 weeks warrants evaluation."},
    "dizziness": {"points": 8, "reason": "Recurring dizziness may need assessment."},
    "fainting": {"points": 20, "reason": "Fainting episodes should be medically evaluated."},
    "pain": {"points": 5, "reason": "Pain that persists or worsens needs evaluation."},
    "nausea": {"points": 5, "reason": "Persistent nausea may require evaluation."},
    "vomiting": {"points": 8, "reason": "Persistent vomiting can lead to dehydration."},
    "bleeding": {"points": 15, "reason": "Any unexplained bleeding needs evaluation."},
    "rash": {"points": 8, "reason": "Widespread or worsening rash may require evaluation."},
    "swelling": {"points": 10, "reason": "Unexplained swelling may indicate an underlying condition."},
    "infection": {"points": 10, "reason": "Signs of infection may require antibiotic treatment."},
    "allergic": {"points": 15, "reason": "Allergic reactions can escalate – monitor carefully."},
}

# Age-based risk modifiers
AGE_RISK_MODIFIERS = {
    "infant": {"range": (0, 2), "multiplier": 1.4, "reason": "Infants are at higher risk for rapid deterioration."},
    "child": {"range": (3, 12), "multiplier": 1.2, "reason": "Children may deteriorate faster than adults."},
    "adult": {"range": (13, 59), "multiplier": 1.0, "reason": "Standard adult risk profile."},
    "senior": {"range": (60, 120), "multiplier": 1.3, "reason": "Seniors have higher risk for complications."},
}

# High-risk medicine combinations for risk scoring
HIGH_RISK_MED_COMBOS = [
    {
        "medicines": ["warfarin", "aspirin"],
        "points": 20,
        "reason": "High-risk anticoagulant + antiplatelet combination.",
    },
    {
        "medicines": ["warfarin", "ibuprofen"],
        "points": 20,
        "reason": "NSAID significantly increases warfarin bleeding risk.",
    },
    {
        "medicines": ["prednisolone", "ibuprofen"],
        "points": 15,
        "reason": "Corticosteroid + NSAID – high GI bleeding risk.",
    },
    {
        "medicines": ["diazepam", "gabapentin"],
        "points": 12,
        "reason": "Combined CNS depressants – respiratory depression risk.",
    },
]


def compute_risk_score(symptom_text, age=None, gender=None, medicines=None, dosages=None):
    """
    Compute emergency risk score (0–100) based on symptoms, age, gender, and medicines.

    Returns:
        dict with:
            - score (int 0–100)
            - level ("LOW" | "MODERATE" | "HIGH" | "CRITICAL")
            - color (for UI display)
            - reasons (list of contributing factors)
            - next_steps (list of recommended actions)
    """
    raw_score = 0
    reasons = []

    text_lower = symptom_text.lower() if symptom_text else ""

    # --- 1. Check high-risk symptoms ---
    for keyword, data in HIGH_RISK_SYMPTOMS.items():
        if keyword in text_lower:
            raw_score += data["points"]
            reasons.append(f"⚠️ {keyword.title()}: {data['reason']}")

    # --- 2. Check moderate-risk symptoms ---
    for keyword, data in MODERATE_RISK_SYMPTOMS.items():
        if keyword in text_lower:
            raw_score += data["points"]
            # Only add moderate reasons if not already critical
            if raw_score < 40:
                reasons.append(f"ℹ️ {keyword.title()}: {data['reason']}")

    # --- 3. Apply age modifier ---
    age_multiplier = 1.0
    age_reason = None
    if age is not None:
        for group, info in AGE_RISK_MODIFIERS.items():
            if info["range"][0] <= age <= info["range"][1]:
                age_multiplier = info["multiplier"]
                if age_multiplier > 1.0:
                    age_reason = f"Age group '{group}' ({age} yrs): {info['reason']}"
                break

    raw_score = int(raw_score * age_multiplier)
    if age_reason:
        reasons.append(f"👤 {age_reason}")

    # --- 4. Check high-risk medicine combinations ---
    if medicines:
        meds_lower = [m.lower().strip() for m in medicines]
        for combo in HIGH_RISK_MED_COMBOS:
            if all(m in meds_lower for m in combo["medicines"]):
                raw_score += combo["points"]
                reasons.append(f"💊 Medicine combo risk: {combo['reason']}")

    # --- 5. High dosage flag ---
    if dosages:
        for d in dosages:
            try:
                dose_val = float(str(d).replace("mg", "").replace("ml", "").strip())
                if dose_val > 1000:
                    raw_score += 10
                    reasons.append(f"💊 High dosage ({dose_val}mg) detected – verify dose with prescriber.")
                    break
            except (ValueError, TypeError):
                pass

    # Cap at 100
    final_score = min(raw_score, 100)

    # --- 6. Determine level ---
    if final_score >= 70:
        level = "CRITICAL"
        color = "red"
        next_steps = [
            "🚨 Call emergency services (112 / 911) immediately.",
            "Do NOT drive yourself to the hospital.",
            "Stay with the person and keep them calm.",
            "Describe all symptoms clearly to emergency responders.",
            "Do not give food or water unless instructed.",
        ]
    elif final_score >= 40:
        level = "HIGH"
        color = "orange"
        next_steps = [
            "🏥 Seek medical attention as soon as possible (same day).",
            "Call your doctor or visit an urgent care center.",
            "Do not ignore worsening symptoms.",
            "Take all prescribed medications and carry a list with you.",
            "If symptoms worsen rapidly, call emergency services.",
        ]
    elif final_score >= 20:
        level = "MODERATE"
        color = "yellow"
        next_steps = [
            "📋 Monitor your symptoms closely over the next 24–48 hours.",
            "Consult your doctor if symptoms do not improve.",
            "Stay hydrated and rest adequately.",
            "Avoid self-medicating without a prescription.",
            "Keep a note of any changes in your condition.",
        ]
    else:
        level = "LOW"
        color = "green"
        next_steps = [
            "✅ Symptoms appear mild at this time.",
            "Follow general self-care guidelines.",
            "Stay hydrated, rest, and eat a balanced diet.",
            "Monitor and consult a doctor if symptoms persist beyond 5–7 days.",
        ]

    if not reasons:
        reasons.append("No high-risk indicators detected from the provided description.")

    return {
        "score": final_score,
        "level": level,
        "color": color,
        "reasons": reasons,
        "next_steps": next_steps,
    }


def get_risk_label_color(level):
    """Return (emoji, hex_color) for a given risk level string."""
    mapping = {
        "LOW": ("✅", "#28a745"),
        "MODERATE": ("⚠️", "#ffc107"),
        "HIGH": ("🔶", "#fd7e14"),
        "CRITICAL": ("🚨", "#dc3545"),
    }
    return mapping.get(level, ("ℹ️", "#6c757d"))
