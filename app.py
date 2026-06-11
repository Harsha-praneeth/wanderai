
import streamlit as st
import google.generativeai as genai

import os

genai.configure(
    api_key=os.getenv("AQ.Ab8RN6KaJJs14XnbT99XNVD4bI8Yy86AX4Ds4ho6unF8JuNEQQ")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="WanderAI",

  layout="wide"
)
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp{
    background:
    radial-gradient(circle at top left,#1a1a1a,#0b0b0b 40%,#000000 100%);
    color:white;
    font-family:'Poppins',sans-serif;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

.hero-title{
    text-align:center;
    font-family:'Cinzel',serif;
    font-size:110px;
    font-weight:700;
    letter-spacing:8px;
    color:white;
    margin-top:80px;
    animation:fadeIn 1.5s ease;
}

.hero-subtitle{
    text-align:center;
    font-size:28px;
    color:#d4d4d4;
    margin-bottom:70px;
    animation:fadeIn 2s ease;
}

.section-title{
    text-align:center;
    font-size:38px;
    font-weight:600;
    margin-bottom:30px;
    color:white;
}

.feature-card{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(15px);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:20px;
    text-align:center;
    font-size:18px;
    margin-bottom:15px;
    transition:all 0.3s ease;
}

.feature-card:hover{
    transform:translateY(-10px);
    box-shadow:0px 15px 40px rgba(255,255,255,0.12);
}

.form-title{
    text-align:center;
    font-size:55px;
    font-weight:700;
    margin-bottom:40px;
    color:white;
}

.result-title{
    text-align:center;
    font-size:55px;
    font-weight:700;
    margin-bottom:40px;
    color:white;
}

label{
    font-size:20px !important;
    font-weight:600 !important;
}

.stTextInput input,
.stNumberInput input{
    border-radius:15px !important;
    font-size:18px !important;
}

.stButton button{
    width:100%;
    height:60px;
    border-radius:40px;
    border:none;
    font-size:18px;
    font-weight:700;
    background:linear-gradient(135deg,#f59e0b,#d97706);
    color:white;
    transition:all 0.3s ease;
}

.stButton button:hover{
    transform:scale(1.05);
    box-shadow:0px 10px 30px rgba(245,158,11,0.4);
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(30px);
    }

    to{
        opacity:1;
        transform:translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# SESSION STATE
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "result" not in st.session_state:
    st.session_state.result = ""

# -------------------------
# PAGE 1 - WELCOME
# -------------------------

if st.session_state.page == "welcome":

    st.markdown(
        '<div class="hero-title">WANDERAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">Plan Amazing Trips Within Seconds</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">What You Will Get Here</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="feature-card">AI Itineraries</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-card">Food Recommendations</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="feature-card">Budget Planning</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-card">Hidden Gems</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="feature-card">Travel Expenses</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-card">Packing Checklist</div>',
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    c1, c2, c3 = st.columns([2,1,2])

    with c2:
        if st.button("START PLANNING", use_container_width=True):
            st.session_state.page = "form"
            st.rerun()

# -------------------------
# PAGE 2 - FORM
# -------------------------

elif st.session_state.page == "form":

    st.markdown(
       '<div class="form-title">Trip Planner</div>',
        unsafe_allow_html=True
    )

    source = st.text_input(
        "Where are you travelling from?"
    )

    destination = st.text_input(
        "Where do you want to go?"
    )

    col1, col2 = st.columns(2)

    with col1:
        days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=3
        )

    with col2:
        budget = st.number_input(
            "Budget (₹)",
            min_value=1000,
            step=1000,
            value=10000
        )

    travel_type = st.selectbox(
        "Travel Type",
        [
            "Solo",
            "Friends",
            "Family",
            "Couple"
        ]
    )

    interests = st.multiselect(
        "Interests",
        [
            "Adventure",
            "Nature",
            "Food",
            "History",
            "Shopping",
            "Nightlife",
            "Culture",
            "Photography",
            "Beaches",
            "Wildlife"
        ]
    )

    st.write("")

    colA, colB = st.columns(2)

    with colA:
        if st.button("Back"):
            st.session_state.page = "welcome"
            st.rerun()

    with colB:

        if st.button("Generate Trip"):

            if not source:
                st.error("Please enter your starting location.")
                st.stop()

            if not destination:
                st.error("Please enter your destination.")
                st.stop()

            with st.spinner("Generating your travel plan..."):

                try:

                    prompt = f"""
You are an expert travel planner.

Create a professional travel itinerary.

Starting Location: {source}
Destination: {destination}
Days: {days}
Budget: ₹{budget}
Travel Type: {travel_type}
Interests: {', '.join(interests)}

Return the response using EXACT headings:

# Trip Overview

# Budget Breakdown

Transportation:
Accommodation:
Food:
Activities:
Miscellaneous:
Total:

# Day Wise Itinerary

Day 1:
Day 2:
Day 3:

# Food Recommendations

# Hidden Gems

# Packing Checklist

# Travel Tips

Keep everything within the specified budget.
"""

                    response = model.generate_content(prompt)

                    st.session_state.result = response.text

                    st.session_state.page = "result"

                    st.rerun()

                except Exception as e:

                    st.error(f"Error: {e}")

# -------------------------
# PAGE 3 - RESULT
# -------------------------

elif st.session_state.page == "result":

    st.markdown(
        '<div class="result-title">Your Personalized Journey</div>',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state.result)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Plan Another Trip"):

            st.session_state.page = "form"

            st.rerun()

    with col2:

        if st.button("Home"):

            st.session_state.page = "welcome"

            st.rerun()