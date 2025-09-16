""" 
hledají se slova, která se nachází v jiném slově jako podstring, ale nejsou k sobě připojeni (ani vzdáleně, tedy že nejsou přes několik hran k sobě připojeni)
často zde bude například slovo 'super', které se nachází ve spoustě slov, ale není k nim nijak připojeno 

upozornění: test běží dlouho
"""

import derinet.lexicon as dlex
import os

def tisk(seznam):
    with open("E_NepripojenyPodstringKDiteti.txt", "w", encoding="utf-8") as f:
        f.write("SLOVA, KTERÁ JSOU PODMNOŽINOU JINÝCH SLOV, ALE NEJSOU K SOBĚ NIJAK NAVÁZANÁ \n")
        f.write("UKÁZKA TISKU:\n")
        f.write("předek \n")
        f.write(f"  slovo, které obsahuje předka \n")
        f.write("\n")

        for slovo, deti in seznam:
            f.write(f"{slovo}\n")
            for m in deti:
                f.write(f"  {m}\n")

def lezeme_nahoru(dite, hledany):
    rodice = dite.all_parents
    if not rodice:
        return False  # nedošli jsme k hledanému
    if hledany in rodice:
        return True  # hledaný je přímo rodičem
    for r in rodice:
        if lezeme_nahoru(r, hledany):  # rekurzivně jdeme dál
            return True
    return False  # pokud jsme ho nikdy nenašli


lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)


lemma_to_lex = {lex.lemma: lex for lex in lexicon.iter_lexemes()}
mnozina = []
all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

for lexeme in lexicon.iter_lexemes():
    #if lexeme.lemma == "super":
    if len(lexeme.lemma) > 4:
        slovicka = []
        kandidati = {lemma for lemma in all_lemmas if lexeme.lemma in lemma and len(lexeme.lemma) < len(lemma)}
        #najdu všechny slova, ve kterých je lexeme podstringem
        if len(kandidati) > 0: 
            for lemma in kandidati:
                s= lemma_to_lex[lemma]
                dobry = True
                for par in s.all_parents: #a podívám se, jestli se lexeme nenachází schované nad nějakým rodičem dítětě
                    if par != lexeme: #když to samotné není předek
                        predek = lezeme_nahoru(s, lexeme) #tak se podíváme, jestli to není předek předka
                        if predek: #jestli to je předek předka, tak tam nějaké propojení je
                            dobry = False

                    if dobry:
                        slovicka.append(lemma)
        
        if slovicka:
            mnozina.append((lexeme.lemma, slovicka))


# seřazení podle počtu dětí
mnozina = sorted(mnozina, key=lambda x: len(x[1]), reverse=True)
tisk(mnozina)



    
