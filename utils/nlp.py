import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import stanza

# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# stanza.download('it')

nlp = stanza.Pipeline('it')

stop_words = set(stopwords.words('italian'))


def preprocess_text(text):
    # Tokenizzazione e rimozione delle stop words
    doc = nlp(text)

    filtered_words = [word.text.lower() for sent in doc.sentences for word in sent.words
                      if word.text.isalnum() and word.text.lower() not in stop_words
                      and word.pos not in ['VERB', 'AUX']]  # 'VERB' per i verbi

    print(filtered_words)

    return filtered_words
