
# Grammar Scoring Engine from Voice Samples

## Overview
This project converts spoken English audio into text and evaluates grammar quality,
providing a grammar score out of 100. Designed for SHL AI Research Intern assessment.

## Tech Stack
- Python
- SpeechRecognition
- LanguageTool (Grammar checking)
- Streamlit (UI)

## How it Works
1. Upload voice sample (.wav)
2. Convert speech to text
3. Analyze grammar mistakes
4. Generate grammar score

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Output
- Transcribed text
- Grammar issues
- Grammar score

## Future Improvements
- ML-based scoring
- Accent analysis
- Fluency detection
