# Tests front-end

# Escopo
- Página de login
- Página de cadastro
- Página de enquetes

## Casos de testes

### CT-01 - Login com credenciais válidas
**Pré-condição:** usuário cadastrado no sistema  
**Passos:**
1. Acessar página de login
2. Inserir e-mail e senha válidos
3. Clicar em “Entrar”  
**Resultado esperado:** Redireciona para a página de enquetes

### CT-02 - Login com credenciais incorretas
**Passos:**
1. Acessar página de login
2. Inserir e-mail inválido e senha incorreta
3. Clicar em “Entrar”  
**Resultado esperado:** Exibe mensagem de erro: “Email ou senha inválidos”.

### CT-03 - Primeiro voto com sucesso
**Passos:**
1. Fazer login
2. Acessar página de enquetes
3. Localizar enquete do dia **"Sexta"**
4. Selecionar a opção **"Ida e volta"**
5. Clicar em **"Atualizar voto"**
**Resultado esperado:** Deve aparecer a mensagem: **"Voto atualizado com sucesso"**

### CT-04 - Alteração de voto com sucesso
**Passos:**
1. Acessar novamente a enquete **"Sexta"**
2. Selecionar a opção **"Apenas ida"** e clicar em **"Atualizar voto"**
3. Confirmar mensagem de confirmação
4. Selecionar a opção **"Não vou"**
5. Clicar novamente em **"Atualizar voto"**
**Resultado esperado:** Nas duas alterações de voto, deve aparecer a mensagem: **"Voto atualizado com sucesso!"**