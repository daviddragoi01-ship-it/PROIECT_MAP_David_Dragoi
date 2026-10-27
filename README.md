# Proiect_MAP
# Analiză Frecvență Cuvinte - Tema 17
Aplicație Python pentru procesarea textelor și statistici NLP.

## Instrucțiuni de rulare (Docker)
1. Construiți imaginea:
   `docker build -t word-analyzer .`
2. Rulați analiza:
   `docker run word-analyzer nume_fisier.txt --top 10`