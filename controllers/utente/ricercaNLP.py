import string

from flask import Blueprint, render_template, request, redirect

import spacy
from nltk.corpus import stopwords
from nltk import word_tokenize, sent_tokenize, pos_tag
from langdetect import detect
from translate import Translator
import language_tool_python
from transformers import T5ForConditionalGeneration, T5Tokenizer
from happytransformer import HappyTextToText
from happytransformer import TTSettings


# Scarica i dati necessari per NLTK
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


app_bp = Blueprint('user_register', __name__)


@app_bp.route('/ricerca', methods=["GET", "POST"])
def ricercaNLP():

    if request.method == 'POST':
        text = request.form.get('text')

        # Verifica la lingua del testo
        text_language = detect(text)
        source_lang = detect(text)
        translator = Translator(from_lang=source_lang, to_lang='en')

        # Traduce il testo in inglese se non è già nella lingua inglese
        if text_language != 'en':
            translated_text = translator.translate(text)
        else:
            translated_text = text

        model = HappyTextToText("T5", "vennify/t5-base-grammar-correction")

        beam_settings = TTSettings(num_beams=5, min_length=1, max_length=100)

        translated_text = model.generate_text("grammar: " + translated_text, args=beam_settings).text

        # python -m spacy download en_core_web_trf
        nlp = spacy.load("en_core_web_trf")
        doc = nlp(translated_text)

        capi_abbigliamento = {}
        capi_di_abbigliamento = [
            'hat', 'hats', 'cap', 'beanie', 'beret', 'bowler', 'fedora', 'top-hat', 'baseball-cap',
            'visor', 'sombrero', 'headband', 'headscarf', 'headwrap', 'bandana', 'turban',
            'tiara', 'crown', 'headphones', 'earmuffs', 'sunglasses', 'glasses', 'monocle',
            'contact-lenses', 'necktie', 'bow-tie', 'cravat', 'scarf', 'shawl', 'wrap', 'stole',
            'necklace', 'choker', 'pendant', 'locket', 'chain', 'bracelet', 'bangle', 'cuff',
            'watch', 'smartwatch', 'wristband', 'ring', 'earrings', 'stud', 'hoop', 'dangle',
            'brooch', 'pin', 'badge', 'corsage', 'lapel pin', 'blouse', 'shirt', 't-shirt', 'tshirt'
            'polo-shirt', 'tank-top', 'sweater', 'cardigan', 'hoodie', 'pullover', 'jumper',
            'jersey', 'tunic', 'vest', 'waistcoat', 'blazer', 'jacket', 'jackets', 'coat', 'overcoat',
            'raincoat', 'poncho', 'trench coat', 'pea-coat', 'dress', 'dresses', 'gown', 'evening-gown',
            'cocktail-dress', 'ball-gown', 'sundress', 'shift-dress', 'wrap dress', 'kimono',
            'kaftan', 'abaya', 'jumpsuit', 'romper', 'playsuit', 'trousers', 'pants', 'slacks',
            'jeans', 'shorts', 'skirt', 'mini skirt', 'midi-skirt', 'maxi-skirt', 'pleated-skirt',
            'pencil-skirt', 'a-line-skirt', 'wrap-skirt', 'culottes', 'leggings', 'tights', 'stockings',
            'socks', 'hosiery', 'tights', 'footwear', 'shoes', 'boots', 'sneakers', 'trainers',
            'sandals', 'flip-flops', 'slippers', 'heels', 'flats', 'sweatshirt', 'scarve', 'scarves',
            'suit', 'suits'
        ]

        for token in doc:
            if token.text.lower() in capi_di_abbigliamento:
                aggettivi = set()
                for child in token.subtree:
                    if child.dep_ == "amod" and child.pos_ == "ADJ" and child.head.text.lower() == token.text.lower():
                        aggettivi.add(child.text)
                    elif child.dep_ == "amod" and child.pos_ == "ADJ" and child.head.dep_ == "compound":
                        aggettivi.add(child.text)
                if aggettivi:
                    capi_abbigliamento[token.text.lower()] = aggettivi

        print(capi_abbigliamento)

        return render_template('/utente/ricerca_NLP.html', data="test")

    return render_template('/utente/ricerca_NLP.html')
