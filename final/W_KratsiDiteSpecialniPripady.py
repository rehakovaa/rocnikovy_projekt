import derinet.lexicon as dlex
import os


lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

def levenhstein(prvni, druhy):
    n = len(prvni)
    m = len(druhy)
    tabulka = [[0] * (m + 2) for _ in range(n + 2)]
    for i in range(1, n+ 2):
        tabulka[i][m+1] = n - i + 1
    for j in range(1, m + 2):
        tabulka[n+ 1][j] = m - j + 1
    for i in range(n, 0, -1):
        for j in range(m, 0, -1):
            delta = 1
            if prvni[i - 1] == druhy[j-1]:
                delta = 0
            tabulka[i][j] = min(delta + tabulka[i + 1][j + 1], 1 + tabulka[i + 1][j], 1 + tabulka[i][j + 1])

    return tabulka[1][1]

def tisk(seznam):
    with open("W_KratsiDiteSpecialniPripady.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("SLOVA, JEJICHŽ RODIČE JSOU KRATŠÍ A MÉNĚ ČASTÉ NEŽ ONY SAMY A NESPLŇUJÍ KRITÉRIUM, ABY TO TAK MOHLO BÝT\n")
        f.write("kritéria: slovo končí na -ismus nebo ika")
        f.write("SEŘAZENO PODLE LEVENHSTEINOVY VZDÁLENOSTI \n")
        f.write("\n")
        f.write(f"{'ZKOUMANÉ SLOVO'.ljust(20)}{'RODIČ'.ljust(20)}{'VZDÁLENOST'.ljust(20)}\n")
        f.write("\n")
        for i in sorted(seznam,  key=lambda x: x[2], reverse=True): 
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}{str(i[2]).ljust(20)}\n")

seznam = []
for lexeme in lexicon.iter_lexemes():
    for i in lexeme.all_parents:
        if len(i.lemma) > len(lexeme.lemma) + 2 and lexeme.pos == i.pos:
            casto_i = i.misc["corpus_stats"]["absolute_count"]
            casto_lemma = lexeme.misc["corpus_stats"]["absolute_count"]

            if casto_i < casto_lemma:
                if lexeme.lemma.endswith(("ismus", "izmus")) and levenhstein(lexeme.lemma[:-5], i.lemma) < 2:
                    continue
                elif lexeme.lemma.endswith(("ika")) and levenhstein(lexeme.lemma[:-3], i.lemma) < 2:
                    continue
                else:
                    seznam.append((lexeme.lemma, i.lemma, levenhstein(lexeme.lemma, i.lemma)))

tisk(seznam)