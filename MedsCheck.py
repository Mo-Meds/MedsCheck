import streamlit as st
import openai
import os

# Load OpenAI API Key securely from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Make sure to set this environment variable securely
if not OPENAI_API_KEY:
    st.error("API key is missing. Please set the OpenAI API key in your environment.")
    st.stop()

openai.api_key = OPENAI_API_KEY

# Streamlit UI
st.title("AI-Powered Meds-Check Assistant")
st.write("Enter patient medications and get AI-powered insights. Please list medications in the format 'medication name (dose, frequency)'. For example: 'Amlodipine (5 mg, once daily)'")

# User input for medications
meds_input = st.text_area("Enter medications (comma-separated):")

# Dropdown for medication category (optional)
category = st.selectbox("Select medication category (optional)", ["", "Antibiotics", "Blood Pressure", "Diabetes", "Other"])

if st.button("Analyze Medications"):
    if meds_input:
        try:
            with st.spinner("Analyzing..."):
                # Constructing the prompt
                prompt = f"Patient is taking {meds_input}."
                if category:
                    prompt += f" The medications belong to the category: {category}."
                prompt += " Identify interactions, missing documentation, and recommendations based on Canadian guidelines."

                # API request to OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI assisting pharmacists with medication reviews. Follow Canadian guidelines."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Output handling
                output = response["choices"][0]["message"]["content"]
                st.subheader("AI Analysis:")
                st.write(output)
        except Exception as e:
            st.error(f"Error analyzing medications: {e}")
    else:
        st.warning("Please enter at least one medication.")
