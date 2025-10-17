# comsats_grade_analyzer.py
import streamlit as st
import pandas as pd

# ------------------------------
# COMSATS Official Grade Conversion
# ------------------------------
def convert_marks_to_points(score):
    if score >= 85:
        return 4.00, "A"
    elif score >= 80:
        return 3.70, "A–"
    elif score >= 75:
        return 3.30, "B+"
    elif score >= 70:
        return 3.00, "B"
    elif score >= 65:
        return 2.70, "B–"
    elif score >= 60:
        return 2.30, "C+"
    elif score >= 55:
        return 2.00, "C"
    elif score >= 50:
        return 1.70, "C–"
    else:
        return 0.00, "F"

# ------------------------------
# GPA Calculation Logic
# ------------------------------
def compute_gpa(marks_data, credit_data):
    earned_points = 0
    attempted_hours = 0
    details = []

    for marks, hours in zip(marks_data, credit_data):
        gp, grade = convert_marks_to_points(marks)
        earned_points += gp * hours
        attempted_hours += hours
        details.append({
            "Marks (%)": marks,
            "Credit Hours": hours,
            "Letter Grade": grade,
            "Grade Points": gp
        })

    gpa_value = round(earned_points / attempted_hours, 2) if attempted_hours else 0.0
    return gpa_value, details

# ------------------------------
# Streamlit Interface
# ------------------------------
st.set_page_config(page_title="COMSATS GPA/CGPA Analyzer", layout="wide")

st.title("📊 COMSATS GPA & CGPA Analyzer")
st.markdown("Use this simple tool to calculate *semester GPA* and *overall CGPA* based on COMSATS grading policy.")

# Input total semesters
semester_count = st.number_input("Enter total semesters completed:", min_value=1, step=1)
cgpa_records = []

# Semester Loop
for sem in range(1, semester_count + 1):
    st.markdown(f"### 🎓 Semester {sem}")
    total_subjects = st.number_input(f"Number of courses in Semester {sem}:", min_value=1, step=1, key=f"subjects_{sem}")

    marks_data, credit_data = [], []

    for sub in range(1, total_subjects + 1):
        c1, c2 = st.columns(2)
        with c1:
            score = st.number_input(f"Enter Marks for Course {sub}", 0, 100, key=f"marks_{sem}_{sub}")
        with c2:
            credit = st.number_input(f"Credit Hours for Course {sub}", 1.0, 5.0, 3.0, 0.5, key=f"credit_{sem}_{sub}")

        marks_data.append(score)
        credit_data.append(credit)

    if st.button(f"Compute GPA for Semester {sem}", key=f"calculate_{sem}"):
        sem_gpa, sem_data = compute_gpa(marks_data, credit_data)
        cgpa_records.append({"semester_gpa": sem_gpa, "total_credits": sum(credit_data)})

        table = pd.DataFrame(sem_data)
        st.subheader(f"📘 Course-wise Summary for Semester {sem}")
        st.dataframe(table, use_container_width=True)

        st.success(f"✅ Semester {sem} GPA: *{sem_gpa}*")

# Calculate CGPA
if len(cgpa_records) > 0:
    total_points = sum(item["semester_gpa"] * item["total_credits"] for item in cgpa_records)
    total_credits = sum(item["total_credits"] for item in cgpa_records)
    overall_cgpa = round(total_points / total_credits, 2)

    st.markdown("---")
    st.header(f"🏅 Cumulative CGPA (Till Now): *{overall_cgpa}*")

    if overall_cgpa >= 3.5:
        rank = "Distinction"
    elif overall_cgpa >= 3.0:
        rank = "First Division"
    elif overall_cgpa >= 2.5:
        rank = "Second Divis
