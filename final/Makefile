# Název virtuálního prostředí
VENV = venv-dir

# Cesta k Pythonu ve virtuálním prostředí
PYTHON = $(VENV)/bin/python

# DeriNet dataset
DERINET_ZIP = allzip.zip
DERINET_URL = https://lindat.mff.cuni.cz/repository/server/api/core/items/62540779-b206-4cf7-ac33-399ce68e35e6/allzip?handleId=11234/1-5846

# Repozitář s derinet lexicon
DERINET_REPO = https://github.com/vidraj/derinet.git

all:statistika

#testuju, jestli tam je už je derinet otevřen, jestli ne, otevírám
allzip: $(DERINET_ZIP)
	powershell -Command "if (-Not (Test-Path './derinet-2-3.tsv')) { \
        Expand-Archive -Path '$(DERINET_ZIP)' -DestinationPath 'slozka'; \
        Move-Item -Path '.\slozka\derinet-2-3.tsv' -Destination '.'; \
        Remove-Item -Recurse -Force '.\slozka' \
    }"


# stáhne dataset jen pokud ještě není
$(DERINET_ZIP):
	curl -L -o $(DERINET_ZIP) "$(DERINET_URL)"
	
#tvorba virtuálního prostředí
venv:
	python -m venv $(VENV)

#klonuju derinet
derinet:
	if not exist derinet git clone https://github.com/vidraj/derinet.git

#něco fuj
install_derinet: venv derinet allzip
	powershell -Command "& '$(VENV)\\Scripts\\pip.exe' install -e '.\\derinet\\tools\\data-api\\derinet2'"

#spouším generování testů
run: install_derinet
	$(VENV)\Scripts\python.exe spousteni_testu.py

# Instalace globálních Python balíčků potřebných pro generování grafů
install_global_packages:
	python -m pip install --upgrade pip
	python -m pip install pandas matplotlib

#generuju statistické grafíky
statistika: run install_global_packages
	python generovani_statistiky.py

clean:
	powershell -Command "Remove-Item -Recurse -Force '$(VENV)', 'derinet', '$(DERINET_ZIP)'"

