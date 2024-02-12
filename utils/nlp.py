from nltk.corpus import stopwords
import stanza
from gensim.models import KeyedVectors

word_vectors = KeyedVectors.load("C:\\Users\\divic\\Desktop\\ProgettoFIA\\SG-300-W10N20E50\\W2V.kv", mmap='r+')
vocabs = word_vectors.index_to_key
vectors = word_vectors.vectors

# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# stanza.download('it')

nlp = stanza.Pipeline('it')

stop_words = set(stopwords.words('italian'))


def auto_map_word(word):
    print("Parola:", word)
    if word in vocabs:
        print("La parola è già presente nel vocabolario:", word)
        return word

    if word.endswith("i") or word.endswith("e"):
        singular_form = word[:-1]
        if singular_form in vocabs:
            print("Trovata forma singolare:", singular_form)
            return singular_form

    elif word.endswith("a"):
        masculine_form = word[:-1] + "o"
        if masculine_form in vocabs:
            print("Trovata forma maschile:", masculine_form)
            return masculine_form

    elif word.endswith("he"):
        masculine_form = word[:-2] + "o"
        if masculine_form in vocabs:
            print("Trovata forma maschile singolare:", masculine_form)
            return masculine_form

    similar_words = word_vectors.similar_by_word(word, topn=1)
    print("Parola simile:", similar_words)
    if similar_words:
        similar_word = similar_words[0][0]
        if similar_word in vocabs:
            print("Parola simile trovata nel vocabolario:", similar_word)
            return similar_word

    return word


def preprocess_text(text):
    doc = nlp(text)

    filtered_words = [word.text.lower() for sent in doc.sentences for word in sent.words
                      if word.text.isalnum() and word.text.lower() not in stop_words
                      and word.pos not in ['VERB', 'AUX']]
    print(filtered_words)

    indumenti = ['maglia', 'pantaloni']
    colori = ['bianco', 'blu', 'rosso', 'marrone', 'nero', 'bordeaux', 'arancione', 'grigio', 'rosa', 'verde']
    categoria = ['uomo', 'donna']

    indumenti_cercati = []
    colori_cercati = []
    categoria_cercata = []

    for token in filtered_words:
        mapped_word=auto_map_word(token)
        if mapped_word in indumenti:
            indumenti_cercati.append(token)
        if mapped_word in colori:
            colori_cercati.append(token)
        if mapped_word in categoria:
            categoria_cercata.append(token)

    print("colori mappati", colori_cercati, "\n")
    print("indumenti mappati", indumenti_cercati, "\n")
    print("categoria mappata", categoria_cercata, "\n")

    return filtered_words, indumenti_cercati, colori_cercati, categoria_cercata