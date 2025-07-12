#!/bin/bash
echo "Posicionando na Home"
cd $HOME

echo "Ativando ambiente virtual"
source .virtualenvs/avalim/bin/activate

echo "Posicionando no projeto MC"
cd ./MC

echo "Alterando DEBUG para falso"
sed -i 's/DEBUG = True/DEBUG = False/g' ./MC/settings.py

echo "Instalando pacotes"
pip3 install -r ./requirements.txt

echo "Executando migrate"
# python3 ./manage.py migrate

echo "Executando collectstatic"
python ./manage.py collectstatic --noinput

echo "Apagando as fontes"
rm -r ./www/docs/html/_sources/
