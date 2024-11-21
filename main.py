from telethon import TelegramClient, events
import re
import asyncio
from trade import RaydiumTrade
from config import API_HASH, API_ID, PHONE_NUMBER, CHANNEL_CHAT_ID  # Assuming these are in config.py

# Initialize the Telegram client
client = TelegramClient('my_session', API_ID, API_HASH)

# Regex patterns for detecting buy messages and extracting contract addresses
buy_message_pattern = re.compile(r"🪙 .+\(\$[A-Z]+\)")
contract_address_pattern = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")

# Store the active trader instance
active_trader = None

# Define the function to initialize and start trading
def start_trader(token_address):
    global active_trader

    print(f"Starting trade for token: {token_address}")

    # Configure the RaydiumTrader instance
    active_trader = RaydiumTrade(
        token_address=token_address,
        sol_in=0.03,  # The amount of SOL to use for buying
        target_percent=20,  # The target profit percentage
        stop_loss_percent=20,  # The stop-loss percentage
        slippage=20,  # Slippage tolerance
        percentage=100,  # Sell 100% of the token balance
        refresh=3  # Price refresh interval in seconds
    )

    try:
        # Start trading
        active_trader.start()
        print(f"Trader successfully started for token: {token_address}")
    except Exception as e:
        print(f"❌ Trading failed for token: {token_address}. Error: {e}")
    finally:
        # Reset active_trader regardless of success or failure
        active_trader = None
        print(f"Trader reset for token: {token_address}")

# Define an event handler for new messages
@client.on(events.NewMessage)
async def handler(event):
    global active_trader

    chat_id = event.chat_id

    # Check if the message is from the specified channel
    if chat_id == CHANNEL_CHAT_ID:
        message = event.raw_text

        # Match buy messages
        if buy_message_pattern.search(message):
            print(f"New BUY message detected: {message}")

            # Extract the contract address
            contract_address = contract_address_pattern.search(message)
            if contract_address:
                contract_address = contract_address.group()
                print(f"Extracted token address: {contract_address}")

                # Start trading if no trader is active
                if active_trader is None:
                    start_trader(contract_address)
                else:
                    print("A trader is already active. Ignoring new token.")
            else:
                print("No valid token address found in the message.")
        else:
            print("Ignoring non-buy message.")
    else:
        print("Message from an unknown source. Ignoring...")

# Main function to start the Telegram client
async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Listening for buy messages from the specified channel...")
    await client.run_until_disconnected()

# Run the main function
if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nExiting...")
        if active_trader:
            active_trader.stop()  # Gracefully stop the trader if running
