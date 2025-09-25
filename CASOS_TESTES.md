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


# Casos de testes - CRUD de Polls
## CT-01 - Criar Voto com Sucesso
**Dado que** um estudante (`student`) autenticado envie uma requisição **POST** para `/api/v1/votes/create/` com um `poll_id` e uma `option` válidos.  

**Quando** a API processar a requisição.  

**Então** a API deve criar um novo registro de **Vote** associado ao estudante e retornar o status **201 Created**.  

---

## CT-02 - Listar Apenas Votos Próprios
**Dado que** existam votos de múltiplos estudantes no sistema para uma mesma enquete.  

**Quando** um estudante (`student_1`) autenticado fizer uma requisição **GET** para `/api/v1/votes/`.  

**Então** a API deve retornar o status **200 OK** e uma lista contendo apenas os votos pertencentes ao `student_1`.  

---

## CT-03 - Impedir Voto Duplicado
**Dado que** um estudante já tenha votado em uma enquete específica.  

**Quando** o mesmo estudante tentar enviar uma segunda requisição **POST** para `/api/v1/votes/create/` para a mesma enquete, mesmo que com uma opção diferente.  

**Então** a API deve impedir a criação do segundo voto e retornar o status **400 Bad Request** com uma mensagem de erro indicando que o voto já existe.  

---

## CT-04 - Gerar Lista de Embarque Agrupada (Sucesso)
**Dado que** múltiplos estudantes, associados a diferentes pontos de embarque, votaram em uma enquete.  

**Quando** um usuário autenticado (`motorista`/`admin`) fizer uma requisição **GET** para `/api/v1/polls/{id}/boarding_list/` com o parâmetro `trip_type` válido.  

**Então** a API deve retornar o status **200 OK** e uma lista de objetos, onde cada objeto representa um **ponto de embarque** e contém uma **sub-lista dos estudantes** daquele ponto que confirmaram presença para a viagem.  

---

## CT-05 - Validar Parâmetro Obrigatório na Lista de Embarque
**Dado que** um usuário autenticado (`motorista`/`admin`) deseja consultar a lista de embarque.  

**Quando** ele fizer uma requisição **GET** para `/api/v1/polls/{id}/boarding_list/` **sem fornecer** o parâmetro obrigatório `trip_type`.  

**Então** a API deve retornar o status **400 Bad Request** com uma mensagem de erro indicando que o parâmetro é necessário.  

---

## CT-06 - Gerar Lista de Embarque Vazia
**Dado que** uma enquete existe, mas **nenhum estudante votou** nela ainda.  

**Quando** um usuário autenticado (`motorista`/`admin`) fizer uma requisição **GET** para `/api/v1/polls/{id}/boarding_list/` com um `trip_type` válido.  

**Então** a API deve retornar o status **200 OK** e uma **lista vazia (`[]`)**, indicando que não há alunos para aquela viagem.  