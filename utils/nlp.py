import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download('stopwords')
stop_words = set(stopwords.words('italian'))


def preprocess_text(text):
    # Tokenizzazione e rimozione delle stop words
    words = word_tokenize(text)
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return filtered_words