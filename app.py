import streamlit as st
import pandas as pd

# Sample dataset for universities
data = {
    "University": [
        "Olabisi Onabanjo University, Ago Iwoye",
        "Tai Solarin University of Education, Ijebu Ode",
        "Moshood Abiola University of Science and Technology, Abeokuta",
        "Babcock University, Ilishan-Remo",
        "Bells University of Technology, Otta",
        "Chrisland University",
        "Covenant University, Ota",
        "Crawford University, Igbesa",
        "Crescent University",
        "Hallmark University, Ijebi Itele, Ogun",
        "Mcpherson University, Seriki Sotayo, Ajebo",
        "Christopher University, Mowe",
        "Mountain Top University",
        "Southwestern University, Oku Owa",
        "Trinity University, Ogun State",
        "Aletheia University, Ago-Iwoye, Ogun State",
        "Vision University, Ikogbo, Ogun State",
        "Gerar University of Medical Science, Imope ljebu, Ogun State",
        "Mercy Medical University, Iwo, Ogun State"
    ],
    "Standard of Living": [8, 7, 6, 9, 7, 6, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "Course of Study": [7, 8, 6, 9, 7, 6, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "School Performance": [8, 7, 6, 10, 9, 8, 10, 9, 8, 7, 6, 7, 8, 7, 7, 9, 8, 9, 8],
    "Ranking": [7, 6, 5, 9, 7, 6, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "Tuition Fees": [3, 4, 5, 2, 3, 4, 2, 3, 4, 4, 4, 4, 3, 5, 4, 3, 4, 3, 4],
    "Facilities": [7, 6, 5, 9, 8, 7, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "Location": [8, 7, 6, 9, 7, 6, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "Student-to-Faculty Ratio": [6, 7, 8, 5, 6, 7, 4, 6, 7, 8, 7, 8, 6, 7, 8, 6, 7, 6, 7],
    "International Student Percentage": [4, 5, 6, 7, 6, 5, 9, 7, 6, 5, 4, 5, 6, 4, 5, 7, 6, 7, 6],
    "Alumni Network Strength": [7, 6, 5, 9, 8, 7, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "Transport System": [8, 7, 6, 9, 8, 7, 10, 8, 7, 6, 5, 6, 7, 5, 6, 8, 7, 8, 7],
    "Feeding": [7, 6, 5, 8, 7, 6, 9, 7, 6, 5, 4, 5, 6, 4, 5, 7, 6, 7, 6],
    "Outfit": [5, 6, 7, 4, 5, 6, 3, 5, 6, 7, 6, 7, 5, 6, 7, 5, 6, 5, 6],
    "JAMB Cut-Off Mark": [180, 170, 160, 200, 180, 170, 220, 200, 180, 170, 160, 180, 190, 170, 160, 180, 170, 190, 180]
}

df = pd.DataFrame(data)

# Tags for the criteria
tags = {
    "Standard of Living": ["Very Low", "Low", "Moderate", "High", "Very High"],
    "Course of Study": ["Limited", "Basic", "Average", "Wide", "Very Extensive"],
    "School Performance": ["Very Poor", "Poor", "Average", "Good", "Excellent"],
    "Ranking": ["Very Low", "Low", "Average", "High", "Top"],
    "Tuition Fees": ["Very High", "High", "Moderate", "Low", "Very Low"],
    "Facilities": ["Very Poor", "Poor", "Average", "Good", "Excellent"],
    "Location": ["Very Unfavorable", "Unfavorable", "Average", "Favorable", "Very Favorable"],
    "Student-to-Faculty Ratio": ["Very High", "High", "Average", "Low", "Very Low"],
    "International Student Percentage": ["Very Low", "Low", "Average", "High", "Very High"],
    "Alumni Network Strength": ["Very Weak", "Weak", "Average", "Strong", "Very Strong"],
    "Transport System": ["Very Poor", "Poor", "Average", "Good", "Excellent"],
    "Feeding": ["Very Poor", "Poor", "Average", "Good", "Excellent"],
    "Outfit": ["Very Strict", "Strict", "Average", "Relaxed", "Very Relaxed"]
}

# Function to map scores to tags
def map_score_to_tag(score, criterion):
    if criterion in tags:
        tag_list = tags[criterion]
        if score <= 2:
            return tag_list[0]
        elif 2 < score <= 4:
            return tag_list[1]
        elif 4 < score <= 6:
            return tag_list[2]
        elif 6 < score <= 8:
            return tag_list[3]
        else:
            return tag_list[4]
    return score

# Map tags to DataFrame
for criterion in tags.keys():
    df[criterion] = df[criterion].apply(lambda x: map_score_to_tag(x, criterion))

# Streamlit Interface
st.title("University Recommendation System")

st.write("Select your preferences for the following criteria:")

# User Inputs
selected_criteria = {}
for criterion in tags.keys():
    selected_criteria[criterion] = st.selectbox(
        f"Preferred {criterion}", options=tags[criterion])

# Matching universities based on user input
matches = df.copy()
for criterion, preference in selected_criteria.items():
    matches = matches[matches[criterion] == preference]
    print(matches)

# Display results
st.subheader("Recommended Universities")
if matches.empty:
    st.write("No universities match your criteria. Try adjusting your preferences.")
else:
    st.write(matches[["University"]])

st.write("### University Details")
st.write(matches)
