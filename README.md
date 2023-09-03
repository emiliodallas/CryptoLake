# CryptoLake

Teste Técnico Cadastra para vaga de Engenheiro de Dados GCP Pleno.
O projeto consistiu em desenvolver uma pipeline de ETL para extrair dados da API do site CoinMarketCap e armazená-los em uma tabela de dados para cada moeda no BigQuery.
- [ETL](#etl)
- [Documentação API](#Documentação)
- [Armazenamento e Modelagem de Dados](#Dados)
- [Cloud Functions](#CloudFunctions)
- [Pré Requisitos](#Requisitos)

  ## ETL
  A ETL segue o seguinte diagrama:
  
    ![Diagram](https://github.com/emiliodallas/CryptoLake/blob/master/ETL_diagram.png)
     
  ## Documentação
  O limite de requests para a API com uma conta no plano Basic (gratuito) é de 10.000 coins/mês. Cada coin equivale à um request GET, por exemplo. Por essa limitação, escolhi coletar os dados de três criptomoedas:
  
    1. Bitcoin
    2. Ethereum
    3. Tether
  
  Isso me permite fazer uma consulta a cada 15 minutos sem estourar o limite mensal.
  Como mencionado, a conexão com a API é feita por requests GET HTTP para obter dados em formato JSON sobre as moedas.

  ## Dados
  Os dados, segregados em _bronze_ e _silver_ (conforme tratamento) foram armazenados num bucket no Cloud Storage. Os dados devidamente tratados armazenados em _silver_ são, então, carregados organizadamente para o BigQuery em suas respectivas tabelas. A estrutura dos diretórios dentro do bucket é:
    - crypto-cap-market/
      - bronze/
        - Bitcoin/
          - ...
        - Ethereum/
          - ...
        - Tether/
          - ...
      - silver/
        - Bitcoin/
          - ...
        - Ethereum/
          - ...
        - Tether/
          - ...
   

  Cada arquivo recebe o nome no formato ```data_YYYY_MM_DD-HH-MM-SS.json``` para que todos tenham nomes únicos e que sejam facilmente acessados. Isso vale tanto para os dados na pasta _bronze_ quanto na pasta _silver_.

  No BigQuery, os dados que compõem a tabela escolhidos, foram:
    1. Quantidade em Circulação.
    2. Preço.
    3. Variação do volume nas últimas 24h.
    4. Variação percentual na última hora.
    5. Market Cap.
    6. Market Cap diluído no total em circulação.

  ## CloudFunctions
  O código foi construido em Python e roda no GCP Cloud Functions. A chave da api é passada como variável de ambiente da própria função. Este respositório está configurado para que seja possivel implementar com facilidade essas funções em qualquer conta GCP. Para isso é necessário possuir o SDK da GCP instalado e configurado.
  
  Foram criadas duas funções:
    1. A primeira roda através de um _trigger_ por tempo, a cada 15 minutos. Essa função é responsável por se comunicar com a API e salvar os dados brutos na primeira etapa dentro do bucket. Para rodar o código no GCP é necessário criar o _scheduler_ com o comando que está no arquivo ```create_gcp_functions.txt```. Feito isso, basta aceder ao diretório ```extract_to_storage``` e rodar o comando de criação da função ```extract_api_load_storage```. Com ela criada, basta criar a variável de ambiente desta função.
    2. A segunda roda a partir da criação de um novo objeto no bucket. Assim que a primeira função cria o arquivo .json, esta função é iniciada. Ela usa esse mesmo arquivo que serviu de _trigger_ e faz o tratamento do mesmo, salvando-o na pasta _silver_. Esse novo arquivo salvo irá acionar essa função novamente, porém, vai utilizar esse arquivo de _trigger_ para incluir esses novos dados tratados na tabela do BigQuery. Para implementar a função, o procedimento é o mesmo da primeira: aceder ao diretório ```transform_into_bigquery``` e rodar o comando onde o nome da função é ```tranform_into_bigquery```. Essa função não tem variáveis de ambiente para serem configuradas.

  Para criar as tabelas no BigQuery, rodei localmente o script Python que está no diretório ```bigquery_tables```. Para executá-lo basta:  
    1. Ter Python 3.10 instalado.
    2. Ter pip 23.2.1 instalado.
    3. Editar a função main.py dentro do diretório na criação da instância da classe ```CryptoMarketTables``` com os devidos parâmetros de projeto e dataset.
    4. Instalar a biblioteca ```virtualenv```:   
          ```        
          pip3 install virtualenv
          ```        
    5. Rodar o comando:          
        ```          
        python3.10 -m venv .venv
        ```         
    6. Entrar no ambiente virtual com:
        ```        
        source .venv/bin/activate
        ```      
    7. Instalar os requisitos com:
        ```        
        pip3 install -r requirements.txt
        ```
    8. Finalmente, rodar a função com:
        ```        
        python3.10 main.py
        ```
 
  ## Requisitos
  Para que seja possível rodar a função em outo GCP, é necessário criar um bucket e alterar alguns parâmetros em ambas funções:
    1. No arquivo ```main.py``` é necessário passar os seguintes parâmetros para a função:
        1. Nome do bucket.
        2. Nome do projeto.
        3. Nome do dataset (apenas função para BigQuery)
        4. Nome da chave API (apenas função que extrai da API)

  Com isso, as funções devem rodar normalmente. 
