from web3 import Web3, Account
from zeno.constants.pricefeed import DEFAULT_PYTH_PRICE_SERVICE_URL
from zeno.constants.assets import (
    ASSET_BTC,
    ASSET_ETH,
    ASSET_USDC
)
from zeno.helpers.mapper import get_contract_address
from zeno.modules.private import Private
from zeno.modules.public import Public
from zeno.modules.oracle.pyth_oracle import PythOracle
from zeno.modules.oracle.cix_oracle import CixOracle
from zeno.modules.oracle.onchain_pricelens_oracle import OnchainPricelensOracle
from zeno.modules.oracle.oracle_middleware import OracleMiddleware
from web3.middleware import geth_poa


class Client(object):
  def __init__(self, rpc_url, eth_private_key=None, pyth_price_service_url=DEFAULT_PYTH_PRICE_SERVICE_URL):
    self.__eth_provider = Web3(Web3.HTTPProvider(
      rpc_url, request_kwargs={'timeout': 60}))
    self.__eth_provider.middleware_onion.inject(
      geth_poa.geth_poa_middleware, layer=0)
    self.__chain_id = self.__eth_provider.eth.chain_id
    if eth_private_key is not None:
      self.__eth_signer = Account.from_key(eth_private_key)

    contract_address = get_contract_address(self.__chain_id)

    pyth_oracle = PythOracle(self.__chain_id, pyth_price_service_url)
    dix_oracle = CixOracle(contract_address["DIX_PRICE_ADAPTER_ADDRESS"],
                           pyth_oracle, self.__eth_provider)
    onchain_pricelens_oracle = OnchainPricelensOracle(
      contract_address["ONCHAIN_PRICELENS_ADDRESS"], pyth_oracle, self.__eth_provider)

    self.__oracle_middleware = OracleMiddleware(
      pyth_oracle, dix_oracle, onchain_pricelens_oracle)

    self.__private = None
    self.__public = Public(
      self.__chain_id, self.__eth_provider, self.__oracle_middleware)

  @property
  def public(self):
    '''
    Get the public module, used for permissionless actions.
    Such as, get price, get funding rate, and etc.
    '''
    return self.__public

  @property
  def private(self):
    '''
    Get the private module, used for permissioned actions.
    Such as, deposit collateral, withdraw collateral, trade, etc.
    '''
    if not self.__private:
      if self.__eth_signer:
        self.__private = Private(
          self.__chain_id, self.__eth_provider, self.__eth_signer, self.__oracle_middleware)
      else:
        raise Exception("Private module requires eth_private_key")
    return self.__private
