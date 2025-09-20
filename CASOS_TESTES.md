# Casos de Testes - CRUD de Students 

## CT-01 - Criar Students
- Dado que o usuário envie uma requisição POST /students/ com dados válidos

- Quando a API processar a requisição

- Então deve retornar 201 Created

## CT-02 - Listar Students
- Dado que existam estudantes cadastrados

- Quando o usuário fizer GET /students/

- Então deve retornar a lista de estudantes com status 200 OK.

## CT-03 - Recuperar Students
- Dado que o usuário envie uma requisição  GET /students/1/

- Então deve retornar 200 OK 

## CT-04 - Atualizar Students
- Dado que o usuário envie uma requisição PUT /students/1/

- Então deve retornar 200 OK 

## CT-05 - Excluir Students
- Dado que o usuário envie uma requisição: DELETE /students/1/

- Então deve retornar 204 No Content.



# Casos de testes - CRUD de Drivers
## CT-01 - Criar Drivers
- Dado que o usuário envie uma requisição POST /drivers/ com dados válidos

- Quando a API processar a requisição

- Então deve retornar 201 Created

## CT-02 - Listar Drivers
- Dado que existam motoristas cadastrados

- Quando o usuário fizer GET /drivers/

- Então deve retornar a lista de motoristas com status 200 OK.

## CT-03 - Recuperar Drivers
- Dado que o usuário envie uma requisição  GET /drivers

- Então deve retornar 200 OK 

## CT-04 - Atualizar Drivers
- Dado que o usuário envie uma requisição PUT /drivers/3/

- Então deve retornar 200 OK 

## CT-05 - Excluir Drivers
- Dado que o usuário envie uma requisição: DELETE /drivers/1

-Então deve retornar 204 No Content.


# Casos de testes - Polls
## CT-01 - Criar Voto
- Dado que um student envie uma requisição POST /votes/create com dados válidos

- Quando a API processar a requisição

- Então deve retornar 201 Created

## CT-02 - Listar Votos
- Dado que existam votos de muitos estudantes

- Quando um estudante fizer GET/votes/

- Então deve retornar apenas os votos daquele estudante com status 200 OK.
