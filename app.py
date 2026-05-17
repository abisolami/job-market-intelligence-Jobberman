import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import ast

st.set_page_config(
    page_title="Nigerian Job Market Intelligence",
    page_icon="🇳🇬",
    layout="wide"
)

st.title("Nigerian Job Market Intelligence")
st.markdown("*Find out what your role pays and what skills you need in the Nigerian job market*")
st.divider()

# loading the model
@st.cache_resource
def load_model():
    return joblib.load("salary_model.pkl")


# loading cleaned data
@st.cache_data
def load_data():
    return pd.read_csv("jobbermann_cleaned.csv")

model = load_model()
data = load_data()

# and to load the json
# loading model columns
with open("model_columns.json", 'r') as f:
    model_columns = json.load(f)
    # and the top titles
with open("top_titles.json", 'r') as f:
    top_titles = json.load(f)


# moving on to the ui
col1, col2 = st.columns(2)

with col1:
    job_title = st.selectbox("Select Job Title", options=top_titles)
    experience_level = st.selectbox("Select Experience Level", options=['Internship & Graduate', 'Entry level', 'Mid level', 'Senior level'])
    location = st.selectbox("Location", options=data['location'].dropna().unique())
    job_category = st.selectbox('Job Category', options=data['job_category'].dropna().unique())
    qualification = st.selectbox("Qualification", options=['High School (S.S.C.E)', 'OND', 'HND', 'Diploma', 'N.C.E', 'Degree', 'MBA / MSc', 'MPhil / PhD'])
    working_hour = st.selectbox("Working Hour", options=['Full Time', 'Part Time', 'Contract', 'Internship & Graduate'])
    experience_length = st.slider("Years of Experience", min_value=0, max_value=15, value=2)
    predict_btn = st.button("Predict Salary Range", key="predict_btn")

with col2:
  with col2:
    if predict_btn:
        # creaitng empty rows for all required columns
        # setting 0 and 1 where necessary
        input_data = pd.DataFrame([
            {col: 0 for col in model_columns}
        ])

        # --------------- Ordinal Encoding ---------------
        experience_map = {
            'Internship & Graduate': 0,
            'Entry level': 1,
            'Mid level': 2,
            'Senior level': 3
        }
        qual_map = {
            'High School (S.S.C.E)': 0,
            'OND': 1,
            'HND': 2,
            'Diploma': 3,
            'N.C.E': 4,
            'Degree': 5,
            'MBA / MSc': 6,
            'MPhil / PhD': 7    
            }
        
        input_data['experience_level'] = experience_map[experience_level]
        input_data['minimum_qualification'] = qual_map[qualification]
        input_data['experience_length'] = experience_length
        # input_data['skill_count'] = data['skill_count'].mean()

        # ------------One Hot Encoding--------------
        # for job title
        title_col = f"job_title_{job_title}"
        if title_col in model_columns:
            input_data[title_col] = 1
        
        # for location
        location_col = f"location_{location}"
        if location_col in model_columns:
            input_data[location_col] = 1

        # for job category
        job_cat_col = f"job_category_{job_category}"    
        if job_cat_col in model_columns:
            input_data[job_cat_col] = 1 

        # for working hour
        working_hour_col = f"working_hour_{working_hour}"
        if working_hour_col in model_columns:
            input_data[working_hour_col] = 1

        # --------------- Making Prediction ---------------
        prediction = model.predict(input_data)[0]

        salary_mapping = {
            0: '₦70,000 - ₦150,000', 
            1: '₦150,000 - ₦400,000',
            2: '₦400,000 and above'
        }
        result = salary_mapping[prediction]

        # --------------- Results Display ---------------
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e);
                    border-left: 5px solid #00d4aa;
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 20px;">
            <p style="color: #00d4aa; font-size: 14px; margin: 0; letter-spacing: 2px;">PREDICTED SALARY RANGE</p>
            <h1 style="color: white; font-size: 36px; margin: 10px 0;">{result}</h1>
            <p style="color: #888; font-size: 13px; margin: 0;">Based on {experience_length} years experience in {location}</p>
        </div>
        """, unsafe_allow_html=True)

        # -------------- top skill required ---------------
        if job_title == 'Other':
            filtered = data[data['job_category'] == job_category].copy()
        else:
            filtered = data[data['job_title'] == job_title].copy()

        # converting the string representation of list to an actual list
        filtered['extracted_skills'] = filtered['extracted_skills'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        # all skills in that role
        all_skills = [skill for sublist in filtered['extracted_skills'].dropna() for skill in sublist]
        top_skills = pd.Series(all_skills).value_counts().head(20).index.tolist()

        #  ------------------- Top Hiring Company -------------
        top_companies = filtered['company'].value_counts().head(5).index.tolist()

        # ------------------- Job in Demand ---------------
        demand = len(filtered)

        # demand indicator color
        if demand > 50:
            demand_color = "#00d4aa"
            demand_label = "High Demand"
        elif demand > 20:
            demand_color = "#f0a500"
            demand_label = "Moderate Demand"
        else:
            demand_color = "#ff6b6b"
            demand_label = "Low Demand"

        # skills card
        skills_html = "".join([f'<span style="background:#1e3a5f; color:#00d4aa; padding:5px 12px; border-radius:20px; margin:4px; display:inline-block; font-size:13px;">{s}</span>' for s in top_skills])
        
        st.markdown(f"""
        <div style="background:#111827; border-radius:12px; padding:20px; margin-bottom:15px;">
            <p style="color:#00d4aa; font-size:13px; letter-spacing:2px; margin-bottom:12px;">TOP SKILLS REQUIRED</p>
            <div>{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)

        # companies and demand side by side
        # companies and demand side by side
        c1, c2 = st.columns(2)
        with c1:
            companies_text = "<br>".join([f"• {c}" for c in top_companies])
            st.markdown(f"""
            <div style="background:#111827; border-radius:12px; padding:20px; min-height:200px;">
                <p style="color:#00d4aa; font-size:13px; letter-spacing:2px; margin-bottom:12px;">TOP HIRING COMPANIES</p>
                <p style="color:white; font-size:13px; line-height:2;">{companies_text}</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div style="background:#111827; border-radius:12px; padding:20px; min-height:200px; text-align:center;">
                <p style="color:#00d4aa; font-size:13px; letter-spacing:2px; margin-bottom:12px;">MARKET DEMAND</p>
                <h1 style="color:{demand_color}; font-size:48px; margin:10px 0;">{demand}</h1>
                <p style="color:{demand_color}; font-size:13px;">{demand_label}</p>
                <p style="color:#888; font-size:11px;">active listings on Jobberman</p>
            </div>
            """, unsafe_allow_html=True)

        # ------------------- Salary Breakdown — full width ---------------
        salary_dist = filtered['salary_range'].value_counts().head(3)
        salary_rows = "".join([f'<div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #1e3a5f;"><span style="color:white; font-size:14px;">• {salary}</span><span style="color:#00d4aa; font-size:14px; font-weight:bold;">{count} listings</span></div>' for salary, count in salary_dist.items()])
        
        st.markdown(f"""
        <div style="background:#111827; border-radius:12px; padding:25px; margin-top:15px;">
            <p style="color:#00d4aa; font-size:13px; letter-spacing:2px; margin-bottom:15px;">COMMON SALARY RANGES POSTED</p>
            {salary_rows}
        </div>
        """, unsafe_allow_html=True)

        # ------------------- Footer ---------------
        st.markdown("""
        <div style="text-align:center; margin-top:40px;">
            <p style="color:#444; font-size:12px;">Data scraped from Jobberman.com · Built by Abisolami</p>
        </div>
        """, unsafe_allow_html=True)
