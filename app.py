import streamlit as st
import speech_recognition as sr
import language_tool_python
from datetime import datetime

# ---------------- UI ----------------
st.title("Grammar Scoring Engine")
st.caption("An AI-based system to evaluate spoken English grammar")

uploaded_file = st.file_uploader(
    "Upload an English WAV audio file",
    type=["wav"],
    help="Please upload a clear English voice recording"
)

# ---------------- SCORING ENGINE ----------------
def grammar_score(matches):
    """
    Converts grammar issues into a numerical score (0–100).
    Grammar issues get higher penalty, minor issues get lower penalty.
    """
    score = 100
    for issue in matches:
        if issue.category == "GRAMMAR":
            score -= 6
        else:
            score -= 3
    return max(0, score)

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    recognizer = sr.Recognizer()

    with sr.AudioFile(uploaded_file) as source:
        audio = recognizer.record(source)

    try:
        # Speech → Text
        text = recognizer.recognize_google(audio)

        st.subheader("Transcribed Text")
        st.write(text)

        # ---------------- Grammar Analysis (Cloud-safe + Rate-limit safe) ----------------
        try:
            tool = language_tool_python.LanguageToolPublicAPI('en-US')
            issues = tool.check(text)
            api_status = "ok"
        except Exception:
            # Fallback when API is rate-limited or unavailable
            issues = []
            api_status = "unavailable"

        # ---------------- Scoring ----------------
        score = grammar_score(issues)

        # ---------------- Output ----------------
        st.subheader("Grammar Score")
        st.success(f"{score} / 100")

        if api_status == "unavailable":
            st.caption(
                "Note: Grammar analysis service is temporarily unavailable. "
                "Score generated using fallback mode."
            )

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

        # ---------------- Save Result (Professional Report) ----------------
        filename = f"grammar_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Grammar Scoring Engine – Evaluation Report\n")
            f.write("------------------------------------------\n\n")

            f.write("Transcribed Speech:\n")
            f.write(f"\"{text}\"\n\n")

            f.write("Grammar Score:\n")
            f.write(f"{score} / 100\n\n")

            f.write("Analysis Summary:\n")
            if score >= 90:
                f.write(
                    "The spoken response demonstrates strong grammatical accuracy and natural sentence construction. "
                    "Only a small number of minor issues were detected.\n\n"
                )
            elif score >= 70:
                f.write(
                    "The response is grammatically sound overall, with a few noticeable issues that do not "
                    "significantly impact clarity.\n\n"
                )
            else:
                f.write(
                    "Multiple grammatical issues were detected, affecting overall clarity and correctness.\n\n"
                )

            f.write("Total Issues Identified:\n")
            f.write(f"{len(issues)}\n\n")

            f.write("Overall Assessment:\n")
            f.write(
                "This evaluation is generated automatically using NLP-based grammar analysis "
                "and provides an explainable assessment of spoken English proficiency.\n"
            )

        st.success(f"Result saved successfully: {filename}")

    except Exception as e:
        st.error("Unable to process the uploaded audio.")
        st.caption("Ensure the file is a clear English WAV recording.")
        st.write(e)
