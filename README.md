# Limit-Order-Book-and-Market-Making-Simulator
Project 9 for CS 193

**Project Goal 
**
This fall at a club's final interview, we simulated a market with a deck of cards and took turns as market makers, and I realized I didn't really understand how markets match buyers and sellers or how a market maker decides on prices. This project is a way to simulate that and learn about more about these mechanics. 

**How it works:
**
- Traders submit bids (to buy) and asks (to sell), each with a price and quantity
- Orders that can't be traded right away wait in the order book, sorted by price.
- Whenever a bid's price is greater than or equal to an ask's price, the matching engine will execute the trade
- Every trade is logged to a csv file

MVP Scope
Includes:
- Order and Trade classes representing orders
- Order book that stores bids and asks
- Matching engine with price-time priority and able to handle partial buy/sell orders
- Order cancellation
- Trade log saved to trades.csv
- Terminal interface
- Some sort of tests

Future Plans:
- Automated traders that send randomized orders so the market moves on its own
- Market making bot that continously quotes both a bid and an ask around the mid price
- Analytics on trade history and the bot's profit and inventory with charts

Tech Stack:
- Python
- Libraries: csv, dataclasses, datetime, random
- Possible Libraries: rich (terminal display), matplotlib (charts)
- Data Storage: local
- External Data Sources: None
