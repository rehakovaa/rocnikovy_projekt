""" 
test hledá slova jako terorista, která jsou osamocena a snaží se k nim najít rodiče
"""

import opakovane_funkce

#prohazuju dlouhou samohlásku za krátkou a vice versa         
def nova_slova(slovo, all_lemmas):
    novoty = set()
    bez = "aeiouuy"
    s = "áéíóůúý"

    for i, znak in enumerate(slovo): #tohle míří na solista a sólo
        nove = None
        if znak in bez:
            index = bez.index(znak)
            nove = slovo[:i] + s[index] + slovo[i + 1:]
        elif znak in s:
            index = s.index(znak)
            nove = slovo[:i] + bez[index] + slovo[i+ 1:]
        
        if nove and nove in all_lemmas:
            novoty.add(nove)
    return novoty


def main(lexicon):
    seznam = []
    bez = []

    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("ista") and lexeme.all_parents == [] and lexeme.pos == "NOUN" and lexeme.lemma[0].islower():
            predek = lexeme.lemma[:-4]

            #socialista a socialismus
            if predek + "ismus" in all_lemmas:
                predek = predek + "ismus"
                seznam.append((lexeme.lemma, predek))
                
            #religionista a religioinstika
            elif predek + "istika" in all_lemmas:
                predek = predek + "istika"
                seznam.append((lexeme.lemma, predek))

            elif lexeme.lemma[6:] in all_lemmas and lexeme.lemma.startswith(("sociál", "krypto", "kardio")):
                seznam.append((lexeme.lemma, lexeme.lemma[6:]))
            
            elif lexeme.lemma[5:] in all_lemmas and lexeme.lemma.startswith(("cyklo", "staro", "multi", "ultra", "spolu", "skoro", "kyber")):
                seznam.append((lexeme.lemma, lexeme.lemma[5:]))
            
            elif lexeme.lemma[4:] in all_lemmas and lexeme.lemma.startswith(("novo", "post", "robo", "sólo", "arci")):
                seznam.append((lexeme.lemma, lexeme.lemma[4:]))
            
            elif lexeme.lemma[3:] in all_lemmas and lexeme.lemma.startswith(("eko")):
                seznam.append((lexeme.lemma, lexeme.lemma[3:]))

            elif lexeme.lemma[2:] in all_lemmas and lexeme.lemma.startswith(("ex")):
                seznam.append((lexeme.lemma, lexeme.lemma[2:]))
            
            elif predek in all_lemmas: 
                seznam.append((lexeme.lemma, predek))
            
            elif predek + "is" in all_lemmas:
                seznam.append((lexeme.lemma, predek))
            
            else:
                #sólista a solista
                kand = nova_slova(lexeme.lemma, all_lemmas)
                nej = None
                if kand and len(kand) != 1:
                    nej = opakovane_funkce.nejlepsi_noun(kand, lexicon)
                elif len(kand) == 1:
                    nej = kand.pop()

                if nej is not None:     
                    seznam.append((lexeme.lemma, predek))
                else:
                    mozny = opakovane_funkce.tvorba_novych_variant_kratke(lexeme.lemma[:-4], all_lemmas)
                    if len(mozny) != 0:
                        nej = opakovane_funkce.nejlepsi_noun(mozny, lexicon)
                        seznam.append((lexeme.lemma, nej))
                    else:
                        bez.append(lexeme.lemma)

    opakovane_funkce.vypis_dva_seznamy(seznam, bez, "E_OsamocenaNounsKonciciNaIsta.tsv", "podstatná jména končící na 'ista' bez rodiče", "chybí hrana")
                    
