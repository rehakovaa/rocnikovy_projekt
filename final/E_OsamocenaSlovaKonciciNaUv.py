import derinet.lexicon as dlex
import os


def tisk_koncovky(spatny_rod, dobry_rod, spatny_nepripojeno, bez, rod, koncovka, soubor):
    with open(f"{soubor}.txt", "w", encoding="utf-8") as f:
        f.write(f"PŘÍDAVNÁ JMÉNA KONČÍCÍ NA -{koncovka}, KTERÁ NEJSOU PŘIPOJENA KE SLOVU {rod} RODU \n")
        f.write(f"{'PŘÍDAVNÉ JMÉNO'.ljust(20)}{'PODSTATNÉ JMÉNO'.ljust(20)}\n")
        f.write("\n")
        f.write(f"JE PŘIPOJENO KE SLOVU, KTERÉ NENÍ {rod} RODU\n")
        for i in spatny_rod:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("\n")
        f.write(f"NENÍ PŘIPOJENO K PŘEDKOVI, KTERÝ JE {rod} RODU \n")
        for i in dobry_rod:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write(f"EXISTUJE NEPŘIPOJENÝ PŘEDEK, KTERÝ NENÍ {rod} RODU\n")
        for i in spatny_nepripojeno:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")
        f.write("NEBYL NALEZEN PŘEDEK \n")
        for i in bez:
            f.write(f"{i} \n")

def tvorba_predka(slovo):
    temp = slovo[:-2]
    nove = temp[0:-1]
    nove2 = temp[-1]
    slovicko = nove + "e" + nove2
    return slovicko
    
def hledani_predka(lexeme):
    rodice = lexeme.all_parents
    pomocnik = tvorba_predka(lexeme.lemma)
    jeden = False # jestli jsme našli nějakou předkyni
    jiny = False # pokud jsme ale nasli predka, co neni muzsky, ale sedí do popisu
    slovo = None
    for r in rodice:
        re = r.lemma
        if r.lemma[-1] in "aeiouyáéíóúůý" and r.lemma[-2] not in "aeiouyáéíóúůý":
            re = r.lemma[:-1]
        if re.endswith("os"):
            re = r.lemma[:-2]
        if r and (re == pomocnik or re == lexeme.lemma[:-2]):
            jiny = True 
            if r.pos == "NOUN" and "Gender" in r.feats.keys() and r.feats["Gender"] == "Masc":
                jeden = True
                break
            else: 
                slovo = r.lemma

    return jeden, jiny, slovo


lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)



all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
spatny_rod, dobry_rod, spatny_nepripojeno, bez = [], [], [], []#špatný rod - předek není ženský 
#dobrý rod - není připojen, ale je ženský, spatny_nepripojeno - nepřipojený předek a ještě není ženský
# bez - bez predka

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("ův") and lexeme.pos == "ADJ": #and not test_samohlasek(lexeme.lemma[:-3]):
        #tady je to dobře, protože to má být hned nad dítětem
        #teď mám posichrováno, pokud je to tvaru 'aristokrat > aristokratův'
        jeden, jiny, slovo = hledani_predka(lexeme)
    
        if not jeden and jiny:
            spatny_rod.append((lexeme.lemma, slovo))
        elif not jeden and not jiny:

            pomocnik = tvorba_predka(lexeme.lemma)
            lex = None
            if pomocnik in all_lemmas:
                lex = lexicon.get_lexemes(pomocnik)[0]
            elif lexeme.lemma[:-2] in all_lemmas:
                lex = lexicon.get_lexemes(lexeme.lemma[:-2])[0]

            if lex is not None:
                if 'Gender' in lex.feats.keys() and lex.feats["Gender"] == "Masc":
                    dobry_rod.append((lexeme.lemma, lex.lemma))
                else:
                    spatny_nepripojeno.append((lexeme.lemma, lex.lemma))
            else:
                bez.append(lexeme.lemma)

print(len(dobry_rod) + len(spatny_nepripojeno), len(bez))    
tisk_koncovky(spatny_rod, dobry_rod, spatny_nepripojeno, bez, "MUŽSKÉHO", "ŮV", "E_OsamocenaSlovaKonciciNaUv")