""" 
test hledá lexémy, jejichž rodiče mají podobnou délku, ale liší se v prvním písmenu (ne velikostně, ale v tom, že jsou to dvě rozdílné písmena)
- jsou vynechány případy, kdy jsou si slova dostatečně podobná anebo slovo začíná na 'apgrejd'
"""
import derinet.lexicon as dlex
import os
import opakovane_funkce

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

def alternativy(otec, syn):
    if syn == "ú" + otec[2:] or syn == "o" + otec[2:]:
        return True
    else:
        return None
                
seznam = []
mozne = []

for lexeme in lexicon.iter_lexemes():
    for i in lexeme.all_parents:
        if len(lexeme.lemma) < len(i.lemma) + 2 and lexeme.lemma[0] != i.lemma[0]:
            #pojistit rozdily:
            if lexeme.lemma[0].lower() == i.lemma[0].lower(): #čáslavský x Čáslav
                continue
            elif i.lemma.startswith("-"):
                continue
            elif len(lexeme.lemma) < 7 and opakovane_funkce.levenhstein(lexeme.lemma, i.lemma) < 2:
                continue
            elif len(lexeme.lemma) > 6 and opakovane_funkce.levenhstein(lexeme.lemma, i.lemma) < 3:
                continue
            elif "apgrejd" in lexeme.lemma:
                if "upgrade" + lexeme.lemma[7:] == i.lemma:
                    continue  
            else:
                reseni = alternativy(lexeme.lemma, i.lemma)
                if reseni is None:
                    seznam.append((lexeme.lemma, i.lemma, opakovane_funkce.levenhstein(lexeme.lemma, i.lemma)))
                else:
                    mozne.append((lexeme.lemma, i.lemma))

opakovane_funkce.vypis_dva_seznamy(mozne, sorted(seznam, key=lambda x: x[2], reverse=True), "W_PodobneDlouhaSlovaJinePocatecniPismeno.tsv", "slova podobně krátká jako rodič, ale začínají na jiné písmeno")
