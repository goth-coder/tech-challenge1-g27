# Guia de Uso - Postman Collection

## Configuração Inicial

### 1. Importe a Collection
1. Abra o Postman
2. Clique em "Import" 
3. Selecione o arquivo `postman_collection.json`
4. A collection "API Embrapa Vitivinicultura" será importada

### 2. Configuração de Variáveis

A collection já vem configurada com as seguintes variáveis:

- `base_url`: `http://localhost:5001` (porta padrão da aplicação)
- `jwt_token`: (será preenchido automaticamente após o login)

## Fluxo de Uso

### Passo 1: Inicie a Aplicação
```bash
cd /Users/adriannylelis/Workspace/POSTECH__ML/tech-challenge1-g27
python main.py
```

### Passo 2: Autenticação

#### 2.1 Registro de Usuário (primeira vez)
- Execute: `Authentication > Register User`
- Corpo da requisição está pré-configurado:
```json
{
    "username": "testuser",
    "password": "testpassword"
}
```

#### 2.2 Login
- Execute: `Authentication > Login User`
- O token JWT será automaticamente salvo na variável `jwt_token`
- Verifique no console se aparece: "JWT Token saved: [token]"

### Passo 3: Teste dos Endpoints

A collection está organizada por categorias:

#### **Produção**
- `Get Todos os Dados de Produção` - `/producao`
- `Get Produção por Ano` - `/producao/{ano}`

#### **Processamento**
- `Get Processamento por Ano` - `/processamento/{ano}`
- `Get Processamento por Tipo e Ano` - `/processamento/{tipo}/{ano}`
  - Tipos: `viniferas`, `americanas`, `mesa`, `semclass`

#### **Comercialização**
- `Get Todos os Dados de Comercialização` - `/comercializacao`
- `Get Comercialização por Ano` - `/comercializacao/{ano}`

#### **Importação**
- `Get Importação por Ano` - `/importacao/{ano}`
- `Get Importação Vinhos` - `/importacao/vinhos/{ano}`
- `Get Importação Espumantes` - `/importacao/espumantes/{ano}`
- `Get Importação Frescas` - `/importacao/frescas/{ano}`
- `Get Importação Passas` - `/importacao/passas/{ano}`
- `Get Importação Suco` - `/importacao/suco/{ano}`

#### **Exportação**
- `Get Exportação por Ano` - `/exportacao/{ano}`
- `Get Exportação Vinhos` - `/exportacao/vinhos/{ano}`
- `Get Exportação Espumantes` - `/exportacao/espumantes/{ano}`
- `Get Exportação Frescas` - `/exportacao/frescas/{ano}`
- `Get Exportação Suco` - `/exportacao/suco/{ano}`

## Dicas de Uso

### Autenticação Automática
- A collection está configurada com autenticação Bearer Token automática
- Todos os endpoints (exceto register/login) usam o token salvo automaticamente

### Alteração de Parâmetros
- Para testar outros anos, modifique os valores nas URLs
- Anos disponíveis: 1970-2024 (dependendo do endpoint)

### Tratamento de Erros
Possíveis respostas de erro:
- **400**: Parâmetros inválidos (ano fora do range, tipo inexistente)
- **401**: Token JWT ausente ou inválido (refaça o login)
- **404**: Dados não encontrados para os parâmetros informados
- **500**: Erro interno do servidor

### Estrutura das Respostas

#### Exemplo de resposta de sucesso:
```json
{
    "ano": 2023,
    "tipo": "vinhos",
    "dados": [
        {
            "pais": "Argentina",
            "quantidade": 1500000,
            "valor": 25000000
        }
    ],
    "fonte": "Web scraping - Embrapa"
}
```

## Testes Recomendados

### Sequência de Teste Básica:
1. Register User
2. Login User
3. Get Produção por Ano (2023)
4. Get Importação Vinhos (2023)
5. Get Exportação por Ano (2023)
6. Get Processamento por Tipo e Ano (viniferas/2023)

### Teste de Diferentes Anos:
- 1970 (primeiro ano disponível)
- 2000 (meio do período)
- 2023 (último ano completo)
- 2024 (pode ter dados parciais)

### Teste de Todos os Tipos:
- **Processamento**: viniferas, americanas, mesa, semclass
- **Importação**: vinhos, espumantes, frescas, passas, suco
- **Exportação**: vinhos, espumantes, frescas, suco

## Solução de Problemas

### Token Expirado
Se receber erro 401:
1. Execute novamente `Login User`
2. O token será renovado automaticamente

### Erro de Conexão
- Verifique se a aplicação está rodando na porta 5001
- Confirme a URL base: `http://localhost:5001`

### Dados Não Encontrados
- Verifique se o ano está no range correto
- Confirme se o tipo está escrito corretamente
- Alguns anos podem não ter dados para determinados tipos

## Validação da API

Para validar completamente a API, execute todos os endpoints da collection em sequência. Todos devem retornar:
- Status 200 (sucesso) ou 
- Status 404 (quando não há dados para os parâmetros)

A API está funcionando corretamente se não retornar erros 500 (servidor) ou 401 (após login válido).
