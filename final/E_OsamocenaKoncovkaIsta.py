""" 
test hledá slova jako terorista, která jsou osamocena a snaží se k nim najít rodiče
"""


import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
adresar = os.getcwd()  # aktuální adresář
cesta_k_souboru = os.path.join(adresar, "./derinet-2-3.tsv")  #sestavení cesty
lexicon.load(cesta_k_souboru)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

#seřazuju je podle četnosti a chci vzít tu nejlepsi
def nejlepsi(kandidati):
    hodnota = 0
    nejvyssi = None

    if len(kandidati) > 0:
        for i in kandidati:
            if i is not None:
                slovo = lexicon.get_lexemes(i)[0]
                if slovo.misc['corpus_stats']['relative_frequency'] > hodnota and slovo.pos == "NOUN":
                    nejvyssi = slovo.lemma
                    hodnota = slovo.misc['corpus_stats']['relative_frequency']    

    return nejvyssi 

#generuju možná slova podle toho, že na konec přidám samohlásku
def test(nove):
    kandidati = set()
    for i in "aeioyu":
        if nove + i in all_lemmas:
            kandidati.add(nove + i)

    return nejlepsi(kandidati)

#prohazuju dlouhou samohlásku za krátkou a vice versa         
def nova_slova(slovo):
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

seznam = []
bez = []

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
            kand = nova_slova(lexeme.lemma)
            nej = None
            if kand and len(kand) != 1:
                nej = nejlepsi(kand)
            elif len(kand) == 1:
                nej = kand.pop()

            if nej is not None:     
                seznam.append((lexeme.lemma, predek))
            else:
                mozny = test(lexeme.lemma[:-4])
                if mozny is not None:
                    seznam.append((lexeme.lemma, mozny))
                else:
                    bez.append(lexeme.lemma)

opakovane_funkce.vypis_dva_seznamy(seznam, bez,"OsamocenaKoncovkaIsta.txt", "opuštěná nouns končící na 'ista' (populista)")

                
