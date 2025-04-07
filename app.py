import streamlit as st
from recommender import recommend_assessments, evaluate_accuracy
from dataset import shl_catalog

# --- PAGE CONFIG ---
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""<style>
body, .main, .block-container {
    background-color: #ffffff;
    color: #000000;
}
.hero-card {
    background-color: #ffffff;
    padding: 1rem;
    color: #000000;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #0078b0;
    border-radius: 6px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.hero-card h2 { color: #1f2937; }
.hero-card p { color: #4b5563; }
.search-container {
    background-color: #f8fafc;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border-left: 6px solid #2e7d32;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.stTextInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #ccc;
    padding: 0.5rem;
    font-size: 1rem;
    border-radius: 6px;
}
.stButton button {
    background-color: #0078b0;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: bold;
}
.stButton button:hover {
    background-color: #005f8d;
}
.card {
    background-color: #ffffff;
    padding: 1rem;
    color: #000000;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #0078b0;
    border-radius: 6px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.card h4 {
    margin: 0;
    color: #0078b0;
}
.card p {
    margin: 0.3rem 0;
    color: #000000;
}
</style>""", unsafe_allow_html=True)

# --- HEADER WITH LOGO ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("shl_logo.png", width=140)
with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>SHL Assessment Recommendation System</h1>", unsafe_allow_html=True)

# --- HERO SECTION + SEARCH ---
st.markdown("""
    <div class='hero-card'>
        <h2>Find assessments that best meet your needs.</h2>
        <p>Browse our catalog for science-backed assessments that evaluate cognitive ability, personality, behavior, skills, and more, by role, industry, and language.</p>
    </div>
    <div class="search-container">
        <h4 style="color: #111111;">🔍 Search for an assessment</h4>
""", unsafe_allow_html=True)

user_query = st.text_input(
    label="Enter a job description",
    placeholder="e.g. I want to manage a bank branch and lead a team in financial operations.",
    label_visibility="collapsed"
)
submit = st.button("Search")

st.markdown("</div>", unsafe_allow_html=True)

# --- RESULTS ---
if submit and user_query:
    try:
        results = recommend_assessments(user_query, shl_catalog, top_n=10)
        if results:
            st.markdown("### ✅ Recommended Assessments:")
            for assessment in results:
                st.markdown(f"""
                    <div class="card">
                        <h4>{assessment['name']}</h4>
                        <p><b>Type:</b> {assessment['type']} | <b>Duration:</b> {assessment['duration']} min</p>
                        <p>{assessment['description']}</p>
                        <p><b>Remote:</b> {assessment['remote']} | <b>Adaptive:</b> {assessment['adaptive']}</p>
                        <p><a href="{assessment['url']}" target="_blank">🌐 View More</a></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No matching assessments found. Try a different keyword.")
    except Exception as e:
        st.error(f"❌ Error occurred: {e}")

# --- EVALUATION (Optional) ---
with st.expander("📊 Run Accuracy Evaluation"):
    queries = [
        "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes.",
        "Here is a JD text, can you recommend some assessment that can help me screen applications. Time limit is less than 30 minutes.",
        "I am hiring for an analyst and wants applications to screen using Cognitive and personality tests, what options are available within 45 mins."
    ]
    ground_truths = [
        ["Java Developer Test"],
        ["Python Skills", "SQL Proficiency", "JavaScript Test"],
        ["Short Screening Test", "Quick Aptitude Test"],
        ["Cognitive Test", "Personality Assessment"]
    ]

    if st.button("Run Evaluation"):
      # Evaluate metrics first (place BEFORE you reference `recall` or `map_score`)
        metrics = evaluate_accuracy(queries, shl_catalog, ground_truths)
        recall = metrics["Mean Recall@3"]
        map_score = metrics["Mean AP@3"]

# Then render the styled metrics (AFTER the above)
with st.container():
    st.markdown("### 📊 Evaluation Metrics")
    st.markdown(
        f"""
        <div style='background-color:#f0f2f6;padding:10px;border-radius:10px;'>
            <div style='display:flex;justify-content:space-between;'>
                <div>
                    <strong>MAP@3</strong><br>
                    <span style='font-size:24px;'>{map_score:.2f}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
