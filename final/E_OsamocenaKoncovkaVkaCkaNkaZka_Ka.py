import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def nejlepsi(kandidati):
    hodnota = 0
    nejvyssi = None 
    for i in kandidati:
        #ještě bych sem mohla přidat kontrolu, že je to rodu mužského, ale to nevím, jestli by zvládl derinet
        #jestli bych se nepřipravil o to slovo
        if i != None:
            slovo = lexicon.get_lexemes(i)[0]
            if slovo.misc.get('corpus_stats') and slovo.misc['corpus_stats']['relative_frequency'] > hodnota:
                nejvyssi = slovo.lemma
                hodnota = slovo.misc['corpus_stats']['relative_frequency']    

    return nejvyssi 

def test(nove):
    kandidati = set()
    for i in "aeioyu":
        if nove + i in all_lemmas:
            slovicko = nove + i
            if slovicko in all_lemmas:
                kandidati.add(slovicko)
    return kandidati

def mozny_predek(predchudce):
    if predchudce in all_lemmas:
        return predchudce
    else:
        if predchudce[-1] not in "aáeěiíoóuůúyý":
            dalsi = test(predchudce)
            if len(dalsi) > 1:
                return nejlepsi(dalsi)
            elif len(dalsi) == 1:
                return dalsi.pop()
            else:
                return None

def vytisknout(seznam, bez):
    with open("E_OsamocenaKoncovkaVkaCkaNkaZka_Ka.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("PODSTATNÁ JMÉNA ŽENSKÉHO RODU KONČÍCÍ NA SPECIÁLNÍ PŘÍPADY 'KA' A JSOU BEZ PŘEDKA \n")
        f.write("SPECIÁLNÍ PŘÍPADY: VKA, ČKA, NKA, ŽKA A TA SLOVA KONČÍCÍ NA KA, U KTERÝCH BYL NALEZEN PŘEDEK \n")
        f.write("pozn. nedokážu totiž efektivně rozlišit slova končící na 'ka', která mají mít předka a která ne")
        f.write("\n")
        f.write("PODSTATNÁ JMÉNA, KE KTERÝM BYL NALEZEN PŘEDEK \n")
        f.write(f"{'PODSTATNÉ JMÉNO'.ljust(20)}{'PŘEDEK'.ljust(20)}\n")
        for i in seznam:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")

        f.write("\n")
        f.write("PODSTATNÁ JMÉNA, PRO NĚŽ NEBYL NALEZEN PŘEDCHŮDCE\n")
        for i in bez:
            f.write(f"{i} \n")



seznam = []
bez = []

def hledani_predka(predek, dite):
    kandidati = {lemma for lemma in all_lemmas if predek in lemma and len(predek) < len(lemma) and lemma != dite and len(dite) > len(lemma)}
    vysledny = nejlepsi(kandidati)
    return vysledny

for lexeme in lexicon.iter_lexemes():
    if lexeme.pos == "NOUN" and lexeme.lemma.endswith("ka"):
        if lexeme.all_parents == []:
            if 'Gender' in lexeme.feats and lexeme.feats['Gender'] == 'Fem':
                predchudce = lexeme.lemma[:-2]
                hotovo = False
                #veci jako profesorka a profesor
                #ale ne veci jako matka a mat
                if predchudce in all_lemmas:
                    slovo = lexicon.get_lexemes(predchudce)[0]
                    casto_pred = slovo.misc['corpus_stats']['absolute_count']
                    casto_po = lexeme.misc['corpus_stats']['absolute_count']

                    if casto_po < casto_pred:
                        hotovo = True
                        seznam.append((lexeme.lemma, slovo.lemma))
                
                if not hotovo:

                    if lexeme.lemma.endswith(("vka", "čka", "nka")):
                        predchudce = lexeme.lemma[:-4]
                        vysledek = mozny_predek(predchudce)
                        if vysledek is not None:
                            seznam.append((lexeme.lemma, predchudce))
                            hotovo = True

                        else:
                            predchudce = lexeme.lemma[:-2]
                            vysledek = mozny_predek(predchudce)
                            if vysledek is not None:
                                seznam.append((lexeme.lemma, slovo.lemma))
                                hotovo = True
                        
                        if not hotovo:
                            predchudce = lexeme.lemma[:-4]
                            cil = hledani_predka(predchudce, lexeme.lemma)
                            if cil is not None:
                                seznam.append((lexeme.lemma, cil))
                                hotovo = True

                        if not hotovo:
                            bez.append(lexeme.lemma)
                    

                    #pedagožka a pedagog
                    elif lexeme.lemma.endswith("žka"):
                        predchudce = predchudce + "g"

                        if predchudce in all_lemmas:
                            seznam.append((lexeme.lemma, predchudce))
                        else:
                            bez.append(lexeme.lemma)
                        
                    else: #teď pořešit skandinavistka a skandinavista
                        vysledek = mozny_predek(predchudce)
                        if vysledek is not None:
                            seznam.append((lexeme.lemma, predchudce))
    
vytisknout(seznam, bez)
