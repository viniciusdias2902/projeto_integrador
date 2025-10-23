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

### CT-02 - Login com senha incorreta
**Passos:**
1. Acessar página de login
2. Inserir e-mail válido e senha incorreta
3. Clicar em “Entrar”  
**Resultado esperado:** Exibe mensagem de erro: “Email ou senha inválidos”.