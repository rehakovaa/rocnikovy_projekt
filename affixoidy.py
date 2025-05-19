import derinet.lexicon as dlex
import os

"""
slova typu jako aero nebo agro maji spoustu moznych potomku v derinetu - jako aerostroj nebo agrostav
ty ale nejsou navzajem propojena jako treba vinoteka na theka 

hledám slova, která by měla být napojena na nějaký affixoid, ale nejsou
"""

lexicon = dlex.Lexicon()
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "./derinet-2-3.tsv") 
lexicon.load(file_path)

with open("affixoidy.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
    for lexeme in lexicon.iter_lexemes():
        if (lexeme.pos == "Affixoid" or lexeme.pos == "NeoCon") and len(lexeme.lemma) > 4:
            # je to 4, protoze -my- jeste obsahuje ty dve pomlcky
            #kdyz to bude delsi nez dva, zbavim se tech casti slov jako jsou -my- -e-
            #na tyhle slova se podivam pote vic zblizka (na ty kratsi) 

            slovo = lexeme.lemma[1:-1] #tak bych se mela zbavit tech pomlcek
            seznam = []

            for lex in lexicon.iter_lexemes():
                #chci zkontrolovat pro ten affixoid vsechna mozna slova, zda neni jejich soucasti a pokud jo, tak zda je jeho rodic
                #potrebuju ale jeste vyresit to, ze by se mi mohlo stat stejne, ze to propojeni je jenom nahoda
                    #i kdyz jsem si myslela, ze se to tak casto dit nebude, deje se to -> treba aden, co mi tam spolklo snad vsechna mesta
                if slovo in lex.lemma and lex not in lexeme.children and lex.lemma != lexeme.lemma:
                    seznam.append(lex.lemma)

            #a ted to vytisknout 
            """print(slovo)
            for i in seznam:
                print("-", i)"""
            
            #ted chci zapisovat do souboru
            f.write(f"{slovo}\n")
            for i in seznam:
                f.write(f"- {i}\n")
                f.write("\n")

print("hotovo")
