from trade import RaydiumTrade

if __name__ == "__main__":
    
    token_address = '5Jok1oYYTLkXwK975W4CTCHtU4QmoM2bxW1SvTbHpump'
    
    trader = RaydiumTrade(
        token_address=token_address,  # The address of the token to be traded
        sol_in=.25,  # The amount of SOL to be used for buying the token
        target_percent=10,  # The percentage gain at which the token should be sold (target profit)
        stop_loss_percent=50,  # The percentage loss at which the token should be sold (stop loss)
        slippage=5,  # The slippage tolerance percentage
        percentage=100,  # The percentage of the token balance to sell (100% means sell everything)
        refresh=3 # Check token price every X seconds
    )
    
    # Start the trading process
    trader.start()
    
    # Ctrl + C to exit the trade
    