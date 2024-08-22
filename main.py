import time
import os
import joblib
import pandas as pd
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize new chat session
new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except FileExistsError:
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except FileNotFoundError:
    past_chats = {}

# Function to map scores to tags
def map_score_to_tag(score, criterion):
    if criterion == "Tuition Fees":
        if score <= 2:
            return "Very High"
        elif 2 < score <= 3:
            return "High"
        elif 3 < score <= 4:
            return "Moderate"
        elif 4 < score <= 5:
            return "Low"
        else:
            return "Very Low"
    return score

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
    "Standard of Living": ["High", "Moderate", "Low", "Very High", "High", "Low", "Very High", "Moderate", "Low", "Low", "Moderate", "High", "Very High", "Low", "Moderate", "Moderate", "Low", "Moderate", "Low"],
    "Course of Study": ["Science", "Education", "Technology", "Science", "Technology", "Science", "Science", "Science", "Science", "Education", "Science", "Science", "Science", "Technology", "Education", "Technology", "Technology", "Medical Science", "Medical Science"],
    "School Performance": ["Good", "Average", "Average", "Excellent", "Good", "Average", "Excellent", "Good", "Average", "Average", "Good", "Average", "Good", "Poor", "Average", "Good", "Average", "Good", "Average"],
    "Ranking": ["Top 100", "Top 200", "Top 300", "Top 50", "Top 100", "Top 300", "Top 50", "Top 200", "Top 300", "Top 200", "Top 200", "Top 200", "Top 100", "Top 300", "Top 200", "Top 200", "Top 300", "Top 100", "Top 200"],
    "Tuition Fees": [3, 4, 5, 2, 3, 4, 2, 3, 4, 4, 4, 4, 3, 5, 4, 3, 4, 3, 4],
    "Facilities": ["Good", "Average", "Poor", "Excellent", "Good", "Poor", "Excellent", "Good", "Average", "Average", "Good", "Average", "Good", "Poor", "Average", "Good", "Average", "Good", "Poor"],
    "Location": ["Urban", "Rural", "Urban", "Urban", "Urban", "Urban", "Urban", "Rural", "Rural", "Urban", "Rural", "Urban", "Urban", "Rural", "Urban", "Rural", "Rural", "Rural", "Rural"],
    "Student-to-Faculty Ratio": ["20:1", "30:1", "25:1", "15:1", "20:1", "30:1", "15:1", "25:1", "30:1", "25:1", "25:1", "20:1", "20:1", "30:1", "25:1", "20:1", "30:1", "20:1", "25:1"],
    "International Student Percentage": [10, 5, 2, 15, 10, 2, 15, 5, 3, 2, 2, 10, 12, 3, 5, 10, 2, 12, 5],
    "Alumni Network Strength": ["Strong", "Moderate", "Weak", "Very Strong", "Strong", "Weak", "Very Strong", "Moderate", "Weak", "Moderate", "Moderate", "Strong", "Strong", "Weak", "Moderate", "Moderate", "Weak", "Strong", "Moderate"],
    "Transport System": ["Good", "Average", "Poor", "Excellent", "Good", "Poor", "Excellent", "Good", "Average", "Average", "Good", "Average", "Good", "Poor", "Average", "Good", "Average", "Good", "Poor"],
    "Feeding": ["Good", "Average", "Poor", "Excellent", "Good", "Poor", "Excellent", "Good", "Average", "Average", "Good", "Average", "Good", "Poor", "Average", "Good", "Average", "Good", "Poor"],
    "Outfit": ["Formal", "Casual", "Casual", "Strict", "Formal", "Casual", "Strict", "Formal", "Casual", "Casual", "Formal", "Casual", "Strict", "Casual", "Formal", "Casual", "Casual", "Formal", "Casual"],
    "JAMB Cut-Off Mark": [180, 170, 160, 200, 180, 170, 220, 200, 180, 170, 160, 180, 190, 170, 160, 180, 170, 190, 180]
}

df = pd.DataFrame(data)

# Streamlit Interface
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Find School", "Chat"])

if selection == "Find School":
    st.title("University Recommendation System")
    st.write("Project By Onakoya Praise Kasope (20192990)")

    # User Inputs
    selected_jamb_score = st.number_input("Enter your JAMB score", min_value=0, max_value=400, step=1)
    selected_tuition_fee = st.selectbox("Preferred Tuition Fees", options=["Very High", "High", "Moderate", "Low", "Very Low"])

    # Matching universities based on user input
    matches = df.copy()
    matches["Tuition Fees"] = matches["Tuition Fees"].apply(lambda x: map_score_to_tag(x, "Tuition Fees"))
    filtered_matches = matches[(matches["JAMB Cut-Off Mark"] <= selected_jamb_score) & 
                               (matches["Tuition Fees"] == selected_tuition_fee)]

    # Display results
    st.subheader("Recommended Universities")
    if filtered_matches.empty:
        st.write("No universities match your criteria. Try adjusting your preferences.")
    else:
        st.write(filtered_matches[["University"]])

        # Show details for selected university
        selected_university = st.selectbox("Select a University for Details", options=["No options to select."] + filtered_matches["University"].tolist())
        if selected_university != "No options to select.":
            university_details = filtered_matches[filtered_matches["University"] == selected_university]

            if not university_details.empty:
                st.subheader("University Details")
                st.write(university_details[[
                    "Standard of Living", "Course of Study", "School Performance",
                    "Ranking", "Tuition Fees", "Facilities", "Location",
                    "Student-to-Faculty Ratio", "International Student Percentage",
                    "Alumni Network Strength", "Transport System", "Feeding", "Outfit"
                ]].reset_index(drop=True))

elif selection == "Chat":
    st.title("Ask AI")
    st.write("kindly type only the school name yoy want to know about thanks")

    # Initialize the AI model
    st.session_state.model = genai.GenerativeModel('gemini-pro')
    if 'chat_id' not in st.session_state:
        st.session_state.chat_id = new_chat_id
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'gemini_history' not in st.session_state:
        st.session_state.gemini_history = []

    # Load chat history
    try:
        st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
        st.session_state.gemini_history = joblib.load(f'data/{st.session_state.chat_id}-gemini_messages')
    except FileNotFoundError:
        st.session_state.messages = []
        st.session_state.gemini_history = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(name=message['role'], avatar=message.get('avatar')):
            st.markdown(message['content'])

    # Chat input and response handling
    if prompt := st.chat_input("Your message here..."):
        custom_prompt = f"I need information about {prompt} university include fees, links info also an dont give wrong info."
        
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append(dict(role='user', content=prompt))

        response = st.session_state.model.start_chat().send_message(custom_prompt, stream=True)
        
        with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
            message_placeholder = st.empty()
            full_response = ''
            for chunk in response:
                for ch in chunk.text.split(' '):
                    full_response += ch + ' '
                    time.sleep(0.05)
                    message_placeholder.write(full_response + '▌')
            message_placeholder.write(full_response)

        st.session_state.messages.append(dict(role=MODEL_ROLE, content=full_response, avatar=AI_AVATAR_ICON))
        st.session_state.gemini_history = st.session_state.model.start_chat().history
        joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
        joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')
