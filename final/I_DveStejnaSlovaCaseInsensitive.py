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
stejny_typ = set()
ruzny_typ = set()
            #ted 1.2 - různá velikost začínajících písmen
for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma not in videno and not lexeme.lemma.startswith("-"):
        cast = lexeme.lemma[1:]
        pismeno = lexeme.lemma[0].swapcase()
        lexeme1 = pismeno + cast #přetvořím si to slovo tak, aby tady bylo na začátku obrácená velikost písmena
        for lex in lexicon.get_lexemes(lemma=lexeme1): #najdu jestli, tam je nějaké obrácené velikosti
            videno.add(lexeme)
            videno.add(lex)
            #oboje tam přidám
            if lexeme.all_parents == [] and lex.all_parents == []:
                if lexeme.pos != lex.pos: #pokud mají různé typy
                    ruzny_typ.add((lexeme.lemma, lex.lemma, lex.pos))
                    #f.write(f"{lexeme.lemma}, {lex.lemma} -  RŮZNÉ typy: {lexeme.pos}, {lex.pos} \n") #nejdříve původní, potom nalezlý
                else:
                    stejny_typ.add((lexeme.lemma, lex.lemma, lexeme.pos, lex.pos ))
                    #f.write(f"{lexeme.lemma}, {lex.lemma} - STEJNÝ typ: {lex.pos} \n")
    
    
tisknuti("TEST: IDENTICKÁ SLOVA LIŠÍCÍ SE VELIKOSTÍ PRVNÍHO PÍSMENE, KTERÁ K SOBĚ NAVZÁJEM NEJSOU NIJAK PŘIPOJENA A MAJÍ STEJNÝ SLOVNÍ DRUH","I_DveStejnaSlovaCaseInsensitiveA", stejny_typ)
tisknuti("TEST: IDENTICKÁ SLOVA LIŠÍCÍ SE VELIKOSTÍ PRVNÍHO PÍSMENE, KTERÁ K SOBĚ NAVZÁJEM NEJSOU NIJAK PŘIPOJENA A NEMAJÍ STEJNÝ SLOVNÍ DRUH","I_DveStejnaSlovaCaseInsensitiveB", ruzny_typ)