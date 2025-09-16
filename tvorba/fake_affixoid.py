import derinet.lexicon as dlex
import os

"""
u nějakých affixoidů a neoconů jsou připojena slova, která by tam podle mě vůbec neměla být 
příklad: -takt- -> architekt nebo -pneu- ->  tachypnoe

moje teorie: ta slova by měla obsahovat ten affixoid v tom daném tvaru
moje teorie je špatná, má to velkou chybovost
"""

lexicon = dlex.Lexicon()
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "./derinet-2-3.tsv") 
lexicon.load(file_path)

with open("fake_affixoid.txt", "w", encoding="utf-8") as f: #kdyz tam dodam with, tak se mi to samo zavre
    for lexeme in lexicon.iter_lexemes():
        if (lexeme.pos == "Affixoid" or lexeme.pos == "NeoCon") and len(lexeme.lemma) > 4:
            # je to 4, protoze -my- jeste obsahuje ty dve pomlcky
            #kdyz to bude delsi nez dva, zbavim se tech casti slov jako jsou -my- -e-
            #na tyhle slova se podivam pote vic zblizka (na ty kratsi) 

            slovo = lexeme.lemma[1:-1] #tak bych se mela zbavit tech pomlcek

            for lem in lexeme.children:
                if slovo not in lem.lemma:
                    f.write(f"{lem.lemma} je pod {slovo}, ale neobsahuje ho\n")
