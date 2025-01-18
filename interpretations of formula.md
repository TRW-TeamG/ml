`trade_winrate` is the `trading_pnl` divided by `realized_pnl` and `unrealized`. 

`nft_pnl` is the `trading_pnl` divided by `realized_pnl` and `unrealized`. 
If winrate is high but profit loss is ratio is low then that means you're taking larger losses that can wipe out small wins
reocmmendation: setting hgiher risk reward target. using trailing stops, not holding long enough. If profit loss ratio is higher than winrate, it could be that you're making big gains. but you might be taking smaller losses

`liquidity_ratio` calculated as  total number of active trades / total number of trades. The higher the ratio, the more locked capital you have. This means that more capital is tied up in your positions, which will reduce your trading capital. This can be a good thing if you are using a conservative risk management strategy, but it can also be a bad thing if you are using a more aggressive strategy.

`porp_success_trades` is the `number_of_closed_trades` divided by the `total_number_of_trades` multiplied by `trade_winrate`. This is a measure of how succesful you are at closing trades.This is important because if `porportion of successful trades` is low, it means that you are not closing trades as often as you should be. Or, it can also mean youre trading in illiquid markets and high volatility markets. Recommended to increase slippage