# app.py
import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- Load Model and Preprocessor ---
# Load the trained pipeline from the pickle file
try:
    with open('model3.pkl', 'rb') as file:
        model_pipeline = pickle.load(file)
except FileNotFoundError:
    st.error("Error: 'model3.pkl' not found. Please make sure the model file is in the same directory as the app.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# Extract the OneHotEncoder from the preprocessor to get the categories
try:
    preprocessor = model_pipeline.named_steps['preprocessor']
    onehot_encoder = preprocessor.named_transformers_['cat']
    categories = onehot_encoder.categories_
except KeyError as e:
    st.error(f"Could not find the preprocessor or one-hot encoder in the pipeline. Error: {e}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while extracting categories: {e}")
    st.stop()

# Assign categories to respective feature names for dropdowns
# The order must match the order of columns in the training data
categorical_features = ['hire_date', 'department', 'job_title', 'education_level', 'city', 'state']
feature_categories = {
    'hire_date': categories[0],
    'department': categories[1],
    'job_title': categories[2],
    'education_level': categories[3],
    'city': categories[4],
    'state': categories[5]
}


# --- Streamlit App Interface ---
st.set_page_config(page_title="Employee Salary Predictor", layout="wide")
st.title('Employee Salary Predictor')
st.write("Enter the employee details below to predict their salary.")

# Create columns for a cleaner layout
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Job & Experience")
    years_of_experience = st.number_input('Years of Experience', min_value=0, max_value=40, value=5, step=1)
    department = st.selectbox('Department', options=feature_categories['department'])
    job_title = st.selectbox('Job Title', options=feature_categories['job_title'])

with col2:
    st.header("Education & Location")
    education_level = st.selectbox('Education Level', options=feature_categories['education_level'])
    city = st.selectbox('City', options=feature_categories['city'])
    state = st.selectbox('State', options=feature_categories['state'])

with col3:
    st.header("Hiring Information")
    hire_date = st.selectbox('Hire Date', options=feature_categories['hire_date'])


# --- Prediction Logic ---
if st.button('Predict Salary', type="primary"):
    # Create a DataFrame from the user's input
    # The column order must match the order the model was trained on
    input_data = {
        'hire_date': [hire_date],
        'department': [department],
        'job_title': [job_title],
        'years_of_experience': [years_of_experience],
        'education_level': [education_level],
        'city': [city],
        'state': [state]
    }
    input_df = pd.DataFrame(input_data)

    # Ensure the column order is correct before prediction
    # This is the order from your notebook after dropping initial columns
    expected_columns = [
        'hire_date', 'department', 'job_title', 'years_of_experience',
        'education_level', 'city', 'state'
    ]
    input_df = input_df[expected_columns]


    # Make a prediction using the loaded pipeline
    try:
        prediction = model_pipeline.predict(input_df)
        predicted_salary = prediction[0]

        st.success(f'Predicted Salary: **${predicted_salary:,.2f}**')
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

st.markdown("---")
st.write("This app uses a Gradient Boosting Regressor model to predict salaries based on employee data.")
