import pandas as pd
from rapidfuzz import process, fuzz

# --- Load NIRF data (2016 + 2025) ---
url_2016 = "https://www.nirfindia.org/Rankings/2016/engg.html"
nirf_2016 = pd.read_html(url_2016)[0]
nirf_2016 = nirf_2016[nirf_2016["INSTITUTE ID"].astype(str).str.startswith("NIRF")]
nirf_2016["Name"] = (
    nirf_2016["Name"]
    .astype(str)
    .str.replace(r"More Details.*", "", regex=True)
    .str.strip()
)

url_2025 = "https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html"
nirf_2025 = pd.read_html(url_2025)[0]
nirf_2025["Name"] = (
    nirf_2025["Name"]
    .astype(str)
    .str.replace(r"More Details.*", "", regex=True)
    .str.strip()
)

# Combine and normalize NIRF universities
nirf_univs = pd.concat([nirf_2016["Name"], nirf_2025["Name"]]).drop_duplicates().reset_index(drop=True)
nirf_univs_norm = nirf_univs.str.strip().str.lower().str.replace(",", "", regex=False)

# Load Excel list and normalize
excel_df = pd.read_excel("list of schools.xlsx")
excel_univs = excel_df["college_name"].dropna().drop_duplicates().reset_index(drop=True)
excel_univs_norm = excel_univs.str.strip().str.lower().str.replace(",", "", regex=False)

# --- Fuzzy Match Function ---
def fuzzy_match(query, choices, threshold=90):
    """
    Match query string against list of choices.
    Returns the best match from the original list if score >= threshold, else None.
    """
    match_norm, score, idx = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return excel_univs.iloc[idx], score  # return original Excel name
    return None, score

# --- Compare NIRF vs Excel ---
results = []
for nirf_uni, nirf_uni_norm in zip(nirf_univs, nirf_univs_norm):
    match, score = fuzzy_match(nirf_uni_norm, excel_univs_norm, threshold=90)
    status = "Found" if match else "Not Found"
    results.append([nirf_uni, match, score, status])

comparison = pd.DataFrame(results, columns=["nirf_univ", "matched_excel_univ", "match_score", "status"])

# Save output
comparison.to_excel("nirf_vs_excel_fuzzy_normalized.xlsx", index=False)

print("✅ Fuzzy normalized comparison saved as nirf_vs_excel_fuzzy_normalized.xlsx")
import pandas as pd