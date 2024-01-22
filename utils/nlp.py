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

    indumenti = ['maglia', 'maglietta', 'pantaloni', 'jeans', 't-shirt', 'pantalone']

    mappatura_indumenti = {
        'maglietta': 'maglia',
        't-shirt': 'maglia',
        'pantalone': 'pantaloni',
    }

    indumenti_cercati = []

    colori = ['bianco', 'bianca', 'bianchi', 'bianche', 'grigio', 'grigia', 'grigi', 'grige', 'arancioni'
              'nero', 'nera', 'neri', 'nere', 'blu', 'verde', 'verdi', 'marrone', 'marroni', 'rosse', 'rose',
              'rosa', 'rosso', 'rossa', 'rossi', 'bordeaux', 'giallo', 'gialla', 'gialli', 'gialle', 'arancione']

    mappatura_colori = {
        'bianca': 'bianco',
        'bianchi': 'bianco',
        'bianche': 'bianco',
        'grigio': 'grigia',
        'grigi': 'grigia',
        'grige': 'grigia',
        'nera': 'nero',
        'neri': 'nero',
        'nere': 'nero',
        'rosse': 'rosso',
        'rose': 'rosso',
        'rossa': 'rosso',
        'rossi': 'rosso',
        'gialla': 'giallo',
        'gialli': 'giallo',
        'gialle': 'giallo',
        'arancioni': 'arancione',
    }

    colori_cercati = []

    categoria = ['uomo', 'donna', 'bambino', 'bambina', 'bambini', 'ragazzo', 'ragazza']

    mappatura_categoria = {
        'ragazzo': 'uomo',
        'ragazza': 'donna',
        'bambina': 'bambino',
        'bambini': 'bambino',
    }

    categoria_cercata = []

    vestibilita = ['regolare', 'largo', 'stretto', 'slim', 'oversize']

    mappatura_vestibilita = {
        'largo': 'oversize',
        'stretto': 'slim',
    }

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

    colori_mappati = [mappatura_colori.get(colore, colore) for colore in colori_cercati]
    indumenti_mappati = [mappatura_indumenti.get(indumenti, indumenti) for indumenti in indumenti_cercati]
    categoria_mappata = [mappatura_categoria.get(categoria, categoria) for categoria in categoria_cercata]
    vestibilita_mappata = [mappatura_vestibilita.get(vestibilita, vestibilita) for vestibilita in vestibilita_cercata]

    print("indumenti trovati", indumenti_cercati)
    print("colori trovati", colori_cercati)
    print("categoria trovati", categoria_cercata)
    print("vestibilita trovati", vestibilita_cercata)

    print("colori mappati", colori_mappati, "\n")
    print("indumenti mappati", indumenti_mappati, "\n")
    print("categoria mappata", categoria_mappata, "\n")
    print("vestibilità mappata", vestibilita_mappata, "\n")

    return filtered_words, indumenti_mappati, colori_mappati, categoria_mappata, vestibilita_mappata
