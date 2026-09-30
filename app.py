import streamlit as st
import google.generativeai as genai
import json
import re

# Set page configuration with a modern look
st.set_page_config(
    page_title="EduGenie — AI Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling for professional Naan Mudhalvan Look
st.markdown("""
    <style>
    /* Gradient Background and Typography */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #1E3A8A;
    }
    .main-title {
        background: linear-gradient(45deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    /* Feature Cards */
    .feature-card {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 4rem;
        color: #9CA3AF;
        font-size: 0.9rem;
        border-top: 1px solid #E5E7EB;
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://wikimedia.org", width=100)
    st.markdown("### 🎓 EduGenie AI")
    st.caption("Naan Mudhalvan Skill Initiative")
    st.markdown("---")
    
    # API Key Configuration
    api_key = st.text_input("🔑 Enter Gemini API Key", type="password", help="Get a free key from Google AI Studio")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.warning("⚠️ Please provide your Gemini API key to activate the engine.")
        
    st.markdown("---")
    st.markdown("### 💡 Demo Mock Content")
    if st.button("📝 Load Sample Physics Notes"):
        st.session_state["input_text"] = (
            "Photosynthesis is the process used by plants, algae and certain bacteria to harness "
            "energy from sunlight and turn it into chemical energy. Carbon dioxide and water are "
            "converted into glucose and oxygen. Light energy is absorbed by chlorophyll, a green pigment "
            "located in chloroplasts. The chemical equation is 6CO2 + 6H2O + Light -> C6H12O6 + 6O2. "
            "This process is essential for sustaining life on Earth by producing oxygen and organic compounds."
        )
        st.rerun()

# Application Header Header
st.markdown('<div class="main-title">EduGenie</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Personalized Learning Assistant — Built for Naan Mudhalvan</div>', unsafe_allow_html=True)

# Main input text area
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

user_input = st.text_area(
    "📥 Paste your Study Notes, Chapter Text, or Syllabus below:",
    value=st.session_state["input_text"],
    height=200,
    placeholder="Type or paste your learning material here..."
)

# App Navigation Modules Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Smart Note Summarizer", 
    "🎯 AI Quiz Generator", 
    "🗂️ Flashcard Generator", 
    "📅 3-Day Revision Planner"
])

# Helper utility to prompt Gemini
def generate_ai_response(prompt_template, input_data):
    if not api_key:
        st.error("❌ Please enter your Gemini API Key in the left sidebar to proceed.")
        return None
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(f"{prompt_template}\n\nInput Text:\n{input_data}")
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return None

# ==========================================
# MODULE 1: SMART NOTE SUMMARIZER
# ==========================================
with tab1:
    st.subheader("📝 Smart Summary & Key Takeaways")
    st.caption("Condenses long paragraphs into 3-4 high-impact learning tokens instantly.")
    
    if st.button("⚡ Generate Summary", key="btn_summary"):
        if user_input.strip() == "":
            st.warning("Please paste some content first!")
        else:
            with st.spinner("Analyzing and summarizing..."):
                prompt = "Act as an expert tutor. Summarize the following text into exactly 3-4 clear, bulleted 'High-Impact Key Takeaways'. Use bold text for core keywords."
                result = generate_ai_response(prompt, user_input)
                if result:
                    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MODULE 2: AI QUIZ GENERATOR
# ==========================================
with tab2:
    st.subheader("🎯 Active Recall Practice Quiz")
    st.caption("Generate instant interactive MCQs with built-in explanatory feedback loop.")
    
    if st.button("🎲 Generate Interactive Quiz", key="btn_quiz"):
        if user_input.strip() == "":
            st.warning("Please paste some content first!")
        else:
            with st.spinner("Crafting custom questions..."):
                prompt = (
                    "Create 3 multiple-choice questions based on the input text. "
                    "Return ONLY a clean JSON array matching this format structure:\n"
                    '[{"question": "Q1 text", "options": ["A", "B", "C", "D"], "answer": "Correct Option text exactly", "explanation": "Why its correct"}]'
                )
                result = generate_ai_response(prompt, user_input)
                if result:
                    try:
                        clean_json = re.sub(r'^```json\s*|\s*```$', '', result.strip(), flags=re.MULTILINE)
                        st.session_state["quiz_data"] = json.loads(clean_json)
                        st.session_state["answers_submitted"] = False
                    except Exception as parse_err:
                        st.error("Failed to cleanly format quiz data. Please click generate again.")
                        st.code(result)

    if "quiz_data" in st.session_state:
        user_selections = []
        for idx, item in enumerate(st.session_state["quiz_data"]):
            st.markdown(f"**Q{idx+1}: {item['question']}**")
            sel = st.radio(f"Select option for Q{idx+1}", item["options"], key=f"q_radio_{idx}", label_visibility="collapsed")
            user_selections.append(sel)
            st.markdown("")
            
        if st.button("Submit Answers Check 📊"):
            st.session_state["answers_submitted"] = True
            
        if st.session_state.get("answers_submitted", False):
            st.markdown("### 📊 Your Results & Explanations:")
            score = 0
            for idx, item in enumerate(st.session_state["quiz_data"]):
                user_ans = user_selections[idx]
                correct_ans = item["answer"]
                
                if user_ans == correct_ans:
                    st.success(f"✅ **Question {idx+1}: Correct!** You selected: {user_ans}")
                    score += 1
                else:
                    st.error(f"❌ **Question {idx+1}: Incorrect.** You selected: {user_ans} | **Correct Answer:** {correct_ans}")
                st.info(f"💡 **Explanation:** {item['explanation']}")
            st.metric("Final Score", f"{score} / {len(st.session_state['quiz_data'])}")

# ==========================================
# MODULE 3: FLASHCARD GENERATOR
# ==========================================
with tab3:
    st.subheader("🗂️ Conceptual Term Flashcards")
    st.caption("Interactive concept-memory testing cards designed for quick term review.")
    
    if st.button("🃏 Generate Flashcards", key="btn_flash"):
        if user_input.strip() == "":
            st.warning("Please paste some content first!")
        else:
            with st.spinner("Extracting critical vocabulary..."):
                prompt = (
                    "Create 3 concepts/terms flashcards from the text. "
                    "Return ONLY a clean JSON array structured exactly like this:\n"
                    '[{"front": "Question/Term", "back": "Definition/Answer explanation"}]'
                )
                result = generate_ai_response(prompt, user_input)
                if result:
                    try:
                        clean_json = re.sub(r'^```json\s*|\s*```$', '', result.strip(), flags=re.MULTILINE)
                        st.session_state["flashcards"] = json.loads(clean_json)
                    except:
                        st.error("Formatting error, try generating again.")
                        st.code(result)
                        
    if "flashcards" in st.session_state:
        for idx, card in enumerate(st.session_state["flashcards"]):
            with st.expander(f"🎴 Flashcard {idx+1}: {card['front']}"):
                st.markdown(f"**Answer / Concept:**\n{card['back']}")

# ==========================================
# MODULE 4: 3-DAY REVISION PLANNER
# ==========================================
with tab4:
    st.subheader("📅 Structured 3-Day Revision Planner")
    st.caption("Organized timeline strategy to prepare you safely before midterms or finals.")
    
    if st.button("🗓️ Create Revision Plan", key="btn_plan"):
        if user_input.strip() == "":
            st.warning("Please paste some content first!")
        else:
            with st.spinner("Structuring your study calendar..."):
                prompt = (
