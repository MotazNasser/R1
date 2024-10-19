import nest_asyncio
from telethon import TelegramClient, events
import uuid
import os
import asyncio
import re
from binance.client import Client

# Allow nested event loops
nest_asyncio.apply()

# Retrieve values from environment variables
api_id = int(os.environ['API_ID'])  # Your actual API ID (as an integer)
api_hash = os.environ['API_HASH']  # Your actual API Hash (keep it as a string)
bot_token = os.environ['BOT_TOKEN']  # Your actual Bot Token (keep it as a string)

# Initialize the Binance client
binance_api_key = os.environ['BINANCE_API_KEY']  # Your actual Binance API Key
binance_api_secret = os.environ['BINANCE_API_SECRET']  # Your actual Binance API Secret
binance_client = Client(binance_api_key, binance_api_secret)

async def main():
    session_name = str(uuid.uuid4())
    client = TelegramClient(session_name, api_id, api_hash)

    await client.start(bot_token=bot_token)

    print("Bot is running and listening for forwarded messages...")  # Debug message

    @client.on(events.NewMessage())
    async def handler(event):
        message_text = event.message.message
        print(f"Received forwarded message: {message_text}")  # Print received message

        await parse_trading_signal(message_text)

    await client.run_until_disconnected()

async def parse_trading_signal(message):
    print(f"Parsing signal: {message}")

    # Regular expression to parse the signal
    match = re.search(r'🤖 Buy\s+\$([\w]+)\/([\w]+)', message)
    
    if match:
        symbol = match.group(0).replace('🤖 Buy $', '').replace('🏷️', '').strip()
        trading_pair = f"{symbol.replace('/', '')}USDT"

        # Extract the entry price, stop loss, and take profits
        entry_match = re.search(r'💲Entry : ([\d.]+) - ([\d.]+)', message)
        sl_match = re.search(r'📮SL:\s+([\d.]+)', message)
        tp_matches = re.findall(r'TP\d:\s+([\d.]+)', message)

        if entry_match and sl_match:
            entry_price_high = float(entry_match.group(1))  # Upper limit of entry price
            entry_price_low = float(entry_match.group(2))  # Lower limit of entry price
            stop_loss = float(sl_match.group(1))  # Stop loss price
            quantity = 1  # Define the quantity you want to trade

            try:
                # Fetch the current market price
                current_price = float(binance_client.get_symbol_ticker(symbol=trading_pair)['price'])
                print(f"Current market price for {trading_pair}: {current_price}")

                # Check if the current price is within the defined range
                if entry_price_low <= current_price <= entry_price_high:
                    # Execute market buy order
                    order = binance_client.order_market_buy(symbol=trading_pair, quantity=quantity)
                    print(f"Buy order executed: {order}")

                    # Split the quantity for selling between TP1 and TP2
                    quantity_tp1 = quantity / 2  # Half for TP1
                    quantity_tp2 = quantity / 2  # Half for TP2

                    # Place take profit orders after the buy order
                    if len(tp_matches) >= 2:  # Ensure there are at least 2 TP levels
                        tp1_price = float(tp_matches[0])  # TP1 price
                        tp2_price = float(tp_matches[1])  # TP2 price

                        # Place limit order for TP1
                        tp1_order = binance_client.order_limit_sell(
                            symbol=trading_pair,
                            quantity=quantity_tp1,
                            price=tp1_price,
                            timeInForce='GTC'  # Good 'Til Canceled
                        )
                        print(f"Take Profit 1 order placed at {tp1_price}: {tp1_order}")

                        # Place limit order for TP2
                        tp2_order = binance_client.order_limit_sell(
                            symbol=trading_pair,
                            quantity=quantity_tp2,
                            price=tp2_price,
                            timeInForce='GTC'  # Good 'Til Canceled
                        )
                        print(f"Take Profit 2 order placed at {tp2_price}: {tp2_order}")

                    # Place a stop loss order after the buy order
                    sl_order = binance_client.order_stop_market(
                        symbol=trading_pair,
                        quantity=quantity,
                        stopPrice=stop_loss,
                    )
                    print(f"Stop Loss order placed at {stop_loss}: {sl_order}")
                else:
                    print(f"Current price {current_price} is outside the range of {entry_price_low} to {entry_price_high}. No buy order placed.")

            except Exception as e:
                print(f"Error executing order: {e}")
        else:
            print("Failed to extract entry price or stop loss.")
    else:
        print("Invalid message format for trading signal.")

if __name__ == "__main__":
    asyncio.run(main())
