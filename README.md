# Dados Publicos Deputados 2022
Dados publicos dos deputados do Brasil e seus gastos e despesas durante o ano de 2022.
Para o desenvolvimento deste projeto utilizei as seguintes ferramentas:
Python + Pandas
AWS S3 - armazenamento dos dados
AWS GLUE - orquestração e mapeamento dos dados gerados no S3
AWS ATHENA - realizar analise utilizando SQL Padrão
AWS QUICKSIGHT - Realizar a visualização dos dados

# Explicação código Python
O arquivo "main.py" irá extrair os dados da api no site "dadosabertos" do governo.
Irá tratar os dados utilizando a biblioteca pandas
Na função "retorna_dataframe_deputados_geral" retorna o dataframe geral com os dados basicos dos deputados
Na função "retorna_dataframe_deputados_detalhado" retorna o dataframe detalhado com os dados completos dos deputados (valor liquido, despesa, fornecedor e etc)
Utilizando a classe AWS do arquivo "AWS.py" ele irá criar o csv utilizando o dataframe e carregar os arquivos no bucket do AWS S3


# Explicação AWS Glue
Após os dados serem carregados no bucket do S3 é inicializado o crawler criado utilizando o AWS GLUE que realizar a orquestração dos dados e mapeamento dos tipos de dados de cada coluna.

Após o mapeamento os dados são armazenados em tabelas no banco de dados do Data Catalog dentro do AWS Glue.

# Explicação AWS ATHENA
Após o processo do crawler entra a consulta no AWS Athena, que é um serviço de consulta que facilita a analise de dados no Amazon S3 utilizando SQL padrão.
Ao entrar no Athena e selecionar o banco de dados do Data catalog, você irá visualizar as tabelas geradas no banco.

Para unificar as duas tabelas criei uma view e realizei um join entre elas. Com isso ja é possivel fazer a visualização de dados.

# Explicação AWS QUICKSIGHT
No AWS QUICKSIGHT é possivel criar visualização de dados com maior facilidade.
No Quicksight criei um Dataset utilizando a View que criei no Athena.

Dentro do Analyses criei um visualização e realizei a construção de todo o visual do meu relatório. 









