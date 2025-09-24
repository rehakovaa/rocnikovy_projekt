""" 
test hledá lexémy, jejichž rodiče mají podobnou délku, ale liší se v prvním písmenu (ne velikostně, ale v tom, že jsou to dvě rozdílné písmena)
- jsou vynechány případy, kdy jsou si slova dostatečně podobná anebo slovo začíná na 'apgrejd'
"""

import opakovane_funkce
def vypis_dva_seznamy(bez, soubor, popis, varianta):
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*" + popis + "\n")
        f.write("*jedna skupina: seznam hran, které vypadají vachrlatě\n")
        f.write(f"*přebývá hrana\tzkoumané slovo\troidč\n")
        for i in bez:
            f.write(f"{varianta}\t{i[0]}\t{i[1]}\n")  
         
def main(lexicon):
    seznam = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.parent is not None:
            i = lexeme.parent
            if len(lexeme.lemma) < len(i.lemma) + 2 and lexeme.lemma[0] != i.lemma[0]:
                #pojistit rozdily:
                if lexeme.lemma[0].lower() == i.lemma[0].lower(): #čáslavský x Čáslav
                    continue
                elif i.lemma.startswith("-"):
                    continue
                elif len(lexeme.lemma) < 7 and opakovane_funkce.levenhstein(lexeme.lemma, i.lemma) < 2:
                    continue
                elif len(lexeme.lemma) > 6 and opakovane_funkce.levenhstein(lexeme.lemma, i.lemma) < 3:
                    continue
                elif "apgrejd" in lexeme.lemma:
                    if "upgrade" + lexeme.lemma[7:] == i.lemma:
                        continue  
                else:
                    seznam.append((lexeme.lemma, i.lemma, opakovane_funkce.levenhstein(lexeme.lemma, i.lemma)))
                        

    sorted(seznam, key=lambda x: x[2], reverse=True)
    seznam1 = []
    for i in seznam:
        seznam1.append((i[0], i[1]))

    vypis_dva_seznamy(seznam1, "W_PodobneDlouhaSlovaJinePocatecniPismeno.tsv", "slova podobně krátká jako rodič, ale začínají na jiné písmeno", "přebývá hrana")
