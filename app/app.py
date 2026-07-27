from pathlib import Path
import streamlit as st
import numpy as np
import joblib
import json
import pandas as pd

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Premium Estimate | Insurance Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Load model & schema
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "model" / "insurance_model.joblib")

with open(BASE_DIR / "columns.json", "r") as f:
    columns = json.load(f)

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Inter:wght@400;500;600&display=swap');

    :root {
        --navy: #142433;
        --navy-soft: #1F3A4D;
        --teal: #0E8388;
        --slate: #5B6B79;
        --bg: #F5F7F9;
        --card: #FFFFFF;
        --line: #E4E9ED;
        --good: #1E8E5A;
        --warn: #B7791F;
        --bad: #B3261E;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: var(--navy);
    }

    .stApp {
        background: var(--bg);
    }

    /* Center the whole app in one comfortable frame instead of full-bleed */
    .block-container {
        max-width: 1180px;
        padding-top: 1.6rem;
        padding-bottom: 2rem;
        margin: 0 auto;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif;
        color: var(--navy);
        letter-spacing: -0.01em;
    }

    /* Header band */
    .app-header {
        background: linear-gradient(135deg, var(--navy) 0%, var(--navy-soft) 100%);
        padding: 2.1rem 2.4rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 24px rgba(20, 36, 51, 0.18);
    }
    .app-header .eyebrow {
        color: #8FD8DA;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .app-header h1 {
        color: #FFFFFF;
        font-size: 1.9rem;
        margin: 0 0 0.3rem 0;
    }
    .app-header p {
        color: #C7D4DC;
        font-size: 0.95rem;
        margin: 0;
    }

    /* Card */
    .card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 2px rgba(20, 36, 51, 0.04);
    }
    .card h3 {
        font-size: 1.02rem;
        margin-top: 0;
        margin-bottom: 0.9rem;
        border-bottom: 1px solid var(--line);
        padding-bottom: 0.6rem;
    }

    /* Result metric */
    .result-label {
        font-size: 0.82rem;
        color: var(--slate);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .result-value {
        font-family: 'Manrope', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: var(--navy);
        line-height: 1.1;
    }
    .result-sub {
        color: var(--slate);
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    /* Risk meter */
    .meter-track {
        position: relative;
        height: 10px;
        border-radius: 6px;
        background: linear-gradient(90deg, #1E8E5A 0%, #B7791F 50%, #B3261E 100%);
        margin: 1.1rem 0 0.6rem 0;
    }
    .meter-marker {
        position: absolute;
        top: -6px;
        width: 3px;
        height: 22px;
        background: var(--navy);
        border-radius: 2px;
    }
    .meter-scale {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        color: var(--slate);
    }
    .risk-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .risk-low { background: #E4F3EA; color: var(--good); }
    .risk-med { background: #FBF0DC; color: var(--warn); }
    .risk-high { background: #F9E3E1; color: var(--bad); }

    /* Recommendation row */
    .rec-row {
        display: flex;
        gap: 0.7rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid var(--line);
        font-size: 0.9rem;
        color: var(--navy-soft);
    }
    .rec-row:last-child { border-bottom: none; }
    .rec-dot {
        min-width: 6px;
        height: 6px;
        margin-top: 0.45rem;
        border-radius: 50%;
        background: var(--teal);
    }

    /* Summary table */
    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 0.45rem 0;
        border-bottom: 1px solid var(--line);
        font-size: 0.88rem;
    }
    .summary-item:last-child { border-bottom: none; }
    .summary-item .k { color: var(--slate); }
    .summary-item .v { font-weight: 600; color: var(--navy); }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--navy);
    }
    /* Light text only for labels/captions/headings, NOT inside the white input controls */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #E7EEF2 !important;
        font-weight: 600;
        font-size: 0.85rem;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #9FB0BA !important;
    }
    /* Slider min/max/current-value labels sit directly on the navy background */
    section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] [data-testid="stTickBarMax"],
    section[data-testid="stSidebar"] [data-testid="stThumbValue"] {
        color: #E7EEF2 !important;
        background: transparent !important;
    }
    /* Selectbox / dropdown control keeps a white field with dark, readable text */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #33495B !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color: var(--navy) !important;
    }

    /* ---- Slider recolor (teal instead of Streamlit's default red) ---- */
    /* Track fill (the colored portion of the bar) */
    div[data-baseweb="slider"] > div > div > div {
        background: var(--teal) !important;
    }
    /* Thumb (the round drag handle) */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--teal) !important;
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 4px rgba(14, 131, 136, 0.18) !important;
    }
    /* Floating value bubble shown above the thumb while dragging */
    section[data-testid="stSidebar"] [data-testid="stThumbValue"] {
        color: #FFFFFF !important;
        background-color: var(--teal) !important;
        border-radius: 6px;
        padding: 0.1rem 0.4rem;
    }

    /* Button */
    div.stButton > button {
        background: var(--teal);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1.2rem;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        transition: background 0.15s ease;
    }
    div.stButton > button:hover {
        background: #0B6C70;
        color: white;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <div class="eyebrow">Insurance Analytics · Cost Estimator</div>
        <h1>Medical Premium Estimate</h1>
        <p>Enter applicant details to generate a data-driven insurance cost estimate with personalized guidance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar — inputs
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Applicant Profile")
    st.caption("Provide the details below, then generate an estimate.")

    age = st.slider("Age", 18, 100, 25)
    sex = st.selectbox("Gender", ["Male", "Female"])
    bmi = st.slider("BMI", 10.0, 50.0, 22.0)
    children = st.slider("Number of Children", 0, 5, 0)
    smoker = st.selectbox("Smoker", ["Yes", "No"])
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.button("Generate Estimate")

# ----------------------------------------------------------------------------
# Encode inputs
# ----------------------------------------------------------------------------
sex_encoded = 0 if sex == "Male" else 1
smoker_encoded = 1 if smoker == "Yes" else 0

input_data = {
    "age": age,
    "sex": sex_encoded,
    "bmi": bmi,
    "children": children,
    "smoker": smoker_encoded,
    "region_northwest": 0,
    "region_southeast": 0,
    "region_southwest": 0,
}

if region == "northwest":
    input_data["region_northwest"] = 1
elif region == "southeast":
    input_data["region_southeast"] = 1
elif region == "southwest":
    input_data["region_southwest"] = 1

input_list = [input_data[col] for col in columns]
input_array = np.array([input_list])

# ----------------------------------------------------------------------------
# Recommendations
# ----------------------------------------------------------------------------
def generate_recommendations(age, bmi, smoker, children, prediction):
    recs = []

    if smoker == 1:
        recs.append("Quitting smoking can meaningfully reduce long-term health risk and premium cost.")

    if bmi >= 30:
        recs.append("A structured diet and exercise plan can help bring BMI into a lower-risk range.")
    elif bmi < 18.5:
        recs.append("Consider a nutrition consultation to reach a healthier weight range.")

    if age >= 45:
        recs.append("Regular checkups and preventive screenings are recommended at this age.")

    if children >= 3:
        recs.append("A family insurance plan may offer more efficient coverage for larger households.")

    if prediction >= 30000:
        recs.append("Preventive care and lifestyle adjustments could help lower future risk exposure.")
    elif prediction < 10000:
        recs.append("Current lifestyle factors are keeping estimated costs low — maintain this trend.")

    return recs

# ----------------------------------------------------------------------------
# Main content
# ----------------------------------------------------------------------------
if predict_clicked:
    prediction = model.predict(input_array)[0]

    # Risk banding for the meter (0-40k mapped to 0-100%)
    meter_pct = max(0, min(100, (prediction / 40000) * 100))

    if prediction < 10000:
        risk_label, risk_class = "Low Risk", "risk-low"
    elif prediction < 30000:
        risk_label, risk_class = "Medium Risk", "risk-med"
    else:
        risk_label, risk_class = "High Risk", "risk-high"

    col_main, col_side = st.columns([1.4, 1], gap="large")

    with col_main:
        st.markdown(
            f"""
            <div class="card">
                <div class="result-label">Estimated Annual Premium</div>
                <div class="result-value">₹ {prediction:,.0f}</div>
                <div class="result-sub">Based on the applicant profile provided</div>
                <div class="meter-track">
                    <div class="meter-marker" style="left: {meter_pct}%;"></div>
                </div>
                <div class="meter-scale">
                    <span>Low</span><span>Medium</span><span>High</span>
                </div>
                <div style="margin-top:0.8rem;">
                    <span class="risk-tag {risk_class}">{risk_label}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        recommendations = generate_recommendations(age, bmi, smoker_encoded, children, prediction)
        rec_html = "".join(
            f'<div class="rec-row"><div class="rec-dot"></div><div>{r}</div></div>'
            for r in recommendations
        )
        st.markdown(
            f"""
            <div class="card">
                <h3>Personalized Guidance</h3>
                {rec_html if recommendations else '<div class="rec-row">No specific flags — profile looks favorable.</div>'}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="card"><h3>Cost Overview</h3>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"Estimated Cost (₹)": [prediction]}, index=["Prediction"])
        st.bar_chart(chart_data, height=220)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_side:
        summary_rows = {
            "Age": age,
            "Gender": sex,
            "BMI": f"{bmi:.1f}",
            "Children": children,
            "Smoker": smoker,
            "Region": region.capitalize(),
        }
        summary_html = "".join(
            f'<div class="summary-item"><span class="k">{k}</span><span class="v">{v}</span></div>'
            for k, v in summary_rows.items()
        )
        st.markdown(
            f"""
            <div class="card">
                <h3>Applicant Summary</h3>
                {summary_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if smoker_encoded == 1:
            st.markdown(
                """
                <div class="card" style="border-left: 3px solid #B3261E;">
                    <h3 style="border-bottom:none; margin-bottom:0.3rem;">Note</h3>
                    <div style="font-size:0.88rem; color:#5B6B79;">
                        Smoking status is the strongest driver of increased premium cost in this estimate.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        """
        <div class="card" style="padding: 2.4rem 2rem; text-align:center;">
            <h3 style="border-bottom:none; margin-bottom:0.4rem;">No estimate generated yet</h3>
            <p style="color:#5B6B79; font-size:0.92rem; max-width:520px; margin:0 auto;">
                Fill in the applicant profile in the sidebar and select
                <b>Generate Estimate</b> to see the predicted premium, risk level, and guidance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(3, gap="medium")
    feature_cards = [
        ("01", "Instant Estimate", "A trained regression model turns age, BMI, smoking status, and region into an annual premium estimate in real time."),
        ("02", "Risk Profiling", "Every estimate is placed on a low-to-high risk scale so applicants can see where they stand at a glance."),
        ("03", "Personalized Guidance", "Actionable, evidence-based suggestions are generated from the applicant's specific profile, not a generic checklist."),
    ]
    for col, (num, title, desc) in zip((f1, f2, f3), feature_cards):
        with col:
            st.markdown(
                f"""
                <div class="card" style="min-height:190px;">
                    <div style="color:#0E8388; font-family:'Manrope',sans-serif; font-weight:800; font-size:0.85rem; margin-bottom:0.5rem;">{num}</div>
                    <h3 style="border-bottom:none; margin-bottom:0.5rem; font-size:0.98rem;">{title}</h3>
                    <div style="color:#5B6B79; font-size:0.85rem; line-height:1.5;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; color:#8B9AA6; font-size:0.78rem; margin-top:2rem;">
        Estimates are model-generated and intended for informational purposes only.
    </div>
    """,
    unsafe_allow_html=True,
)