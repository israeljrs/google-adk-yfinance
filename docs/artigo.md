# Google ADK + YFinance em Python: construindo um agente para consultar cotações de ações

![Screenshot – Google ADK + YFinance](images/google-adk.png)

## Resumo
Este artigo apresenta um agente construído com o Google ADK (Agent Development Kit) que consulta cotações de ações via YFinance. O agente expõe a ferramenta `fetch_stock_info` para responder perguntas sobre preço atual, mínima/máxima do dia e recomendação, usando o modelo Gemini. Abaixo estão a arquitetura, o passo a passo de configuração e execução, além de ideias de evolução.

## Por que este projeto
- Acessar cotações de forma conversacional com contexto.
- Integrar modelos Gemini a uma fonte de dados prática (Yahoo Finance via YFinance).
- Demonstrar como publicar ferramentas Python em um agente com o Google ADK.

## Arquitetura
- **Agente**: `query_yfinance_agent` (modelo `gemini-2.0-flash`), definido em `query-yfinance/agent.py`.
- **Ferramenta**: `fetch_stock_info(ticker_symbol: str)`, que usa `yfinance` para buscar:
  - `displayName` (ou `shortName`)
  - `currentPrice`
  - `dayLow`
  - `dayHigh`
  - `recommendationKey`
- **Orquestração**: Google ADK aciona o modelo e decide quando chamar a ferramenta com base no prompt do usuário.
- **Configuração**: variáveis em `query-yfinance/.env` (carregadas automaticamente pelo ADK).

## Código-chave
Arquivo `query-yfinance/agent.py`:
- Ferramenta de consulta:
  - Recebe `ticker_symbol` (ex.: `PETR4.SA`, `AAPL`).
  - Usa `yfinance.Ticker(...).info` e retorna um dicionário com campos úteis.
- Agente ADK:
  - Define `name`, `model`, `description` e `instruction`.
  - Registra a ferramenta em `tools=[fetch_stock_info]`.

## Pré-requisitos
- Python `>= 3.12`.
- Chave de API do Google Generative AI (para a API pública): variável `GOOGLE_API_KEY`.
- Opcional: Vertex AI (com `GOOGLE_GENAI_USE_VERTEXAI=TRUE` + credenciais GCP).

## Instalação
Com `uv` (recomendado):
1. Instale o `uv`: https://docs.astral.sh/uv/
2. No diretório do projeto, rode `uv sync`.
3. Ative o ambiente: `source .venv/bin/activate`.

Com `pip`:
1. Crie e ative o venv: `python3.12 -m venv .venv && source .venv/bin/activate`
2. Atualize o pip: `pip install -U pip`
3. Instale o projeto: `pip install -e .`

As dependências principais estão em `pyproject.toml`: `google-adk` e `yfinance`.

## Configuração
1. Copie o exemplo de variáveis: `cp query-yfinance/.env-sample query-yfinance/.env`
2. Edite `query-yfinance/.env`:
   - `GOOGLE_API_KEY=...` (quando não usa Vertex)
   - `GOOGLE_GENAI_USE_VERTEXAI=FALSE` (ou `TRUE` + `gcloud auth application-default login` + exporte `GOOGLE_CLOUD_PROJECT` e `GOOGLE_CLOUD_REGION`)

Observação: o ADK lê o `.env` da pasta do agente; mantenha-o em `query-yfinance/`.

## Execução (CLI)
1. Ative o venv.
2. Rode `adk run query-yfinance`.
3. Exemplos de perguntas:
   - “Qual o preço atual de `PETR4.SA`?”
   - “Mostre a mínima e a máxima do dia para `AAPL`.”

Exemplos de tickers:
- Brasil (B3): `PETR4.SA`, `VALE3.SA` (note o sufixo `.SA`).
- EUA: `AAPL`, `GOOGL`, `MSFT`.

## Fluxo em tempo de execução
1. Você conversa com o agente no terminal.
2. O modelo Gemini interpreta a intenção e decide chamar `fetch_stock_info` com o ticker.
3. A ferramenta usa YFinance e retorna os campos.
4. O agente compõe uma resposta natural com os dados retornados.

## Tratamento de erros e limitações
- **Ticker inválido**: YFinance pode retornar dados incompletos; o agente ainda responde com o nome/ticker fornecido.
- **Campos ausentes**: nem todos os ativos possuem `currentPrice`/`recommendationKey`; o código já lida com `dict` vazio.
- **Rede/limites**: YFinance depende do Yahoo Finance e pode falhar temporariamente; tente novamente.
- **Precisão e atraso**: dados são de terceiros e podem ter latência; valide antes de decisões financeiras.

## Evoluções sugeridas
- **Formatação**: incluir moeda, variação intradiária e horário do último preço.
- **Validação**: sugerir automaticamente o sufixo `.SA` para tickers brasileiros.
- **Cache**: TTL curto para reduzir chamadas repetidas ao YFinance.
- **Multitool**: adicionar histórico (`history`) e cálculos (médias móveis, volatilidade).
- **Observabilidade**: logs estruturados e métricas de chamadas por ticker.
- **i18n**: respostas em PT/EN conforme preferência do usuário.

## Estrutura do repositório
- `query-yfinance/agent.py`: agente e ferramenta `fetch_stock_info`.
- `query-yfinance/.env-sample`: exemplo de variáveis.
- `README.md`: guia rápido.
- `pyproject.toml`: metadados e dependências.

## Conclusão
Com poucas linhas de código e o Google ADK, integramos um modelo Gemini a uma fonte de dados financeira prática (YFinance), criando um agente conversacional que responde consultas de mercado. A abordagem é extensível: novas ferramentas podem ser adicionadas para enriquecer análises, histórico e formatação de relatórios.
