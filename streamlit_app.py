# streamlit_app.py - MedSafe AI - Intelligent Medicine Safety Assistant
# Main Streamlit application with multi-tab layout

import streamlit as st
import datetime
import logging

from med_db import (
    MED_DB,
    get_all_medicine_names,
    get_medicine_info,
    check_interactions,
)
from symptom import (
    parse_symptoms,
    get_symptom_advice,
    SYMPTOM_DB,
    get_all_symptom_labels,
)
from ocr_utils import (
    OCR_AVAILABLE,
    OLLAMA_AVAILABLE,
    extract_text_from_image,
    find_medicine_fuzzy,
    parse_ocr_text_rule_based,
    extract_medicines_with_llm,
    explain_interaction_with_llm,
    generate_symptom_explanation_with_llm,
    generate_side_effect_explanation_with_llm,
)
from risk_engine import compute_risk_score, get_risk_label_color

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
logging.basicConfig(
    filename="medsafe_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MedSafe AI – Intelligent Medicine Safety Assistant",
    page_icon="+",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Custom CSS – dark theme matching project spec
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Global background ── */
    .stApp { background-color: #0e1117; color: #f0f0f0; }

    /* ── Header ── */
    .medsafe-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-bottom: 2px solid #e63946;
        padding: 18px 28px 14px 28px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    .medsafe-header h1 {
        color: #ffffff;
        font-size: 1.9rem;
        margin: 0;
        font-weight: 700;
    }
    .medsafe-header .subtitle { color: #adb5bd; font-size: 0.85rem; }

    /* ── Tab bar ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #c9d1d9;
        background-color: #21262d;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e63946 !important;
        color: #ffffff !important;
    }

    /* ── Cards ── */
    .med-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .interaction-high   { border-left: 4px solid #dc3545; }
    .interaction-mod    { border-left: 4px solid #fd7e14; }
    .interaction-low    { border-left: 4px solid #ffc107; }

    /* ── Risk gauge ── */
    .risk-score-box {
        text-align: center;
        padding: 20px;
        border-radius: 12px;
        font-size: 2.5rem;
        font-weight: 800;
    }
    .risk-critical { background-color: #2d0a0a; color: #ff4d4d; }
    .risk-high     { background-color: #2d1a00; color: #ff8c00; }
    .risk-moderate { background-color: #2d2500; color: #ffc107; }
    .risk-low      { background-color: #0a2d0a; color: #28a745; }

    /* ── AI Advice box ── */
    .ai-advice {
        background: linear-gradient(135deg, #0a3d1f, #0d4f1a);
        border: 1px solid #2ea043;
        border-radius: 10px;
        padding: 16px 20px;
        color: #88e6a0;
        font-size: 0.88rem;
        line-height: 1.65;
    }

    /* ── Warning box ── */
    .warning-box {
        background-color: #2d1a00;
        border: 1px solid #fd7e14;
        border-radius: 8px;
        padding: 12px 16px;
        color: #ffc07c;
        font-size: 0.85rem;
    }
    .error-box {
        background-color: #2d0a0a;
        border: 1px solid #dc3545;
        border-radius: 8px;
        padding: 12px 16px;
        color: #ff8080;
        font-size: 0.85rem;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 8px 20px;
    }
    .stButton > button:hover { background-color: #c1121f; }

    /* ── Medicine pill badge ── */
    .pill-badge {
        display: inline-block;
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        color: #79c0ff;
        margin: 2px;
    }

    /* Hide default Streamlit branding */
    #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="medsafe-header">
        <h1>MedSafe AI &ndash; Intelligent Medicine Safety Assistant</h1>
        <div class="subtitle">
            AI-powered medicine safety, prescription analysis, symptom guidance &amp; risk assessment &nbsp;|&nbsp;
            <em>For educational use only – not a substitute for professional medical advice</em>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────
if "ocr_medicines" not in st.session_state:
    st.session_state.ocr_medicines = []
if "interaction_results" not in st.session_state:
    st.session_state.interaction_results = []
if "side_effect_logs" not in st.session_state:
    st.session_state.side_effect_logs = []
if "risk_result" not in st.session_state:
    st.session_state.risk_result = None
if "last_ocr_text" not in st.session_state:
    st.session_state.last_ocr_text = ""

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Medicine Interaction Checker",
        "Prescription OCR",
        "Symptom & Doubt Solver",
        "Side-Effect Monitor",
        "Emergency Risk Predictor",
    ]
)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 – MEDICINE INTERACTION CHECKER
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## Medicine Interaction Checker")
    st.markdown(
        "Enter multiple medicine names (comma-separated) to check for known drug–drug interactions."
    )

    col_input, col_info = st.columns([2, 1])

    with col_input:
        med_input = st.text_area(
            "Enter medicines:",
            placeholder="e.g., Aspirin, Warfarin, Metformin, Ibuprofen",
            height=90,
            key="med_interaction_input",
        )

        check_btn = st.button("Check Interactions", key="check_interactions_btn")

    with col_info:
        st.markdown(
            """
            <div class="med-card" style="font-size:0.82rem; color:#adb5bd;">
            <b>How it works</b><br>
            1. Enter medicine names separated by commas<br>
            2. Uses fuzzy matching to identify medicines<br>
            3. Cross-checks against known interaction database<br>
            4. AI generates patient-friendly explanations
            </div>
            """,
            unsafe_allow_html=True,
        )

    if check_btn:
        if not med_input.strip():
            st.markdown(
                '<div class="error-box">Please enter at least one medicine name.</div>',
                unsafe_allow_html=True,
            )
        else:
            raw_meds = [m.strip() for m in med_input.split(",") if m.strip()]
            medicine_names = get_all_medicine_names()

            identified = []
            unrecognized = []

            with st.spinner("Identifying medicines and checking interactions..."):
                for raw in raw_meds:
                    matched = find_medicine_fuzzy(raw, medicine_names)
                    if matched:
                        identified.append(matched)
                    else:
                        unrecognized.append(raw)

            # Show identification results
            st.markdown("### Identified Medicines")
            if identified:
                badges = "".join(
                    f'<span class="pill-badge">{m.title()}</span>' for m in identified
                )
                if unrecognized:
                    badges += "".join(
                        f'<span class="pill-badge" style="color:#ff8080;">{m} (unrecognized)</span>'
                        for m in unrecognized
                    )
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="error-box">No medicines could be identified. Please check spelling or try different names.</div>',
                    unsafe_allow_html=True,
                )

            if identified:
                # Show medicine info
                with st.expander("Medicine Details", expanded=False):
                    for med in identified:
                        info = get_medicine_info(med)
                        if info:
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Medicine", med.title())
                            c2.metric("Generic", info["generic"])
                            c3.metric("Category", info["category"])
                            st.caption(f"Active Salt: {info['salt']} | Brands: {', '.join(info['brand_names'][:3])}")
                            st.divider()

                # Check interactions
                warnings = check_interactions(identified)
                st.session_state.interaction_results = warnings

                st.markdown("### Interaction Analysis")

                if not warnings:
                    st.success(
                        "No known interactions detected among the identified medicines. "
                        "Always consult your doctor before combining any medications."
                    )
                    logger.info(f"Interaction check: no interactions for {identified}")
                else:
                    st.markdown(
                        f'<div class="warning-box"><b>{len(warnings)} interaction(s) detected.</b> '
                        "Review carefully and consult your doctor.</div>",
                        unsafe_allow_html=True,
                    )
                    for i, w in enumerate(warnings, 1):
                        severity = w["severity"]
                        css_class = {
                            "HIGH": "interaction-high",
                            "MODERATE": "interaction-mod",
                            "LOW": "interaction-low",
                        }.get(severity, "")
                        st.markdown(
                            f"""
                            <div class="med-card {css_class}">
                                <b>Severity: {severity}</b><br>
                                {w['warning']}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # AI explanation
                        if OLLAMA_AVAILABLE:
                            meds_in_warning = [m for m in identified if m.lower() in w["warning"].lower()]
                            if len(meds_in_warning) >= 2:
                                with st.spinner(f"Generating AI explanation for interaction {i}..."):
                                    ai_exp = explain_interaction_with_llm(
                                        meds_in_warning[0], meds_in_warning[1], w["warning"]
                                    )
                                if ai_exp:
                                    st.markdown(
                                        f'<div class="ai-advice"><b>AI Safety Note:</b> {ai_exp}</div>',
                                        unsafe_allow_html=True,
                                    )

                    logger.info(f"Interaction check: {len(warnings)} warnings for {identified}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 – PRESCRIPTION OCR
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Extract Medicines From Prescription Image")
    st.markdown(
        "Upload a prescription image (JPG, PNG, JPEG). "
        "MedSafe AI uses OCR + AI to extract medicines and their active salts."
    )

    if not OCR_AVAILABLE:
        st.warning(
            "OCR libraries (pytesseract / Pillow) are not installed. "
            "Install them with: `pip install pytesseract Pillow`"
        )

    uploaded_file = st.file_uploader(
        "Upload prescription image",
        type=["jpg", "png", "jpeg"],
        key="prescription_upload",
    )

    col_ocr_btn, col_ocr_opt = st.columns([1, 2])
    with col_ocr_btn:
        ocr_btn = st.button("Read Prescription", key="ocr_btn", disabled=(uploaded_file is None))

    with col_ocr_opt:
        use_ai_extract = st.checkbox(
            "Use AI (LLaMA 3) for structured extraction",
            value=True,
            help="If disabled, uses rule-based OCR parsing only.",
            key="use_ai_extract",
        )

    if ocr_btn and uploaded_file is not None:
        with st.spinner("Reading prescription..."):
            raw_text = extract_text_from_image(uploaded_file)
            st.session_state.last_ocr_text = raw_text

        if raw_text.startswith("[OCR"):
            st.markdown(
                f'<div class="error-box">{raw_text}</div>', unsafe_allow_html=True
            )
        else:
            with st.expander("Raw OCR Text", expanded=False):
                st.text(raw_text)

            medicine_names = get_all_medicine_names()

            # LLM-based extraction
            extracted = None
            if use_ai_extract and OLLAMA_AVAILABLE:
                with st.spinner("AI extracting medicines and salts..."):
                    extracted = extract_medicines_with_llm(raw_text)

            # Fallback to rule-based
            if extracted is None:
                with st.spinner("Applying rule-based extraction..."):
                    rule_based = parse_ocr_text_rule_based(raw_text, medicine_names)
                    extracted = [
                        {
                            "type": r["type"],
                            "medicine": r["raw"],
                            "salt": r["matched"].title() if r["matched"] else "None",
                        }
                        for r in rule_based
                    ]

            st.session_state.ocr_medicines = extracted

            st.markdown("### Detected Medicines")

            if extracted:
                for item in extracted:
                    med_type = item.get("type", "").upper() or "MED"
                    medicine = item.get("medicine", "Unknown")
                    salt = item.get("salt", "None")
                    salt_display = f"→ *{salt}*" if salt and salt != "None" else "→ *None*"

                    # Validate against DB
                    db_match = find_medicine_fuzzy(medicine, medicine_names)
                    dot_color = "#28a745" if db_match else "#ffc107"
                    dot = f'<span style="color:{dot_color};">●</span>'

                    st.markdown(
                        f"<div class='med-card'>"
                        f"{dot} <b>{med_type}. {medicine.upper()}</b> {salt_display}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                # Show as JSON
                with st.expander("Structured JSON Output", expanded=False):
                    st.json(extracted)

                logger.info(f"OCR extracted {len(extracted)} medicines from prescription.")
            else:
                st.info("No medicines could be extracted. Try a clearer image.")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 – SYMPTOM & DOUBT SOLVER
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Symptom & Doubt Solver")
    st.markdown(
        "Describe your symptoms in plain language, or select from common symptoms below. "
        "Receive educational guidance including home remedies, yoga, diet tips, and warning signs."
    )

    col_sym1, col_sym2 = st.columns([3, 2])

    with col_sym1:
        symptom_text = st.text_area(
            "Describe your symptoms:",
            placeholder="e.g., I have a headache and back pain with slight fever...",
            height=100,
            key="symptom_text_input",
        )
        symptom_btn = st.button("Get Guidance", key="symptom_btn")

    with col_sym2:
        label_map = get_all_symptom_labels()
        selected_symptoms = st.multiselect(
            "Or select symptoms:",
            options=list(label_map.keys()),
            key="symptom_multiselect",
        )

    # Combine text + multiselect
    if symptom_btn or selected_symptoms:
        combined_keys = []

        if symptom_text.strip():
            combined_keys = parse_symptoms(symptom_text)

        for label in selected_symptoms:
            key = label_map.get(label)
            if key and key not in combined_keys:
                combined_keys.append(key)

        if not combined_keys:
            st.markdown(
                '<div class="warning-box">No recognizable symptoms found. '
                "Try describing differently or select from the list.</div>",
                unsafe_allow_html=True,
            )
        else:
            advice_dict = get_symptom_advice(combined_keys)

            # Basic rule-based advice
            st.markdown("### Basic Advice")
            all_basic_advice = []
            for key, data in advice_dict.items():
                st.markdown(
                    f"**{data['label']}**",
                )
                for tip in data["advice"]:
                    st.markdown(f"- {tip}")
                    all_basic_advice.append(tip)

                # Yoga
                if data["yoga"]:
                    st.markdown(f"*Yoga / Exercises:* {', '.join(data['yoga'])}")

                # Diet
                if data["diet"]:
                    with st.expander(f"Diet Tips for {data['label']}", expanded=False):
                        for d in data["diet"]:
                            st.markdown(f"- {d}")

                # Warning
                st.markdown(
                    f'<div class="warning-box">{data["warning"]}</div>',
                    unsafe_allow_html=True,
                )
                st.divider()

            # AI Enhanced Advice
            if OLLAMA_AVAILABLE:
                with st.spinner("Generating AI-enhanced advice..."):
                    ai_advice = generate_symptom_explanation_with_llm(
                        symptom_text or ", ".join(selected_symptoms),
                        all_basic_advice,
                    )
                if ai_advice:
                    st.markdown("### AI Enhanced Advice")
                    st.markdown(
                        f'<div class="ai-advice"><b>AI Enhanced Advice:</b><br><br>{ai_advice}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    "AI-enhanced explanations require Ollama (LLaMA 3). "
                    "Install Ollama and pull the llama3 model for richer guidance."
                )

            logger.info(f"Symptom guidance: {combined_keys}")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 4 – SIDE-EFFECT MONITOR
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## Experience & Side-Effect Monitor")
    st.markdown(
        "Log your post-medication experience. MedSafe AI analyzes your inputs and "
        "provides educational insights about possible contributing factors."
    )

    col_se1, col_se2 = st.columns(2)

    with col_se1:
        se_age = st.number_input(
            "Enter your age:",
            min_value=1,
            max_value=120,
            value=25,
            step=1,
            key="se_age",
        )
        se_gender = st.selectbox(
            "Select your gender:",
            options=["Male", "Female", "Other", "Prefer not to say"],
            key="se_gender",
        )

    with col_se2:
        se_medicines_raw = st.text_input(
            "Enter medicine(s) taken (comma-separated):",
            placeholder="e.g., Metformin, Aspirin",
            key="se_medicines",
        )
        se_dosages_raw = st.text_input(
            "Enter dose(s) taken (mg, comma-separated if multiple):",
            placeholder="e.g., 500, 100",
            key="se_dosages",
        )

    se_experience = st.text_area(
        "Describe your experience / side effects:",
        placeholder="e.g., I felt dizzy and had a stomach ache about 1 hour after taking Metformin...",
        height=90,
        key="se_experience",
    )

    se_btn = st.button("Analyze Experience", key="se_analyze_btn")

    if se_btn:
        if not se_experience.strip():
            st.markdown(
                '<div class="error-box">Please describe your experience before submitting.</div>',
                unsafe_allow_html=True,
            )
        else:
            se_medicines = [m.strip() for m in se_medicines_raw.split(",") if m.strip()]
            se_dosages = [d.strip() for d in se_dosages_raw.split(",") if d.strip()]

            if not se_medicines:
                st.markdown(
                    '<div class="warning-box">No medicines entered – analysis will be limited.</div>',
                    unsafe_allow_html=True,
                )

            # Log the entry
            log_entry = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "age": se_age,
                "gender": se_gender,
                "medicines": se_medicines,
                "dosages": se_dosages,
                "experience": se_experience,
            }
            st.session_state.side_effect_logs.append(log_entry)
            logger.info(f"Side-effect log: {log_entry}")

            # Display logged info
            st.markdown("### Logged Information")
            c1, c2, c3 = st.columns(3)
            c1.metric("Age", se_age)
            c2.metric("Gender", se_gender)
            c3.metric("Medicines Logged", len(se_medicines))

            if se_medicines:
                st.markdown(
                    "**Medicines:** "
                    + "".join(f'<span class="pill-badge">{m}</span>' for m in se_medicines),
                    unsafe_allow_html=True,
                )

            # AI Side-Effect Analysis
            if OLLAMA_AVAILABLE:
                with st.spinner("Analyzing experience with AI..."):
                    ai_se = generate_side_effect_explanation_with_llm(
                        se_age, se_gender, se_medicines or ["unspecified"],
                        se_dosages or ["unspecified"], se_experience
                    )
                if ai_se:
                    st.markdown("### AI Analysis")
                    st.markdown(
                        f'<div class="ai-advice"><b>Educational Analysis:</b><br><br>{ai_se}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("AI response unavailable. Check Ollama is running with 'llama3' model.")
            else:
                st.info(
                    "AI analysis requires Ollama (LLaMA 3). "
                    "Basic logging has been recorded."
                )

            # Quick risk check based on experience description
            quick_risk = compute_risk_score(se_experience, se_age)
            if quick_risk["score"] >= 30:
                st.markdown(
                    f'<div class="warning-box">Risk indicator detected in your description: '
                    f'<b>{quick_risk["level"]}</b> — '
                    f'{quick_risk["next_steps"][0]}</div>',
                    unsafe_allow_html=True,
                )

    # Side Effect Log History
    if st.session_state.side_effect_logs:
        with st.expander(
            f"Session Log ({len(st.session_state.side_effect_logs)} entries)", expanded=False
        ):
            for idx, entry in enumerate(reversed(st.session_state.side_effect_logs), 1):
                st.markdown(
                    f"**Entry {idx}** | {entry['timestamp']} | "
                    f"Age: {entry['age']} | {entry['gender']} | "
                    f"Medicines: {', '.join(entry['medicines']) or 'N/A'}"
                )
                st.caption(f"Experience: {entry['experience'][:120]}...")
                st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# TAB 5 – EMERGENCY RISK PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## Emergency Risk Predictor")
    st.markdown(
        "Describe your current symptoms and health context. "
        "MedSafe AI calculates a transparent risk score based on predefined safety rules."
    )

    col_rp1, col_rp2 = st.columns([2, 1])

    with col_rp1:
        rp_symptoms = st.text_area(
            "Describe your current symptoms in detail:",
            placeholder="e.g., I have sudden severe chest pain radiating to my left arm, sweating, and shortness of breath...",
            height=110,
            key="rp_symptoms",
        )

    with col_rp2:
        rp_age = st.number_input(
            "Your age:",
            min_value=1,
            max_value=120,
            value=30,
            step=1,
            key="rp_age",
        )
        rp_gender = st.selectbox(
            "Gender:",
            ["Male", "Female", "Other"],
            key="rp_gender",
        )
        rp_meds_raw = st.text_input(
            "Current medicines (optional):",
            placeholder="e.g., Warfarin, Aspirin",
            key="rp_meds",
        )

    rp_btn = st.button("Predict Emergency Risk", key="rp_btn")

    if rp_btn:
        if not rp_symptoms.strip():
            st.markdown(
                '<div class="error-box">Please describe your symptoms.</div>',
                unsafe_allow_html=True,
            )
        else:
            rp_meds = [m.strip() for m in rp_meds_raw.split(",") if m.strip()]

            with st.spinner("Computing risk score..."):
                result = compute_risk_score(
                    rp_symptoms, age=rp_age, gender=rp_gender, medicines=rp_meds
                )
            st.session_state.risk_result = result

            score = result["score"]
            level = result["level"]
            emoji_icon, hex_color = get_risk_label_color(level)
            css_class = f"risk-{level.lower()}"

            # Score display
            st.markdown("### Risk Assessment Result")

            col_score, col_level = st.columns([1, 2])

            with col_score:
                st.markdown(
                    f'<div class="risk-score-box {css_class}">{score}<br>'
                    f'<span style="font-size:1rem;">/ 100</span></div>',
                    unsafe_allow_html=True,
                )

            with col_level:
                st.markdown(f"### Risk Level: **{level}**")
                st.progress(min(score / 100, 1.0))
                st.caption(f"Score: {score}/100 — based on symptom analysis, age group, and medicine profile.")

            # Contributing factors
            st.markdown("### Contributing Factors")
            for reason in result["reasons"]:
                st.markdown(f"- {reason}")

            # Next steps
            st.markdown("### Recommended Next Steps")
            next_class = "error-box" if level in ("CRITICAL", "HIGH") else "warning-box"
            steps_html = "".join(f"<li>{step}</li>" for step in result["next_steps"])
            st.markdown(
                f'<div class="{next_class}"><ul>{steps_html}</ul></div>',
                unsafe_allow_html=True,
            )

            # Disclaimer
            st.markdown(
                """
                <div class="med-card" style="border-left:4px solid #6c757d; font-size:0.78rem; color:#adb5bd;">
                <b>Disclaimer:</b> This risk score is for educational awareness only and is NOT a medical diagnosis.
                The assessment is based on predefined rules and does not replace professional clinical evaluation.
                Always consult a qualified healthcare provider for any medical concern.
                </div>
                """,
                unsafe_allow_html=True,
            )

            logger.info(
                f"Risk prediction: score={score}, level={level}, age={rp_age}, "
                f"gender={rp_gender}, meds={rp_meds}"
            )

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown(
    """
    <hr style="border-color:#30363d; margin-top:40px;">
    <div style="text-align:center; color:#6c757d; font-size:0.75rem; padding-bottom:20px;">
    <b>MedSafe AI</b> &nbsp;|&nbsp; Intelligent Medicine Safety Assistant &nbsp;|&nbsp;
    For educational and research purposes only &nbsp;|&nbsp;
    Not a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    """,
    unsafe_allow_html=True,
)
