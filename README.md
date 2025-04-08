## FastAPI with SQL lite and dummy ml model to classify saas companies

## Ubuntu 24.04.2 LTS

this project runs with python3.12

in order to setup the env, run following lines

```shell
#update software packages
sudo apt update
sudo apt upgrade
#install compilers and dev tools
sudo apt install build-essential
#include newer versions of python
sudo add-apt-repository ppa:deadsnakes/ppa
#install 
sudo apt install python3.12-pip
sudo apt install python3.12-venv
sudo apt install python3.12-dev
#install uvicorn for running api
sudo apt install uvicorn
#upgrade packages
python3.12 -m ensurepip --upgrade
python3.12 -m pip install --upgrade pip
#create venv
python3.12 -m venv venv
#activate venv
source venv/bin/activate
#upgrade cython, some libs need to compile code
pip install --upgrade cython
#handle binaries/libs
pip install wheel
#update again packages
sudo apt update
sudo apt upgrade
#install dependencies
pip install -r prod-requirements.txt
```

```shell
#with venv activate, create local db
python src/create_db.py
```

run project 
```shell
python src.main:app
```
check swagger for documentation and testing on localhost:8000/docs

with docker
```shell
docker build -t api .
docker run -p 8000:8000 api
```

to access log file
```shell
sudo docker exec -it <CONTAINER_ID> cat logs/app.log
```

file to import in order to test process companies is files/process_companies.json

any feature name can be given, i'm saving features as a json in order to make it unstructured and able to handle unpredictable incomes

log folder will be created first time running this project. it will log all requests,responses and errors.


## V2

implemented a TFIDF to classify descriptions based on the importance of each word. Instead of defining a saas company by already defined words, Now companies will have a probability, and probability threshold to be a saas company. used a dummy LogisticRegression Model, but could be a set of models, and could be tuned as well. please, read ml_dummy_models.py for a little deepdive

implemented unit testing for basic cenarios and edge cases for each endpoint. created mockdb to test some cases.

with venv activated and dev-requirements.txt installed, run pytest tests/ for unity testing