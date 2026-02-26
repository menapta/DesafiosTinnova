# DesafiosTinnova
Conjuntos de desafios realizado para empresa Tinnova em 24/04/2026
Matheus Frantz de Faria

## Possuir Python 3.10 

## CRIAR AMBIENTE VIRTUAL
python -m venv .venv

## EXECUTAR AMBEINTE VIRTUAL
  ### Linux | mac/OS
source .venv/bin/activate
  ### Windows
.venv\Scripts\activate 

## INSTALAR PACOTES NECESSÀRIOS
pip install -r requirements.txt


## INTRO

## EXECUÇÔES

#### Execução de testes geral para unitários
python -m unittest discover -s tests -p "Tests*.py"

#### Execução de testes geral para integração
python -m pytest tests/integration/ -o "python_files=Tests*.py" -v


python -m unittest discover -s tests tests/unit/ -v

#### Execução de testes individuais para unitários
python -m pytest tests/integration/TestsLoginController.py -v  

#### Execução de testes individuais para integração
python -m unittest tests/unit/TestsVehicleRepository.py -v


## Execução do APP 
uvicorn app.main:app --reload 

### Para ver logs
uvicorn app.main:app --reload --log-level debug