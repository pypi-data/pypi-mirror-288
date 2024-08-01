from zeno.modules.oracle.pyth_oracle import PythOracle
from zeno.modules.oracle.cix_oracle import CixOracle
from zeno.modules.oracle.onchain_pricelens_oracle import OnchainPricelensOracle
from zeno.constants.assets import (
  ASSETS,
  ASSET_USDCe,
  ASSET_DIX,
  ASSET_JPY,
  ASSET_1000PEPE,
  ASSET_1000SHIB
)
from typing import List


class OracleMiddleware(object):
  def __init__(self, pyth_oracle: PythOracle, dix_oracle: CixOracle, onchain_pricelens_oracle: OnchainPricelensOracle):
    self.pyth_oracle = pyth_oracle
    self.dix_oracle = dix_oracle
    self.onchain_pricelens_oracle = onchain_pricelens_oracle

  def get_price(self, asset_id: str):
    '''
    Get the latest price of the asset.

    :param asset_id: required
    :type asset_id: str in list ASSET_IDS
    '''
    if asset_id not in ASSETS:
      raise Exception('Invalid asset_id')

    if asset_id == ASSET_DIX:
      return self.dix_oracle.get_price(asset_id)

    if asset_id in [ASSET_1000PEPE, ASSET_1000SHIB]:
      return self.pyth_oracle.get_price(asset_id) * 1000

    if asset_id in [ASSET_JPY]:
      return 1 / self.pyth_oracle.get_price(asset_id)

    return self.pyth_oracle.get_price(asset_id)

  def get_multiple_price(self, asset_ids: List[str]):

    price_object = {}

    if set(asset_ids) - set(ASSETS):
      raise Exception('Invalid asset_ids')

    if ASSET_DIX in asset_ids:
      price_object[ASSET_DIX] = self.dix_oracle.get_price(ASSET_DIX)
      asset_ids.remove(ASSET_DIX)

    raw_prices = self.pyth_oracle.get_multiple_price(asset_ids)

    for index, asset_id in enumerate(asset_ids):
      if asset_id in [ASSET_1000PEPE, ASSET_1000SHIB]:
        price_object[asset_id] = raw_prices[index] * 1000

      elif asset_id in [ASSET_JPY]:
        price_object[asset_id] = 1 / raw_prices[index]

      else:
        price_object[asset_id] = raw_prices[index]

    return price_object
