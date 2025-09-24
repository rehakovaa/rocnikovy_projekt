import opakovane_funkce

#dodat tam ty hranice slov
#podivam se, jestli tam zacina hranice slova, a pokud jo, tak to tam dohodim

def tvorba_pruniku(prvni, druhy):
    m, n = len(prvni), len(druhy)
    #tabulka tabulka: délka shody končící na (i,j)
    tabulka = [[0] * (n + 1) for _ in range(m + 1)]
    nejdelsi = 0
    pod = set()

    for i in range(m):
        for j in range(n):
            if prvni[i] == druhy[j]:
                tabulka[i+1][j+1] =tabulka[i][j] + 1
                if tabulka[i+1][j+1] > nejdelsi:
                    nejdelsi =tabulka[i+1][j+1]
                    pod = {prvni[i-nejdelsi+1:i+1]}
                elif tabulka[i+1][j+1] == nejdelsi:
                    pod.add(prvni[i-nejdelsi+1:i+1])

    return list(pod)

def hledani_pruniku(seznam):
    prubezny = [seznam[0]]
    for i in range(len(seznam)):
        if i == 0:
            continue
        else: 
            pomocnik = []
            for j in prubezny:
                pomocnik.extend(tvorba_pruniku(j, seznam[i]))
            prubezny = pomocnik    

    return sorted(prubezny, key=len, reverse=True)

def kontrola_kandidata(slovo, podstring, lexicon):
    celkove_slovo = lexicon.get_lexemes(slovo)[0]
    if 'Loanword' in celkove_slovo.feats.keys() and celkove_slovo.feats['Loanword'] :
            hranice = slovo.index(podstring)
            if celkove_slovo.is_boundary_allowed(hranice) and celkove_slovo.is_boundary_allowed(hranice + len(podstring)):
                return True
    return False


def deti(deticky, podstring, all_lemmas, lexicon):
    mozne_deti = []
    for i in all_lemmas:
        if podstring in i and i not in deticky:
            if kontrola_kandidata(i, podstring, lexicon):
                mozne_deti.append(i)
    
    return mozne_deti

def main(lexicon):
    seznam = []
    all_lemmas = {lex.lemma for lex in lexicon.iter_lexemes()}
    for lexeme in lexicon.iter_lexemes():
        if (lexeme.pos == "Affixoid" or lexeme.pos == "NeoCon") and len(lexeme.lemma) > 5:
            deticky = []
            for i in lexeme.children:
                deticky.append(i.lemma)

            if deticky == [] :
                aff = lexeme.lemma[1:-1]
                nalezeni = deti(deticky,aff, all_lemmas, lexicon)
            
            elif len(deticky) == 1:
                aff = lexeme.lemma[1:-1]
                if aff in deticky[0]:
                    nalezeni = deti(deticky, aff, all_lemmas, lexicon)
            
            else: 
                #tuhle prisernou funkci pisu kvuli tomu, že název affixoidu neodpovídá tomu, co se nachází ve slovech
                podstringy = hledani_pruniku(deticky)
                podstring = podstringy[0]

                nalezeni = deti(deticky, podstring, all_lemmas, lexicon)   

            seznam.append((lexeme.lemma, nalezeni))  

    opakovane_funkce.vypis_jeden_seznam_vic_moznosti(seznam, "E_MozniPotomciAffixoidu.tsv", "dohledaná slova, která mají stejnou podčást jako potomci daného affixoidu", "chybí hrana")
                
