# Python SDK for Zeno

This library is tested against Python versions 2.7, 3.4, 3.5, 3.9, and 3.11.

## Installation

This package is available on PyPI. To install run the command below:

```
$ pip install zeno-python-sdk
```

## Getting Started

The `Client` object contains two major attributes: Public and Private. As the names suggest, Public is for public functions that don't require an Ethereum private key, and Private is for functions specifically for the given key. For more comprehensive examples, please refer to the [examples](https://github.com/ZenoExchange/zeno-sdk/tree/main/examples) directory as well as the [tests](https://github.com/ZenoExchange/zeno-sdk/tree/main/tests).

### Public functions

```python
from zeno.zeno_client import Client
from zeno.constants.markets import (
  MARKET_ETH_USD,
  MARKET_METIS_USD
)

#
# Using publicly access functions
#
client = Client(
    rpc_url=RPC_URL
)
# Get oracle price, adaptive price, and price impact of a new position
# `buy` and `size` is optional
client.public.get_price(market_index=MARKET_ETH_USD, buy=Action.SELL, size=1000)
# Get market information
client.public.get_market_info(market_index=MARKET_ETH_USD)
# Get every market information
client.public.get_all_market_info()
# Get sub account in address format
client.public.get_sub_account(1)
# Get position ID
client.public.get_position_id(
  account=some_account,
  sub_account_id=some_sub_account_id,
  market_index=MARKET_ETH_USD
)
# Get position info
client.public.get_position_info(
  account=some_account,
  sub_account_id=some_sub_account_id,
  market_index=MARKET_ETH_USD
)
# Get collateral info
client.public.get_collaterals(
    account=some_account,
    sub_account_id=some_account_id
  )
# Get all position info
client.public.get_all_position_info(
  account=some_account,
  sub_account_id=[some_account_id] # optional
)
# Get active limit order info
client.public.get_active_limit_orders(
  account=some_account,
  sub_account_ids=[sub_account_id] # optional
)
# Get portfolio value
client.public.get_portfolio_value(
  account=some_account,
  sub_account_id=sub_account_id
)
# Get Equity value
client.public.get_equity(
  account=some_account,
  sub_account_id=sub_account_id
)
# Get leverage
client.public.get_leverage(
  account=some_account,
  sub_account_id=sub_account_id
)
```

### Private function

```python
from zeno.client import Client
from zeno.constants.markets import MARKET_ETH_USD
from zeno.constants.tokens import COLLATERAL_mUSDC
from zeno.enum import Action

#
# Initailized client with private key
#
client = Client(
    eth_private_key=PRIVATE_KEY,
    rpc_url=RPC_URL
)
# Get public address of the ethereum key
client.private.get_public_address()
# Deposit ETH as collateral
client.private.deposit_eth_collateral(sub_account_id=0, amount=10.123)
# Deposit ERC20 as collateral. This function will automatically
# approve CrossMarginHandler if needed.
client.private.deposit_erc20_collateral(sub_account_id=0, token_address=COLLATERAL_mUSDC, amount=100.10)
# Withdraw Collateral
client.private.withdraw_collateral(
    sub_account_id=0,
    token_address=COLLATERAL_mUSDT,
    amount=1
  )
# Create a market order
create_market_order = client.private.create_market_order(
  sub_account_id=0,
  market_index=MARKET_ETH_USD,
  buy=Action.BUY,
  size=100,
  reduce_only=False
)
print(create_market_order)
# Create a trigger order
# trigger_above_threshold = The current price must go above (if True) or below (if False)
# the trigger price in order for the order to be executed
create_order = client.private.create_trigger_order(
    sub_account_id=0,
    market_index=MARKET_ETH_USD,
    buy=Action.BUY,
    size=100,
    trigger_price=3000,
    trigger_above_threshold=False,
    reduce_only=False,
    tp_token=COLLATERAL_mUSDC,
  )
print(create_order)
# Cancel the order
cancel_order = client.private.cancel_trigger_order(
  0, create_order["data"]["intentTradeOrders"][0]["id"])
print(cancel_order)
```

## Running Tests

To run tests, you will need have to clone the repo, update .env, and run:

```
$ make test
```

Please note that to run tests, Tenderly account is required.

## License

The primary license for ZenoExchange/zeno-sdk is the MIT License, see [here](https://github.com/ZenoExchange/zeno-sdk/blob/main/LICENSE).
