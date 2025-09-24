
import opakovane_funkce

def kandidati_po_odstraneni_a_pridani_samohlasky(lexeme, rodic, all_lemmas, lexicon):
    moznosti = []
    moznosti = opakovane_funkce.tvorba_moznych_variant(rodic, all_lemmas, False, lexeme.lemma, lexicon)
    if moznosti != []:
       return moznosti[0]
    else:
        return None

def kontrola_rodice(rodic, dite, lexicon):
    celkovy_rodic = lexicon.get_lexemes(rodic)[0]
    if 'corpus_stats' in celkovy_rodic.misc.keys() and celkovy_rodic.pos == "NOUN":
        if 'absolute_count' in celkovy_rodic.misc['corpus_stats'].keys() and 'absolute_count' in dite.misc['corpus_stats'].keys():
            pozornost_rodic = celkovy_rodic.misc['corpus_stats']['absolute_count']
            pozornost_dite = dite.misc['corpus_stats']['absolute_count']

            if pozornost_rodic > pozornost_dite:
                return True
    
    return False

def serazeni_podle_levenhsteina(seznam, dite, lexicon):
    nejlepsi = None
    hodnota = 10

    for i in seznam:
        vzdalenost = opakovane_funkce.levenhstein(i, dite)
        if vzdalenost < hodnota:
            cele_slovo = lexicon.get_lexemes(i)[0]
            if cele_slovo.pos == "NOUN":
                nejlepsi = i
                hodnota = vzdalenost
    
    dalsi = None
    hodnota = -1

    for i in seznam:
        cele_slovo = lexicon.get_lexemes(i)[0]
        if cele_slovo.pos == "NOUN":
            if 'corpus_stats' in cele_slovo.misc.keys() and cele_slovo.pos == "NOUN":
                if 'absolute_count' in cele_slovo.misc['corpus_stats'].keys():
                    pozornost = cele_slovo.misc['corpus_stats']['absolute_count']
            
                if pozornost > hodnota:
                    dalsi = i
                    hodnota = pozornost

    if dalsi is not None and dalsi != nejlepsi:
        return [nejlepsi, dalsi]
    else:
        return nejlepsi

def vypis(seznam_dobry, seznam_spatny, seznam_dva, bez):
    soubor = "E_OsamocenyAdjKonciciNaNi.tsv"
    with open(opakovane_funkce.hledani_cesty(soubor), "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*opuštěná přídavná jména končící na 'ní'\n")
        f.write("*čtyři skupiny: častější možný předek než slovo, méně častý předek než slovo, dva možní předci, žádný předek nenalezen \n")
        f.write(f"*chybí hrana\tzkoumané slovo\tnalezené slovo'\n")
        f.write("*\n")
        f.write(f"*častější předek\n")
        for i in seznam_dobry:
            f.write(f"chybí hrana\t{i[0]}\t{i[1]}\n")  
        f.write("*\n")
        f.write("*méně častý předek\n")
        for i in seznam_spatny:
            f.write(f"chybí hrana\t{i[0]}\t{i[1]}\n")    
        f.write("*\n")
        f.write("*dva předci\n")
        for slovo, rodice in seznam_dva:
            f.write(f"chybí hrana\t{slovo}\t{rodice[0]}\n") 
            f.write(f"chybí hrana\t{slovo}\t{rodice[1]}\n") 
        f.write("*\n")
        f.write("*žádný předek\n")
        for i in bez:
            f.write(f"chybí hrana\t{i}\n")

def main(lexicon):
    seznam_dobry = []
    seznam_spatny = []
    seznam_dva = []
    bez = []

    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    for lexeme in lexicon.iter_lexemes():
        if lexeme.pos == "ADJ" and lexeme.lemma.endswith("ní"):
            if 'Loanword' in lexeme.feats.keys() and not lexeme.feats.get('Loanword') and lexeme.all_parents == []: #tedy nejsou odvozena od jiného českého slova
                    
                    if 'unmotivated' in lexeme.misc.keys() and lexeme.misc['unmotivated']:
                        continue
                    else:
                        uvazovane = []

                        if lexeme.lemma[:-2] in all_lemmas:
                            uvazovane.append(lexeme.lemma[:-2])
                            #seznam_dobry, seznam_spatny = muze_se_pridat(lexeme.lemma[:-2], lexeme, seznam_dobry, seznam_spatny)
                        if lexeme.lemma[:-1] in all_lemmas: 
                            uvazovane.append(lexeme.lemma[:-1])
                            #seznam_dobry, seznam_spatny = muze_se_pridat(lexeme.lemma[:-1], lexeme, seznam_dobry, seznam_spatny)
                        if lexeme.lemma[:-4] in all_lemmas: 
                            uvazovane.append(lexeme.lemma[:-4])
                                    #seznam_dobry, seznam_spatny = muze_se_pridat(lexeme.lemma[:-4], lexeme, seznam_dobry, seznam_spatny)
                        rodic = lexeme.lemma[:-2]
                        kand = kandidati_po_odstraneni_a_pridani_samohlasky(lexeme, rodic, all_lemmas, lexicon)
                        if kand != None:
                            uvazovane.append(kand)
                        
                        rodic = lexeme.lemma[:-1]
                        kand = kandidati_po_odstraneni_a_pridani_samohlasky(lexeme, rodic, all_lemmas, lexicon)
                        if kand != None:
                            uvazovane.append(kand)

                        if len(lexeme.lemma) > 5:
                            rodic = lexeme.lemma[:-4]
                            kand = kandidati_po_odstraneni_a_pridani_samohlasky(lexeme, rodic, all_lemmas, lexicon)
                            if kand != None:
                                uvazovane.append(kand)
                        
                        zvoleny = None
                        if len(uvazovane) == 1:
                            cele_slovo = lexicon.get_lexemes(uvazovane[0])[0]
                            if cele_slovo.pos == "NOUN":
                                zvoleny = uvazovane[0]
                        elif uvazovane != []:
                            zvoleny = serazeni_podle_levenhsteina(uvazovane, lexeme.lemma, lexicon)
                        
                        if zvoleny is not None:
                            if isinstance(zvoleny, list):
                                seznam_dva.append((lexeme.lemma, zvoleny))
                            else:
                                castejsi = kontrola_rodice(zvoleny, lexeme, lexicon)
                                if castejsi:
                                    seznam_dobry.append((lexeme.lemma, zvoleny))
                                else:
                                    seznam_spatny.append((lexeme.lemma, zvoleny))
                            
                        else:
                            bez.append(lexeme)

    bez = opakovane_funkce.je_spravne_bez_rodice(bez)
    vypis(seznam_dobry, seznam_spatny, seznam_dva, bez)
                                    
    #potřebuju rozlišit, když to budou slova přejatá z jiného jazyka - lumbální tu nemá co dělat, ale fauní by mělo být u fauna nebo faun (??)
