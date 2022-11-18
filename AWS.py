import boto3
from botocore.exceptions import NoCredentialsError
from io import StringIO
from dotenv import load_dotenv
import os

class AWS():
  def __init__(self, df, bucket, s3_file=None, delimitador='|'):
    '''
    df: dataframe com os dados que deseja subir para o S3
    bucket: nome do bucket no no AWS S3
    s3_file: caminho dentro do bucket que vai ser inserido o dataframe
    delimitador: o tipo de delimitador que seu arquivo vai possuir quando subir para o AWS S3
    '''
    load_dotenv()
    self.ACCESS_KEY = os.getenv('ACCESS_KEY') #chave de acesso do AWS
    self.SECRET_KEY = os.getenv('SECRET_KEY') #chave secreta do AWS
    self.df = df
    self.bucket = bucket
    self.s3_file = s3_file
    self.delimitador = delimitador


  def upload_to_aws(self):
    '''Realiza o upload do arquivo para o S3'''
    try:
      s3 = boto3.client('s3', aws_access_key_id=self.ACCESS_KEY, aws_secret_access_key=self.SECRET_KEY)
      csv_buf = StringIO()
      self.df.to_csv(csv_buf, sep=self.delimitador, header=True, index=False)
      csv_buf.seek(0)
      s3.put_object(Bucket=self.bucket, Body=csv_buf.getvalue(), Key=self.s3_file)
      print("Carga no S3 realizada com sucesso!")
    except Exception as e:
      print(f"Ocorreu o seguinte erro: {e}")
    

