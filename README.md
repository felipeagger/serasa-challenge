# Serasa Consumidor - Teste para Software Developer

O objetivo deste teste é verificar (até certo ponto) suas habilidades de codificação e arquitetura. 

Considere um cenário em que você esteja construindo uma aplicação pronta para produção, onde outros desenvolvedores precisarão trabalhar e manter essa aplicação ao longo do tempo.

Como este é um processo de "code review", evite adicionar código gerado ao projeto.

Utilize Docker para Entregar suas aplicações.


## Requisitos mínimos para o teste:

- Persistência de dados em banco relacional e não relacional. PostgreeSQL e ElasticSearch!
- Camada de cache em memória com Redis.
- Utilização de um ORM para manipulação dos dados.
- Testes unitários.
- Documentação de setup e do funcionamento das APIs (um Makefile cai muito bem!).


## Requisitos das aplicações:

Nós desejamos que você crie 2 aplicações básicas (microserviços) que comuniquem-se entre si.

O primeiro deles deverá ser um cadastro de usuários, contendo os seguintes recursos:

- Listar, exibir, criar, alterar e excluir usuários

Tabela de usuários `user` deverá conter os campos: id, name, cpf, email, phone_number, created_at, updated_at.

E o segundo deverá ser um serviço de pedidos, onde este deverá conter o id do usuário que fez o pedido e se comunicar com o serviço de usuários para retornar as informações do mesmo. Esse serviço deverá ter os seguintes recursos:

- Listar, Listar por usuário, exibir, criar, alterar e excluir.

Tabela de pedidos `order` deverá conter os campos: id, user_id, item_description, item_quantity, item_price, total_value, created_at, updated_at.


Lembre-se de fazer a comunicação necessária entre os serviços para garantir a consistência de dados.

Essas aplicações também **DEVEM** estar de acordo com os padrões REST e **DEVE** ser disponibilizada uma documentação contendo os endpoints e payloads utilizados nas requisições.


## Critérios de avaliação

Dê uma atenção especial aos seguintes aspectos:

- Você **DEVE** usar bibliotecas de terceiros, e pode escolher usar um framework, e voce vai precisar justificar a sua escolha.
- Suas aplicações **DEVEM** executar em containers Docker.
- Suas aplicações **DEVEM** retornar um JSON válido e **DEVEM** conter os recursos citados anteriormente.
- Você **DEVE** escrever um código testável e demonstrar isso escrevendo testes unitários.
- Você **DEVE** prestar atenção nas melhores práticas para segurança de APIs.
- Você **DEVE** seguir as diretizes de estilo de código.

Pontos que consideramos um bônus:

- Fazer uso de uma criptografia reversível de dados sensíveis do usuário, como: email, cpf e telefone, antes de persisti-los no banco de dados
- Setup da aplicação em apenas um comando ou um script que facilite esse setup
- Outros tipos de testes, como:  teste de integração

---

Resultado:

#Dois Microserviços que comunicam entre si, Persistindo os Dados, em Bancos Relacionais e Nao Relacionais.

O primeiro é um serviço de cadastro de usuários, contendo os seguintes recursos:
Listar, exibir, criar, alterar e excluir usuários.

E o segundo é um serviço de pedidos, onde este contem o id do usuário que fez o pedido e se comunica com o serviço de usuários para retornar as informações do mesmo. Esse serviço contem os seguintes recursos:

Listar, Listar por usuário, exibir, criar, alterar e excluir.

Cada Serviço Persiste os dados em suas respectivas bases e utiliza os padrões REST. 

O Servico de Usuarios persiste os dados sensíveis(CPF, E-Mail, Telefone) com uso de criptografia.

# Requisitos :

Deixar as Porta (8080, 8081, 3306, 9200, 9300, 11211) do seu host local livre, pois serão essas portas que as aplicacões irao utilizar.

# Libraries Utilizadas

- User_API:
  Flask, MySQL, SQLAlchemy(ORM), MemCached, PyTest, Cryptography e Swagger-UI(Documentacao).


- Order_API:
  Flask, ElasticSearch, Requests(Requisicoes HTTP), PyTest, Swagger-UI(Documentacao).


Flask: É um microframework mais utilizados para web em python.

SQLAlchemy: É a biblioteca de mapeamento objeto-relacional mais robusta e completa.

MemCached: É um sistema distribuído de cache em memória amplamente utilizado.

PyTest: É o melhor framework de testes em python.

Cryptography: É um pacote que fornece criptografias primitivas para python.

Swagger-UI: É uma ferramente que permite a criacao de documentacao de API's, seguindo os padroes da "OpenAPI Initiative".

## Comandos

```shell
make clean:
       Removes all pyc, pyo and __pycache__

make setup
       set virtualenv on this path
       Install prod dependencies       

make test:
       Run tests with pytest(necessary databases ON)

make docker:
       Run app with docker and docke-compose

make dockerdown:
       Remove app from docker with docke-compose down

make rundev:
       Run the application locally(necessary databases ON)

```

# Subir a Aplicacao com Docker:
  Acesse a raiz de cada API e rode: 
  
```  
  make docker  
```

  Parar a Aplicacao: make dockerdown

# Executar os Testes de Integracao:
  
  Acesse a raiz de cada API e rode: 
  
```  
  make docker

  sudo make setup	

  make test   
```  
Lembrando que o "make docker" é para subir o Banco de Dados, Para os Testes ocorrerem com sucesso.

Obs: O Servico Order depende do servico User para o teste funcionar corretamente.


# Fluxo de Inicialização da Aplicacao

 1. Baixa as images da DockerHub;
 2. Docker Faz o Build da Imagem do Python com o Fonte da Aplicacao;
 3. Docker-Compose sobe uma stack com os Containers necessario de Cada API;

# Endereços e Servicos

No Navegador acesse: 

User_API = http://127.0.0.1:8080/api-docs

Order_API = http://127.0.0.1:8081/api-docs

 
MySQL: localhost:3306; 
- Usuario: root 
- Senha:   toor 

ElasticSearch: localhost:9200/

Variáveis de ambiente no arquivo ".env_". 

# Links e Observações

Observacao: Na instalacao padrao do Docker geralmente a interface de rede do docker chamada "docker0" recebe o IP padrao = 172.17.0.1.

Caso sua Interface do Docker seja diferente, altere o valor da variavel "USERS_HOST" para o IP Correto, no Arquivo "order_api/docker-compose.yml"

É possivel verificar esse IP com "ip addr | grep docker" ou "ifconfig".

Isso é necessario para o microservico Order conseguir comunicar com o microservico User.  

Para Utilizar Docker é necessario ter instalado:

```  
  Docker: https://www.docker.com/

  Docker-Compose: https://docs.docker.com/compose/
  
```  

