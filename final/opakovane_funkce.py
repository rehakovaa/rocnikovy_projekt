def vypis_identicka_slova(veta, soubor, seznam):
        # -------------------- výstup --------------------
    with open(f"{soubor}.sv", "w", encoding="utf-8") as f:
        f.write(f"*{veta}\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        f.write("*\n")

        zmena = "velké"
        for i in sorted(seznam, key=lambda x: x[0]):
            if i[0][0].islower() and zmena == "velké":
                f.write("*\n")
                zmena = "malé"
            elif i[0][0].isupper() and zmena == "malé":
                f.write("*\n")
                zmena = "velké"
            
            f.write(f"{i[0]}\t{i[1]}\n") 

def vypis_tri_seznamy(seznam_dobry, seznam_spatny, bez, soubor, popis):
    with open(soubor, "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*" + popis + "\n")
        f.write("*tři skupiny: nalezený rodič, který je častější než nalezené slovo, nalezený rodič, který je méně častý než nalezené slovo, nenalezen rodič\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        f.write("*\n")
        f.write(f"*častější předek\n")
        for i in seznam_dobry:
            f.write(f"{i[0]}\t{i[1]}\n")  
        f.write("*\n")
        f.write("*méně častý předek\n")
        for i in seznam_spatny:
            f.write(f"{i[0]}\t{i[1]}\n")    
        f.write("*\n")
        f.write("*nenalezen předek\n")
        for i in bez:
            f.write(f"{i}\n")

def vypis_jeden_seznam(seznam, soubor, popis):
    with open(soubor, "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*" + popis + "\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        for i in seznam: 
            f.write(f"{i[0]}\t{i[1]}\n")

def vypis_jeden_seznam_vic_moznosti(seznam, soubor, popis):
    with open(soubor, "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*" + popis + "\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        for slovo, deti in seznam:
            for i in deti: 
                f.write(f"{slovo}\t{i}\n")

def vypis_dva_seznamy(seznam, bez, soubor, popis):
    with open(soubor, "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("*" + popis + "\n")
        f.write("*dvě skupiny: nalezený rodič a nenalezený rodič\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        f.write("*\n")
        f.write(f"*nalezen předek\n")
        for i in seznam:
            f.write(f"{i[0]}\t{i[1]}\n")  
        f.write("*\n")
        f.write("*nenalezen předek\n")
        for i in bez:
            f.write(f"{i}\n")

def vypis_matcin_otcuv(spatny_rod, dobry_rod, spatny_nepripojeno, bez, rod, koncovka, soubor, vzdalene):
    with open(f"{soubor}.txt", "w", encoding="utf-8") as f:
        f.write(f"*přídavná jména končící na '{koncovka}', která nejsou připojena ke slovu {rod} rodu\n")
        f.write(f"*zkoumané slovo\tnalezené slovo'\n")
        f.write("*\n")
        f.write(f"*rodič není {rod} rodu\n")
        for i in spatny_rod:
           f.write(f"{i[0]}\t{i[1]}\n")
        f.write("*\n")
        f.write(f"*rodič a slovo jsou vzdáleně příbuzní\n")
        for i in vzdalene:
           f.write(f"{i[0]}\t{i[1]}\n")
        f.write("*\n")
        f.write(f"*možný předek {rod} rodu\n")
        for i in dobry_rod:
            f.write(f"{i[0]}\t{i[1]}\n")
        f.write(f"*možný předek, který není {rod} rodu\n")
        f.write("*\n")
        for i in spatny_nepripojeno:
            f.write(f"{i[0]}\t{i[1]}\n")
        f.write("*\n")
        f.write("*předek nenalezen\n")
        for i in bez:
            f.write(f"{i}\n")



def kontrola_rodice(rodic, dite, lexicon):
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

def muze_se_pridat(rodic, lexeme, seznam_dobry, seznam_spatny, lexicon):
    if rodic != lexeme.lemma:
        if kontrola_rodice(rodic, lexeme):
            seznam_dobry.append((lexeme.lemma, rodic))
        else: 
            seznam_spatny.append((lexeme.lemma, rodic))

    return seznam_dobry, seznam_spatny 

def seradit_moznosti(moznosti, lexicon):
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
 
def tvorba_moznych_variant(slovicko, all_lemmas, vzorkar, dite, lexicon):
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
    
    return seradit_moznosti(moznosti, lexicon)

def nejlepsi(kandidati, lexicon):
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


def tvorba_novych_variant_kratke(nove, all_lemmas):
    kandidati = set()
    for i in "aeioyu":
        if nove + i in all_lemmas:
            slovicko = nove + i
            if slovicko in all_lemmas:
                kandidati.add(slovicko)
    return kandidati


def vzdalene_pribuzny(dite, rodic):
    daleko = False
    if dite.all_parents != []:
        for i in dite.all_parents:
            if lezeme_nahoru(i, rodic):
                daleko = True
    if daleko:
        return True
    return False

def lezeme_nahoru(dite, hledany): #podívám se, jestli nejsou nějak propojené
    rodice = dite.all_parents
    if not rodice:
        return False  # nedošli jsme k hledanému
    if hledany in rodice:
        return True  # hledaný je přímo rodičem
    for r in rodice:
        if lezeme_nahoru(r, hledany):  # rekurzivně jdeme dál
            return True
    return False  # pokud jsme ho nikdy nenašli
