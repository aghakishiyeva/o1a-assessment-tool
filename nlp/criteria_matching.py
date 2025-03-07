import os
import re
import nltk
from sentence_transformers import SentenceTransformer, util

# Ensure punkt tokenizer is downloaded
nltk.download("punkt", quiet=True)

# Load AI model for semantic similarity
model = SentenceTransformer("all-mpnet-base-v2")

# Get absolute path for criteria.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def clean_text(text):
    """Clean and preprocess the CV text."""
    # Remove symbols and non-alphanumeric characters
    text = re.sub(r"[^\w\s.,-]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_criteria():
    """Load O-1A visa criteria from a file."""
    criteria_path = os.path.join(BASE_DIR, "criteria.txt")
    if not os.path.exists(criteria_path):
        raise FileNotFoundError(f"Criteria file not found: {criteria_path}")

    with open(criteria_path, "r", encoding="utf-8") as f:
        criteria = [line.strip() for line in f.readlines()]
    return criteria


def compute_embeddings(text_list):
    """Convert a list of texts to vector embeddings."""
    return model.encode(text_list, convert_to_tensor=True)


def keyword_match(cv_text, criteria):
    """Match CV text to criteria using keyword matching."""
    keyword_matches = {criterion: [] for criterion in criteria}
    for criterion in criteria:
        # Extract keywords from the criterion description
        keywords = re.findall(r"\b\w+\b", criterion.lower())
        for sentence in nltk.sent_tokenize(cv_text.lower()):
            if any(keyword in sentence for keyword in keywords):
                keyword_matches[criterion].append({"text": sentence})
    return keyword_matches


def match_criteria(cv_text, threshold=0.4):
    """Match CV content to O-1A criteria and categorize results."""

    # Clean the CV text
    cv_text = clean_text(cv_text)

    # Load O-1A criteria
    criteria = load_criteria()
    print("Loaded Criteria:", criteria)

    # Tokenize CV text into sentences
    cv_sentences = nltk.sent_tokenize(cv_text)
    print("CV Sentences:", cv_sentences)

    # Compute embeddings
    criteria_embeddings = compute_embeddings(criteria)
    cv_embeddings = compute_embeddings(cv_sentences)

    # Calculate similarity scores
    similarity_matrix = util.pytorch_cos_sim(cv_embeddings, criteria_embeddings)
    print("Similarity Matrix:", similarity_matrix)

    # Group matches into criteria categories
    categorized_results = {criterion: [] for criterion in criteria}

    for i, criterion in enumerate(criteria):
        for j, sentence in enumerate(cv_sentences):
            score = similarity_matrix[j][i].item()
            if score >= threshold:
                categorized_results[criterion].append(
                    {"score": round(score, 2), "text": sentence}
                )

    # Fallback to keyword matching if no matches found
    if all(len(matches) == 0 for matches in categorized_results.values()):
        print(
            "No matches found with semantic similarity. Falling back to keyword matching."
        )
        keyword_matches = keyword_match(cv_text, criteria)
        for criterion, matches in keyword_matches.items():
            if matches:
                categorized_results[criterion].extend(matches)

    print("Categorized Results:", categorized_results)

    # Assign overall qualification rating
    num_matched_criteria = sum(1 for matches in categorized_results.values() if matches)
    print("Number of Matched Criteria:", num_matched_criteria)

    if num_matched_criteria >= 5:
        qualification_rating = "High"
    elif num_matched_criteria >= 3:
        qualification_rating = "Medium"
    else:
        qualification_rating = "Low"

    return {
        "qualifications": categorized_results,
        "O-1A Qualification Rating": qualification_rating,
    }
