import streamlit as st
import pandas as pd
import pickle
import joblib

# Load trained components
model = joblib.load(open("lightgbm_churn_model.pkl", "rb"))
scaler = joblib.load(open("scaler.pkl", "rb"))
feature_names = joblib.load(open("feature_columns.pkl", "rb"))  # Save this during training

st.set_page_config(page_title="Customer Churn Prediction", layout="centered")

st.title("📊 Customer Churn Prediction Dashboard")
st.markdown("Fill the customer details below:")

# Input form
with st.form("churn_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Has Partner?", ["No", "Yes"])
        dependents = st.selectbox("Has Dependents?", ["No", "Yes"])
        tenure = st.slider("Tenure (in months)", 0, 72, 12)
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])

    with col2:
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly_charges = st.slider("Monthly Charges", 0, 150, 70)
        total_charges = st.slider("Total Charges", 0, 10000, 1500)

    submitted = st.form_submit_button("Predict Churn")

if submitted:
    # Collect user input in a DataFrame
    user_input = pd.DataFrame({
        "gender": [gender],
        "SeniorCitizen": [1 if senior_citizen == "Yes" else 0],
        "Partner": [partner],
        "Dependents": [dependents],
        "tenure": [tenure],
        "PhoneService": [phone_service],
        "MultipleLines": [multiple_lines],
        "InternetService": [internet_service],
        "OnlineSecurity": [online_security],
        "DeviceProtection": [device_protection],
        "TechSupport": [tech_support],
        "Contract": [contract],
        "PaperlessBilling": [paperless_billing],
        "PaymentMethod": [payment_method],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges]
    })

    # One-hot encode
    input_encoded = pd.get_dummies(user_input)

    # Align with training features
    input_aligned = input_encoded.reindex(columns=feature_names, fill_value=0)

    # Scale the data
    input_scaled = scaler.transform(input_aligned)

    # Predict
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    if prediction == 1:
        st.error(f"⚠️ This customer is likely to churn. Probability: {probability:.2f}")
    else:
        st.success(f"✅ This customer is likely to stay. Probability: {probability:.2f}")
