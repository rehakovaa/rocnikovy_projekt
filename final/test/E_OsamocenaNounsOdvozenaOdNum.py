""" 
test hledá podstatná jména odvozená od číslovky, kterým by mohl chybět rodič 
jelikož je tohle test věnující se úzké a dobře popsatelné skupině lexémů, nachází se zde i lexémy, které sice mají rodiče, ale ne všechny 
(třeba stodesítka má nad sebou sto, ale chybí mu mezi rodiči deset)
"""
import opakovane_funkce

prevod = {
    "jednička" : "jedna",
    "dvojka" : "dva", 
    "trojka" : "tři",
    "čtyřka": "čtyři",
    "pětka": "pět",
    "šestka" : "šest",
    "sedmička" : "sedm",
    "osmička" : "osm",
    "devítka" : "devět", 
    "desítka" : "deset"
}

def vypisovani(seznamik):
    soubor = "E_OsamocenaNounsOdvozenaOdNum.tsv"
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f:
        f.write("*osamocená nouns,která by měla být připojena k číslovkám\n")
        f.write(f"*chybí hrana\tzkoumané slovo\tnalezené slovo\n")
        for lemma, rodice in sorted(seznamik):
            for i in rodice:
                f.write(f"chybí hrana\t{lemma}\t{i}\n")

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    seznam = []
    for lexeme in lexicon.iter_lexemes():
        rodinka = []
        if lexeme.lemma in prevod.keys(): #tak je tam prostě to slovo (není to dvacetjednička, ale jenom jednička)
            #tohle je prostě pro věci jako je jednička a jedna
            for k in prevod.keys(): 
                if k == lexeme.lemma: 
                    rodice = []
                    for i in lexeme.all_parents:
                        rodice.append(i.lemma)

                    if prevod[k] not in rodice: 
                        rodinka.append(prevod[k])

        elif lexeme.lemma.endswith("náctka"): 
            #patnáctka a tak
            rodic = lexeme.lemma[:-2]
            if rodic in all_lemmas:  
                cele = lexicon.get_lexemes(rodic)[0]
                if cele not in lexeme.all_parents:
                    rodinka.append(rodic)
        
        elif lexeme.lemma.endswith("ka") and not lexeme.lemma.endswith("strojka"):
            for k in prevod.keys(): 
                if k in lexeme.lemma:
                    cast = lexeme.lemma.removesuffix(k)
                    rodice = []
                    for i in lexeme.all_parents:
                        rodice.append(i.lemma)
                    if prevod[k] not in rodice: 
                        rodinka.append(prevod[k])

                    if cast != "super":
                        if cast in all_lemmas:  
                            cele = lexicon.get_lexemes(cast)[0]
                            if cele not in lexeme.all_parents:
                                rodinka.append(cast)
                                break

        if rodinka:
            seznam.append((lexeme.lemma, rodinka))

    vypisovani(seznam)
