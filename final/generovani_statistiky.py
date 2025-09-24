import os
import pandas as pd
import matplotlib.pyplot as plt
import random

def pocet_kategorii_testu():
    seznam = {"E": 0, "I": 0, "W": 0}
    for nazev in jmena:
        seznam[nazev[0]] += 1

    # správně pojmenujeme sloupce
    df = pd.DataFrame(list(seznam.items()), columns=["Kategorie", "Pocet"])

    # vygenerujeme koláčový graf
    df.set_index("Kategorie").plot.pie(
        y="Pocet",
        autopct='%1.1f%%',
        legend=False,
        ylabel=""
    )

    plt.title("Rozdělení kategorií testu podle závažnosti")
    plt.tight_layout()
    plt.savefig(os.path.join(adresar, "kategorie_testu.png"))
    plt.close()

def uspenost_hledani_reseni_jeden_seznam_E():
    uspesnost = dict()
    pomer = 10/len([f for f in os.listdir(adresar) if f.startswith(("E_Osam")) and f.endswith(".tsv")])
    celkove_dva = 0
    celkove_tri = 0
    vybrano = 0

    random.seed(42)
    for nazev in jmena:
        if nazev.startswith("E_Osam"):
            if random.random() < pomer:
                dva, tri = 0, 0
                vybrano += 1
                with open(os.path.join(adresar, nazev), encoding="utf-8") as f:
                    for radek in f:
                        radek = radek.strip()
                        if not radek.startswith("*") and radek:
                            sloupce = radek.split("\t")
                            #nenašlo se řešení
                            if len(sloupce) == 2:
                                dva += 1
                            #našlo se řešení
                            elif len(sloupce) == 3:
                                tri += 1
                
                uspesnost[nazev] = (dva, tri)
                celkove_dva += dva
                celkove_tri += tri
                    # pokud je víc nebo míň, můžeš to taky logovat
    
    uspesnost['průměrně'] = (celkove_dva/vybrano, celkove_tri/vybrano)


    # převod slovníku na DataFrame
    df = pd.DataFrame.from_dict(
        uspesnost,
        orient="index",
        columns=["nenalezen rodič", "nalezen rodič"]
    )

    # sloupcový graf – vedle sebe sloupce pro nalezeno / nenalezeno
    ax = df.plot(
        kind="bar",
        figsize=(12,6),
        color=["tomato", "seagreen"]  # volitelně barvy
    )

    ax.set_title("Úspěšnost hledání řešení pro E_Osamoceny/a")
    ax.set_xlabel("Název testu")
    ax.set_ylabel("Počet slov")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Stav rodiče")
    plt.tight_layout()
    plt.savefig(os.path.join(adresar, "uspesnost_E_Osam.png"))
    plt.close()

def je_cislo(s):
    try:
        float(s)  # zkusíme převést na float
        return True
    except ValueError:
        return False

def alfonz_a_spol():
    informace = dict()

    for nazev in jmena:
        if "Nestale" in nazev:
            bez = 0
            vzdalene = 0
            blizko = 0
            sedm = 0
            with open(os.path.join(adresar, nazev), encoding="utf-8") as f:
                for radek in f:
                    if sedm < 7:
                        sedm += 1
                        sloupce = radek.split("\t")
                        if len(sloupce) > 1:
                            if je_cislo(sloupce[1]):
                                if "nijak" in sloupce[0]:
                                    bez = float(sloupce[1])
                                elif "napřímo" in sloupce[0]:
                                    vzdalene = float(sloupce[1])
                                else:
                                    blizko += float(sloupce[1])
            
            informace[nazev] = (bez, vzdalene, blizko)

        # převod slovníku na DataFrame
    df = pd.DataFrame.from_dict(
        informace,
        orient="index",
        columns=["nijak nespojeni", "vzdáleně spojeni", "rodič a syn"]
    )

    # sloupcový graf – vedle sebe sloupce pro nalezeno / nenalezeno
    ax = df.plot(
        kind="bar",
        figsize=(12,6),
        color=["tomato", "seagreen", "yellow"]  # volitelně barvy
    )

    ax.set_title("Hodnoty v procentech, jaké vztahy mají mezi sebou daná slova")
    ax.set_xlabel("Název testu")
    ax.set_ylabel("Počet slov z celku v procentech")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Stav rodiče")
    plt.tight_layout()
    plt.savefig(os.path.join(adresar, "alfonz_vztahy.png"))
    plt.close()

def cin_uv_jeden(podstring):
    slovnicek = dict()

    for soubor in jmena:
        if podstring in soubor:
            with open(os.path.join(adresar, soubor), encoding="utf-8") as f: 
                for radek in f:
                    radek = radek.strip()
                    if "*" in radek and len(radek.split("\t")) == 1:
                        if "přídavná jména" not in radek:
                            nazev = radek.lstrip("*").strip()
                            if len(nazev) > 2:
                                slovnicek[nazev] = 0
                    elif "*" not in radek and nazev:
                        slovnicek[nazev] += 1

    df = pd.DataFrame.from_dict(slovnicek, orient="index", columns=["Počet řádků"])
    df.plot(kind="bar", figsize=(12,6), color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(adresar, f"{podstring}_graf.png"))
    plt.close()

# vyhledáme soubory v adresáři
adresar = os.path.dirname(os.path.abspath(__file__))
jmena = [f for f in os.listdir(adresar) if f.startswith(("E_", "W_", "I_")) and f.endswith(".tsv")]

pocet_kategorii_testu()
uspenost_hledani_reseni_jeden_seznam_E()
alfonz_a_spol()
cin_uv_jeden("Cin")
cin_uv_jeden("Uv")