import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model.pkl")

st.set_page_config(page_title="Titanic Survival Predictor", layout="centered")

st.title("🚢 Titanic Survival Prediction")
st.markdown("Enter passenger details to predict survival probability.")

# Input fields
pclass = st.selectbox("Passenger Class", [1, 2, 3])
sex = st.selectbox("Sex", ["male", "female"])
age = st.slider("Age", 1, 80, 25)
fare = st.slider("Fare", 0.0, 500.0, 50.0)
sibsp = st.slider("Siblings/Spouses Aboard", 0, 8, 0)
parch = st.slider("Parents/Children Aboard", 0, 6, 0)
embarked = st.selectbox("Embarked Port", ["C", "Q", "S"])

if st.button("Predict Survival"):

    input_data = pd.DataFrame({
        'Pclass': [pclass],
        'Sex': [sex],
        'Age': [age],
        'Fare': [fare],
        'SibSp': [sibsp],
        'Parch': [parch],
        'Embarked': [embarked]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success(f"🎉 Passenger Survived")
    else:
        st.error(f"❌ Passenger Did Not Survive")

    st.write(f"Survival Probability: **{probability:.2%}**")