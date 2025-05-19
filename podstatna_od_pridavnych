#TESTUJU PŘÍDAVNÁ JMÉNA, CO BY MĚLA BYT K NĚČEMU PŘIPOJENA A NEJSOU

import derinet.lexicon as dlex
import os

    
def kontrola_slova(lexicon, slovo, koreny):
    for lex in lexicon.iter_lexemes():
        if lex.lemma in koreny or (lex.lemma[:-1] in slovo and lex.lemma != slovo): #vezmu v potaz, ze tam to slovo nemusi byt cele
            # ted nevim, jestli by nestacilo alespon jedno 
            print(f"{slovo} → vypadá příbuzně k: {lex.lemma}")

            
def testovani():
    lexicon = dlex.Lexicon()
    current_dir = os.getcwd()  # aktualni adresar
    file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
    lexicon.load(file_path)
    """
    testuju pridavna jmena, ktera by by mela byt navazana na nejakeho rodice, ale nejsou
    """
    for lexeme in lexicon.iter_lexemes():

        if lexeme.pos == "ADJ" and lexeme.parent is None:
            slovo = lexeme.lemma
            hranice = lexeme._segmentation.get('boundaries')
            koren = lexeme._segmentation.get('morphs')
            koreny = [] #najdu si vsechny casti slova, co jsou oznacene jako koren
            for clanek in koren: 
                if clanek['Type'] == 'R':
                    koreny.append(clanek.get('Morph'))

            #nejdriv porovnavam koncovky -> pridavna jmena, ktera maji koncovku znacici, ze se od nekoho vytvorily
            #tahle sekce kontroluje, zda neni od podstatneho jmena
            if slovo.startswith(('nej', 'pra', 'roz', 'pře')) and hranice[2] and hranice[3]: #nejvetsi, prastary, rozmilý
               print(f"{slovo} → má předponu 'nej/pra/roz/pře' a není připojeno")
            elif slovo.endswith(('ští', 'ský', 'ská', 'ecký', 'ecká')):
                print(f"{slovo} → končí na 'ští/ský/ská/ecký/ecká'")
            elif slovo.endswith(('ový', 'ová', 'oví')) and hranice[-3]:
                print(f"{slovo} → končí na 'ový/ová/oví'")
            elif slovo.endswith(('ičký', 'inký', 'ičká', 'inká')) and hranice[-4]: #staricky, hebounký
                 print(f"{slovo} → zdrobnělina s koncovkou 'ičký/inký/ičká/inká'")
            elif slovo.endswith(('oučký','ounký','oučká', 'ounká')) and hranice[-5]: #lehoucky, lehounky
                print(f"{slovo} → silnější zdrobnělina 'oučký/ounký/...'")
            elif slovo.endswith(('ný', 'ní', 'čí', 'ší')) and hranice[-2]: #beraní, slepičí, jarní, kamenný
               print(f"{slovo} → běžná koncovka 'ný/ní/čí/ší'")
            elif slovo.endswith(('ější', 'ejší')) and hranice[-4]:
                print(f"{slovo} → 2. stupeň přídavného jména 'ejší/ější'")


            #ted se dostaneme k přídavným jménům od sloves
            elif slovo.endswith(('íc', 'oucí')):
                print(slovo)
            elif slovo.endswith(('avý', 'ivý', 'čný')):
                print(slovo)


            #kdyz to slovo ma vic nez jeden koren    
            elif len(koreny) >= 2:
                 print(f"{slovo} → má více než jeden kořen: {koreny}")
            
            elif len(slovo) > 6:
                 print(f"{slovo} → dlouhé slovo bez rodiče (len > 6)")
            
            else: #kdyz uz tam neni zadne spojeni, tak jenom zkontroluju, ze tam neni zadne slovo, ktere nemuze byt jemu pribuzne
                kontrola_slova(lexicon, slovo, koreny)

    

            
