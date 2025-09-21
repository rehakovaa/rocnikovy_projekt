""" 
test hledá affixoidy, které mají mezi svými dětmi uvedena slova, která ale tento affixoid neobsahují 

pozn. tento test dávám pouze do skupiny I, protože se mi sice ta slova nezdají, ale očividně se nějak skloňují a já nevím, co je 
úmysl a co už je chyba (třeba krat a andokracie bude nejspíš úmyslný vztah, ale nevím co architektura a takt)
takže tam radši nechám všechny
"""

import derinet.lexicon as dlex
import os

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

def vypis(seznam):
    with open("I_AffixoidyCoSeNenachaziVPrirazenychSlovech.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
        f.write("NALEZENÉ AFFIXOIDY, KTERÉ NEJSOU OBSAŽENY VE SLOVECH, KTERÉ JSOU K NIM PŘIŘAZENY \n")
        f.write("UKÁZKA VÝPISU:\n")
        f.write("affixoid")
        f.write(f"  dite \n")
        f.write("\n")
        for slovo, deti in sorted(seznam, key=lambda x: len(x[1]), reverse=True):
            f.write(f"{slovo} \n")
            for i in deti:
                f.write(f"  {i}\n")
            f.write("\n")

seznam = []
for lexeme in lexicon.iter_lexemes():
    if (lexeme.pos == "Affixoid" or lexeme.pos == "NeoCon"):  #and len(lexeme.lemma) > 4:
        # je to 4, protoze -my- jeste obsahuje ty dve pomlcky
        #kdyz to bude delsi nez dva, zbavim se tech casti slov jako jsou -my- -e-
        slovo = lexeme.lemma[1:-1] #tak bych se mela zbavit tech pomlcek

        deti = []
        for lem in lexeme.children:
            if slovo not in lem.lemma or not lem.lemma.startswith(slovo):
                deti.append(lem.lemma)
        
        if deti != []:
            seznam.append((slovo, deti))

vypis(seznam)