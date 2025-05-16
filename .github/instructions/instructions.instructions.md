---
applyTo: '**'
---
Coding standards, domain knowledge, and preferences that AI should follow.

# GitHub Copilot - Instruções para Construção da API Embrapa Vitivinicultura

# Objetivo Geral
Construir uma API Flask com JWT e endpoints que fazem scraping dos dados da Embrapa.

# Regras Gerais
- A arquitetura deve seguir o padrão MVC simples do Flask.
- A autenticação JWT deve incluir `/register` e `/login`.
- Usar BeautifulSoup para o scraping.
- Utilizar arquivos HTML de exemplo como referência durante o desenvolvimento.
- Criar fallback para arquivos CSV em `/static_data` quando o scraping falhar.
- Cada endpoint deve ser testável via Postman.
- Código precisa estar documentado.

# Etapas de Execução
- As tarefas devem ser executadas por etapa.
- Após minha aprovação, a próxima etapa será executada.
- As etapas concluídas devem ser marcadas em um checklist no arquivo `progress_tracker.md`.

## 📌 Descrição Geral

Você foi contratado(a) para desenvolver uma **API pública REST** em **Python com Flask**, que disponibiliza os dados do site da **Embrapa Uva e Vinho** por meio de **web scraping**, respeitando a seguinte estrutura de URL:

```
http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opcao}&subopcao={subopcao?}
```

A API permitirá consultas organizadas nas seguintes categorias:

- 🟣 Produção (`opcao=opt_02`)
- 🔵 Processamento (`opcao=opt_03`)
- 🟡 Comercialização (`opcao=opt_04`)
- 🟢 Importação (`opcao=opt_05`)
- 🔴 Exportação (`opcao=opt_06`)

## 🎯 Objetivos do Projeto

- ✅ Criar uma API REST com **Python Flask**.
- ✅ Utilizar **autenticação JWT** com rotas de **register** e **login**.
- ✅ Implementar fallback via arquivos `.csv` armazenados em `./static_data` caso o site da Embrapa esteja fora do ar.
- ✅ Organizar o projeto seguindo uma arquitetura **MVC simplificada**, conforme boas práticas Flask.
- ✅ Documentar todas as rotas da API com exemplos de uso.
- ✅ Preparar para o deploy na vercel.
- ✅ Executar cada etapa **somente após aprovação manual**.

## 🔐 Autenticação

A API deve implementar JWT com as seguintes rotas:

- `POST /register`: Cadastra novo usuário.
- `POST /login`: Retorna o token de autenticação.

## 📊 Endpoints por Categoria

### 🟣 Produção

- `GET /producao`: Retorna todos os dados de 1970 a 2023.
- `GET /producao/{ano}`: Retorna dados do ano específico.

**Exemplo de scraping:**  
[http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_02](http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_02)

HTML de referência: `./exemplo_retorno_html/html_producao.html`

### 🔵 Processamento

- `GET /processamento/{ano}`: Retorna dados de todas as subopções no ano informado.
- `GET /processamento/{tipoProcessamento}/{ano}`: Retorna dados de uma subopção específica no ano.

**Exemplos de subopções:**

- VINIFERAS: `subopt_01`
- AMERICANAS E HÍBRIDAS: `subopt_02`
- UVAS DE MESA: `subopt_03`
- SEM CLASSIFICAÇÃO: `subopt_04`

[http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_03&subopcao=subopt_01](http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_03&subopcao=subopt_01)

### 🟡 Comercialização

- `GET /comercializacao`: Retorna todos os dados de 1970 a 2023.
- `GET /comercializacao/{ano}`: Retorna dados do ano específico.

[http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_04](http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2023&opcao=opt_04)

### 🟢 Importação

- `GET /importacao/{ano}`: Retorna dados de todos os derivados no ano.
- `GET /importacao/{subopcao}/{ano}`: Retorna dados de um derivado específico no ano.

**Subopções:**
- VINHO DE MESA: `subopt_01`
- ESPUMANTES: `subopt_02`
- UVAS FRESCAS: `subopt_03`
- UVAS PASSADAS: `subopt_04`
- SUCO DE UVA: `subopt_05`

[http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2024&opcao=opt_05&subopcao=subopt_01](http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2024&opcao=opt_05&subopcao=subopt_01)

### 🔴 Exportação

- `GET /exportacao/{ano}`: Retorna dados de todos os derivados no ano.
- `GET /exportacao/{subopcao}/{ano}`: Retorna dados de um derivado específico no ano.

**Subopções:**
- VINHO DE MESA: `subopt_01`
- ESPUMANTES: `subopt_02`
- UVAS FRESCAS: `subopt_03`
- SUCO DE UVA: `subopt_04`

[http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2024&opcao=opt_06&subopcao=subopt_01](http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2024&opcao=opt_06&subopcao=subopt_01)

## ⚙️ Regras de Execução e Aprovação

Este projeto será conduzido com **controle manual de etapas**. O Copilot deverá seguir o fluxo abaixo:

1. **Analisar o escopo solicitado.**
2. **Executar apenas a etapa aprovada.**
3. **Documentar em comentário claro no PR ou commit**:
   - O que foi feito.
   - Em qual etapa se encontra.
   - O que será proposto como próxima ação.
4. **Aguardar aprovação explícita da próxima tarefa.**
5. **Testar cada funcionalidade com exemplos reais ou mocks.**

### ✅ Exemplo de Registro no Commit/PR:

```
🧩 ETAPA: Implementação do endpoint /producao
🔧 STATUS: OK
🧪 TESTES: Realizados com BeautifulSoup e dados reais de 2023.
📌 PRÓXIMO PASSO: Criar fallback para arquivo CSV.
```

## 📁 Estrutura esperada

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
├── exemplo_retorno_html/
│   └── *.html
├── .env
├── requirements.txt
├── main.py
└── README.md
```

## 🚀 Deploy

O deploy final será feito na **Vercel**, com ajustes para suporte ao Flask usando o adaptador adequado (`vercel-python`).

## 📞 Suporte e Dúvidas

Para qualquer ambiguidade ou erro de scraping, o agente deverá:

- Indicar o problema.
- Sugerir solução.
- Aguardar instruções antes de continuar.

