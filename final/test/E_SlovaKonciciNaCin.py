""" 
test se věnuje přídavným jménům přivlastňovacím, které končí na 'čin'
jelikož je to dobře popsatelná skupina, v testu se kontroluje několik možností 
    - slovo má předchůdce, ale to podstatné jméno není rodu ženského
    - slovo nemá předchůdce, který by odpovídal vzoru (matčin -> matka)
        - existuje takové slovo a je rodu ženského
        - existuje takové slovo, ale není rodu ženského
        - takové slovo neexistuje 
"""

import opakovane_funkce

def main(lexicon):
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}

    spatny_rod, dobry_rod, spatny_nepripojeno, bez = [], [], [], []#špatný rod - předek není ženský 
    #dobrý rod - není připojen, ale je ženský, spatny_nepripojeno - nepřipojený předek a ještě není ženský
    # bez - bez predka
    vzdalene = []

    for lexeme in lexicon.iter_lexemes():
        if lexeme.lemma.endswith("čin") and lexeme.pos == "ADJ":
            #tady je to dobře, protože to má být hned nad dítětem
            rodice = lexeme.all_parents
            jeden = False # jestli jsme našli nějakou předkyni
            jiny = False # pokud jsme ale nasli predka, co neni zensky, ale sedí do popisu
            slovo = None
            for r in rodice:
                if r.lemma[:-2] == lexeme.lemma[:-3]:
                    jiny = True 
                    if r.pos == "NOUN" and r.feats["Gender"] == "Fem":
                        jeden = True
                    else: 
                        slovo = r.lemma

            if not jeden and jiny: #máme rodiče, ale není to ženský rod
                spatny_rod.append((lexeme.lemma, slovo))

            elif not jeden and not jiny:
                rodic = lexeme.lemma[:-3] + "ka"
                if rodic in all_lemmas:
                    predek = lexicon.get_lexemes(rodic)[0]
                    if opakovane_funkce.vzdalene_pribuzny(lexeme, predek):
                        vzdalene.append((lexeme.lemma, predek.lemma))
                    elif opakovane_funkce.vzdalene_pribuzny(predek, lexeme):
                        vzdalene.append((predek.lemma, lexeme.lemma))
                    elif predek.pos == "NOUN" and predek.feats["Gender"] == "Fem":
                        dobry_rod.append((lexeme.lemma, predek.lemma))
                    else:
                        spatny_nepripojeno.append((lexeme.lemma, predek.lemma))
                else:
                    bez.append(lexeme.lemma)
                
    opakovane_funkce.vypis_matcin_otcuv(spatny_rod, dobry_rod, spatny_nepripojeno, bez, "ženského", "čin", "E_SlovaKonciciNaCin", vzdalene, "špatný rod rodiče", "chybí hrana")
                    
