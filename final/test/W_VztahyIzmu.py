""" 
test se zabývá slovy, které končí na 'izmus' a zkoumá u nich několik vlatností 
- zda je slovo bez rodiče, a pokud ano, tak zda pro něj existuje verze, kdy slovo končí na 'ismus' 
- a zda slovo nemá potomka končící na 'ista', a pokud ano, tak zda neexistuje verze 'ismus', pod který by mělo být to dítě připojeno
"""
import opakovane_funkce

def tisk(jenom_jeden):
    soubor = "W_VztahyIsticky.tsv"
    
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre¨
        f.write("*slova končící na 'istický', která jsou pod 'izmus', ale ne pod 'ismus'\n")
        f.write(f"*přebývá hrana\tistický\tizmus\n")
        f.write("*\n")
        for i in jenom_jeden: 
            f.write(f"přebývá hrana\t{i[1]}\t{i[0]}\n")
        f.write(f"*chybí hrana\tistický\tismus\n")
        f.write("*\n")
        for i in jenom_jeden: 
            f.write(f"chybí hrana\t{i[1]}\t{i[2]}\n")

def main(lexicon):   
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
                        if rodic not in jmena:
                            nespojeno.append((lexeme.lemma, d.lemma, rodic))
                    
    tisk(nespojeno)
    opakovane_funkce.vypis_jeden_seznam(seznam, "E_VztahyIzmu.tsv", "slova končící na 'izmus' bez rodiče", "chybí hrana")

