import derinet.lexicon as dlex
import os
lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def vypis(seznam_dobry, seznam_spatny, bez):
    with open("E_OsamocenaSlovesaKonciciNaRit.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("TEST HLEDÁ SLOVESA KONČÍCÍ NA 'ŘIT', KTERÁ BY MĚLA BÝT NAD SEBOU RODIČE, ALE NEMAJÍ \n")
        f.write("TŘI SKUPINY: NALEZEN RODIČ, KTERÝ JE ČASTĚJŠÍ NEŽ SLOVO, NALEZEN RODIČ, KTERÝ JE MÉNĚ ČASTÝ NEŽ SLOVO, NENAŠEL SE RODIČ \n")
        f.write("UKÁZKA VÝPISU: \n")
        f.write(f"{'NALEZENÉ SLOVO'.ljust(20)}{'MOŽNÝ PŘEDEK'.ljust(20)}\n")
        f.write("\n")
        f.write(f"MOŽNÝ PŘEDEK JE ČASTĚJŠÍ \n")
        for i in seznam_dobry:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")  
        f.write("\n")
        f.write("MOŽNÝ PŘEDEK JE MÉNĚ ČASTÝ \n")
        for i in seznam_spatny:
            f.write(f"{i[0].ljust(20)}{i[1].ljust(20)}\n")  
        f.write("\n")
        f.write("PRO SLOVO NEBYL NALEZEN PŘEDEK \n")
        for i in bez:
            f.write(f"{i} \n")

def je_spravne_bez_rodice(bez):
    spravne = []

    for i in bez:
        if 'unmotivated' in i.misc.keys() and i.misc['unmotivated']:
            continue
        else:
            spravne.append(i.lemma)

    return spravne

def kontrola_rodice(rodic, dite):
    celkovy_rodic = lexicon.get_lexemes(rodic)[0]
    if 'corpus_stats' in celkovy_rodic.misc.keys():
        if 'absolute_count' in celkovy_rodic.misc['corpus_stats'].keys() and 'absolute_count' in dite.misc['corpus_stats'].keys():
            pozornost_rodic = celkovy_rodic.misc['corpus_stats']['absolute_count']
            pozornost_dite = dite.misc['corpus_stats']['absolute_count']

            if pozornost_rodic > pozornost_dite:
                return True
    
    return False

def muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny):
    if kontrola_rodice(rodic, lexeme):
        seznam_dobry.append((lexeme.lemma, rodic))
        #if len(rodic) < len(lexeme.lemma) - 1:
            #f.write(f"{lexeme.lemma} {rodic} \n")
    else: 
        seznam_spatny.append((lexeme.lemma, rodic))

    return seznam_dobry, seznam_spatny 

def koncovky(lexeme, slovo): 
    seznamik_dobry = []
    seznamik_spatny = []
    if slovo[:-2] in all_lemmas: 
        rodic = slovo[:-2]
        seznamik_dobry, seznamik_spatny = muze_se_pridat(rodic, lexeme, [], [])
    elif slovo[:-3] in all_lemmas:
        rodic = slovo[:-3]
        seznamik_dobry, seznamik_spatny = muze_se_pridat(rodic, lexeme, [], [])

    zmena = not seznamik_dobry == [] or not seznamik_spatny == []
    
    return seznamik_dobry, seznamik_spatny, zmena

seznam_dobry, seznam_spatny = [], []
bez = []

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("řit") and lexeme.pos == "VERB" and lexeme.all_parents == []:
        hotovo = False
        pomocnik_dobry = []
        pomocnik_spatny = []
        pomocnik_dobry, pomocnik_spatny, hotovo = koncovky(lexeme, lexeme.lemma)

        if not hotovo:
            if lexeme.lemma[1:] in all_lemmas:
                rodic = lexeme.lemma[1:]
                pomocnik_dobry, pomocnik_spatny = muze_se_pridat(rodic, lexeme, [], [])
                hotovo = True

            elif lexeme.lemma[2:] in all_lemmas:
                rodic = lexeme.lemma[2:]
                pomocnik_dobry, pomocnik_spatny = muze_se_pridat(rodic, lexeme, [], [])
                hotovo = True
            
            if not hotovo:
                slovo = lexeme.lemma[2:]
                pomocnik_dobry, pomocnik_spatny, hotovo = koncovky(lexeme, slovo)

            if not hotovo:
                slovo = lexeme.lemma[1:]
                pomocnik_dobry, pomocnik_spatny, hotovo = koncovky(lexeme, slovo)
            
            if not hotovo:
                if lexeme.lemma[:-4] in all_lemmas:
                    rodic = lexeme.lemma[:-4]
                    pomocnik_dobry, pomocnik_spatny = muze_se_pridat(rodic, lexeme, [], [])
                    hotovo = True

            if not hotovo:
                bez.append(lexeme)

        seznam_dobry.extend(pomocnik_dobry)
        seznam_spatny.extend(pomocnik_spatny)

bez = je_spravne_bez_rodice(bez)
vypis(seznam_dobry, seznam_spatny, bez)
        #bezka -> bezkar -> bezkarit