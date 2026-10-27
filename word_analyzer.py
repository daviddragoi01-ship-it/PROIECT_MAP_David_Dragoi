import argparse
import sys
import re
import json
import csv
import os
from collections import Counter
STOPWORDS_RO = {'și', 'de', 'pentru', 'că', 'un', 'o', 'la', 'în', 'pe', 'cu', 'din', 'să', 'este'}
STOPWORDS_EN = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'for', 'on'}
def clean_text(text):
    text = text.lower()
    return re.findall(r'\b\w+\b', text)
def get_stats(words):
    if not words: return 0, 0, 0
    unique = set(words)
    avg_len = sum(len(w) for w in words) / len(words)
    ttr = len(unique) / len(words) # Type-Token Ratio
    return avg_len, len(unique), ttr
def generate_word_cloud_text(counter, limit=15):
    # GENERARE WORD CLOUD (TEXT)
    print("\n--- WORD CLOUD (TEXT) ---")
    max_freq = counter.most_common(1)[0][1] if counter else 1
    for word, freq in counter.most_common(limit):
        size = int((freq / max_freq) * 10) + 1
        print(f"{word.upper() if size > 5 else word} {'*' * size}")
def run_analysis(file_path, n_gram=1, top_n=10, export=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Eroare: Fișierul '{file_path}' nu a putut fi găsit.")
        sys.exit(1)
    all_words = clean_text(text)
    filtered = [w for w in all_words if w not in STOPWORDS_RO and w not in STOPWORDS_EN]
    if n_gram > 1:
        tokens = [" ".join(all_words[i:i+n_gram]) for i in range(len(all_words)-n_gram+1)]
    else:
        tokens = filtered
    counts = Counter(tokens)
    top_results = counts.most_common(top_n)
    print(f"\nAnaliză: {file_path} ({len(all_words)} cuvinte)")
    for i, (item, freq) in enumerate(top_results, 1):
        print(f"{i}. {item}: {freq}")
    if export == 'json':
        export_path = 'results.json'
        with open(export_path, 'w', encoding='utf-8') as f: 
            json.dump(dict(top_results), f, ensure_ascii=False, indent=4)
        print(f"\nRezultatele au fost exportate în {export_path}")
    elif export == 'csv':
        export_path = 'results.csv'
        with open(export_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Cuvant/N-grama', 'Frecventa'])
            writer.writerows(top_results)
        print(f"\nRezultatele au fost exportate în {export_path}")
    return all_words, counts
def compare_docs(file1, file2):
    try:
        words1 = set(clean_text(open(file1, 'r', encoding='utf-8').read()))
        words2 = set(clean_text(open(file2, 'r', encoding='utf-8').read()))
    except FileNotFoundError as e:
        print(f"Eroare la citirea fișierelor: {e}")
        sys.exit(1)       
    common = words1.intersection(words2)
    print(f"\nComparație: {len(common)} cuvinte comune între '{file1}' și '{file2}'.")
def search_concordance(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except FileNotFoundError:
        print(f"Eroare: Fișierul '{file_path}' nu a putut fi găsit.")
        sys.exit(1)
    matches = re.findall(r'(.{0,30}' + re.escape(keyword.lower()) + r'.{0,30})', content)
    print(f"\nConcordanță pentru '{keyword}':")
    if not matches:
        print("Cuvântul nu a fost găsit în text.")
    for m in matches[:5]: 
        print(f"...{m}...")
def main():
    parser = argparse.ArgumentParser(description="Aplicație Python pentru procesarea textelor și statistici NLP.")
    parser.add_argument("file", help="Calea către fișierul text principal de analizat")
    parser.add_argument("--top", type=int, default=10, help="Numărul de rezultate de afișat în top (implicit: 10)")
    parser.add_argument("--ngram", type=int, default=1, help="Dimensiunea n-gramei (implicit: 1 pentru cuvinte simple)")
    parser.add_argument("--export", choices=['csv', 'json'], help="Exportă rezultatele topului în format CSV sau JSON")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--compare", metavar="FILE2", help="Compară vocabularul fișierului principal cu un al doilea fișier")
    group.add_argument("--concordance", metavar="KEYWORD", help="Caută contextul (concordanța) unui cuvânt specific în text")
    group.add_argument("--diversity", action="store_true", help="Afișează doar statistici de diversitate lexicală și lungime medie")
    args = parser.parse_args()
    if args.compare:
        compare_docs(args.file, args.compare)
    elif args.concordance:
        search_concordance(args.file, args.concordance)
    elif args.diversity:
        try:
            w = clean_text(open(args.file, 'r', encoding='utf-8').read())
            avg, uniq, ttr = get_stats(w)
            print(f"\nFișier: {args.file}")
            print(f"Diversitate (TTR): {ttr:.3f}")
            print(f"Lungime medie cuvinte: {avg:.2f} caractere")
        except FileNotFoundError:
            print(f"Eroare: Fișierul '{args.file}' nu a putut fi găsit.")
    else:
        words, counts = run_analysis(args.file, n_gram=args.ngram, top_n=args.top, export=args.export)
        generate_word_cloud_text(counts, limit=args.top)
if __name__ == "__main__":
    main()