from nltk.corpus import stopwords
import stanza
from gensim.models import KeyedVectors

word_vectors = KeyedVectors.load("C:\\Users\\divic\\Desktop\\ProgettoFIA\\SG-300-W10N20E50\\W2V.kv", mmap='r+')
vocabs = word_vectors.index_to_key

# nltk.download('stopwords')
# stanza.download('it')

nlp = stanza.Pipeline('it')

stop_words = set(stopwords.words('italian'))


def auto_map_word(word):
    print("parola: ", word)
    if word in vocabs:
        if word.endswith("i") or word.endswith("e"):
            if word == "uomini":
                singular_form = word[:-3] + "o"
                print("forma:", singular_form)
                return singular_form
            if word == "donne" or word == "maglie" or word == "rose":
                singular_form = word[:-1] + "a"
                print("forma:", singular_form)
                return singular_form
            if word == "verdi" or word == "marroni" or word == "arancioni":
                singular_form = word[:-1] + "e"
                print("forma:", singular_form)
                return singular_form
            if word == "verde" or word == "marrone" or word == "arancione":
                singular_form = word
                print("forma:", singular_form)
                return singular_form
            if word == "pantaloni":
                singular_form = word
                print("forma:", singular_form)
                return singular_form
            if word == "pantalone":
                singular_form = word[:-1] + "i"
                print("forma:", singular_form)
                return singular_form
            if word == "grigi":
                singular_form = word + "o"
                print("forma:", singular_form)
                return singular_form
            if word == "bianchi" or word == "bianche":
                singular_form = word[:-2] + "o"
                print("forma:", singular_form)
                return singular_form
            singular_form = word[:-1] + "o"
            if singular_form in vocabs:
                return singular_form
        elif word.endswith("a"):
            if word == "maglia" or word == "donna" or word == "rosa":
                return word
            masculine_form = word[:-1] + "o"
            if masculine_form in vocabs:
                return masculine_form
        else:
            return word
    else:
        similar_words = word_vectors.similar_by_word(word, topn=1)
        print("Parola simile?", similar_words)
        if similar_words:
            similar_word = similar_words[0][0]
            if similar_word in vocabs:
                print("1. ", similar_word)
                return similar_word
            else:
                return word


def preprocess_text(text):
    doc = nlp(text)

    filtered_words = [word.text.lower() for sent in doc.sentences for word in sent.words
                      if word.text.isalnum() and word.text.lower() not in stop_words
                      and word.pos not in ['VERB', 'AUX']]
    print(filtered_words)

    indumenti = ['maglia', 'pantaloni']
    colori = ['bianco', 'blu', 'rosso', 'marrone', 'nero', 'bordeaux', 'arancione', 'grigio', 'rosa', 'verde']
    categoria = ['uomo', 'donna', 'bambino']

    indumenti_cercati = []
    colori_cercati = []
    categoria_cercata = []

    mapped_word = []

    for token in filtered_words:
        mapped_word.append(auto_map_word(token))

    for token in mapped_word:
        print("token: ", token)
        if token in indumenti:
            indumenti_cercati.append(token)
        if token in colori:
            colori_cercati.append(token)
        if token in categoria:
            categoria_cercata.append(token)

    print("colori mappati", colori_cercati, "\n")
    print("indumenti mappati", indumenti_cercati, "\n")
    print("categoria mappata", categoria_cercata, "\n")

    return indumenti_cercati, colori_cercati, categoria_cercata
