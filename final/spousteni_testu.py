import os
import requests
import urllib.request
import importlib.util
import derinet.lexicon as dlex
import testy

def nalezeni_a_spousteni_testu():
    # cesta k adresáři, kde je spuštěn tento skript
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("načítám derinet")
    lexicon = dlex.Lexicon()
    file_path = os.path.join(base_dir, "derinet-2-3.tsv")
    lexicon.load(file_path)
    print("derinet načten")

    adresar_testy = os.path.join(cesta_adresar, "test")
    # správná cesta ke složce testů
    
    jmena = [f for f in os.listdir(adresar_testy) if f.startswith(("E_", "W_", "I_")) and f.endswith(".py")]
    
    for test in jmena:
        cesta = os.path.join(adresar_testy, test)
        print("cesta pro test: " + cesta)
        print(f"Spouštím {test}...")

        # dynamicky importovat test
        spec = importlib.util.spec_from_file_location("modul_test", cesta)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)

        # spustit funkci main(lexicon), pokud existuje
        if hasattr(modul, "main"):
            modul.main(lexicon)
        
    print("Hotovo, všechny testy byly spuštěny.")

# DeriNet
derinet_url = "https://lindat.mff.cuni.cz/repository/bitstreams/6fa2bce5-51cd-42a9-ba70-cb640542cd13/download"
derinet_jmeno = "derinet-2-3.tsv"

cesta_adresar= os.path.dirname(os.path.abspath(__file__))

cesta_derinet = os.path.join(cesta_adresar, derinet_jmeno)


if not os.path.isfile(cesta_derinet):
    print(f"soubor {derinet_jmeno} není ve stejném adresáři, stahuji")
    print(f"{derinet_jmeno} chybí, stahuji...")

else:
    print(f"soubor {derinet_jmeno} je ve stejném adresáři, nemusím stahovat")

nalezeni_a_spousteni_testu()
