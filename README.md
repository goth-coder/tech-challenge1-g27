# API Embrapa Vitivinicultura

## Descrição

API REST em Python/Flask para consulta de dados públicos da vitivinicultura do Rio Grande do Sul, obtidos via web scraping do site da Embrapa Uva e Vinho. A API segue arquitetura MVC simplificada, utiliza autenticação JWT e possui fallback para dados CSV locais caso o scraping falhe.

## Funcionalidades já implementadas

- Autenticação JWT (`/register`, `/login`)
- Endpoints de produção:
  - `GET /producao` — Retorna todos os dados de produção de 1970 a 2023, agrupados por ano, categoria e produtos.
  - `GET /producao/{ano}` — Retorna dados de produção do ano específico, agrupados por categoria e produtos.
- Scraping dinâmico de todas as categorias e produtos da tabela de produção, conforme o HTML de referência.
- Fallback automático para arquivo CSV (`static_data/producao.csv`) caso o scraping falhe ou não retorne dados.
- Código documentado e pronto para testes via Postman.

## Estrutura de resposta dos endpoints de produção

- `/producao/{ano}`:
```json
{
  "2023": [
    {
      "categoria": "VINHO DE MESA",
      "produtos": [
        {"produto": "Tinto", "quantidade": 139320884},
        {"produto": "Branco", "quantidade": 27910299},
        ...
      ]
    },
    ...
  ]
}
```

- `/producao`:
```json
{
  "anos": {
    "2023": [ ... ],
    "2022": [ ... ],
    ...
  }
}
```

## Como rodar o projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Certifique-se de que o arquivo `static_data/producao.csv` está presente.
3. Execute a aplicação:
   ```bash
   python main.py
   ```
4. Use Postman ou outro cliente HTTP para testar os endpoints (JWT obrigatório).

## Observações
- O scraping utiliza BeautifulSoup e segue a estrutura do HTML oficial da Embrapa.
- O fallback CSV garante disponibilidade dos dados mesmo se o site estiver fora do ar.
- O projeto está preparado para extensão futura (processamento, comercialização, importação, exportação).

## Próximos passos
- Implementar endpoints de processamento, comercialização, importação e exportação.
- Documentar todos os endpoints com exemplos no Swagger.
- Preparar para deploy na Vercel.

---

Desenvolvido para fins acadêmicos e de demonstração.