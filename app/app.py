import streamlit as st
import numpy as np
import joblib
import json
import pandas as pd

# Load Model & Columns
model = joblib.load("insurance_model.joblib")

with open("columns.json", "r") as f:
    columns = json.load(f)

# Page Config
st.set_page_config(page_title="Insurance Predictor", layout="centered")

# Title
st.title("🏥 Medical Insurance Cost Predictor")
st.markdown("### Enter your details to estimate insurance cost")

# User Inputs
age = st.slider("Age", 18, 100, 25)
sex = st.selectbox("Gender", ["Male", "Female"])
bmi = st.slider("BMI", 10.0, 50.0, 22.0)
children = st.slider("Number of Children", 0, 5, 0)
smoker = st.selectbox("Smoker", ["Yes", "No"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

# Convert Inputs → Model Format
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
    "region_southwest": 0
}

if region == "northwest":
    input_data["region_northwest"] = 1
elif region == "southeast":
    input_data["region_southeast"] = 1
elif region == "southwest":
    input_data["region_southwest"] = 1

# Maintain correct order
input_list = [input_data[col] for col in columns]
input_array = np.array([input_list])

# Recommendation Function
def generate_recommendations(age, bmi, smoker, children, prediction):
    recs = []

    if smoker == 1:
        recs.append("🚭 Consider quitting smoking to reduce health risks and insurance cost.")

    if bmi >= 30:
        recs.append("⚖️ Aim to reduce BMI through balanced diet and regular exercise.")
    elif bmi < 18.5:
        recs.append("🍽️ Maintain a healthy weight; consider consulting a nutritionist.")

    if age >= 45:
        recs.append("🩺 Schedule regular health checkups and screenings.")

    if children >= 3:
        recs.append("👨‍👩‍👧‍👦 Explore family insurance plans for better coverage.")

    if prediction >= 30000:
        recs.append("💡 Consider preventive healthcare and lifestyle changes to lower risk.")
    elif prediction < 10000:
        recs.append("✅ Maintain your healthy lifestyle to keep insurance costs low.")

    return recs

# Prediction Button
if st.button("Predict Insurance Cost 💰"):

    prediction = model.predict(input_array)[0]

    # Result
    st.success(f"Estimated Insurance Cost: ₹ {prediction:,.2f}")

    # Input Summary (User Friendly)
    st.subheader("📋 Input Summary")
    display_data = {
        "Age": age,
        "Gender": sex,
        "BMI": bmi,
        "Children": children,
        "Smoker": smoker,
        "Region": region
    }
    st.write(display_data)

    # Recommendations
    recommendations = generate_recommendations(age, bmi, smoker_encoded, children, prediction)

    st.subheader("💡 Personalized Recommendations")
    for rec in recommendations:
        st.success(rec)

    # Risk Level
    if prediction < 10000:
        st.info("🟢 Low Risk")
    elif prediction < 30000:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")

    # Smoking Insight
    if smoker_encoded == 1:
        st.warning("⚠️ Smoking significantly increases insurance cost.")

    # Visualization
    st.subheader("📊 Prediction Visualization")
    chart_data = pd.DataFrame({
        "Insurance Cost": [prediction]
    })
    st.bar_chart(chart_data)

# Footer
st.markdown("---")
