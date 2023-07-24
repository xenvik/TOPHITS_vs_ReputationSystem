import numpy as np
from scipy.stats import kendalltau

# Suppose you have two rankings obtained from the reputation and TOPHITS methods
reputation_ranking = ['jack', 'elonmusk', 'michael_saylor', 'apompliano', 'cynthiamlummis', 'brian_armstrong', 'vitalikbuterin', 'udiwertheimer',
                      'bustarhymes', 'nayibbukele', 'coinbase', 'bitcoinmagazine', 'danheld', 'twobitidiot', 'balajis', 'nic__carter', 'lopp', 'sentoomey',
                      'cryptocobain', '0xpolygon', 'ftx_official', 'solana', 'cz_binance', 'prestonpysh', 'twitter', 'iohk_charles', 'peterschiff',
                      'petermccormack', 'jackmallers', 'ronwyden', 'uniswap', 'axieinfinity', 'sbf_alameda', 'krakenfx', 'novogratz', '3lau', 'wclementeiii',
                      'woonomic', 'erikvoorhees', 'cathiedwood', 'rleshner', 'documentingbtc', 'gladstein', 'zackvoell', 'microstrategy', 'chivowallet',
                      'bitcoinbeach', 'garygensler', 'saifedean', 'adam3us', 'coindesk', 'binance', 'garyvee', 'lootproject', 'yieldguild', 'sushiswap',
                      'coinmarketcap', 'thecryptodog', 'makerdao', 'arbitrum', 'opensea', 'reddit', 'thorchain', 'francissuarez', 'cashapp', 'banklesshq',
                      'blockfi', 'cnbc', 'zhusu', 'josephdelong', 'bitcoinzay', 'maxkeiser', 'dylanleclair_']  # Replace with the actual rankings
tophits_ranking = ['mcshane_writes', 'ethereumJoseph', 'ethereum', 'Bitcoin', 'adam3us', 'ethhub_io', 'NeerajKA', 'BitcoinMagazine', 'CoinDesk', 'iamjosephyoung',
                   'cointelegraphzn', 'todayindefi', 'AndreCronje123', 'OurNetwork__', 'maxkeiser', 'BTCTN', '0xpolygon', 'shapeshift_io', 'coindanslecoin',
                   'defipulse', 'jamiecrawleycd', 'coinmetrics', 'grayscale', 'zhusu', 'tanzeel_akhtar', 'Unchained_pod', 'liquid_btc', 'cryptocom', 'thorchain',
                   'solana', 'novogratz', 'naval', 'bitfinex', 'krakenfx', 'WeekInEthNews', 'elonmusk', 'NischalShetty', 'brian_armstrong', 'aantonop', 'iohk_charles',
                   'godbole17', 'nayibbukele', 'DefiantNews', 'real_vijay', 'coingecko', 'CoinMarketCap', 'by_defi', 'noshitcoins', 'orangepillpod', 'coindeskmarkets',
                   'stacks', '100trillionusd', 'namcios', 'muneeb', 'blockworks_', 'lawmaster', 'mcuban', 'binance', 'cz_binance', 'dylanleclair_', 'barrysilbert',
                   'pete_rizzo_', 'Cointelegraph', 'blockstream', 'saylor', 'APompliano', 'coinbase', 'ErikVoorhees', 'lopp', 'danheld', 'RaoulGMI', 'VitalikButerin',
                   'SatoshiLite']  # Replace with the actual rankings

# Create a dictionary to map channel names to their ranks in each ranking
reputation_ranks = {channel: rank + 1 for rank, channel in enumerate(reputation_ranking)}
tophits_ranks = {channel: rank + 1 for rank, channel in enumerate(tophits_ranking)}

# Create a list of ranks for each channel in both rankings
reputation_ranks_list = [reputation_ranks.get(channel, len(reputation_ranking) + 1) for channel in tophits_ranking]
tophits_ranks_list = [tophits_ranks.get(channel, len(tophits_ranking) + 1) for channel in tophits_ranking]

# Calculate Kendall rank correlation
correlation, p_value = kendalltau(reputation_ranks_list, tophits_ranks_list)

# Print the correlation coefficient and p-value
print("Kendall Rank Correlation:", correlation)
print("p-value:", p_value)

# Interpretation of the correlation value:
# - A positive correlation (close to 1) indicates that the rankings are similar.
# - A negative correlation (close to -1) indicates that the rankings are dissimilar.
# - A correlation close to 0 indicates no strong relationship between the rankings.
# - The p-value indicates the statistical significance of the correlation.
#   A small p-value (e.g., p < 0.05) suggests a significant correlation.

