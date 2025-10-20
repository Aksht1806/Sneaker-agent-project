# scraper.py - Simulates fetching data from retail and resell websites.

import random
from datetime import datetime, timedelta

def get_mock_price_listings():
    """
    Generates a list of fake price listings from various sources.
    In a real application, this function would use libraries like
    BeautifulSoup or Scrapy to scrape websites, or connect to official APIs.
    """
    base_price = 200 + random.randint(0, 300)
    
    sources = [
        {'name': 'StockX', 'logo': 'https://placehold.co/32x32/000000/FFFFFF?text=S', 'condition': 'New', 'size': '10.5 US', 'price': base_price + random.randint(0, 50)},
        {'name': 'GOAT', 'logo': 'https://placehold.co/32x32/4A4A4A/FFFFFF?text=G', 'condition': 'New', 'size': '10.5 US', 'price': base_price + random.randint(5, 55)},
        {'name': 'eBay', 'logo': 'https://placehold.co/32x32/E53238/FFFFFF?text=e', 'condition': 'Used (9/10)', 'size': '10.5 US', 'price': base_price - random.randint(20, 50)},
        {'name': 'Flight Club', 'logo': 'https://placehold.co/32x32/111111/FFFFFF?text=FC', 'condition': 'New', 'size': '10.5 US', 'price': base_price + random.randint(15, 60)},
    ]
    return sources

def get_mock_price_history():
    """
    Generates fake historical price data for the chart.
    In a real application, this data would come from an API like StockX's
    or be scraped and stored in your own database over time.
    """
    labels = []
    data = []
    base_price = 250 + random.randint(0, 150)
    today = datetime.now()

    for i in range(90, -1, -1):
        date = today - timedelta(days=i)
        # Format date as 'YYYY-MM-DD'
        labels.append(date.strftime('%Y-%m-%d'))
        
        # Simulate price fluctuations with a slight upward trend
        price_fluctuation = (random.random() - 0.5) * 20
        trend = (90 - i) * 0.5 
        data.append(round(base_price + price_fluctuation + trend, 2))
        
    return {'labels': labels, 'data': data}