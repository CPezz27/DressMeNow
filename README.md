# DressMeNow

Obiettivo del sistema 

L'obiettivo primario di DressMeNow consiste nel migliorare significativamente la precisione nella selezione della taglia e nella valutazione della vestibilità, mediante l'introduzione di un avatar virtuale. Tale innovazione mira a ridurre in modo sostanziale il numero di resi da parte degli utenti. L'avatar consentirà agli utenti di visualizzare in maniera realistica e dettagliata come i prodotti si adattano alle varie morfologie del corpo, con l'obiettivo di migliorare l'esperienza di shopping online e di minimizzare le probabilità di acquisti errati. Inoltre, l'implementazione di questa tecnologia contribuirà a promuovere transazioni più sostenibili dal punto di vista ecologico, considerando che i resi rappresentano una delle principali fonti di inquinamento derivanti dagli acquisti online. 

 

# Ambito del sistema 

DressMeNow è un e-commerce specializzato nella vendita di abbigliamento. 

 

# Obiettivi e criteri di successo del sistema 

Assumendo aziende grandi come Zalando che nell’anno 2020 ha effettuato 185,5 milioni di ordini. Secondo dati di mercato, è noto che il 10% di questi ordini, pari a 18.550.000 circa, viene reso. Di questi 18.550.000 ordini il 42% corrispondenti a 7.797.000 ordini corrispondono a resi dovuti a cambi di idea sulla vestibilità del prodotto. Poiché il nostro software mira a ridurre significativamente questi resi, che rappresentano un costo totale di 7.797.000*5€ (dove 5€ rappresenta il costo di una spedizione in media per una azienda) annui per resi dovuti al cambio di idea della vestibilità arriviamo a parlare di 38,985,000€ di spedizioni secondo le statistiche. Ci aspettiamo di catturare il 0,5% di questo importo, ovvero 194.250€. Tale collaborazione si tradurrà in un notevole miglioramento nella precisione degli ordini effettuati dagli utenti. Questa collaborazione con aziende di alto profilo incoraggerà i clienti a effettuare acquisti con maggiore fiducia e, di conseguenza, a ridurre il numero di resi. Ciò, a sua volta, comporterà risparmi per l'azienda e nel tempo attirerà un numero crescente di clienti. Portando un guadano di minimo un milione l’anno. Sicuramente agni anno puteremo a far sì che il nostro software sì sempre più preciso e perfetto nella simulazione e puntando in base al successo di aumentare anche le tasse per d’uso in base all’inflazione dell'aggiunta del nostro software. 

 
DressMeNow si impegna a far ridurre la quantità di resi effettuati dai clienti per avere un impatto dal punto di vista ecologico migliore rispetto ai principali competitor nell’ambito di e-commerce specializzati nella vendita di indumenti. In particolar modo si è studiato che: 

Nel 2020, il tasso di restituzione dei prodotti di e-commerce è aumentato del 70% rispetto all'anno precedente (soocial.com). 

Si stima che nel 2020 siano stati restituiti 428 miliardi di dollari di merce al dettaglio, con poco più di 100 miliardi di dollari di merce online restituita (clevertap.com). 

Solo negli Stati Uniti, il 21% dei prodotti restituiti erano articoli di abbigliamento (nosto.com). 

Il tasso medio di ritorno nell'e-commerce è del 18,1% (NRF, HubSpot). 

Il 34% degli acquirenti Amazon ha restituito un articolo perché la taglia, il colore o la vestibilità erano sbagliati (Narvar). 

Shopify registra una diminuzione del 40% dei resi di prodotti grazie alla visualizzazione in 3D (Wizeline) 

# Parte FIA

La parte di FIA lato backand è divisa in 3 file: La prima parte è quella che ci permette di connetterla al server specificando la rotta (così da averla raggiunggibile), poi c'è la seconda in cui si concentra la parte di intelligenza artificiale, infine la terza in Prodotto.py in cui abbiamo la funzione search_products contenente la query che si interfaccia con il database una volta ottenute le informazioni di cui necessita e controlla se nel DB sono presenti prodotti corrispondenti. Soffermandoci sulla seconda è presente l'importazione delle librerie necessarie e del modello (Caricato tramite path) e la lisa di vocaboli in vocabs.

Sono necessari i download delle stopwords in nltk e del linguaggio italiano tramite la libreria stanza. Il linguaggio italiano viene poi caricato e vengono specificate le stop words della lingua italiana.

Per prima cosa nella funzione preprocess_text creiamo un documento che contenga le informazioni delle parole nel testo passato alla funzione.
Tali parole vengono successivamente filtrate, rimuovendo eventuali stop word, segni di punteggiatura, verbi ed ausiliari.
Salviamo in una lista tutte le parole filtrate.
Creiamo quindi delle liste contenenti tutti i possibili elementi che ci interessa cercare nel database, e creiamo delle liste vuote che, qualora questi elementi dovessero essere trovati, verrebbero salvati nelle liste appropriate. 
Creiamo quindi una lista in cui mappiamo le parole in base alle nostre necessità e le mappiamo tramite un'altra funzione, auto_map_word in cui ci sono tutte le informazione e tutto il mapping necessario affinché possiamo avere le parole che ci interessano elaborate nel modo in cui ci interessa.
Una volta ottenuta la parola filtrata (salvata nella lista delle parole mappata), andiamo a confrontare token per token se è presente in una delle liste con le caratteristiche che ci servono e, in caso sia presente, la salviamo nella lista vuota creata precedentemente.
Una volta effettuato questo procedimento, restituiamo le liste con tutti gli elementi trovati. Se le liste sono vuote non verranno trovati risultati, altrimenti per ogni caratteristica/gruppo di caratteristiche con prodotti corrispondenti, avremo un elenco di risultati.
