import requests
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from AWS import AWS



class Deputados():
  def __init__(self):
    self.URL = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
    self.PARAMETROS = {
      'ordem': 'ASC',
      'ordenarPor': 'ID'
    }


  def retorna_json_api(self):
    '''Retorna o json dos deputados'''
    try:
      deputados_json = requests.get(self.URL, self.PARAMETROS).json()
      return deputados_json
    except Exception as e:
      print(f'Ocorreu o seguinte erro: {e}')


  def trata_dados_df(self, dataframe, colunaRemoveSeNulo: list = None):
    #Remover duplicidades
    df_tratado = dataframe.drop_duplicates()
    # Verificar valores nulos no id e apaga se houver
    df_tratado = df_tratado.dropna(subset=colunaRemoveSeNulo)
    return df_tratado


  def retorna_dataframe_deputados_geral(self):
    '''Retorna a informação basica dos deputados'''
    df_dep_geral = pd.DataFrame(self.retorna_json_api()['dados'])
    df_dep_geral_tratado = self.trata_dados_df(df_dep_geral, ['id'])
    aws_geral = AWS(df_dep_geral_tratado, 'dadosdeputadosanalise', 'brutos/geral/deputados_geral.csv')
    aws_geral.upload_to_aws()


  def retorna_dataframe_deputados_detalhado(self):
    '''Retorna os dados detalhados dos deputados'''
    deputados = self.retorna_json_api()
    df_deputados_detalhado = pd.DataFrame(deputados['dados'])
    df_deputados_detalhado = pd.DataFrame(columns=['id', 'ano', 'mes', 'tipoDespesa', 'codDocumento', 'tipoDocumento', 'codTipoDocumento', 'dataDocumento', 'numDocumento', 'valorDocumento', 'urlDocumento', 'nomeFornecedor', 'cnpjCpfFornecedor', 'valorLiquido', 'valorGlosa', 'numRessarcimento', 'codLote', 'parcela'])
    #Percorre o id de cada deputado e insere as informações detalhadas no dataframe
    for deputado in deputados['dados']:
      deputados_detalhado = requests.get(self.URL + f"/{deputado['id']}/despesas").json()
      df_deputados_detalhado = df_deputados_detalhado.append(deputados_detalhado['dados'], ignore_index=True)
      df_deputados_detalhado["id"].fillna(deputado['id'], inplace = True)
    
    #carga no S3
    aws_detalhado = AWS(df_deputados_detalhado, 'dadosdeputadosanalise', 'brutos/detalhado/deputados_detalhado.csv',delimitador='|')
    aws_detalhado.upload_to_aws()

deputados = Deputados()
deputados.retorna_dataframe_deputados_geral()
deputados.retorna_dataframe_deputados_detalhado()

