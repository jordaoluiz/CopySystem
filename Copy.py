from iqoptionapi.stable_api import IQ_Option
import time, json, logging, configparser
from datetime import datetime, date, timedelta
from dateutil import tz
import sys
import numpy as np
import requests
from bs4 import BeautifulSoup

logging.disable(level=(logging.DEBUG))
API = IQ_Option('mail@mail.com', 'password')

def Analisys():
    URL = 'https://br.investing.com/technical/technical-summary'
    page = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    soup = BeautifulSoup(page.content, 'html.parser')
    pares = soup.find_all('td',class_='symbol middle center')
    
    result = soup.find_all('td',class_='greenFont bold left arial_14 js-socket-elem' )
    for par in pares:
        print(par)
        titulo = par.find('a')
        print(titulo)
    for results in result:
        title = results
        
        print(title)
def loginIQ():
    API.connect()

    API.change_balance('PRACTICE') # PRACTICE / REAL
    
    while True:
        if API.check_connect() == False:
            print('Erro ao se conectar')
            
            API.connect()
        else:
            print('\n\nConectado com sucesso')
            break
        
        time.sleep(2)
# Pega as informações do perfil do usuário logado
def getProfileLogged():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    return perfil
def changeAccountType(accountType):
    if accountType == 'treinamento':
        print(accountType)
        
        API.change_balance('PRACTICE')
    elif accountType == 'real' :
        API.change_balance('REAL')
def getAmmount():
    return API.get_balance()
def getCurrency():
    return API.get_currency()
# PEGA A TENDENCIA ATUAL DE QUALQUER ATIVO - GRAFICO DE 1H
def getTrend(ativo,tempoGrafico,quantidade_de_candles):
    end = time.time()
    tendencia = ''
    print('QUANTIDADE DE CANDLES ANALISADA: ',int(quantidade_de_candles))
    candles = API.get_candles(str(ativo),tempoGrafico,quantidade_de_candles,end)
    print('CANDLE 0: ', candles[0]['close'])
    print('CANDLE 99: ', candles[int(quantidade_de_candles-1)]['close'])
    if candles[int(quantidade_de_candles-1)]['close'] > candles[0]['close']:
        tendencia = "TENDENCIA DE ALTA - "+ativo
    else:
         tendencia = "TENDENCIA DE BAIXA - "+ativo    

    return tendencia


loginIQ()
moeda = getCurrency()
banca = getAmmount()
perfil = getProfileLogged()

changeAccountType('treinamento')
print('SEU SALDO É DE: ',moeda,banca)
trendEURUSD = getTrend('EURNZD',1,30)
print(trendEURUSD)
print(Analisys())


