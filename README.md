# Intelligent Resume Analyzer

A Python-based GUI application that automates resume screening by parsing resume text, matching candidate skills against job requirements, and generating a hiring recommendation.

---

## Features

- Extracts **name, email, skills, and experience**
- Calculates **match score (0–100)**
- Generates **hiring recommendation**
- Saves candidate data and report in **JSON format**
- Simple and user-friendly **Tkinter GUI**

---

## How It Works

1. Paste resume text into the application.
2. The system extracts key information.
3. Skills and experience are matched against predefined job requirements.
4. A match score is calculated.
5. A hiring recommendation is generated.

---

## Example Resume Format

```
Name: John Doe
Email: john@example.com
Skills: Python, SQL, Git
4 years experience
```

---

## Installation

Make sure Python 3 is installed.

```bash
python main.py
```

> Note: Tkinter must be available (works on local machines with GUI support).

---

## Output

- Displays match score and recommendation in the GUI
- Saves:
  - `candidate.json`
  - `report.json`

---

## Recommendation Logic

- **80–100** → Strong Hire  
- **50–79** → Consider  
- **Below 50** → Not Recommended  

---

## Author

Ahas Kaushik
