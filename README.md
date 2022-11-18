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
Irá tratar os dados utilizando a biblioteca pandas.
Na função "retorna_dataframe_deputados_geral" retorna o dataframe geral com os dados básicos dos deputados
Na função "retorna_dataframe_deputados_detalhado" retorna o dataframe detalhado com os dados completos dos deputados (valor líquido, despesa, fornecedor e etc)
Utilizando a classe AWS do arquivo "AWS.py" ele irá criar o csv utilizando o dataframe e carregar os arquivos no bucket do AWS S3
![image](https://user-images.githubusercontent.com/46444726/202587538-01d9a8c0-533b-4fc0-ab60-9410e833723d.png)
![image](https://user-images.githubusercontent.com/46444726/202587557-bc9b2aa4-d697-4eda-9aa9-92443b2d3d36.png)

# Explicação AWS Glue
Após os dados serem carregados no bucket do S3 é inicializado o crawler criado utilizando o AWS GLUE que realizar a orquestração dos dados e mapeamento dos tipos de dados de cada coluna.
![image](https://user-images.githubusercontent.com/46444726/202587629-f629a4c8-bc73-4f54-8ccb-babef8773863.png)

Após o mapeamento os dados são armazenados em tabelas no banco de dados do Data Catalog dentro do AWS Glue.
![image](https://user-images.githubusercontent.com/46444726/202587667-acf07030-5500-4213-8915-b011619f232d.png)
![image](https://user-images.githubusercontent.com/46444726/202587697-41a136d5-255e-4b4c-9042-7693e40a0990.png)


# Explicação AWS ATHENA
Após o processo do crawler entra a consulta no AWS Athena, que é um serviço de consulta que facilita a analise de dados no Amazon S3 utilizando SQL padrão.
Ao entrar no Athena e selecionar o banco de dados do Data catalog, você irá visualizar as tabelas geradas no banco.
![image](https://user-images.githubusercontent.com/46444726/202587745-24d33041-edd6-454c-8d11-a859ced5452b.png)
![image](https://user-images.githubusercontent.com/46444726/202587762-a6e189b4-01e1-4a60-a515-3eb03b3725dc.png)


Para unificar as duas tabelas criei uma view e realizei um join entre elas. 
![image](https://user-images.githubusercontent.com/46444726/202587801-0ce11b3b-354c-42bb-92bf-c3c6e4a1a483.png)

Com isso ja é possivel fazer a visualização de dados.

# Explicação AWS QUICKSIGHT
No AWS QUICKSIGHT é possivel criar visualização de dados com maior facilidade.
No Quicksight criei um Dataset utilizando a View que criei no Athena.
![image](https://user-images.githubusercontent.com/46444726/202587829-efab3cd9-150c-4ee8-b2dd-07558140e0ed.png)

Dentro do Analyses criei um visualização e realizei a construção de todo o visual do meu relatório. 
![image](https://user-images.githubusercontent.com/46444726/202587864-bff394da-1dc9-4c39-8796-6e7a45c73bf0.png)
![image](https://user-images.githubusercontent.com/46444726/202587879-e87a3f4f-8424-4a38-af1a-edb977679efe.png)
![image](https://user-images.githubusercontent.com/46444726/202587888-8c941365-99c1-44ee-8e80-94b6f9a324a6.png)












