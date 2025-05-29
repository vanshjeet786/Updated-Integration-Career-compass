#!/usr/bin/env python3
"""
Career Mapping Prototype CLI
"""

import json
# Response scale for Likert questions
RESPONSE_SCALE = {
    "Never": 1, "Sometimes": 2, "Often": 3, "Usually": 4, "Always": 5,
}
# Define sample question sets for Layer 1
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

# ------------------------ LAYER 2: MBTI, Big Five, SDT ------------------------
# Define sample question sets for Layer 2
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

# ------------------------ LAYER 3: Aptitude and Skill Assessment ------------------------
# Define sample question sets for Layer 3
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

# ------------------------ LAYER 4: Background, Context, and Exposure ------------------------
# Define sample question sets for Layer 4
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
# ------------------------ LAYER 5: Real-world Alignment ------------------------
# Define sample question sets for Layer 5
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
# Career Mapping
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
    "Values_Impact": ["Nonprofit Management", "Environmental Advocacy", "Public Health"],
    "Industry_Technology": ["Software Engineer", "AI Specialist", "Cybersecurity Analyst"],
    "Career_Clustering_Creative": ["Content Creator", "Graphic Designer", "Filmmaker"],
    "Career_Clustering_Analytical": ["Data Scientist", "Research Scientist", "Financial Analyst"]
}
# Define weightage
layer_weights = {
    "Layer 1": 0.30,
    "Layer 2": 0.25,
    "Layer 3": 0.25,
    "Layer 4": 0.20,
    "Layer 5": 0.25  # Layer 5 will be treated separately in final suggestion tuning
}
def collect_responses(questions, scale, open_ended=False):
    """Collect user responses for a set of questions."""
    responses = {}
    for category, qs in questions.items():
        responses[category] = []
        print(f"\n{category}:")
        for q in qs:
            if open_ended:
                response = input(f"{q}: ")
                responses[category].append(response)
            else:
                print(f"{q}")
                response = input(f"Enter response ({', '.join(scale.keys())}): ").capitalize()
                while response not in scale:
                    response = input(f"Invalid response. Enter ({', '.join(scale.keys())}): ").capitalize()
                responses[category].append(scale[response])
    return responses

def score_responses(responses):
    """Score responses by averaging or summing numerical values."""
    scores = {}
    for category, vals in responses.items():
        if isinstance(vals[0], int):
            scores[category] = sum(vals) / len(vals)
        else:
            scores[category] = vals
    return scores

def map_to_careers(scores, mapping):
    """Map high-scoring categories to career paths."""
    careers = []
    for category, score in scores.items():
        if isinstance(score, float) and score >= 4:  # Threshold for high score
            if category in mapping:
                careers.extend(mapping[category])
    return list(set(careers))  # Remove duplicates

def main():
    print("Welcome to the 5-Layer Career Mapping System!")

    # Layer 1: Core Intelligence & Cognitive Style
    print("\nLayer 1: Core Intelligence & Cognitive Style")
    layer_1_responses = collect_responses(LAYER_1_QUESTIONS, RESPONSE_SCALE)
    layer_1_scores = score_responses(layer_1_responses)

    # Layer 2: Personality & Motivation
    print("\nLayer 2: Personality & Motivation")
    layer_2_responses = collect_responses(LAYER_2_QUESTIONS, RESPONSE_SCALE)
    layer_2_scores = score_responses(layer_2_responses)

    # Layer 3: Interests, Values, and Work Preferences
    print("\nLayer 3: Interests, Values, and Work Preferences")
    layer_3_responses = collect_responses(LAYER_3_QUESTIONS, RESPONSE_SCALE)
    layer_3_scores = score_responses(layer_3_responses)

    # Layer 4: Real-World Fit & Industry Exposure
    print("\nLayer 4: Real-World Fit & Industry Exposure")
    layer_4_responses = collect_responses(LAYER_4_QUESTIONS, RESPONSE_SCALE)
    layer_4_scores = score_responses(layer_4_responses)

    # Layer 5: Synthesis & Career Mapping
    print("\nLayer 5: Synthesis & Career Mapping")
    layer_5_responses = collect_responses(LAYER_5_QUESTIONS, RESPONSE_SCALE, open_ended=True)

    # Combine scores and map to careers
    all_scores = {**layer_1_scores, **layer_2_scores, **layer_3_scores, **layer_4_scores}
    recommended_careers = map_to_careers(all_scores, CAREER_MAPPING)

    # Output results
    print("\nCareer Recommendations:")
    if recommended_careers:
        for career in recommended_careers:
            print(f"- {career}")
    else:
        print("No strong career matches found. Try adjusting your responses or exploring more options.")

    # Save responses for future reference
    with open("career_mapping_results.json", "w") as f:
        json.dump({
            "Layer_1": layer_1_responses,
            "Layer_2": layer_2_responses,
            "Layer_3": layer_3_responses,
            "Layer_4": layer_4_responses,
            "Layer_5": layer_5_responses,
            "Recommended_Careers": recommended_careers
        }, f, indent=4)
    print("\nResults saved to 'career_mapping_results.json'.")
if __name__ == "__main__":
    main()