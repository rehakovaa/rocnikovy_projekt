""" 
test hledá slova, která končí na 'owský' nebo 'owská', co jsou bez rodiče a hledá k nim možné rodiče
"""
import opakovane_funkce
def vypis(seznam_dva,seznam, bez):
    soubor = "E_OsamocenaSlovaKonciciNaOwskyNeboOwska.tsv"
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*osamocená slova končící na 'owský' nebo 'owská'\n")
        f.write("*nalezeni dva možní rodiče, jeden možný anebo žádný\n")
        f.write("*\n")
        f.write("*dva rodiče\n")
        f.write(f"*chybí hrana\tzkoumané slovo\tnalezené slovo'\n")
        f.write("\n")
        for slovo, rodice in sorted(seznam_dva, key=lambda x: x[0]):
            f.write(f"chybí hrana\t{slovo}\t{rodice[0]}\n")
            f.write(f"chybí hrana\t{slovo}\t{rodice[1]}\n")
        f.write("*\n")
        f.write("*jeden možný rodič\n")
        for slovo, rodic in sorted(seznam, key=lambda x: x[0]):
            f.write(f"chybí hrana\t{slovo}\t{rodic}\n")
        f.write("*\n")
        f.write("*rodič nenalezen\n")
        for i in sorted(bez):
            f.write(f"chybí hrana\t{i}\n")

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    
    seznam = []
    seznam_dva = []
    sami = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith(("owský", "owská")) and lexeme.all_parents == []:
            nove = lexeme.lemma[:-4] + "v" + lexeme.lemma[-3:] #najdu nový tvar
            rodice = []
            #najdu všechna w, co byly v tom slově
            if "w" in nove:
                index = nove.index("w")
                lepsi = nove[:index] + "v" + nove[index + 1:]
                #buď ten předek začíná malým nebo velkým písmenem
                if lepsi in all_lemmas:
                    rodice.append(lepsi)
                elif lepsi.lower() in all_lemmas:
                    rodice.append(lepsi.lower())

            #tady to samé, jen nechávám ostatní w na pokoji
            if nove in all_lemmas:
                    rodice.append(nove)
            elif nove.lower() in all_lemmas: 
                rodice.append(nove.lower())
            
            if len(rodice) == 2:
                seznam_dva.append((lexeme.lemma, rodice))
            elif len(rodice) == 1:
                seznam.append((lexeme.lemma, rodice[0]))
            else:
                sami.append(lexeme.lemma)

    vypis(seznam_dva, seznam, sami)
            
