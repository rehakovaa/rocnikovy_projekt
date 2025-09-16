import derinet.lexicon as dlex
import os

"""
dost se stava, ze tam jsou stejna slova, ale s jinym typem -> Adam (NNI) a Adam (NNM)

taky jede dost dlouho
"""

lexicon = dlex.Lexicon()
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "./derinet-2-3.tsv") 
lexicon.load(file_path)

jiz_videno = set()

with open("stejna_slova.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
    for lexeme in lexicon.iter_lexemes(): 
        if lexeme.lemma not in jiz_videno:
            for lex in lexicon.iter_lexemes():
                #jeste potrebuju poresit to, aby se mi ta slova znovu nekontrolovala -> seznam
                if lexeme.lemma == lex.lemma and lexeme.pos != lex.pos:
                    #jsou to ocividne stejna slova, ale kazdy s jinym typem
                    jiz_videno.add(lexeme.lemma)
                    f.write(f"{lex.lemma} - typy: {lex.pos}, {lexeme.pos} \n")
                    break
