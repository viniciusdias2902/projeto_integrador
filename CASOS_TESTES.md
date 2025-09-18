# Casos de Testes - CRUD de Students 

## CT-01 - Criar Students
Dado que o usuário envie uma requisição POST /students/ com dados válidos


Quando a API processar a requisição


Então deve retornar 201 Created

CT-02 - Listar Students
Dado que existam estudantes cadastrados


Quando o usuário fizer GET /students/


Então deve retornar a lista de estudantes com status 200 OK.

CT-03 - Recuperar Students
Dado que o usuário envie uma requisição  GET /students/1/


Então deve retornar 200 OK 


CT-04 - Atualizar Students
Dado que o usuário envie uma requisição PUT /students/1/


Então deve retornar 200 OK 

CT-05 - Excluir Students
Dado que o usuário envie uma requisição: DELETE /students/1/


Então deve retornar 204 No Content.