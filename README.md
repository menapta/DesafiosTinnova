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
Para conseguir a documentação swagger, acessar http://127.0.0.1:8000/docs ou buscar em um dos arquivos dentro da pasta 'documents' que contém openapi.json e swagger.yaml

As colections usadas para testes no Postamn se encontram no arquivo 0000000000Tinnova.postman_collection.json

## EXECUÇÔES
Passos para ralizar as execuções

#### Execução de testes geral para unitários
python -m unittest discover -s tests -p "Tests*.py"

#### Execução de testes geral para integração
python -m pytest tests/integration/ -o "python_files=Tests*.py" -v

#### Execução de testes individuais para unitários
python -m unittest tests/unit/TestsVehicleRepository.py -v  
python -m unittest tests/unit/TestsVehicleService.py -v  
python -m unittest tests/unit/TestsPasswordManager.py -v  
python -m unittest tests/unit/TestsLoginService.py -v  
python -m unittest tests/unit/TestsLoginRepositoriy.py -v  


#### Execução de testes individuais para integração
python -m pytest tests/integration/TestsVehiclesController.py -v
python -m pytest tests/integration/TestsLoginController.py -v
python -m pytest tests/integration/TestsRoot.py -v

### Executar o docker
docker-compose up

### Execução do APP 
uvicorn app.main:app --reload 

### Para ver logs
uvicorn app.main:app --reload --log-level debug