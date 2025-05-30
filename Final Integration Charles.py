#!/usr/bin/env python3
"""
Unified AI-Driven Career Mapping System (Enhanced)
Combines Grok Updated with Integration Suggestions.
Includes: Full Question Set, AI Assistance, ML, Visuals, API-ready
"""

import os
import json
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from typing import AnyStr
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
from dotenv import load_dotenv
import openai
import requests

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------- Response Scale -------------------
RESPONSE_SCALE = {"Never": 1, "Sometimes": 2, "Often": 3, "Usually": 4, "Always": 5}

# ------------------- Layered Questions -------------------
# Layer definitions (Layers 1-5 remain unchanged from the original)
LAYER_1_QUESTIONS = {
    "Linguistic": [
        "I enjoy writing essays, stories, or journal entries for fun.",
        "I find it easy to explain complex topics in simple terms.",
        "I actively participate in debates, discussions, or public speaking.",
        "I enjoy reading and analyzing books, research papers, or blogs.",
        "I like to express my ideas clearly through written or spoken communication."
    ],
    "Logical-Mathematical Intelligence": [
        "I enjoy solving logical puzzles, riddles, or brain teasers.",
        "I analyze data, statistics, or numerical trends to make decisions.",
        "I like working on research projects that involve problem-solving.",
        "I enjoy subjects like math, coding, finance, or science.",
        "I easily identify patterns and relationships in data or concepts."
    ],
    "Interpersonal Intelligence": [
        "I enjoy working in teams and collaborating with peers on projects.",
        "I am good at resolving conflicts between friends or classmates.",
        "I often help others understand concepts by explaining them in different ways.",
        "I enjoy networking, meeting new people, and forming connections.",
        "I understand and respond well to people’s emotions and perspectives."
    ],
    "Intrapersonal Intelligence": [
        "I regularly reflect on my personal strengths and weaknesses.",
        "I set clear personal and academic goals for myself.",
        "I stay motivated and disciplined even when studying independently.",
        "I understand my emotions and how they affect my decision-making.",
        "I choose career paths based on my interests, values, and long-term aspirations."
    ],
    "Naturalistic Intelligence": [
        "I enjoy studying environmental topics like sustainability, ecology, or agriculture.",
        "I like spending time in nature and observing patterns in the environment.",
        "I notice and appreciate details in my surroundings that others often overlook.",
        "I advocate for environmental and sustainability initiatives in my college.",
        "I connect academic subjects with real-world applications in nature and science."
    ],
    "Bodily-Kinesthetic Intelligence": [
        "I enjoy physical activities like sports, dance, or acting.",
        "I learn better by doing rather than just reading or listening.",
        "I like building things with my hands or tools.",
        "I have good hand-eye coordination and body control.",
        "I express myself physically (e.g., gestures, movement)."
    ],
    "Musical Intelligence": [
        "I can identify or reproduce musical patterns easily.",
        "I enjoy listening to or creating music.",
        "I use rhythm or music to memorize concepts.",
        "I can differentiate tones, pitches, and instruments.",
        "I often notice background music or ambient sounds."
    ],
    "Visual-Spatial Intelligence": [
        "I enjoy drawing, painting, or visual designing.",
        "I can visualize objects from different angles in my mind.",
        "I prefer visual aids like diagrams, charts, or videos.",
        "I am good at navigating or reading maps.",
        "I often think in pictures rather than words."
    ],
    "Cognitive Styles": [
        "I prefer visual materials (diagrams, flowcharts) when learning new things.",
        "I tend to think in words and prefer reading or writing to learn.",
        "I like learning by doing and engaging in hands-on tasks."
    ]
}

LAYER_2_QUESTIONS = {
    "MBTI": [
        "I get energized by spending time alone (I) vs with others (E).",
        "I prefer focusing on facts (S) vs big picture ideas (N).",
        "I prioritize logic and consistency (T) vs empathy and values (F).",
        "I prefer planned and organized (J) vs flexible and spontaneous (P)."
    ],
    "Big Five - Openness": [
        "I enjoy trying new and different activities.",
        "I am imaginative and full of ideas.",
        "I appreciate art, music, and literature."
    ],
    "Big Five - Conscientiousness": [
        "I like to keep things organized and tidy.",
        "I follow through with tasks and responsibilities."
    ],
    "Big Five - Extraversion": [
        "I feel comfortable in social situations.",
        "I enjoy being the center of attention."
    ],
    "Big Five - Agreeableness": [
        "I am considerate and kind to almost everyone.",
        "I try to see things from others’ perspectives."
    ],
    "Big Five - Neuroticism": [
        "I get stressed or anxious easily.",
        "I experience frequent mood changes."
    ],
    "SDT - Autonomy": [
        "I feel free to choose how to approach my work or study.",
        "I enjoy tasks more when I have control over them."
    ],
    "SDT - Competence": [
        "I feel capable and effective in what I do.",
        "I take pride in mastering new skills or challenges."
    ],
    "SDT - Relatedness": [
        "I feel connected and close to people around me.",
        "I value meaningful relationships in my life."
    ]
}

LAYER_3_QUESTIONS = {
    "Numerical Aptitude": [
        "I am comfortable working with numbers and data.",
        "I can solve arithmetic and algebraic problems easily.",
        "I enjoy tasks involving statistics, accounting, or finance."
    ],
    "Verbal Aptitude": [
        "I understand and use new vocabulary quickly.",
        "I can comprehend and analyze written passages.",
        "I enjoy word-based games and language puzzles."
    ],
    "Abstract Reasoning": [
        "I can spot logical patterns in unfamiliar problems.",
        "I can mentally manipulate shapes and figures.",
        "I solve visual puzzles and reasoning questions with ease."
    ],
    "Technical Skills": [
        "I have experience with software/tools relevant to my field.",
        "I can troubleshoot or learn new technical skills quickly.",
        "I understand technical manuals, processes, or systems."
    ],
    "Creative/Design Skills": [
        "I can generate original ideas and solutions.",
        "I am skilled at sketching, designing, or multimedia work.",
        "I enjoy innovating in visual or artistic formats."
    ],
    "Communication Skills": [
        "I express my ideas clearly in speaking or writing.",
        "I adapt my message to suit the audience.",
        "I am persuasive and confident in presentations."
    ]
}

LAYER_4_QUESTIONS = {
    "Educational Background": [
        "I have access to quality academic resources (books, teachers, labs).",
        "I attend or have attended a school/college with strong academic performance.",
        "My academic environment encourages exploration and innovation.",
        "My curriculum included diverse subjects and career awareness programs."
    ],
    "Socioeconomic Factors": [
        "I have access to stable internet, computer, and other learning tools.",
        "Financial limitations have restricted my career exploration so far.",
        "My family can support me in pursuing higher education or specialized training.",
        "I’ve had opportunities to attend coaching, mentorship, or skill programs."
    ],
    "Career Exposure": [
        "I’ve interacted with professionals from various career paths.",
        "I have participated in internships, shadowing, or volunteering roles.",
        "I’ve been exposed to diverse career stories through media or workshops.",
        "My school/college offers good career counseling services."
    ]
}

LAYER_5_QUESTIONS = {
    "Interests and Passions": [
        "I have clear hobbies or subjects that I love spending time on.",
        "I often find myself researching or learning about certain topics outside class.",
        "I get excited about working on personal or creative projects.",
        "I follow certain professionals or industries with great interest."
    ],
    "Career Trends Awareness": [
        "I am aware of new and emerging fields in the job market.",
        "I regularly explore how careers are evolving with technology and globalization.",
        "I consider long-term career sustainability when thinking about professions."
    ],
    "Personal Goals and Values": [
        "I have written down or thought deeply about my career goals.",
        "My career decisions are guided by my personal values (e.g., helping others, creativity, stability).",
        "I think about the impact I want to create through my work.",
        "I consider work-life balance and personal fulfillment when imagining my future job."
    ]
}

LAYER_6_QUESTIONS = {
    "Self_Synthesis": [
        "Based on my intelligence strengths, the types of activities I naturally enjoy are: (open-ended)",
        "Based on my personality, I thrive in environments that are: (open-ended)",
        "The industries and roles that excite me most are: (open-ended)",
        "I feel most motivated when my work allows me to: (open-ended)",
        "I now realize that I need a career that balances: (open-ended)",
        "My top 3 career interest areas are: (open-ended)",
        "A role I now want to research deeper or shadow is: (open-ended)"
    ],
    "Passion_Practicality": [
        "Career 1: How passionate are you about this career?",
        "Career 1: How well does it match your intelligence/personality?",
        "Career 1: How practical is it in terms of income/lifestyle?",
        "Career 1: How accessible is it to you (education/network)?",
        "Career 1: How sustainable is it in the long term?",
        "Career 2: How passionate are you about this career?",
        "Career 2: How well does it match your intelligence/personality?",
        "Career 2: How practical is it in terms of income/lifestyle?",
        "Career 2: How accessible is it to you (education/network)?",
        "Career 2: How sustainable is it in the long term?",
        "Career 3: How passionate are you about this career?",
        "Career 3: How well does it match your intelligence/personality?",
        "Career 3: How practical is it in terms of income/lifestyle?",
        "Career 3: How accessible is it to you (education/network)?",
        "Career 3: How sustainable is it in the long term?"
    ],
    "Confidence_Check": [
        "How confident do you feel in your current career direction? (1-5)",
        "What’s holding you back from pursuing your top option(s)? (open-ended)",
        "What fears or doubts do you still have? (open-ended)",
        "What kind of support would help you feel more confident? (open-ended)"
    ],
    "Career_Clustering": [
        "Creative & Expressive (High linguistic/artistic, intuitive, low structure, values expression)",
        "Analytical & Investigative (Logical-mathematical, investigative, high in openness & autonomy)",
        "Social Impact & People-Centric (Interpersonal, high empathy, values connection, collaboration)",
        "Structured & Strategic (Conventional/enterprising, conscientious, prefers clarity, order)",
        "Tech & Engineering (Realistic + logical, enjoys tools, systems, innovation)",
        "Nature & Sustainability (Naturalistic, values environment, real-world application)",
        "Entrepreneurial & Leadership (High enterprising, self-determined, values risk-taking and autonomy)"
    ],
    "Action_Plan": [
        "What are 3 things you can do in the next 30 days to explore your top choice(s)? (open-ended)",
        "What specific skills or knowledge gaps do you need to address? (open-ended)",
        "What timeline do you want to give yourself before making a decision? (3 months, 6 months, 1 year)",
        "Who can help you on this journey? (Mentors, peers, family, online groups) (open-ended)"
    ]
}

# noinspection SpellCheckingInspection
CAREER_MAPPING = {
    "Linguistic": ["Journalism", "Content Writing", "Law", "Public Relations", "Teaching"],
    "Logical-Mathematical": ["Data Science", "Engineering", "Finance", "Research", "Software Development"],
    "Spatial": ["Graphic Design", "Architecture", "UX Design", "Animation", "Cartography"],
    "Bodily-Kinesthetic": ["Sports Coaching", "Physical Therapy", "Dance", "Carpentry", "Surgery"],
    "Interpersonal": ["Human Resources", "Psychology", "Social Work", "Marketing", "Counseling"],
    "Intrapersonal": ["Entrepreneur", "Researcher", "Philosopher", "Author", "Career Consultant"],
    "Naturalistic": ["Environmental Science", "Forestry", "Agriculture", "Wildlife Conservation", "Geology"],
    "Musical": ["Music Production", "Sound Engineering", "Music Therapy", "Performing Arts", "Composer"],
    "Sternberg_Analytical": ["Data Analysis", "Policy Analysis", "Academic Research", "Management Consulting"],
    "Sternberg_Creative": ["Advertising", "Film Production", "Game Design", "Creative Writing"],
    "Sternberg_Practical": ["Project Management", "Logistics", "Entrepreneurship", "Sales"],
    "MBTI_INFP": ["Counseling", "Writing", "Nonprofit Work", "Art Therapy"],
    "RIASEC_Investigative": ["Scientist", "Researcher", "Data Analyst", "Engineer"],
    "RIASEC_Artistic": ["Artist", "Writer", "Designer", "Musician"],
    "RIASEC_Social": ["Teacher", "Social Worker", "Nurse", "Counselor"],
    "Technology": ["Software Engineer", "Data Scientist", "Cybersecurity Analyst", "AI Researcher", "DevOps Engineer", "Cloud Architect"],
    "Healthcare": ["Doctor", "Nurse", "Pharmacist", "Medical Researcher", "Physical Therapist", "Healthcare Administrator"],
    "Business": ["Entrepreneur", "Marketing Manager", "Financial Analyst", "HR Specialist", "Management Consultant", "Supply Chain Analyst"],
    "Creative": ["Graphic Designer", "Writer", "Musician", "Film Director", "Game Designer", "Interior Designer"],
    "Education": ["Teacher", "Professor", "Educational Consultant", "Librarian", "Instructional Designer"],
    "Engineering": ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Aerospace Engineer", "Environmental Engineer"],
    "Science": ["Biologist", "Chemist", "Physicist", "Geologist", "Astronomer"],
    "Values_Impact": ["Nonprofit Management", "Environmental Advocacy", "Public Health"],
    "Industry_Technology": ["Software Engineer", "AI Specialist", "Cybersecurity Analyst"],
    "Career_Clustering_Creative": ["Content Creator", "Graphic Designer", "Filmmaker"],
    "Career_Clustering_Analytical": ["Data Scientist", "Research Scientist", "Financial Analyst"]
}
ONET_DATA = {
    "Data Science": {"skills": ["Python", "Statistics"], "outlook": "High demand, growing field"},
    "Software Development": {"skills": ["Coding", "Problem-solving"], "outlook": "Stable, high demand"},
    "Journalism": {"skills": ["Writing", "Research"], "outlook": "Moderate demand, competitive"},
    "Teaching": {"skills": ["Communication", "Patience"], "outlook": "Stable, consistent need"}
}
# ------------------- AI Helper Functions -------------------
def get_conversational_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "AI response unavailable."

def ai_explain_question(question):
    return get_conversational_response(f"Explain why this question matters for career guidance: {question}")

def ai_suggest_answer(question, scores, careers):
    top_trait = max(scores, key=scores.get) if scores else "your top strengths"
    top_career = careers[0] if careers else "a related path"
    return f"Given your interest in {top_trait}, you might explore {top_career}—want to know more?"

def ai_recommend_careers(scores, careers):
    if not scores or not careers:
        return "Not enough data to suggest careers."
    top = max(scores, key=scores.get)
    msg = f"You scored highly in {top}. Consider: {', '.join(careers[:3])}."
    return msg

# ------------------- Utility Functions -------------------
def get_user_consent():
    return input("Consent to save your data for improving guidance? (yes/no): ").strip().lower() == "yes"

def anonymize_data(responses):
    return {f"q{i+1}": r for i, r in enumerate(responses)}

def randomize_layer_questions(layer):
    return {k: random.sample(v, min(len(v), 3)) for k, v in layer.items()}

def collect_responses(questions, scale, open_ended=False, scores=None, careers=None):
    results = {}
    for category, q_list in questions.items():
        results[category] = []
        for q in q_list:
            if open_ended:
                print(q)
                act = input("Type 'help', 'suggest', or your answer: ").lower()
                if act == 'help':
                    print(ai_explain_question(q))
                    ans = input("Answer: ")
                elif act == 'suggest':
                    print(ai_suggest_answer(q, scores, careers))
                    ans = input("Answer: ")
                else:
                    ans = act
            else:
                print(q)
                ans = input(f"Enter ({'/'.join(scale.keys())}): ").capitalize()
                while ans not in scale:
                    ans = input(f"Invalid. Try again ({'/'.join(scale.keys())}): ").capitalize()
                ans = scale[ans]
            results[category].append(ans)
    return results

def score_responses(response_dict):
    scores = {}
    for cat, vals in response_dict.items():
        if all(isinstance(v, int) for v in vals):
            scores[cat] = sum(vals) / len(vals)
        else:
            scores[cat] = ", ".join(str(v) for v in vals)
    return scores

def map_to_careers(scores, mapping):
    out = []
    for k, v in scores.items():
        if isinstance(v, float) and v >= 4.0 and k in mapping:
            out.extend(mapping[k])
    return list(set(out))

def plot_cluster_scores(scores, filename="cluster_scores.png"):
    keys = list(scores.keys())
    vals = [v for v in scores.values() if isinstance(v, (int, float))]
    plt.bar(keys[:len(vals)], vals[:len(keys)])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.title("Career Cluster Scores")
    plt.savefig(filename)
    plt.close()

# ------------------- ML Model -------------------
class CareerModel:
    def __init__(self, path="career_model.pkl"):
        self.path = path
        self.model = RandomForestClassifier(n_estimators=200)
        self.encoder = OrdinalEncoder()
        self.columns = []

    def load(self):
        if os.path.exists(self.path):
            data = joblib.load(self.path)
            self.model = data['model']
            self.encoder = data['encoder']
            self.columns = data['columns']

    def save(self):
        joblib.dump({"model": self.model, "encoder": self.encoder, "columns": self.columns}, self.path)

    def train(self, df):
        self.columns = [c for c in df.columns if c != 'career']
        X = df[self.columns]
        y = self.encoder.fit_transform(df[['career']]).ravel()
        self.model.fit(X, y)
        self.save()

    def predict(self, scores):
        X = pd.DataFrame([scores], columns=self.columns).fillna(0)
        label = self.model.predict(X)[0]
        return self.encoder.inverse_transform([[label]])[0]

# ------------------- Main Workflow -------------------
def main():
    print("Welcome to the Career Compass (AI Edition)!")

    consent = get_user_consent()
    all_scores, all_responses = {}, {}

    layers = [
        ("Layer 1 - Intelligences", LAYER_1_QUESTIONS, False),
        ("Layer 2 - Personality", LAYER_2_QUESTIONS, False),
        ("Layer 3 - Aptitude", LAYER_3_QUESTIONS, False),
        ("Layer 4 - Background", LAYER_4_QUESTIONS, False),
        ("Layer 5 - Interests", LAYER_5_QUESTIONS, False),
        ("Layer 6 - Synthesis", LAYER_6_QUESTIONS, True),
    ]

    for name, layer, open_ended in layers:
        print(f"\n{name}")
        q_set = randomize_layer_questions(layer)
        res = collect_responses(q_set, RESPONSE_SCALE, open_ended, all_scores, [])
        all_responses[name] = res
        scores = score_responses(res)
        all_scores.update(scores)

    careers = map_to_careers(all_scores, CAREER_MAPPING)
    print("\nRecommended Careers:", careers[:5])
    print("\nAI Insight:", ai_recommend_careers(all_scores, careers))

    # Train and predict with ML
    model = CareerModel()
    model.load()
    if consent:
        df = pd.DataFrame({**all_scores, "career": random.choice(careers) if careers else "Unknown"}, index=[0])
        model.train(df)
        print("\nML Suggestion:", model.predict(all_scores))

    # Save session
    if consent:
        with open("career_session.json", "w") as f:
            json.dump({"scores": all_scores, "careers": careers}, f, indent=2)
        print("Session saved as career_session.json")

    # Visualize
    numerical = {k: v for k, v in all_scores.items() if isinstance(v, float)}
    if numerical:
        plot_cluster_scores(numerical)
        print("Cluster scores chart saved as cluster_scores.png")

if __name__ == "__main__":
    main()
