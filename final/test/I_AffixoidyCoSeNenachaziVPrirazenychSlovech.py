""" 
test hledá affixoidy, které mají mezi svými dětmi uvedena slova, která ale tento affixoid neobsahují 

pozn. tento test dávám pouze do skupiny I, protože se mi sice ta slova nezdají, ale očividně se nějak skloňují a já nevím, co je 
úmysl a co už je chyba (třeba krat a andokracie bude nejspíš úmyslný vztah, ale nevím co architektura a takt)
takže tam radši nechám všechny
"""

import opakovane_funkce
def main(lexicon):
    seznam = []
    for lexeme in lexicon.iter_lexemes():
        if (lexeme.pos == "Affixoid" or lexeme.pos == "NeoCon"): #and lexeme.lemma == "-lith-":  #and len(lexeme.lemma) > 4:
            # je to 4, protoze -my- jeste obsahuje ty dve pomlcky
            #kdyz to bude delsi nez dva, zbavim se tech casti slov jako jsou -my- -e-
            slovo = lexeme.lemma[1:-1] #tak bych se mela zbavit tech pomlcek

            deti = []
            nove = None
            if "h" in slovo: 
                index = slovo.index("h")
                nove = slovo[:index] + slovo[index + 1:]
                
            for lem in lexeme.children:
                if slovo not in lem.lemma: #or not lem.lemma.startswith(slovo):
                    if nove is not None: 
                        if nove not in lem.lemma:
                            deti.append(lem.lemma)
                    else:
                        deti.append(lem.lemma)
            
            if deti != []:
                seznam.append((slovo, deti))

    opakovane_funkce.vypis_jeden_seznam_vic_moznosti(seznam, "I_AffixoidyCoSeNenachaziVPrirazenychSlovech.tsv", "affixoidy, které se nenachází ve svých dětech", "přebývá hrana")
