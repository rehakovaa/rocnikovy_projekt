""" 
tento test hledá číslovky končící na 'ero', 'erý', 'krát' a 'istý', které jsou bez rodiče, což by neměly být
"""

import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def tvorba_predku():
    predci = set()
    for lex in lexicon.iter_lexemes(): 
        if lex.pos == "NUM":
            predci.add(lex.lemma)
    return predci 

def hledani_predku(predci, dite):
    mozni = set()
    for lex in predci:
        if lex in dite and lex != dite: 
            mozni.add(lex)
    
    konecny = set()
    #tohle to míří na to, abych tam neměl sto a stodva zároveň
    for i in mozni:
        for j in mozni:
            if i in j and i != j:
                konecny.add(i)
    
    return mozni.difference(konecny)

def vypisovani(existuji, neexistuji):
    with open("E_OsamocenaKoncovkaEroEryKratIsty.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("ČÍSLOVKY KONČÍCÍ NA 'ERO', 'ERÝ', 'KRÁT', 'ISTÝ', KTERÉ JSOU BEZ RODIČE \n")
        f.write("ČÍSLOVKY S NALEZENÝMI PŘEDKY: \n")

        f.write("PŘÍKLAD TISKU: \n")
        f.write("číslovka \n")
        f.write(f"  předek\n")
        f.write("\n")

        for pod, cisla in sorted(existuji, key=lambda x: len(x[1]), reverse=False):
            f.write(f"{pod}\n")
            for i in cisla:
                f.write(f"  {i}\n")

        f.write("\n")
        f.write("ČÍSLOVKY, PRO KTERÉ NEBYL NALEZEN PŘEDEK: \n")
        f.write("\n")
        for i in neexistuji:
            f.write(f"{i} \n")

#mireno na slova jako desatero, devátý,

seznam = []
bez = []
predci = tvorba_predku()

for lexeme in lexicon.iter_lexemes():
    if lexeme.pos == "NUM" and lexeme.lemma.endswith(("krát", "istý", "erý", "ero")) :
        if lexeme.all_parents == []:
            moznosti = []
            hotovo = False
            rodic = None

            if lexeme.lemma.endswith("krát"):
                rodic = lexeme.lemma[:-4]
            elif lexeme.lemma.endswith("istý"):
                moznosti.append("sto")
                rodic = lexeme.lemma[:-4]
            elif lexeme.lemma.endswith(("erý", "ero")):
                rodic = lexeme.lemma[:-3]
            else:
                print(lexeme.lemma)

            #když stačí uříznout jenom konec
            if rodic is not None:
                if rodic in all_lemmas:
                    moznosti.append(rodic)
                    hotovo = True
            
            if not hotovo:  
                dalsi = None      
                if rodic.endswith(("dvacát", "čtyřicát", "třicat")):
                    dalsi = rodic[:-2] + "e" + rodic[-1]
                elif rodic.endswith("devat"):
                    dalsi = rodic[:-2] + "ě" + rodic[-1]
                elif rodic == "desat":
                    dalsi = "deset"
                elif rodic.endswith("desat"):
                    dalsi = rodic[:-2] + "á" + rodic[-1]
                elif rodic.startswith("dvou"):
                    dalsi = rodic[4:]
                    moznosti.append("dva")
                elif rodic.startswith("tří"):
                    dalsi = rodic[3:]
                    moznosti.append("tři")
                elif lexeme.lemma.endswith("krát"):
                    dalsi = lexeme.lemma[:-3]
                elif rodic == "st":
                    moznosti.append("sto")
                    hotovo = True

                if dalsi is not None:
                    if dalsi in all_lemmas:
                        moznosti.append(dalsi)
                        hotovo = True
                    else:
                        rodic = dalsi
                
                if not hotovo:
                    mozni_rodice = list(hledani_predku(predci, rodic))
                    if mozni_rodice != []:
                        moznosti_pom = moznosti + mozni_rodice
                        moznosti = moznosti_pom
                        hotovo = True

                    else:
                        bez.append(lexeme.lemma)
            
            if moznosti != []:
                seznam.append((lexeme.lemma, moznosti))
             
                    
vypisovani(seznam, bez)



