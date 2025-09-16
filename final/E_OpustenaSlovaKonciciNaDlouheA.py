""" 
v tomto testu se hledají slova, která končí na á, ale nejsou k ničemu připojena (často jsem spadají příjmení)
"""

import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

seznam = []
bez = []

def tisk(seznam, bez):   
    with open("E_OpustenaSlovaKonciciNaDlouheA.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("SLOVA KONČÍCÍ NA 'Á, KTERÁ NEJSOU K NIČEMU PŘIPOJENA")
        f.write("SEZNAM TĚCH, KE KTERÝM BYL NALEZEN POTENCIÁLNÍ PŘEDEK\n")
        f.write(f"{'NALEZENÉ SLOVO'.ljust(20)}{'MOŽNÝ PŘEDEK'.ljust(20)}\n")
        f.write("\n")
        for i in seznam: 
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("\n")

        f.write("SEZNAM TĚCH, KE KTERÝM PŘEDEK NEBYL NALEZEN \n")
        f.write("NALEZENÉ SLOVO \n")
        for i in bez:
            f.write(f"{i}\n")
        
all_lemmas1 = {lemma.lower() for lemma in all_lemmas}

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma[-1] in "á":
        if lexeme.all_parents == [] and (len(lexeme.lemma) > 3 or lexeme.lemma[0].isupper()):
            rodic = ""
            dalsi = ""
            if lexeme.lemma.endswith("ová"): #and lexeme.lemma != "Nová":
                if lexeme.lemma[0].isupper():
                    rodic = lexeme.lemma[:-3]
                    if rodic[-2] not in "aáeěiíoóuůúyý":
                        pomoc = rodic[:-1] + "e" + rodic[-1]
                        dalsi = pomoc
                else:
                    rodic = lexeme.lemma[:-1] + "ý" 

            elif lexeme.lemma.endswith("ická"):
                rodic = lexeme.lemma[:-2] + "e"
            else:
                rodic = lexeme.lemma[:-1].lower()
                rodic = rodic + "ý"

            if rodic in all_lemmas:
                seznam.append((lexeme.lemma, rodic))
            elif dalsi in all_lemmas:
                seznam.append((lexeme.lemma, dalsi))

            else:
                if lexeme.lemma.endswith("ová"):
                    if rodic + "a" in all_lemmas:
                        seznam.append((lexeme.lemma, rodic + "a"))
                    else:
                        rodic = rodic.lower()
                        if rodic in all_lemmas1:
                            seznam.append((lexeme.lemma, rodic))
                        elif dalsi in all_lemmas1:
                            seznam.append((lexeme.lemma, dalsi))
                        else:
                            if lexeme.lemma.endswith("ová"):
                                if rodic + "a" in all_lemmas1:
                                    seznam.append((lexeme.lemma, rodic + "a"))
                                else:
                                    bez.append(lexeme.lemma)


tisk(seznam, bez)
