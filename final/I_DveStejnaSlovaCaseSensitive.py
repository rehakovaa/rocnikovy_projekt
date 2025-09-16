""" 
test hledá lexémy, které jsou identické, ale ani jeden z nich nemá rodiče
identické ve smyslu, že první písmeno je stejně velké 
výtisk se dělí podle toho, jestli lexémy sdílí stejný slovní druh a každá kategorie má vlastní soubor
"""


import derinet.lexicon as dlex
import os
lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

#testování 1
def tisknuti(veta, soubor, seznam):

    # -------------------- výstup --------------------
    with open(f"{soubor}.txt", "w", encoding="utf-8") as f:
        f.write(f"{veta}\n")
        f.write(f"{'SLOVO 1'.ljust(20)}{'SLOVO 2'.ljust(20)}{'SLOVNÍ DRUH'.ljust(10)}\n")
        f.write("\n")

        zmena = "velké"
        for i in sorted(seznam, key=lambda x: x[0]):
            if i[0][0].islower() and zmena == "velké":
                f.write("\n")
                zmena = "malé"
            elif i[0][0].isupper() and zmena == "malé":
                f.write("\n")
                zmena = "velké"
            
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}{i[2].ljust(10)}\n")


videno = set()
stejny_typ, ruzny_typ = set(), set()

for lexeme in lexicon.iter_lexemes():
    if lexeme not in videno: #pokud už jsem to slovo testoval, tak ho přeskočím
        dalsi = lexicon.get_lexemes(lemma=lexeme.lemma)
        if len(dalsi) > 1:
            dalsi.remove(lexeme) #takhle předejdu tomu, abych zpracoval stejné slovo dvakrát 
            videno.add(lexeme)
            for lex in dalsi:
                if lexeme.all_parents == [] and lex.all_parents == []:
                    if lexeme.pos != lex.pos: #pokud mají různé typy
                        ruzny_typ.add((lexeme.lemma, lex.lemma, lex.pos))
                        #f.write(f"{lexeme.lemma}, {lex.lemma} -  RŮZNÉ typy: {lexeme.pos}, {lex.pos} \n") #nejdříve původní, potom nalezlý
                    else:
                        stejny_typ.add((lexeme.lemma, lex.lemma, lexeme.pos, lex.pos))
                        #f.write(f"{lexeme.lemma}, {lex.lemma} - STEJNÝ typ: {lex.pos} \n")

tisknuti("TEST: IDENTICKÁ SLOVA, KTERÁ K SOBĚ NAVZÁJEM NEJSOU NIJAK PŘIPOJENA A MAJÍ STEJNÝ SLOVNÍ DRUH","I_DveStejnaSlovaCaseSensitiveA", stejny_typ)
tisknuti("TEST: IDENTICKÁ SLOVA, KTERÁ K SOBĚ NEJSOU PŘIPOJENA A NESDÍLÍ STEJNÝ SLOVNÍ DRUH","I_DveStejnaSlovaCaseSensitiveB", ruzny_typ)


