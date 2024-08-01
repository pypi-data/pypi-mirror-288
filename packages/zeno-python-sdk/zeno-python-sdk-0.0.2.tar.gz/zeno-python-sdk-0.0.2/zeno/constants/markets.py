from zeno.constants.assets import (
  ASSET_ETH,
  ASSET_BTC,
  ASSET_JPY,
  ASSET_XAU,
  ASSET_EUR,
  ASSET_GBP,
  ASSET_METIS,
)


# ------ Market ------
MARKET_ETH_USD = 0
MARKET_BTC_USD = 1
MARKET_JPY_USD = 2
MARKET_XAU_USD = 3
MARKET_EUR_USD = 4
MARKET_GBP_USD = 7
MARKET_METIS_USD = 43

# ------ Market ----
MARKET_PROFILE = {
  MARKET_ETH_USD: {
    "name": "ETHUSD",
    "asset": ASSET_ETH,
    "display_decimal": 2,
  },
  MARKET_BTC_USD: {
    "name": "BTCUSD",
    "asset": ASSET_BTC,
    "display_decimal": 2,
  },
  MARKET_JPY_USD: {
    "name": "JPYUSD",
    "asset": ASSET_JPY,
    "display_decimal": 8,
  },
  MARKET_XAU_USD: {
    "name": "XAUUSD",
    "asset": ASSET_XAU,
    "display_decimal": 2,
  },
  MARKET_EUR_USD: {
    "name": "EURUSD",
    "asset": ASSET_EUR,
    "display_decimal": 5,
  },
  MARKET_GBP_USD: {
    "name": "GBPUSD",
    "asset": ASSET_GBP,
    "display_decimal": 5,
  },
  MARKET_METIS_USD: {
    "name": "METISUSD",
    "asset": ASSET_METIS,
    "display_decimal": 4,
  },
}
