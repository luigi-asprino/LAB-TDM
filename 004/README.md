# Lezione 4 — Approfondimenti dopo la lezione

Questa nota riprende tre domande emerse durante la lezione sull'elaborazione video frame-by-frame con OpenCV. La prima risposta data va precisata. Sulle altre due si aggiungono alcune considerazioni.

---

## 1. Leggere e riscrivere un video fa perdere qualità?

**In aula** la risposta è stata che la qualità si perde solo alla cattura del video e che le successive letture e scritture non la riducono. **Questa risposta va precisata.**

- **La lettura non perde qualità.** `cap.read()` decodifica il video e restituisce esattamente ciò che il file contiene.
- **La scrittura perde qualità.** `cv2.VideoWriter` *ricodifica* ogni frame con un codec con perdita (`mp4v` o H.264). Ogni ciclo decodifica → ricodifica aggiunge nuovo errore, **anche se il video non viene modificato e il codec è lo stesso**. Il fenomeno si chiama *generation loss*.

### Perché anche con lo stesso codec

1. **Il codificatore riparte da capo.** Riceve frame già decodificati, non i dati compressi del file originale. Rifà la stima del moto, la suddivisione in blocchi e la quantizzazione, e le sue decisioni non coincidono con quelle della prima codifica. Quantizzare una seconda volta un segnale già quantizzato non restituisce lo stesso segnale: l'errore si accumula.
2. **OpenCV converte anche lo spazio colore.** Il video è memorizzato in YCbCr con sottocampionamento della crominanza 4:2:0, mentre `read()` restituisce frame BGR. Ogni riscrittura esegue quindi YCbCr 4:2:0 → BGR → YCbCr 4:2:0, un passaggio che da solo introduce errori di arrotondamento e di ricostruzione della crominanza.


---

## 2. Perché la frame generation delle schede video ha problemi con il testo?

Durante la discussione sull'esercizio del raddoppio dei frame è stata citata la *frame generation* delle schede video recenti, che nelle prime versioni produceva errori evidenti sul testo.

La frame generation inserisce frame generati tra quelli realmente renderizzati, stimando il movimento tra frame consecutivi. NVIDIA descrive DLSS 3 come basato su *optical flow* e sui vettori di moto del motore di gioco. È quindi l'idea vista in aula: non duplicare i frame, ma generare frame intermedi che seguano il movimento.

Il testo e gli elementi dell'interfaccia (indicatori, etichette, menu) mettono in difficoltà questa stima per alcune ragioni:

- **Non si muovono come la scena.** Sono disegnati sopra l'immagine, spesso fermi rispetto allo schermo o legati a oggetti in movimento. Se il frame intermedio viene ricostruito per intero seguendo il moto della scena, anche l'interfaccia viene spostata e deformata.
- **Hanno bordi netti e dettagli di pochi pixel.** Una lettera occupa poche decine di pixel con transizioni brusche tra aree di colore uniforme. Un piccolo errore nella stima del moto basta a renderla illeggibile, mentre su un'immagine naturale, con variazioni più graduali, lo stesso errore passa inosservato.

Le recensioni delle prime versioni di DLSS 3 indicano proprio l'interfaccia come il problema più evidente: etichette e testi che appaiono "garbled", cioè rimescolati, nei frame generati. La soluzione suggerita è applicare la frame generation alla sola scena e aggiungere l'interfaccia dopo.

Per approfondire:
- [DLSS 3 Tested (TechSpot)](https://www.techspot.com/article/2546-dlss-3/)
- [NVIDIA DLSS 3: annuncio e descrizione tecnica](https://www.nvidia.com/en-sg/geforce/news/dlss3-ai-powered-neural-graphics-innovations)

---

## 3. Esistono funzioni che elaborano l'intero video in un colpo solo?

**In OpenCV no.** Le funzioni viste a lezione (`cvtColor`, `GaussianBlur`, `Canny`, `adaptiveThreshold`) lavorano su una singola immagine. Il modo standard di elaborare un video è il ciclo frame per frame implementato nel notebook.