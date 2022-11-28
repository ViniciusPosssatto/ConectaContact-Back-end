<p align="center">
  <img src="https://user-images.githubusercontent.com/101053966/204116071-f42933b9-bf07-4705-86ce-6a65f8e27d5b.png" width="300" />
</p>

# Conecta Contact

<p align="justify">Somos a Conecta Nuvem e este é um dos nossos produtos pricipais.</p>
<p align="justify">Com o Conecta Contact você tem acesso rápido e prático aos seus contatos cadastrados na sua conta Google. Após o login, você será redirecionado para tela inicial e irá visualizar os domínios de email cadastrados nos seus contatos, podendo realizar pesquisas através da barra de pesquisa ou clicando no card, onde irá apresentar todos os emails relacionados à aquele domínio.</p>
<p align="justify">Totalmente gratuito, é só entrar e utilizar nosso sistema.</p>
</br>

# Aplicação disponível em:

- Deploy realizado no Cloud Run do GCP

```js
  https://conectacontactbackend-myb7gebzdq-rj.a.run.app
```

# Frontend do projeto disponível em:

```js
https://github.com/ViniciusPosssatto/ConectaContact-Back-end
```
Aplicação frontend rodando no Firebase Hosting:

```js
https://conectacontactcc.firebaseapp.com/login
```


## Tópicos

- [Descrição do projeto](#descrição-do-projeto)
- [Dependencias utilizadas](#dependencias-utilizadas)
- [Como executar](#como-executar-o-projeto-local)
- [Desenvolvedor](#desenvolvedor)
- [Exemplos das telas](#exemplos-das-telas)

</br>
</br>

# Descrição do projeto

<p align="justify">A ideia principal do projeto é apresentar ao usuário os seus contatos cadastrados na sua conta Google, podendo escolher quais domínios deseja visualizar.</p>
<p align="justify">O objetivo é por em prática conhecimentos de Python, Flask, MongoDB, utilizando conceitos de API rest com seus enpoints, validações, testes unitários e deploy no Cloud Run do Google Cloud Platform.</p>

</br>

# Dependencias utilizadas

 `Python` - linguagem principal utilizada na construção do backend.

 `Flask `- framework, conjunto de ferramentas do Python usado para desenvolvimento web.

 `PyJWT` - condificação do token de autenticação.

 `pymongo` - módulo Python que pode ser usado para interagir entre o banco de dados mongo e os aplicativos Python. Os dados que são trocados entre o aplicativo Python e o banco de dados mongo estão no formato JSON binário

 `google-auth / google-auth-oauthlib` - protocolo de autorização que permite que aplicativos obtenham acesso limitado a contas de usuários em um serviço HTTP sem a necessidade de enviar seu usuário e senha. Basicamente, o usuário delega, a um determinado aplicativo, acesso aos seus dados em um determinado serviço ou API.

 `pytest` - realiza os testes sob o comando: 

 ```js
 pytest tests/ -v -W ignore::DeprecationWarning
 ```

 `pytest-cov` - realiza os testes sob o comando a seguir, sendo gerado um percentual de cobertura de código realizado pelos testes:

 ```js
 pytest tests/ -v -W ignore::DeprecationWarning --cov  
 ```

 `mongoDB-Atlas` - responsável por armazenar a database em um cluster do ATLAS.


</br>

# Como executar o projeto local
<p align="justify">Faça o clone do repositório e então execute os comandos a seguir:</p>

```
poetry config --local virtualenvs.in-project true
```
- para instalar as dependências contidas no pyproject.json

```
poetry install
```
- executar a aplicação Flask:
```
flask run
```

</br>

# Endpoints

1. `[POST] /login/auth/google (login)`

 - realiza a compilação da URL de login no OAuth com as permissões que devem ser concedidas para entrar na aplicação.

2. `[GET] /login/callback (login)`

- cadastra o usuário na database do mongoDB e faz a requisição da lista de contatos do usuário que realizou o login na aplicação, assim como salva esses contatos com relacionamento ao usuário através do "id_user".
Por fim redireciona o usuário para a tela do front end.


3. `[GET] /contacts/< id_user > (contacts)`

- retorna uma lista de objetos com todos os contatos salvos na database do usuário vinculado ao ID enviado como query param (obrigatório).
Ex:

```js 
[
    {
      _id: ...,
      email: ...,
      photo: ....
    }
]
```

4. `[GET] /contacts/domain/ < id_user > (contacts)`

-  retorna uma lista com todos os domínios dos emails dos contatos salvos na database do usuário vinculado ao ID enviado como query param (obrigatório).


</br>

# Desenvolvedor

| [<sub>Vinicius Possatto Stormoski</sub><br><img src="https://avatars.githubusercontent.com/u/101053966?v=4" width=100><br>](https://github.com/ViniciusPosssatto)
| :---: | 

[`Linkedin disponível aqui`](https://www.linkedin.com/in/vinicius-possatto-stormoski-3696a922b/)

</br>

# Exemplos das pipelines de CI/CD executadas ao realizar um PR ou merge

<p align="center">
  <img src="https://user-images.githubusercontent.com/101053966/204183270-58b675a4-c8a1-4b82-ac32-751201e64b3a.png" width="420" />

</p>