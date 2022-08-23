import requests
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import sqlite3
import sqlalchemy

URL = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
PARAMETROS = {
    'ordem': 'ASC',
    'ordenarPor': 'ID'
  }


def retorna_json_api():
  '''Retorna o json dos deputados'''
  try:
    deputados_json = requests.get(URL, PARAMETROS).json()
    return deputados_json
  except Exception as e:
    print(f'Ocorreu o seguinte erro: {e}')


def trata_dados_df(dataframe, colunaRemoveSeNulo: list = None):
  #Remover duplicidades
  df_tratado = dataframe.drop_duplicates()
  # Verificar valores nulos no id e apaga se houver
  df_tratado = df_tratado.dropna(subset=colunaRemoveSeNulo)
  return df_tratado


def retorna_dataframe_deputados_geral():
  '''Retorna a informação basica dos deputados'''
  df_dep_geral = pd.DataFrame(retorna_json_api()['dados'])
  df_dep_geral_tratado = trata_dados_df(df_dep_geral, ['id'])
  return df_dep_geral_tratado


def retorna_dataframe_deputados_detalhado():
  '''Retorna os dados detalhados dos deputados'''
  deputados = retorna_json_api()
  df_deputados_detalhado = pd.DataFrame(deputados['dados'])
  df_deputados_detalhado = pd.DataFrame(columns=['id', 'ano', 'mes', 'tipoDespesa', 'codDocumento', 'tipoDocumento', 'codTipoDocumento', 'dataDocumento', 'numDocumento', 'valorDocumento', 'urlDocumento', 'nomeFornecedor', 'cnpjCpfFornecedor', 'valorLiquido', 'valorGlosa', 'numRessarcimento', 'codLote', 'parcela'])
  for deputado in deputados['dados']:
    deputados_detalhado = requests.get(URL + f"/{deputado['id']}/despesas").json()
    df_deputados_detalhado = df_deputados_detalhado.append(deputados_detalhado['dados'], ignore_index=True)
    df_deputados_detalhado["id"].fillna(deputado['id'], inplace = True)
  
  return df_deputados_detalhado


def conecta_banco():
  connection = sqlite3.connect("deputados.db")
  cursor = connection.cursor()
  return cursor
  

def cria_popula_tabelas():
  cursor = conecta_banco()
  cursor.execute("DROP TABLE IF EXISTS tb_deputado_geral")
  cursor.execute("DROP TABLE  IF EXISTS tb_deputado_detalhado")
  cursor.execute("CREATE TABLE IF NOT EXISTS tb_deputado_geral (id INTEGER PRIMARY KEY, uri TEXT, nome TEXT, siglaPartido TEXT, uriPartido TEXT, siglaUf TEXT, idLegislatura INTEGER, urlFoto TEXT, email TEXT)")
  cursor.execute("CREATE TABLE IF NOT EXISTS tb_deputado_detalhado (id INTEGER, ano INTEGER, mes INTEGER, tipoDespesa TEXT , codDocumento INTEGER, tipoDocumento TEXT, codTipoDocumento INTEGER, dataDocumento NUMERIC, numDocumento INTEGER, valorDocumento REAL, urlDocumento TEXT, nomeFornecedor TEXT, cnpjCpfFornecedor TEXT, valorLiquido REAL, valorGlosa REAL, numRessarcimento INTEGER, codLote INTEGER, parcela REAL)")
  engine = sqlalchemy.create_engine('sqlite:///deputados.db', echo=False)
  df_dep_geral_tratado = retorna_dataframe_deputados_geral()
  df_dep_geral_tratado.to_sql('tb_deputado_geral', con=engine, if_exists='append', index=False)
  df_deputados_detalhado = retorna_dataframe_deputados_detalhado()
  df_deputados_detalhado.to_sql('tb_deputado_detalhado', con=engine, if_exists='append', index=False)



cria_popula_tabelas()
