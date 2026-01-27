from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def extract_keywords(corpus, top_n=10):
    """
    Extract top N TF-IDF keywords for each document

    corpus: list of cleaned text documents
    top_n: number of keywords per paper
    """

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
    max_df=0.85,
    min_df=2,
    ngram_range=(1, 2),
    token_pattern=r"(?u)\b[a-zA-Z]{4,}\b"
)

    # Fit and transform corpus
    tfidf_matrix = vectorizer.fit_transform(corpus)

    feature_names = np.array(vectorizer.get_feature_names_out())

    keywords_per_paper = []

    # Extract keywords for each document
    for row in tfidf_matrix:
        scores = row.toarray().flatten()
        top_indices = scores.argsort()[-top_n:][::-1]
        keywords = feature_names[top_indices]
        keywords_per_paper.append(keywords.tolist())

    return keywords_per_paper, tfidf_matrix, vectorizer