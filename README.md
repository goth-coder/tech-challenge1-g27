# API Embrapa Vitivinicultura

## Descrição

API REST em Python/Flask para consulta de dados públicos da vitivinicultura do Brasil, obtidos via web scraping do site da Embrapa Uva e Vinho. A API segue arquitetura MVC simplificada, utiliza autenticação JWT e possui fallback para dados CSV locais caso o scraping falhe.

## Funcionalidades

- Autenticação JWT (`/register`, `/login`)
- Endpoints de produção:
  - `GET /producao` — Todos os dados de produção de 1970 a 2023.
  - `GET /producao/{ano}` — Dados de produção do ano específico.
- Endpoints de processamento:
  - `GET /processamento/{ano}` — Dados de todas as subopções (viníferas, americanas, mesa, sem classificação) para o ano.
  - `GET /processamento/{tipo}/{ano}` — Dados de uma subopção específica para o ano.
- Endpoints de comercialização:
  - `GET /comercializacao` — Todos os dados de comercialização de 1970 a 2023.
  - `GET /comercializacao/{ano}` — Dados de comercialização do ano específico.
- Scraping dinâmico com BeautifulSoup e fallback automático para CSV (`static_data/`).
- Código documentado e pronto para testes via Postman.

## Endpoints principais

### Autenticação
- `POST /register` — Cadastro de usuário
- `POST /login` — Login e obtenção do token JWT

### Produção
- `GET /producao`
- `GET /producao/{ano}`

### Processamento
- `GET /processamento/{ano}`
- `GET /processamento/{tipo}/{ano}`
  - Tipos: `viniferas`, `americanas`, `mesa`, `semclass`

### Comercialização
- `GET /comercializacao`
- `GET /comercializacao/{ano}`

## Exemplos de resposta

- `/producao/2023`:
```json
{
  "2023": [
    {
      "categoria": "VINHO DE MESA",
      "produtos": [
        {"produto": "Tinto", "quantidade": 139320884},
        {"produto": "Branco", "quantidade": 27910299}
      ]
    }
  ]
}
```

- `/processamento/2023`:
```json
{
  "2023": {
    "viniferas": [ {"cultivar": "TINTAS", "quantidade": 35881118}, ... ],
    "americanas": [ {"cultivar": "BORDO", "quantidade": 154310837}, ... ],
    "mesa": [ {"cultivar": "TINTAS", "quantidade": 175030}, ... ],
    "semclass": [ {"cultivar": "Sem classificação", "quantidade": 0} ]
  }
}
```

- `/processamento/viniferas/2023`:
```json
{
  "ano": 2023,
  "tipo": "viniferas",
  "dados": [
    {"cultivar": "TINTAS", "quantidade": 35881118},
    {"cultivar": "Alicante Bouschet", "quantidade": 4108858}
  ]
}
```

- `/comercializacao/2023`:
```json
{
  "2023": [
    {
      "categoria": "VINHO FINO DE MESA",
      "produtos": [
        {"produto": "Tinto", "quantidade": 12450606},
        {"produto": "Rosado", "quantidade": 1214583}
      ]
    }
  ]
}
```

## Como rodar o projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Certifique-se de que os arquivos CSV estão presentes em `static_data/`.
3. Execute a aplicação:
   ```bash
   python main.py
   ```
4. Use Postman ou outro cliente HTTP para testar os endpoints (JWT obrigatório).

## Observações
- O scraping utiliza BeautifulSoup e segue a estrutura do HTML oficial da Embrapa.
- Se o scraping falhar, os dados são carregados automaticamente dos arquivos CSV.
- O projeto está pronto para deploy na Vercel.

## Estrutura esperada

```
/
├── app/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── static_data/
│   └── *.csv
├── .env
├── requirements.txt
├── main.py
└── README.md
```

## Licença
MIT
