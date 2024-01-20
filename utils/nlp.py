from nltk.corpus import stopwords
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



    indumenti = ['maglia', 'maglietta', 'pantaloni', 'jeans', 't-shirt']

    indumenti_cercati = []

    colori = ['bianco', 'bianca', 'bianchi', 'bianche', 'grigio', 'grigia', 'grigi', 'grige',
    'nero', 'nera', 'neri', 'nere', 'blu', 'verde', 'verdi', 'marrone', 'marroni', 'rosse', 'rose',
    'rosa', 'rosso', 'rossa', 'rossi', 'bordeaux', 'giallo', 'gialla', 'gialli', 'gialle', 'arancione', 'arancioni']

    colori_cercati = []

    categoria = ['uomo', 'donna', 'bambino', 'bambina', 'bambini', 'ragazzo', 'ragazza']

    categoria_cercata = []

    vestibilita = ['regolare', 'slim', 'oversize']

    vestibilita_cercata = []

    for token in filtered_words:
        if token in indumenti:
            indumenti_cercati.append(token)
        if token in colori:
            colori_cercati.append(token)
        if token in categoria:
            categoria_cercata.append(token)
        if token in vestibilita:
            vestibilita_cercata.append(token)

    print("indumenti trovati", indumenti_cercati)
    print("colori trovati", colori_cercati)
    print("categoria trovati", categoria_cercata)
    print("vestibilita trovati", vestibilita_cercata)


    return filtered_words, indumenti_cercati, colori_cercati, categoria_cercata, vestibilita_cercata
