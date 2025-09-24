import opakovane_funkce

""" 
hledají se slova, která jsou příslovci, jejichž rodičem by měla být číslovka, ale v databázi žádného rodiče nemají 
pro zjednodušení vyhledávání se hledají pouze ty příslovce končící na 'é'
"""
prirazeni = {
    "osedm" : "sedm",
    "pátnáct" : "patnáct",
    "šedesátédevát" : "šedesátýdevátý",
    "tisícát": "tisíc",
}

def vypis(existuje):
    soubor = "E_OsamocenaCislovkovaPrislovce.tsv" 
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*osamocená číslovková příslovce\n")
        f.write("*existuje jeden možný rodič\n")
        f.write(f"*chybí hrana\tzkoumané slovo\tnalezené slovo\n")
        for i in sorted(existuje): 
            f.write(f"chybí hrana\t{i[0]}\t{i[1]}\n")

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    existuje_delsi = set()
    for lexeme in lexicon.iter_lexemes():
        if lexeme.pos == "ADV" and lexeme.parent is None and "unmotivated" not in lexeme.misc and lexeme.lemma.endswith("é"):
            #a teď mám několik verzí, co by to mohlo být 
            if lexeme.lemma.startswith("propo"):
                slovo = lexeme.lemma[3:]
            elif lexeme.lemma.startswith(("napo", "po", "za", "na")):
                slovo = lexeme.lemma[2:]
            else:
                slovo = lexeme.lemma

            if slovo[:-1] + "ý" in all_lemmas:
                    existuje_delsi.add((lexeme.lemma, slovo[:-1] + "ý"))
            elif slovo in all_lemmas and slovo != lexeme.lemma:
                existuje_delsi.add((lexeme.lemma, slovo))
            else:
                    if lexeme.lemma.startswith("propo"):
                        slovo = lexeme.lemma[5:]
                    elif lexeme.lemma.startswith("napo"):
                        slovo = lexeme.lemma[4:]
                        
                    kandidat = []
                    volny = []
                    for k in prirazeni.keys():
                        if slovo[:-1] == k:
                            kandidat.append(prirazeni[k])

                    if kandidat != []:
                        existuje_delsi.add((lexeme.lemma, kandidat[0]))

                        
    vypis(existuje_delsi)
