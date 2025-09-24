import opakovane_funkce

#chci zjistit, jestli jsou ta slova k sobě nějak navázaná, i když ne napřimo
def jsou_pribuzny(bez_h, h, lexicon):
    otec_h = lexicon.get_lexemes(h)[0]
    rodice_h = otec_h.all_parents
    otec_bez = lexicon.get_lexemes(bez_h)[0]
    rodice_bez_h = otec_bez.all_parents

    #jestli je gotaj otcem gothaje
    if any(rodic.lemma == bez_h for rodic in rodice_h):
        return 0
    #jestli je gothaj otcem gotaje
    elif any(rodic.lemma == h for rodic in rodice_bez_h):
        return 1
    else:
        #pokud to není ani jedno, tak se podíváme, jestli nejsou příbuzní oklikou
        #je gotaj nějak dítětem gothaje?
        etiopie = opakovane_funkce.vzdalene_pribuzny(otec_bez, otec_h)
        #je gothaj nějak dítětem gotaje?
        gothaj = opakovane_funkce.vzdalene_pribuzny(otec_h, otec_bez)

        if etiopie or gothaj:
            return 2
        else:
            return 3


def pomery(celkove, h, bez_h, vzdalene, vubec, dohromady, soubor, vypisy):
    seznam = { "h": h/celkove*100, "bez_h" : bez_h/celkove*100, "vubec" : vubec/celkove*100,  "vzdalene" : vzdalene/celkove*100}
    
    #chci nejdriv vypsat všechny četnosti a poté je vypsat jejich pořadí  
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f:
        f.write("*s jakou četností se liší slova s rozdílem jednoho písmena\n")
        f.write("*tabulka četností sestupně \n")
        sortovano = sorted(seznam.items(), key=lambda x: x[1], reverse=True)
        f.write(f"*typ vztahu\tčetnost v procentech\n")
        for k, v in sortovano:
            f.write(f"*{vypisy[k]}\t{str(v)}\n")

        for k, v in sortovano: #kdyz tam dodam with, tak se mi to samo zavre
            f.write("*\n")
            f.write(f"*{vypisy[k]}\n")
            if k == "h" or k == "bez_h":
                f.write(f"*hrana\totec\tsyn\n")
            else:
                f.write(f"*chybí hrana\tslovo\tslovo\n")
            seznamik = dohromady[k]
            if k == "h" or k == "bez_h":
                for i in sorted(seznamik, key=lambda x: x[0]):
                    f.write(f"hrana\t{i[0]}\t{i[1]}\n")
            else:
                for i in sorted(seznamik, key=lambda x: x[0]):
                    f.write(f"chybí hrana\t{i[0]}\t{i[1]}\n")

def analyzuj_vztahy(lexicon, all_lemmas, generator_kandidatu, soubor, vypisy):
    celkove = 0
    h_ne, h_ano, vzdalene, vubec = 0, 0, 0, 0 
    h_ne_seznam, h_ano_seznam, vzdalene_seznam, vubec_seznam = set(), set(), set(), set()

    for lexeme in lexicon.iter_lexemes():
        if not lexeme.lemma.startswith("-"):
            # kandidáti pro porovnání
            novotvary = generator_kandidatu(lexeme.lemma)
            if novotvary != []:
                for k in novotvary:
                    if k in all_lemmas:
                        stav = jsou_pribuzny(k, lexeme.lemma, lexicon)
                        celkove += 1

                        #je to vždycky (rodič, syn)
                        if stav == 0:  #znamená to, že etiopský je rodičem ethiopský
                            h_ano += 1
                            h_ano_seznam.add((lexeme.lemma, k))
                        elif stav == 1:#gothaj je rodičem gotaj
                            h_ne += 1
                            h_ne_seznam.add((k, lexeme.lemma))
                        elif stav == 2:
                            vzdalene += 1
                            vzdalene_seznam.add((lexeme.lemma, k))
                        else:
                            vubec += 1
                            vubec_seznam.add((lexeme.lemma, k))

    dohromady = {"h": h_ano_seznam, "bez_h": h_ne_seznam, "vubec": vubec_seznam, "vzdalene": vzdalene_seznam}
    pomery(celkove, h_ano, h_ne, vzdalene, vubec, dohromady, soubor, vypisy)
