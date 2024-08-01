from zeno.constants.assets import (
  ASSET_BTC,
  ASSET_ETH,
  ASSET_mUSDC,
  ASSET_mUSDT
)

COLLATERAL_WETH = "0x420000000000000000000000000000000000000A"
COLLATERAL_WBTC = "0xa5B55ab1dAF0F8e1EFc0eB1931a957fd89B918f4"
COLLATERAL_mUSDC = "0xEA32A96608495e54156Ae48931A7c20f0dcc1a21"
COLLATERAL_mUSDT = "0xbB06DCA3AE6887fAbF931640f67cab3e3a16F4dC"

COLLATERAL_tWETH = "0x10b154123a856dde846AB539C3dC8E6415f6F4B8"
COLLATERAL_tWBTC = "0xB5DD48bbE7d9453d53253580842e4028931eE119"
COLLATERAL_tmUSDC = "0xBbF4abea704E874886876F00Baf44544666C12BB"
COLLATERAL_tmUSDT = "0x65F0FdFffB3Bd07275CfDCE34393B765EbaB2e16"

CHAIN_COLLATERAL = {
  1088: [
      COLLATERAL_WETH,
      COLLATERAL_WBTC,
      COLLATERAL_mUSDC,
      COLLATERAL_mUSDT,
  ],
  59902: [
      COLLATERAL_tWETH,
      COLLATERAL_tWBTC,
      COLLATERAL_tmUSDC,
      COLLATERAL_tmUSDT,
  ]
}

# ------ Token Profiles ------
TOKEN_PROFILE = {
  # Metis
  1088: {
    "m.USDC": {
      "symbol": "m.USDC",
      "address": COLLATERAL_mUSDC,
      "asset": ASSET_mUSDC,
      "decimals": 6
    },
    COLLATERAL_mUSDC: {
      "symbol": "m.USDC",
      "address": COLLATERAL_mUSDC,
      "asset": ASSET_mUSDC,
      "decimals": 6
    },
    "m.USDT": {
      "symbol": "m.USDT",
      "address": COLLATERAL_mUSDT,
      "asset": ASSET_mUSDT,
      "decimals": 6
    },
    COLLATERAL_mUSDT: {
      "symbol": "m.USDT",
      "address": COLLATERAL_mUSDT,
      "asset": ASSET_mUSDT,
      "decimals": 6
    },
      "WETH": {
        "symbol": "WETH",
        "address": COLLATERAL_WETH,
        "asset": ASSET_ETH,
        "decimals": 18
    },
      COLLATERAL_WETH: {
        "symbol": "WETH",
        "address": COLLATERAL_WETH,
        "asset": ASSET_ETH,
        "decimals": 18
    },
      "WBTC": {
        "symbol": "WBTC",
        "address": COLLATERAL_WBTC,
        "asset": ASSET_BTC,
        "decimals": 8
    },
      COLLATERAL_WBTC: {
        "symbol": "WBTC",
        "address": COLLATERAL_WBTC,
        "asset": ASSET_BTC,
        "decimals": 8
    },
  },
  59902: {
    "m.USDC": {
      "symbol": "m.USDC",
      "address": COLLATERAL_tmUSDC,
      "asset": ASSET_mUSDC,
      "decimals": 6
    },
    COLLATERAL_tmUSDC: {
      "symbol": "m.USDC",
      "address": COLLATERAL_tmUSDC,
      "asset": ASSET_mUSDC,
      "decimals": 6
    },
    "m.USDT": {
      "symbol": "m.USDT",
      "address": COLLATERAL_tmUSDT,
      "asset": ASSET_mUSDT,
      "decimals": 6
    },
    COLLATERAL_tmUSDT: {
      "symbol": "m.USDT",
      "address": COLLATERAL_tmUSDT,
      "asset": ASSET_mUSDT,
      "decimals": 6
    },
      "WETH": {
        "symbol": "WETH",
        "address": COLLATERAL_tWETH,
        "asset": ASSET_ETH,
        "decimals": 18
    },
      COLLATERAL_tWETH: {
        "symbol": "WETH",
        "address": COLLATERAL_tWETH,
        "asset": ASSET_ETH,
        "decimals": 18
    },
      "WBTC": {
        "symbol": "WBTC",
        "address": COLLATERAL_tWBTC,
        "asset": ASSET_BTC,
        "decimals": 8
    },
      COLLATERAL_tWBTC: {
        "symbol": "WBTC",
        "address": COLLATERAL_tWBTC,
        "asset": ASSET_BTC,
        "decimals": 8
    },
  }
}
