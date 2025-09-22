# Usage Demo (Terminal Transcript)

Below is a sample terminal transcript showing how the agent behaves. You can use this as a guide to capture your own screenshots while running locally.

## How to run
1. Activate your environment: `source .venv/bin/activate`
2. Start the agent: `adk run query-yfinance`

## Example session
```
$ adk run query-yfinance
Starting agent: query_yfinance_agent (model: gemini-2.0-flash)
Type 'exit' to quit.

> User: What's the current price of AAPL?
[tool] fetch_stock_info called with: ticker_symbol='AAPL'
[tool] result: {
  "displayName": "Apple Inc.",
  "currentPrice": ...,
  "dayLow": ...,
  "dayHigh": ...,
  "recommendationKey": ...
}

Assistant: Apple's current price is ... .
Intraday range: low ... / high ... .
Analyst recommendation: ... .

> User: Show PETR4 on B3.
[tool] fetch_stock_info called with: ticker_symbol='PETR4.SA'
[tool] result: {
  "displayName": "Petrobras PN",
  "currentPrice": ...,
  "dayLow": ...,
  "dayHigh": ...,
  "recommendationKey": ...
}

Assistant: PETR4.SA is trading at ... .
Day low ... / day high ... .
Recommendation: ... .

> exit
Goodbye!
```

Notes:
- Replace `...` with actual values when capturing screenshots.
- For Brazilian tickers, remember the `.SA` suffix (e.g., `VALE3.SA`).

