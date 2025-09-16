import derinet.lexicon as dlex
import os
"""
slova, která mají předka anebo jsou delší než nějaký počet, ale nejsou nijak segmentované
tak ty hledám
"""

#nacitani derinetu
lexicon = dlex.Lexicon()
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "./derinet-2-3.tsv") 
lexicon.load(file_path)

with open("without_boundaries.txt", "w", encoding="utf-8") as f:
    for lexeme in lexicon.iter_lexemes():
        if lexeme.parent is not None and len(lexeme.lemma) > 5:
            hranice = lexeme._segmentation['boundaries']
            if not any(hranice.values()):
                f.write(f"{lexeme.lemma} \n")
        
        elif len(lexeme.lemma) >= 10: 
            hranice = lexeme._segmentation['boundaries']
            if not any(hranice.values()):
                f.write(f"{lexeme.lemma} \n")
