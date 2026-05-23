from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf
from crewai.tools import tool

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
@tool('Get Stock Data')
def get_stock_data(ticker: str) -> str:
    """Get current price and recent news for a stock ticker."""
    stock = yf.Ticker(ticker)
    info = stock.info
    
    current_price = info.get('currentPrice', 'N/A')
    previous_close = info.get('previousClose', 'N/A')
    
    if current_price != 'N/A' and previous_close != 'N/A':
        change_pct = ((current_price - previous_close) / previous_close) * 100
        price_info = f'Price: ${current_price:.2f} ({change_pct:+.2f}%)'
    else:
        price_info = 'Price data unavailable'
        
    news = stock.news
    headlines = []        
    
    for news_item in news[:8]:
        title = news_item['content'].get('title', '').strip()
        
        if title:
            headlines.append(f'- {title}')
            
    if not headlines:
        headlines = ['- No headlines available.']
    
    news_text = '\n'.join(headlines)    

    return f'{price_info}\n\nRecent Headlines:\n{news_text}'