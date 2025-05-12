# 3_💬_Feedback.py

import streamlit as st
import datetime
import json
from auth.auth import is_authenticated, logout


st.title("💬 Feedback")
st.write("We’d love to hear your thoughts about our Diet Recommendation System!")

if not is_authenticated():
    st.warning("Please login to access the app.")
    st.stop()

# Add logout button to sidebar
with st.sidebar:
    if st.button("Logout"):
        logout()

# Feedback Form
name = st.text_input("Your Name (optional)")
email = st.text_input("Your Email (optional)")
feedback = st.text_area("Your Feedback", height=150)
rating = st.slider("Rate the app", 1, 5, 3)
st.caption("1 = Very Bad, 5 = Excellent")

if st.button("Submit Feedback"):
    if feedback.strip() == "":
        st.warning("Please provide some feedback before submitting.")
    else:
        feedback_entry = {
            "timestamp": str(datetime.datetime.now()),
            "name": name,
            "email": email,
            "rating": rating,
            "feedback": feedback
        }
        try:
            with open("feedback_log.json", "a", encoding='utf-8') as f:
                f.write(json.dumps(feedback_entry) + "\n")
            st.success("Thank you for your feedback!")
        except Exception as e:
            st.error(f"Error saving feedback: {e}")
