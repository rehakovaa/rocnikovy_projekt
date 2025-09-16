import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}


def alternativy(otec, syn):
    if syn == "ú" + otec[2:] or syn == "o" + otec[2:]:
        return True
    else:
        return None

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

def tisk(resitelne, neresitelne):
    with open("W_PodobneDlouhaSlovaJinePocatecniPismeno.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("SLOVA, KTERÁ JSOU PODOBNĚ KRÁTKÁ JAKO JEJICH PŘEDEK, ALE ZAČÍNAJÍ NA JINÉ PÍSMENO \n")
        f.write("SEZNAM TĚCH, KTERÉ BY MĚLY BÝT PROHOZENÉ, TEDY RODIČ BY MĚL BÝT POD SYNEM\n")
        f.write(f"{'PŮVODNÍ SLOVO'.ljust(20)}{'PŮVODNÍ PŘEDEK'.ljust(20)}\n")
        f.write("\n")
        for i in resitelne: 
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("\n")

        f.write("SEZNAM TĚCH, KTERÉ SPLNILY KRITÉRIA, SEŘAZENY PODLE LEVENHSTEINOVY VZDÁLENOSTI \n")
        f.write(f"{'PŮVODNÍ SLOVO'.ljust(20)}{'PŮVODNÍ PŘEDEK'.ljust(20)}{'VZDÁLENOST'.ljust(20)}\n")
        for i in  sorted(neresitelne, key=lambda x: x[2], reverse=True):
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}{str(i[2]).ljust(20)}\n")
    
            
seznam = []
mozne = []

for lexeme in lexicon.iter_lexemes():
    for i in lexeme.all_parents:
        if len(lexeme.lemma) < len(i.lemma) + 2 and lexeme.lemma[0] != i.lemma[0]:
            #pojistit rozdily:
            if lexeme.lemma[0].lower() == i.lemma[0].lower(): #čáslavský x Čáslav
                continue
            elif i.lemma.startswith("-"):
                continue
            elif len(lexeme.lemma) < 7 and levenhstein(lexeme.lemma, i.lemma) < 2:
                continue
            elif len(lexeme.lemma) > 6 and levenhstein(lexeme.lemma, i.lemma) < 3:
                continue
            elif "apgrejd" in lexeme.lemma:
                if "upgrade" + lexeme.lemma[7:] == i.lemma:
                    continue  
            else:
                reseni = alternativy(lexeme.lemma, i.lemma)
                if reseni is None:
                    seznam.append((lexeme.lemma, i.lemma, levenhstein(lexeme.lemma, i.lemma)))
                else:
                    mozne.append((lexeme.lemma, i.lemma))

tisk(mozne, seznam)
