#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox
import re
import json
from datetime import datetime


# ---------------- Resume Parser ----------------

class ResumeParser:

    @staticmethod
    def extract_name(text):
        match = re.search(r"name:\s*(.+)", text, re.IGNORECASE)
        return match.group(1).strip().title() if match else "Not Found"

    @staticmethod
    def extract_email(text):
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        return match.group(0).lower() if match else "Not Found"

    @staticmethod
    def extract_skills(text):
        match = re.search(r"skills:\s*(.+)", text, re.IGNORECASE)
        if match:
            skills = match.group(1).split(",")
            return [skill.strip().capitalize() for skill in skills]
        return []

    @staticmethod
    def extract_experience(text):
        match = re.search(r"(\d+)\s+years?", text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    @classmethod
    def parse(cls, text):
        return {
            "name": cls.extract_name(text),
            "email": cls.extract_email(text),
            "skills": cls.extract_skills(text),
            "experience": cls.extract_experience(text)
        }


# ---------------- Matching Logic ----------------

class Matcher:

    @staticmethod
    def calculate_score(candidate, job):
        required = set(job["required_skills"])
        candidate_skills = set(candidate["skills"])

        if not required:
            return 0

        matched = required.intersection(candidate_skills)
        skill_score = (len(matched) / len(required)) * 70

        exp_score = min(
            (candidate["experience"] / job["min_experience"]) * 30,
            30
        ) if job["min_experience"] > 0 else 30

        return round(skill_score + exp_score, 2)


# ---------------- Report Generator ----------------

class ReportGenerator:

    @staticmethod
    def generate(candidate, job, score):
        if score >= 80:
            recommendation = "Strong Hire"
        elif score >= 50:
            recommendation = "Consider"
        else:
            recommendation = "Not Recommended"

        return {
            "candidate_name": candidate["name"],
            "job_title": job["title"],
            "match_score": score,
            "recommendation": recommendation,
            "analysis_date": datetime.now().isoformat()
        }


# ---------------- GUI Application ----------------

class ResumeScreeningApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Resume Screening System")
        self.root.geometry("700x600")

        self.job_requirements = {
            "title": "Python Developer",
            "required_skills": ["Python", "Sql", "Git"],
            "min_experience": 3
        }

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Paste Resume Text Below:", font=("Arial", 14)).pack(pady=10)

        self.text_area = tk.Text(self.root, height=12, width=80)
        self.text_area.pack()

        tk.Button(self.root, text="Analyze Resume", command=self.analyze_resume).pack(pady=10)

        self.result_area = tk.Text(self.root, height=15, width=80)
        self.result_area.pack()

    def analyze_resume(self):
        resume_text = self.text_area.get("1.0", tk.END).strip()

        if not resume_text:
            messagebox.showerror("Error", "Please enter resume text.")
            return

        candidate = ResumeParser.parse(resume_text)
        score = Matcher.calculate_score(candidate, self.job_requirements)
        report = ReportGenerator.generate(candidate, self.job_requirements, score)

        # Save JSON files
        with open("candidate.json", "w") as f:
            json.dump(candidate, f, indent=4)

        with open("report.json", "w") as f:
            json.dump(report, f, indent=4)

        self.display_results(candidate, report)

    def display_results(self, candidate, report):
        self.result_area.delete("1.0", tk.END)

        output = (
            f"Candidate Name: {candidate['name']}\n"
            f"Email: {candidate['email']}\n"
            f"Skills: {candidate['skills']}\n"
            f"Experience: {candidate['experience']} years\n\n"
            f"Match Score: {report['match_score']}/100\n"
            f"Recommendation: {report['recommendation']}\n"
        )

        self.result_area.insert(tk.END, output)


# ---------------- Run App ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeScreeningApp(root)
    root.mainloop()


# In[ ]:




