""" 
test se zabývá slovy, které končí na 'izmus' a zkoumá u nich několik vlatností 
- zda je slovo bez rodiče, a pokud ano, tak zda pro něj existuje verze, kdy slovo končí na 'ismus' 
- a zda slovo nemá potomka končící na 'ista', a pokud ano, tak zda neexistuje verze 'ismus', pod který by mělo být to dítě připojeno
"""

import derinet.lexicon as dlex
import os


lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)
def tisk(ismy, jenom_jeden):
    with open("W_VztahyIzmu.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre¨
        f.write("TEST ZABÝVAJÍCÍ SE VZTAHY MEZI -IZMUS, -ISMUS A -ISTICKÝ\n")
        f.write("SEZNAM SLOV, KTERÉ KONČÍ NA 'IZMUS', ALE NEJSOU PŘIPOJENA K VERZI 'ISMUS'\n")
        f.write(f"{'-IZMUS'.ljust(30)}{'-ISMUS'.ljust(30)}\n")
        f.write("\n")
        for i in ismy: 
            f.write(f"{i[0].ljust(30)}{i[1].ljust(30)}\n")
        f.write("\n")

        f.write("SEZNAM SLOV KONČÍCÍ NA 'ISTICKÝ', KTERÁ JSOU PŘIPOJENA NA 'IZMUS', ALE NE 'ISMUS\n")
        f.write(f"{'-ISTICKÝ'.ljust(30)}{'ŠPATNĚ: -IZMUS'.ljust(30)}{'SPRÁVNĚ: -ISMUS'.ljust(30)}\n")
        f.write("\n")
        for i in jenom_jeden: 
            f.write(f"{i[1].ljust(30)}{i[0].ljust(30)}{i[2].ljust(30)}\n")
        f.write("\n")

    
seznam = [] #když masochizmus není příbuzný masochismu
nespojeno = [] #nespojeno - nacionalista je pouze pod nacionalizmem a ne pod nacionalismem
#spojeno_blbe - pripojen k obema (nacionalista jak pod nacionalizmus tak nacionalismus)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("izmus"): #podívám se, jestli má předka to slovo se 's'
        rodic = lexeme.lemma[:-4] + "s" + lexeme.lemma[-3:]
        if lexeme.all_parents == []:
            if rodic in all_lemmas:
                seznam.append((lexeme.lemma, rodic))
                #f.write(f"????{lexeme.lemma} a {rodic} by měly být příbuzní \n")
        
        #pak se podívám do všech dětí, jestli tam nemá 'ista', i když by tam být neměl, protože to je od jiného slova
        deti = lexeme.children 
        for d in deti:
            if d.lemma.endswith("ista"):
                if rodic in all_lemmas: 
                    #podívám se na všechny předky toho dítěte od izmu
                    predci = d.all_parents
                    jmena = []
                    for i in predci: 
                        jmena.append(i.lemma)
                    
                    #pokud tam není -ismus, tak je to špatně
                    if rodic not in jmena: #pokud má to dítě dva rodiče - masochista má jak masochizmus a masochismus
                        nespojeno.append((lexeme.lemma, d.lemma, rodic))
                
tisk(seznam, nespojeno)



