import streamlit as st
import speech_recognition as sr
import language_tool_python
from datetime import datetime

st.title("Grammar Scoring Engine")
st.caption("An AI-based system to evaluate spoken English grammar")

uploaded_file = st.file_uploader(
    "Upload an English WAV audio file",
    type=["wav"],
    help="Please upload a clear English voice recording"
)

def grammar_score(matches):
    """
    Converts grammar issues into a numerical score (0–100).
    """
    score = 100
    for issue in matches:
        if issue.category == "GRAMMAR":
            score -= 6
        else:
            score -= 3
    return max(0, score)

if uploaded_file:
    recognizer = sr.Recognizer()

    with sr.AudioFile(uploaded_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)

        st.subheader("Transcribed Text")
        st.write(text)

        tool = language_tool_python.LanguageTool('en-US')
        issues = tool.check(text)

        score = grammar_score(issues)

        st.subheader("Grammar Score")
        st.success(f"{score} / 100")

        if score >= 90:
            st.info("Excellent grammatical accuracy.")
        elif score >= 70:
            st.info("Good grammar with minor issues.")
        elif score >= 50:
            st.warning("Grammar needs improvement.")
        else:
            st.error("Significant grammatical issues detected.")

        st.write(f"Total issues identified: {len(issues)}")

        st.subheader("Identified Grammar Issues")
        if issues:
            for i, issue in enumerate(issues, 1):
                st.write(f"{i}. {issue.message}")
        else:
            st.write("No grammar issues detected.")

        filename = f"grammar_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Grammar Scoring Engine Result\n")
            f.write("-----------------------------\n")
            f.write(f"Transcribed Text:\n{text}\n\n")
            f.write(f"Grammar Score: {score} / 100\n")
            f.write(f"Total Issues: {len(issues)}\n")

        st.success(f"Result saved successfully: {filename}")

    except Exception as e:
        st.error("Unable to process the uploaded audio.")
        st.caption("Ensure the file is a clear English WAV recording.")
        st.write(e)
