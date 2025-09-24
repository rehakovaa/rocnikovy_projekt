""" 
test se zaměřuje na lexémy, kde lemma je naprosto identická, liší se pouze velikostí prvního písmena. tyto lexémy také nesmí mít žádného rodiče a navzájem k sobě nejsou připojena
ve výstupu se dělí podle toho, jestli mají stejný slovní druh anebo se v něm liší
pro přehlednost se každá z těchto dvou kategorií vytiskne do vlastního souboru
"""
import opakovane_funkce

def main(lexicon):
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
        
        
    opakovane_funkce.vypis_identicka_slova("identická slova s rozdílnou velikostí prvního písmene a stejným slovním druhem","I_DveStejnaSlovaCaseInsensitiveA", stejny_typ, "chybí hrana")
    opakovane_funkce.vypis_identicka_slova("identická slova s rozdílnou velikostí prvního písmene a různým slovním druhem","I_DveStejnaSlovaCaseInsensitiveB", ruzny_typ, "chybí hrana")
