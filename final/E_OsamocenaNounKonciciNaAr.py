import derinet.lexicon as dlex
import os
lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def vypis(seznam_dobry, seznam_spatny, bez):
    with open("E_OsamocenaNounKonciciNaAr.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("TEST HLEDÁ SLOVA KONČÍCÍ NA 'AŘ', KTERÁ BY MĚLA BÝT NAD SEBOU RODIČE, ALE NEMAJÍ \n")
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


def kontrola_rodice(rodic, dite):
    celkovy_rodic = lexicon.get_lexemes(rodic)[0]
    if 'corpus_stats' in celkovy_rodic.misc.keys():
        if 'absolute_count' in celkovy_rodic.misc['corpus_stats'].keys() and 'absolute_count' in dite.misc['corpus_stats'].keys():
            pozornost_rodic = celkovy_rodic.misc['corpus_stats']['absolute_count']
            pozornost_dite = dite.misc['corpus_stats']['absolute_count']

            if pozornost_rodic > pozornost_dite:
                return True
    
    return False

def je_spravne_bez_rodice(bez):
    spravne = []

    for i in bez:
        if 'unmotivated' in i.misc.keys() and i.misc['unmotivated']:
            continue
        else:
            spravne.append(i.lemma)

    return spravne

def muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny):
    if rodic != lexeme.lemma:
        if kontrola_rodice(rodic, lexeme):
            seznam_dobry.append((lexeme.lemma, rodic))

        else: 
            seznam_spatny.append((lexeme.lemma, rodic))

    return seznam_dobry, seznam_spatny 

def seradit_moznosti(moznosti):
    if len(moznosti) > 1:
        cetnosti = []
        for i in moznosti: 
            cele_slovo = lexicon.get_lexemes(i)[0]
            if 'corpus_stats' in cele_slovo.misc.keys():
                if 'absolute_count' in cele_slovo.misc['corpus_stats'].keys():
                    pozornost = cele_slovo.misc['corpus_stats']['absolute_count']
                    cetnosti.append(pozornost)
                else:
                    cetnosti.append(0)

        for i in range(len(moznosti)):
            for j in range(len(moznosti) - 1):
                if cetnosti[j] < cetnosti[j + 1]:
                    # swap
                    moznosti[j], moznosti[j + 1] = moznosti[j + 1], moznosti[j]
                    cetnosti[j], cetnosti[j + 1] = cetnosti[j + 1], cetnosti[j]

    return moznosti
 
def tvorba_moznych_variant(slovicko, all_lemmas, vzorkar, dite):
    moznosti = []
    if vzorkar:
        for i in "aeiouyáéíóúůý":
            slovo = slovicko + i + "k"

            if slovo in all_lemmas and slovo != dite:
                moznosti.append(slovo)
    else: 
        for i in "aeiouyáéíóúůý":
            slovo = slovicko + i 

            if slovo in all_lemmas and slovo != dite:
                moznosti.append(slovo)
    
    return seradit_moznosti(moznosti)

seznam_dobry = []
seznam_spatny = []
bez = []

for lexeme in lexicon.iter_lexemes():
    if lexeme.lemma.endswith("ař") and lexeme.pos == "NOUN" and lexeme.all_parents == []:

        #běžka -> běžkař
        if lexeme.lemma[:-1] in all_lemmas: 
            rodic = lexeme.lemma[:-1]
            seznam_dobry, seznam_spatny = muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)

        #Hrobař -> hrob
        elif lexeme.lemma[0].isupper() and lexeme.lemma[:-1].lower() in all_lemmas:
            rodic = lexeme.lemma[:-1].lower()
            seznam_dobry, seznam_spatny = muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)

        #vrchař -> vrch
        elif lexeme.lemma[:-2] in all_lemmas:
            rodic = lexeme.lemma[:-2]
            seznam_dobry, seznam_spatny = muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)
        elif lexeme.lemma[:-2].lower() in all_lemmas: 
            rodic = lexeme.lemma[:-2].lower()
            seznam_dobry, seznam_spatny = muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny)
        
        else: 
            hotovo = False 
            #vzorkař -> vzorek
            if not (lexeme.lemma[-3] in "aeiouyáéíóúůý") and not (lexeme.lemma[-4] in "aeiouyáéíóúůý"):
                rodic = lexeme.lemma[:-3]
                moznosti = tvorba_moznych_variant(rodic, all_lemmas, True, lexeme.lemma)
                if moznosti != []:
                    seznam_dobry, seznam_spatny = muze_se_pridat(moznosti[0], lexeme, seznam_dobry, seznam_spatny)
                    hotovo = True

            #zmijař -> zmije
            if lexeme.lemma[0].islower() and not hotovo:
                rodic = lexeme.lemma[:-2]
                moznosti = tvorba_moznych_variant(rodic, all_lemmas, False, lexeme.lemma)
                if moznosti != []:
                    seznam_dobry, seznam_spatny = muze_se_pridat(moznosti[0], lexeme, seznam_dobry, seznam_spatny)
                else: 
                    bez.append(lexeme)
            #Zmijař -> zmije
            elif lexeme.lemma[0].isupper() and not hotovo: 
                rodic = lexeme.lemma[:-2].lower()
                moznosti = tvorba_moznych_variant(rodic, all_lemmas, False, lexeme.lemma)
                if moznosti != []:
                    seznam_dobry, seznam_spatny = muze_se_pridat(moznosti[0], lexeme, seznam_dobry, seznam_spatny)
                else: 
                    bez.append(lexeme)

bez = je_spravne_bez_rodice(bez)
vypis(seznam_dobry, seznam_spatny, bez)
            
    #tady to vezmu podle toho, co mi vyběhlo