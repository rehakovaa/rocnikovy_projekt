import derinet.lexicon as dlex
import os

"""
hledám podstatná jména, která jsou odvozena od přídavných jmen, ale nejsou na ně napojena 
příklady: balzakovací -> balzakovanost
"""

lexicon = dlex.Lexicon()
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "./derinet-2-3.tsv") 
lexicon.load(file_path)

with open("noun_from_adj.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
    for lexeme in lexicon.iter_lexemes():
        if lexeme.pos == "NOUN":
            if lexeme.lemma.endswith("kost"): #antidemokratická -> antidemokratickost
                slovo = lexeme.lemma[:-4] #chci odstranit posledních pět písmen
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-2] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break
          
            elif lexeme.lemma.endswith("anost"): #zdemokratizovaný - zdemokratizovanost
                slovo = lexeme.lemma[:-5]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-3] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break

            elif lexeme.lemma.endswith("čtěnost"): #poameričtěný -> poameričtěnost 
                slovo = lexeme.lemma[:-7]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-5] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break

            elif lexeme.lemma.endswith("enost"): #ctěnost je od ctěný?? existuje vůbec to slovo
                slovo = lexeme.lemma[:-5]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-3] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break

            elif lexeme.lemma.endswith("itost"): #hruštičkovitý -> hruštičkovitost
                slovo = lexeme.lemma[:-5]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-3] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break

            elif lexeme.lemma.endswith("vost"): #babravý -> babravost
                slovo = lexeme.lemma[:-4]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-2] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break


            elif lexeme.lemma.endswith("alismus"): #liberální -> liberalismus (nebo je to obráceně?? musím si pořídit slovník)
                slovo = lexeme.lemma[:-7]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-4] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break
            
            
            elif lexeme.lemma.endswith("ost"): #krutý -> krutost
                slovo = lexeme.lemma[:-3]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-1] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break
            
            elif lexeme.lemma.endswith("ita"): #efektivní -> efektivita
                slovo = lexeme.lemma[:-3]
                for lem in lexicon.iter_lexemes():
                    if lem.pos == "ADJ" and lem.lemma[:-2] == slovo and lem not in lexeme.all_parents and lexeme not in lem.all_parents:
                        f.write(f"{lem.lemma} -> {lexeme.lemma}\n")
                        break
            
            
print("done")
            
