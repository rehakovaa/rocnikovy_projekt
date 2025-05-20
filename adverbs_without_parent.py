import derinet.lexicon as dlex
import os

"""
příslovce by mělo být vždy na něco napojeno - hledám taková, která nejsou připojena
"""

lexicon = dlex.Lexicon()
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "./derinet-2-3.tsv") 
lexicon.load(file_path)

with open("affixoidy.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
    for lexeme in lexicon.iter_lexemes():
        if lexeme.pos == "ADV" and lexeme.all_parents is None:
            f.write(f"{lexeme.lemma}\n")
