import derinet.lexicon as dlex
import os


prevod = {
    "jednička" : "jedna",
    "dvojka" : "dva", 
    "trojka" : "tři",
    "čtyřka": "čtyři",
    "pětka": "pět",
    "šestka" : "šest",
    "sedmička" : "sedm",
    "osmička" : "osm",
    "devítka" : "devět", 
    "desítka" : "deset"
}

lexicon = dlex.Lexicon()
current_dir = os.getcwd()  # aktualni adresar
file_path = os.path.join(current_dir, "./derinet-2-3.tsv")  #sestaveni cesty
lexicon.load(file_path)

def vypisovani(seznamik):
    with open("E_OsamocenaNounsOdvozenaOdNum.txt", "w", encoding="utf-8") as f:
        f.write("PODSTATNÁ JMÉNA ODVOZENÁ OD ČÍSLOVEK, ALE NEJSOU K NIM PŘIPOJENA \n")
        f.write("PŘÍKLAD TISKU: \n")
        f.write("podstatné jméno \n")
        f.write(f"  číslovka \n")
        f.write("\n")

        for pod, cisla in seznamik:
            f.write(f"{pod}\n")
            for i in cisla:
                f.write(f"  {i}\n")

seznam = []
for lexeme in lexicon.iter_lexemes():
    rodinka = []
    if lexeme.lemma in prevod.keys(): #tak je tam prostě to slovo (není to dvacetjednička, ale jenom jednička)
        #tohle je prostě pro věci jako je jednička a jedna
        for k in prevod.keys(): 
            if k == lexeme.lemma: 
                rodice = []
                for i in lexeme.all_parents:
                    rodice.append(i.lemma)

                if prevod[k] not in rodice: 
                    rodinka.append(prevod[k])

    elif lexeme.lemma.endswith("náctka"): 
        #patnáctka a tak
        rodic = lexeme.lemma[:-2]
        for i in lexicon.iter_lexemes():
            if i.lemma == rodic and i not in lexeme.all_parents:
                rodinka.append(i.lemma)
    
    elif lexeme.lemma.endswith("ka") and not lexeme.lemma.endswith("strojka"):
        for k in prevod.keys(): 
            if k in lexeme.lemma:
                cast = lexeme.lemma.removesuffix(k)
                rodice = []
                for i in lexeme.all_parents:
                    rodice.append(i.lemma)
                if prevod[k] not in rodice: 
                    rodinka.append(prevod[k])

                if cast != "super":
                    for lex in lexicon.iter_lexemes():
                        #chci, aby pro stošestka se mi jako rodič našlo stošest a ne sto a šest
                        #tak ne, je to rozděleně -> sto šest
                        if lex.lemma == cast and cast not in rodice:
                            rodinka.append(cast)
                            break

    if rodinka:
        seznam.append((lexeme.lemma, rodinka))

vypisovani(seznam)
