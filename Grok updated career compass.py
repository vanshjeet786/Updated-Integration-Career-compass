#!/usr/bin/env python3
"""
Enhanced Career Mapping Prototype CLI with AI Integration and Machine Learning
"""

import json
import random
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import openai
import joblib

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
[]
# Response scale for Likert questions
RESPONSE_SCALE = {
    "Never": 1, "Sometimes": 2, "Often": 3, "Usually": 4, "Always": 5
}

# Layer Definitions
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

# AI Helper Functions
def get_conversational_response(prompt: str) -> str:
    """Get a conversational response from OpenAI."""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error fetching AI response: {str(e)}"

def ai_explain_question(question: str) -> str:
    """Provide an AI explanation for a question."""
    explanations = {
        "Based on my intelligence strengths, the types of activities I naturally enjoy are: (open-ended)":
            "Hi! This question is about reflecting on what you’re naturally good at—like problem-solving or creativity—and what activities you enjoy. Think about what comes easily to you and feels fun!",
        "What are 3 things you can do in the next 30 days to explore your top choice(s)? (open-ended)":
            "This is about taking small, practical steps toward your career interests. I can suggest ideas based on your results if you’d like—want some help?"
    }
    return explanations.get(question, "I’m here to help! This question is asking you to reflect on your preferences or plans. What part feels tricky? I’ll break it down for you.")

def ai_suggest_answer(question: str, scores: dict, careers: list) -> str:
    """Suggest an answer based on user scores and careers."""
    suggestions = {
        "Based on my intelligence strengths, the types of activities I naturally enjoy are: (open-ended)":
            f"Given your high scores in {max(scores, key=scores.get)}, you might enjoy activities like {random.choice(['writing', 'coding', 'team projects'])}.",
        "My top 3 career interest areas are: (open-ended)":
            f"Based on your results, how about exploring {', '.join(careers[:3])}? They align with your strengths!"
    }
    return suggestions.get(question, "Hmm, I’d suggest something tied to your strengths—want a specific idea based on your scores?")

def ai_recommend_careers(scores: dict, careers: list) -> str:
    """Recommend careers based on scores with O*NET insights."""
    top_category = max(scores, key=scores.get)
    onet_info = [ONET_DATA.get(career, {"skills": ["N/A"], "outlook": "N/A"}) for career in careers]
    return f"Looking at your profile, you scored high in {top_category} (score: {scores[top_category]:.2f}). I’d recommend {', '.join(careers[:3])}. For example, {careers[0]} requires skills like {', '.join(onet_info[0]['skills'])}, and the job outlook is {onet_info[0]['outlook']}. What do you think?"

# Data Handling and Machine Learning
def get_linkedin_trends(career: str) -> dict:
    """Simulate LinkedIn job market trends."""
    trends = {
        "Data Science": {"demand": "High", "salary_range": "$80k-$120k"},
        "Software Development": {"demand": "High", "salary_range": "$90k-$130k"},
        "Journalism": {"demand": "Moderate", "salary_range": "$40k-$70k"},
        "Teaching": {"demand": "Stable", "salary_range": "$40k-$60k"}
    }
    return trends.get(career, {"demand": "Unknown", "salary_range": "N/A"})

class CareerModel:
    """Machine learning model for career prediction."""
    def __init__(self, model_path="career_model.pkl"):
        self.path = model_path
        self.model = LogisticRegression(max_iter=1000)
        self.encoder = None
        self.columns = []

    def load(self):
        if os.path.exists(self.path):
            data = joblib.load(self.path)
            self.model = data["model"]
            self.encoder = data["encoder"]
            self.columns = data["columns"]

    def save(self):
        """Save the model to file."""
        joblib.dump({"model": self.model, "encoder": self.encoder, "columns": self.columns}, self.path)

    def train(self, df: pd.DataFrame):
        """Train the model on provided data."""
        from sklearn.preprocessing import LabelEncoder
        assert 'career' in df, "Missing career column"
        self.columns = [c for c in df.columns if c != 'career']
        X = df[self.columns]
        self.encoder = LabelEncoder()
        y = self.encoder.fit_transform(df['career'])
        self.model.fit(X, y)
        self.save()

    def predict(self, input_scores: dict) -> str:
        """Predict a career based on input scores."""
        X = pd.DataFrame([input_scores], columns=self.columns).fillna(0)
        label = self.model.predict(X)[0]
        return self.encoder.inverse_transform([label])[0]

def anonymize_data(user_responses: list) -> dict:
    """Anonymize user responses."""
    return {f"q{i+1}": resp for i, resp in enumerate(user_responses)}

# Core Functions
def randomize_layer_questions(layer_questions: dict) -> dict:
    """Randomize the order of questions within each category."""
    return {category: random.sample(questions, len(questions)) for category, questions in layer_questions.items()}

def collect_responses(questions: dict, scale: dict, open_ended: bool = False, scores: dict = None, careers: list = None) -> dict:
    """Collect user responses with optional AI assistance."""
    responses = {}
    for category, qs in questions.items():
        responses[category] = []
        print(f"\n{category}:")
        for q in qs:
            if open_ended:
                print(f"{q}")
                assist = input("Type 'help' for an explanation, 'suggest' for a suggestion, or your answer directly: ").lower()
                if assist == "help":
                    print(ai_explain_question(q))
                    response = input(f"{q}: ")
                elif assist == "suggest" and scores and careers:
                    print(ai_suggest_answer(q, scores, careers))
                    response = input(f"{q}: ")
                else:
                    response = assist
                responses[category].append(response)
            else:
                print(f"{q}")
                response = input(f"Enter response ({', '.join(scale.keys())}): ").capitalize()
                while response not in scale:
                    response = input(f"Invalid response. Enter ({', '.join(scale.keys())}): ").capitalize()
                responses[category].append(scale[response])
    return responses

def score_responses(responses: dict) -> dict:
    """Score responses by averaging numerical values or retaining text."""
    scores = {}
    for category, vals in responses.items():
        if isinstance(vals[0], int):
            scores[category] = sum(vals) / len(vals)
        else:
            scores[category] = vals
    return scores

def map_to_careers(scores: dict, mapping: dict) -> list:
    """Map high-scoring categories to career paths."""
    careers = []
    for category, score in scores.items():
        if isinstance(score, float) and score >= 4 and category in mapping:
            careers.extend(mapping[category])
    return list(set(careers))

def plot_cluster_scores(cluster_scores: dict, save_path: str = "cluster_scores.png"):
    """Plot cluster scores and save to file."""
    names = list(cluster_scores.keys())
    vals = list(cluster_scores.values())
    plt.figure(figsize=(10, 6))
    plt.bar(names, vals)
    plt.xticks(rotation=45, ha='right')
    plt.title("Career Cluster Scores")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def get_user_consent() -> bool:
    """Obtain user consent for data collection."""
    consent = input("Do you consent to us collecting your responses to improve our recommendations? (yes/no): ").lower()
    return consent == "yes"

# Main Execution
def main():
    """Run the career mapping system."""
    print("Welcome to the Enhanced Career Mapping System!")
    print("I’m your AI career counselor—here to guide you step-by-step.")

    # Initialize data structures
    all_responses = {}
    all_scores = {}
    model = CareerModel()
    model.load()

    # Collect responses for Layers 1-5
    layers = [
        ("Layer 1: Core Intelligence & Cognitive Style", LAYER_1_QUESTIONS, False),
        ("Layer 2: Personality & Motivation", LAYER_2_QUESTIONS, False),
        ("Layer 3: Aptitude and Skill Assessment", LAYER_3_QUESTIONS, False),
        ("Layer 4: Background, Context, and Exposure", LAYER_4_QUESTIONS, False),
        ("Layer 5: Real-world Alignment", LAYER_5_QUESTIONS, False)
    ]
    for name, questions, open_ended in layers:
        print(f"\n{name}")
        responses = collect_responses(randomize_layer_questions(questions), RESPONSE_SCALE, open_ended)
        all_responses[name] = responses
        scores = score_responses(responses)
        all_scores.update(scores)

    # Initial career mapping
    recommended_careers = map_to_careers(all_scores, CAREER_MAPPING)
    print("\nHere’s what we’ve learned from Layers 1-5:")
    print("**Your Top Scores:**")
    for category, score in sorted(all_scores.items(), key=lambda x: x[1] if isinstance(x[1], float) else 0, reverse=True)[:5]:
        if isinstance(score, float):
            print(f"- {category}: {score:.2f}")
    print("\n**Initial Career Recommendations:**")
    if recommended_careers:
        for career in recommended_careers[:5]:
            print(f"- {career}")
    else:
        print("No strong matches yet—let’s refine this in Layer 6!")
    print("\n**AI Insight:**")
    print(ai_recommend_careers(all_scores, recommended_careers))

    # Layer 6 with AI assistance
    print("\nLayer 6: Synthesis & Career Mapping")
    print("Let’s reflect and plan—type 'help' or 'suggest' anytime!")
    layer_6_responses = collect_responses(randomize_layer_questions(LAYER_6_QUESTIONS), RESPONSE_SCALE, open_ended=True, scores=all_scores, careers=recommended_careers)
    all_responses["Layer 6"] = layer_6_responses

    # Final output with market insights
    print("\n**Final Career Recommendations with Market Insights:**")
    for career in recommended_careers[:3]:
        linkedin_data = get_linkedin_trends(career)
        onet_data = ONET_DATA.get(career, {"skills": ["N/A"], "outlook": "N/A"})
        print(f"- {career}: Demand: {linkedin_data['demand']}, Salary: {linkedin_data['salary_range']}, Skills: {', '.join(onet_data['skills'])}")

    # Machine Learning Prediction (if trained)
    if model.columns and get_user_consent():
        try:
            predicted_career = model.predict(all_scores)
            print(f"\n**ML Prediction:** Based on our model, you might excel in: {predicted_career}")
        except Exception as e:
            print(f"Error in ML prediction: {str(e)}")

    # Save results and plot
    with open("career_mapping_results.json", "w") as f:
        json.dump(all_responses | {"Recommended_Careers": recommended_careers}, f, indent=4)
    plot_cluster_scores({k: v for k, v in all_scores.items() if isinstance(v, float)})
    print("\nResults saved to 'career_mapping_results.json' and cluster scores plotted to 'cluster_scores.png'.")
    print("Feel free to ask me anything about your results or next steps—I’m here to help!")

if __name__ == "__main__":
    main()