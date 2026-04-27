# med_db.py - Medicine database and interaction metadata

MED_DB = {
    "paracetamol": {
        "generic": "Acetaminophen",
        "salt": "Paracetamol",
        "category": "Analgesic/Antipyretic",
        "brand_names": ["Crocin", "Dolo", "Calpol", "Tylenol"],
    },
    #this for the varity
    "ibuprofen": {
        "generic": "Ibuprofen",
        "salt": "Ibuprofen",
        "category": "NSAID",
        "brand_names": ["Brufen", "Advil", "Nurofen"],
    },
    "aspirin": {
        "generic": "Aspirin",
        "salt": "Acetylsalicylic Acid",
        "category": "NSAID/Antiplatelet",
        "brand_names": ["Disprin", "Ecosprin"],
    },
    "metformin": {
        "generic": "Metformin",
        "salt": "Metformin Hydrochloride",
        "category": "Antidiabetic (Biguanide)",
        "brand_names": ["Glycomet", "Glucophage", "Janumet"],
    },
    "amlodipine": {
        "generic": "Amlodipine",
        "salt": "Amlodipine Besylate",
        "category": "Calcium Channel Blocker",
        "brand_names": ["Amlip", "Norvasc", "Amlong"],
    },
    "atorvastatin": {
        "generic": "Atorvastatin",
        "salt": "Atorvastatin Calcium",
        "category": "Statin (Lipid-lowering)",
        "brand_names": ["Lipitor", "Atorva", "Storvas"],
    },
    "omeprazole": {
        "generic": "Omeprazole",
        "salt": "Omeprazole Magnesium",
        "category": "Proton Pump Inhibitor",
        "brand_names": ["Prilosec", "Omez", "Ocid"],
    },
    "amoxicillin": {
        "generic": "Amoxicillin",
        "salt": "Amoxicillin Trihydrate",
        "category": "Antibiotic (Penicillin)",
        "brand_names": ["Novamox", "Moxikind", "Amoxil"],
    },
    "azithromycin": {
        "generic": "Azithromycin",
        "salt": "Azithromycin Dihydrate",
        "category": "Antibiotic (Macrolide)",
        "brand_names": ["Zithromax", "Azee", "Azithral"],
    },
    "cetirizine": {
        "generic": "Cetirizine",
        "salt": "Cetirizine Hydrochloride",
        "category": "Antihistamine",
        "brand_names": ["Zyrtec", "Cetzine", "Alerid"],
    },
    "montelukast": {
        "generic": "Montelukast",
        "salt": "Montelukast Sodium",
        "category": "Leukotriene Antagonist",
        "brand_names": ["Singulair", "Montair", "Menovit"],
    },
    "pantoprazole": {
        "generic": "Pantoprazole",
        "salt": "Pantoprazole Sodium",
        "category": "Proton Pump Inhibitor",
        "brand_names": ["Pantocid", "Pantop", "Protonix"],
    },
    "ciprofloxacin": {
        "generic": "Ciprofloxacin",
        "salt": "Ciprofloxacin Hydrochloride",
        "category": "Antibiotic (Fluoroquinolone)",
        "brand_names": ["Cipro", "Ciplox", "Cifran"],
    },
    "losartan": {
        "generic": "Losartan",
        "salt": "Losartan Potassium",
        "category": "ARB (Antihypertensive)",
        "brand_names": ["Cozaar", "Losar", "Repace"],
    },
    "doxycycline": {
        "generic": "Doxycycline",
        "salt": "Doxycycline Hyclate",
        "category": "Antibiotic (Tetracycline)",
        "brand_names": ["Vibramycin", "Doxybact", "Doxt"],
    },
    "clopidogrel": {
        "generic": "Clopidogrel",
        "salt": "Clopidogrel Bisulfate",
        "category": "Antiplatelet",
        "brand_names": ["Plavix", "Clopilet", "Deplatt"],
    },
    "sertraline": {
        "generic": "Sertraline",
        "salt": "Sertraline Hydrochloride",
        "category": "SSRI (Antidepressant)",
        "brand_names": ["Zoloft", "Serta", "Daxid"],
    },
    "metoprolol": {
        "generic": "Metoprolol",
        "salt": "Metoprolol Tartrate",
        "category": "Beta Blocker",
        "brand_names": ["Lopressor", "Metolar", "Betaloc"],
    },
    "diazepam": {
        "generic": "Diazepam",
        "salt": "Diazepam",
        "category": "Benzodiazepine",
        "brand_names": ["Valium", "Calmpose", "Diastat"],
    },
    "levothyroxine": {
        "generic": "Levothyroxine",
        "salt": "Levothyroxine Sodium",
        "category": "Thyroid Hormone",
        "brand_names": ["Synthroid", "Thyronorm", "Eltroxin"],
    },
    "warfarin": {
        "generic": "Warfarin",
        "salt": "Warfarin Sodium",
        "category": "Anticoagulant",
        "brand_names": ["Coumadin", "Warf", "Warfin"],
    },
    "gabapentin": {
        "generic": "Gabapentin",
        "salt": "Gabapentin",
        "category": "Anticonvulsant/Neuropathic",
        "brand_names": ["Neurontin", "Gabantin", "Gabacap"],
    },
    "ranitidine": {
        "generic": "Ranitidine",
        "salt": "Ranitidine Hydrochloride",
        "category": "H2 Blocker",
        "brand_names": ["Zantac", "Aciloc", "Rantac"],
    },
    "prednisolone": {
        "generic": "Prednisolone",
        "salt": "Prednisolone",
        "category": "Corticosteroid",
        "brand_names": ["Wysolone", "Omnacortil", "Deltacortril"],
    },
    "insulin": {
        "generic": "Insulin",
        "salt": "Insulin (various forms)",
        "category": "Antidiabetic (Insulin)",
        "brand_names": ["Humulin", "Novolin", "Lantus"],
    },
    "abciximab": {
        "generic": "Abciximab",
        "salt": "Abciximab",
        "category": "Antiplatelet (GPIIb/IIIa inhibitor)",
        "brand_names": ["ReoPro", "Abciximab"],
    },
    "vomilast": {
        "generic": "Vomilast",
        "salt": "Domperidone + Omeprazole",
        "category": "Antiemetic/PPI Combination",
        "brand_names": ["Vomilast"],
    },
    "doxylamine": {
        "generic": "Doxylamine",
        "salt": "Doxylamine Succinate",
        "category": "Antihistamine/Antiemetic",
        "brand_names": ["Unisom", "Diclegis"],
    },
    "pyridoxine": {
        "generic": "Pyridoxine",
        "salt": "Pyridoxine Hydrochloride",
        "category": "Vitamin B6",
        "brand_names": ["Neurobin", "B6"],
    },
    "folic acid": {
        "generic": "Folic Acid",
        "salt": "Folic Acid",
        "category": "Vitamin/Supplement",
        "brand_names": ["Folvite", "Foliter"],
    },
    "clarithromycin": {
        "generic": "Clarithromycin",
        "salt": "Clarithromycin",
        "category": "Antibiotic (Macrolide)",
        "brand_names": ["Zoclar", "Biaxin", "Klacid"],
    },
    "gestakind": {
        "generic": "Gestakind",
        "salt": "Dydrogesterone",
        "category": "Progestogen",
        "brand_names": ["Gestakind", "Duphaston"],
    },
}

# Known drug-drug interactions
INTERACTIONS = {
    frozenset(["aspirin", "warfarin"]): {
        "severity": "HIGH",
        "warning": "Aspirin + Warfarin: Increased bleeding risk. This combination significantly increases the risk of serious bleeding. Avoid unless prescribed by a doctor.",
    },
    frozenset(["aspirin", "clopidogrel"]): {
        "severity": "MODERATE",
        "warning": "Aspirin + Clopidogrel: Dual antiplatelet therapy increases bleeding risk. Use only under medical supervision.",
    },
    frozenset(["ibuprofen", "warfarin"]): {
        "severity": "HIGH",
        "warning": "Ibuprofen + Warfarin: NSAIDs can potentiate anticoagulant effect, significantly increasing bleeding risk.",
    },
    frozenset(["ibuprofen", "aspirin"]): {
        "severity": "MODERATE",
        "warning": "Ibuprofen + Aspirin: Concurrent use of two NSAIDs increases risk of GI bleeding and ulcers.",
    },
    frozenset(["metformin", "alcohol"]): {
        "severity": "MODERATE",
        "warning": "Metformin + Alcohol: Increases risk of lactic acidosis. Avoid alcohol while on Metformin.",
    },
    frozenset(["sertraline", "diazepam"]): {
        "severity": "MODERATE",
        "warning": "Sertraline + Diazepam: Increased sedation and CNS depression possible. Use with caution.",
    },
    frozenset(["ciprofloxacin", "metformin"]): {
        "severity": "MODERATE",
        "warning": "Ciprofloxacin + Metformin: Ciprofloxacin may affect blood glucose levels. Monitor closely.",
    },
    frozenset(["atorvastatin", "amlodipine"]): {
        "severity": "LOW",
        "warning": "Atorvastatin + Amlodipine: Amlodipine may slightly increase atorvastatin levels. Monitor for muscle pain (myopathy).",
    },
    frozenset(["levothyroxine", "metformin"]): {
        "severity": "LOW",
        "warning": "Levothyroxine + Metformin: Metformin may reduce thyroid hormone levels. Monitor thyroid function.",
    },
    frozenset(["omeprazole", "clopidogrel"]): {
        "severity": "MODERATE",
        "warning": "Omeprazole + Clopidogrel: Omeprazole reduces the antiplatelet effect of Clopidogrel. Consider alternative PPI.",
    },
    frozenset(["pantoprazole", "clopidogrel"]): {
        "severity": "LOW",
        "warning": "Pantoprazole + Clopidogrel: Minimal interaction compared to Omeprazole. Preferred PPI with Clopidogrel.",
    },
    frozenset(["ciprofloxacin", "doxycycline"]): {
        "severity": "LOW",
        "warning": "Ciprofloxacin + Doxycycline: Dual antibiotic therapy. Use only when both are clearly indicated.",
    },
    frozenset(["gabapentin", "diazepam"]): {
        "severity": "MODERATE",
        "warning": "Gabapentin + Diazepam: Combined CNS depressant effect; increased risk of drowsiness and respiratory depression.",
    },
    frozenset(["prednisolone", "ibuprofen"]): {
        "severity": "HIGH",
        "warning": "Prednisolone + Ibuprofen: Combination of corticosteroid and NSAID significantly increases GI ulcer and bleeding risk.",
    },
    frozenset(["metoprolol", "amlodipine"]): {
        "severity": "LOW",
        "warning": "Metoprolol + Amlodipine: Can cause additive blood pressure lowering. Monitor for hypotension.",
    },
}


def get_all_medicine_names():
    """Return all medicine names from the database."""
    return list(MED_DB.keys())


def get_medicine_info(name):
    """Get detailed information about a medicine."""
    return MED_DB.get(name.lower(), None)


def check_interactions(medicine_list):
    """Check for interactions between a list of medicines."""
    warnings = []
    checked = set()
    for i in range(len(medicine_list)):
        for j in range(i + 1, len(medicine_list)):
            pair = frozenset([medicine_list[i].lower(), medicine_list[j].lower()])
            if pair in INTERACTIONS and pair not in checked:
                warnings.append(INTERACTIONS[pair])
                checked.add(pair)
    return warnings
