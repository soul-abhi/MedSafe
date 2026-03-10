# symptom.py - Rule-based symptom advice logic

SYMPTOM_DB = {
    "fever": {
        "icon": "🌡️",
        "label": "Fever",
        "advice": [
            "Stay hydrated – drink plenty of water, ORS, or coconut water.",
            "Rest adequately and avoid physical exertion.",
            "Use a cool damp cloth on forehead for comfort.",
            "Take paracetamol (as directed) to manage high temperature.",
            "Wear light, breathable clothing.",
            "Monitor temperature every few hours.",
        ],
        "yoga": ["Shavasana (Corpse Pose) for full-body rest"],
        "diet": [
            "Warm soups, khichdi, and easily digestible foods",
            "Avoid oily, spicy, or heavy meals",
            "Increase fluid intake (water, herbal tea, fresh juices)",
        ],
        "warning": "Seek immediate medical attention if fever exceeds 103°F (39.4°C), lasts more than 3 days, or is accompanied by severe headache, stiff neck, or rash.",
    },
    "headache": {
        "icon": "🤕",
        "label": "Headache",
        "advice": [
            "Rest in a quiet, dark room away from screens.",
            "Apply a cold or warm compress to your forehead or neck.",
            "Stay well hydrated – dehydration is a common cause.",
            "Practice slow, deep breathing to reduce tension.",
            "Massage temples gently in circular motions.",
            "Avoid loud noise and bright lights.",
        ],
        "yoga": [
            "Balasana (Child's Pose)",
            "Uttanasana (Standing Forward Bend)",
            "Shavasana (Corpse Pose)",
        ],
        "diet": [
            "Avoid caffeine excess and alcohol",
            "Eat regular meals to prevent blood sugar dips",
            "Magnesium-rich foods: almonds, spinach, bananas",
        ],
        "warning": "Seek urgent care if headache is sudden and severe ('thunderclap'), associated with vision changes, weakness, confusion, or follows a head injury.",
    },
    "cough": {
        "icon": "😷",
        "label": "Cough",
        "advice": [
            "Gargle with warm salt water 2–3 times daily.",
            "Drink warm water, herbal tea, or honey-ginger tea.",
            "Use steam inhalation to loosen congestion.",
            "Avoid cold drinks, ice cream, and dusty environments.",
            "Keep the head slightly elevated while sleeping.",
            "Humidify your room if the air is dry.",
        ],
        "yoga": [
            "Pranayama – Anulom Vilom (alternate nostril breathing)",
            "Bhujangasana (Cobra Pose) to open the chest",
        ],
        "diet": [
            "Warm turmeric milk before sleep",
            "Honey and ginger juice with warm water",
            "Avoid cold, sour, and refrigerated foods",
        ],
        "warning": "See a doctor if cough persists more than 2 weeks, produces blood or thick coloured mucus, or is accompanied by shortness of breath or chest pain.",
    },
    "cold": {
        "icon": "🤧",
        "label": "Cold / Nasal Congestion",
        "advice": [
            "Rest and stay warm.",
            "Use steam inhalation with a few drops of eucalyptus oil.",
            "Blow nose gently; avoid hard blowing.",
            "Drink warm fluids frequently.",
            "Use saline nasal drops for congestion relief.",
            "Avoid dairy products which may thicken mucus.",
        ],
        "yoga": ["Jala Neti (nasal cleansing)", "Kapalbhati Pranayama (gentle)"],
        "diet": [
            "Warm soups with garlic and ginger",
            "Tulsi (basil) tea",
            "Increase Vitamin C intake – citrus fruits, amla",
        ],
        "warning": "Consult a doctor if symptoms worsen after 10 days, you develop high fever, or experience facial pain/pressure suggesting sinusitis.",
    },
    "stomach pain": {
        "icon": "🫃",
        "label": "Stomach Pain / Abdominal Discomfort",
        "advice": [
            "Rest and avoid solid food temporarily; try clear liquids first.",
            "Apply a warm heating pad to the abdomen.",
            "Avoid spicy, fatty, or fried foods.",
            "Try peppermint tea or warm ginger water.",
            "Avoid lying down immediately after eating.",
            "Small, frequent meals rather than large portions.",
        ],
        "yoga": ["Pawanmuktasana (Wind-Relieving Pose)", "Vajrasana after meals"],
        "diet": [
            "BRAT diet: Bananas, Rice, Applesauce, Toast",
            "Avoid alcohol, caffeine, and carbonated drinks",
            "Probiotic-rich foods: curd, buttermilk",
        ],
        "warning": "Seek emergency care if pain is severe and sudden, accompanied by vomiting blood, black stools, high fever, or the abdomen is rigid and tender.",
    },
    "nausea": {
        "icon": "🤢",
        "label": "Nausea / Vomiting",
        "advice": [
            "Sip small amounts of clear fluids frequently.",
            "Avoid strong smells and greasy foods.",
            "Eat small, bland meals (crackers, toast).",
            "Rest in a cool, ventilated space.",
            "Try ginger tea or ginger candy for relief.",
            "Avoid lying flat immediately after eating.",
        ],
        "yoga": ["Shavasana", "Gentle Pranayama breathing"],
        "diet": [
            "Cold or room-temperature foods (hot foods may worsen nausea)",
            "Ginger ale or ginger tea",
            "Avoid dairy and high-fat foods",
        ],
        "warning": "Seek help if vomiting is persistent (> 24 hours), contains blood, or is accompanied by severe abdominal pain, dizziness, or signs of dehydration.",
    },
    "back pain": {
        "icon": "🔙",
        "label": "Back Pain",
        "advice": [
            "Apply a hot compress to the affected area.",
            "Avoid long sitting hours; take breaks every 30–45 minutes.",
            "Do gentle stretching exercises.",
            "Sleep on a firm mattress in a comfortable position.",
            "Use ergonomic seating and maintain proper posture.",
            "Avoid heavy lifting; if lifting, bend from knees.",
        ],
        "yoga": [
            "Bhujangasana (Cobra Pose)",
            "Cat-Cow Stretch",
            "Bridge Pose (Setu Bandhasana)",
            "Child's Pose (Balasana)",
        ],
        "diet": [
            "Anti-inflammatory foods: turmeric, ginger, omega-3 fatty acids",
            "Calcium-rich foods: dairy, leafy greens",
            "Vitamin D: sunlight exposure and fortified foods",
        ],
        "warning": "If pain radiates to your legs, causes numbness/tingling, or is accompanied by bladder/bowel changes, seek medical evaluation immediately.",
    },
    "dizziness": {
        "icon": "😵",
        "label": "Dizziness / Vertigo",
        "advice": [
            "Sit or lie down immediately to avoid falls.",
            "Move slowly when changing positions (lying → sitting → standing).",
            "Stay well hydrated.",
            "Avoid caffeine, alcohol, and tobacco.",
            "Ensure adequate sleep.",
            "Try the Epley maneuver for BPPV-related vertigo (if advised by a doctor).",
        ],
        "yoga": ["Shavasana", "Seated Meditation and Pranayama"],
        "diet": [
            "Reduce salt intake to manage inner ear pressure",
            "Small, frequent meals to stabilize blood sugar",
            "Stay hydrated with water and electrolyte drinks",
        ],
        "warning": "Seek emergency care if dizziness is severe, sudden, accompanied by chest pain, difficulty speaking, double vision, severe headache, or weakness in limbs.",
    },
    "chest pain": {
        "icon": "💔",
        "label": "Chest Pain",
        "advice": [
            "Stop any physical activity immediately.",
            "Sit or lie down in a comfortable position.",
            "Loosen tight clothing.",
            "Do not ignore chest pain – it can be serious.",
        ],
        "yoga": [],
        "diet": [],
        "warning": "IMPORTANT: Chest pain can be a sign of a heart attack. Call emergency services (112/911) immediately if pain is crushing, squeezing, spreads to arm/jaw/back, or is accompanied by sweating, nausea, or shortness of breath.",
    },
    "shortness of breath": {
        "icon": "😮‍💨",
        "label": "Shortness of Breath",
        "advice": [
            "Sit upright or in a forward-leaning position.",
            "Stay calm and try slow, controlled breathing.",
            "Avoid triggers like smoke, dust, or allergens.",
            "Use prescribed inhaler if available.",
        ],
        "yoga": ["Pursed-lip breathing", "Diaphragmatic (belly) breathing"],
        "diet": [
            "Avoid heavy, large meals that press on the diaphragm",
            "Anti-inflammatory diet",
        ],
        "warning": "Seek IMMEDIATE emergency care if breathing difficulty is sudden, severe, or accompanied by chest pain, bluish lips, or confusion.",
    },
    "eye pain": {
        "icon": "👁️",
        "label": "Eye Pain / Redness",
        "advice": [
            "Wash eyes gently with clean, cool water.",
            "Avoid rubbing your eyes.",
            "Reduce screen brightness and take screen breaks.",
            "Apply a cool, damp cloth over closed eyes.",
            "Avoid contact lenses until the irritation resolves.",
            "Use lubricating eye drops if prescribed.",
        ],
        "yoga": ["Palming (rub palms together and place over closed eyes)", "Eye rotations"],
        "diet": [
            "Vitamin A-rich foods: carrots, sweet potato, spinach",
            "Omega-3 fatty acids for eye health",
            "Stay hydrated",
        ],
        "warning": "Seek urgent eye evaluation if you experience sudden vision loss, severe eye pain, halos around lights, or if foreign body is suspected in the eye.",
    },
    "skin rash": {
        "icon": "🔴",
        "label": "Skin Rash",
        "advice": [
            "Avoid scratching the affected area.",
            "Apply a cool, damp cloth to soothe irritation.",
            "Use mild, fragrance-free soap and moisturizer.",
            "Avoid potential allergens: new foods, detergents, or fabrics.",
            "Wear loose, breathable cotton clothing.",
        ],
        "yoga": [],
        "diet": [
            "Anti-inflammatory foods: turmeric, green tea",
            "Avoid known food allergens",
            "Stay hydrated",
        ],
        "warning": "Seek immediate care if rash is spreading rapidly, accompanied by difficulty breathing, swelling of face/lips, or follows taking a new medication.",
    },
    "joint pain": {
        "icon": "🦴",
        "label": "Joint Pain / Arthritis",
        "advice": [
            "Apply ice/cold pack for acute injury (first 48 hours).",
            "Apply warm compress for chronic joint pain.",
            "Gentle range-of-motion exercises.",
            "Maintain a healthy weight to reduce joint load.",
            "Avoid sitting in one position for too long.",
        ],
        "yoga": ["Trikonasana (Triangle Pose)", "Vrikshasana (Tree Pose)", "Gentle joint rotations"],
        "diet": [
            "Anti-inflammatory: turmeric, ginger, omega-3 fatty acids",
            "Calcium and Vitamin D for bone health",
            "Avoid processed foods, refined sugar, and alcohol",
        ],
        "warning": "Consult a doctor if joint pain is severe, associated with significant swelling, redness and warmth, or if you have symptoms in multiple joints.",
    },
    "insomnia": {
        "icon": "😴",
        "label": "Insomnia / Sleep Issues",
        "advice": [
            "Maintain a consistent sleep schedule (same time every day).",
            "Avoid screens (phones, TV) at least 1 hour before bed.",
            "Keep your bedroom cool, dark, and quiet.",
            "Avoid caffeine after 2 PM.",
            "Try relaxation techniques before bed.",
        ],
        "yoga": [
            "Viparita Karani (Legs-up-the-Wall Pose)",
            "Balasana (Child's Pose)",
            "4-7-8 breathing: inhale 4 counts, hold 7, exhale 8",
        ],
        "diet": [
            "Warm milk or chamomile tea before bed",
            "Light dinner at least 2 hours before sleep",
            "Avoid alcohol – it disrupts sleep quality",
        ],
        "warning": "Consult a doctor if insomnia persists for more than a month, significantly affects daily functioning, or is accompanied by mood changes, anxiety, or depression.",
    },
}

# Map common keywords/phrases to symptom keys
SYMPTOM_KEYWORDS = {
    "fever": ["fever", "temperature", "hot", "chills", "pyrexia"],
    "headache": ["headache", "head ache", "head pain", "migraine", "head hurts"],
    "cough": ["cough", "coughing", "dry cough", "wet cough", "coughed"],
    "cold": ["cold", "runny nose", "stuffy nose", "nasal", "sneezing", "sneeze", "congestion"],
    "stomach pain": ["stomach", "abdomen", "abdominal", "belly", "tummy", "stomach ache", "stomach pain"],
    "nausea": ["nausea", "nauseous", "vomit", "vomiting", "throwing up", "sick to stomach"],
    "back pain": ["back pain", "back ache", "lower back", "spine", "lumbar", "back hurts"],
    "dizziness": ["dizzy", "dizziness", "vertigo", "lightheaded", "spinning"],
    "chest pain": ["chest pain", "chest tightness", "chest pressure", "heart pain", "palpitation"],
    "shortness of breath": ["shortness of breath", "breathless", "breathing difficulty", "cant breathe", "dyspnea"],
    "eye pain": ["eye pain", "eye ache", "red eye", "redness in eye", "eye irritation", "eye", "red eyes"],
    "skin rash": ["rash", "skin rash", "itching", "hives", "urticaria", "skin irritation"],
    "joint pain": ["joint pain", "joint ache", "knee pain", "arthritis", "swollen joint"],
    "insomnia": ["insomnia", "can't sleep", "sleepless", "sleep problem", "not sleeping", "difficulty sleeping"],
}


def parse_symptoms(text):
    """Parse symptom text and return matched symptom keys."""
    text_lower = text.lower()
    found = []
    for key, keywords in SYMPTOM_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower and key not in found:
                found.append(key)
                break
    return found


def get_symptom_advice(symptom_keys):
    """Return advice for a list of symptom keys."""
    results = {}
    for key in symptom_keys:
        if key in SYMPTOM_DB:
            results[key] = SYMPTOM_DB[key]
    return results


def get_all_symptom_labels():
    """Return a label→key mapping for UI dropdowns."""
    return {v["label"]: k for k, v in SYMPTOM_DB.items()}
