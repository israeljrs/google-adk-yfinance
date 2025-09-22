import yfinance as yf
from google.adk.agents import Agent


def fetch_stock_info(ticker_symbol: str) -> dict:
    """Consulta o yahoo finance sobre a cotação de um ativo.

    Args:
        ticker_symbol (str): codigo do ativo que vai ser consultado.

    Returns:
        dict: status and result or error msg.
    """
    ticket = yf.Ticker(ticker_symbol)
    data = ticket.info if hasattr(ticket, "info") else {}
    if not isinstance(data, dict):
        data = {}
    return {
        "displayName": data.get("displayName")
        or data.get("shortName")
        or ticker_symbol,
        "currentPrice": data.get("currentPrice"),
        "dayLow": data.get("dayLow"),
        "dayHigh": data.get("dayHigh"),
        "recommendationKey": data.get("recommendationKey"),
    }


root_agent = Agent(
    name="query_yfinance_agent",
    model="gemini-2.0-flash",
    description=(
        "Este agente responde perguntas sobre cotação de ações usando o yahoo finance."
    ),
    instruction=(
        "Você é um assistente financeiro que consulta informações sobre ações na bolsa usando as ferramentas do yahoo finance."
    ),
    tools=[fetch_stock_info],
)
