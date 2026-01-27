import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize once (efficient)
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    """
    Clean and preprocess text for ML analysis
    Steps:
    - Lowercasing
    - Remove punctuation
    - Remove stopwords
    - Lemmatization
    """

    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 3. Remove numbers and extra spaces
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\b(et al|fig|table)\b", "", text)

    # 4. Tokenize and clean
    tokens = text.split()

    cleaned_tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token not in stop_words and len(token) > 2
    ]

    # 5. Reconstruct text
    cleaned_text = " ".join(cleaned_tokens)

    return cleaned_text