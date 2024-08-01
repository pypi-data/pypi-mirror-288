from zeno.constants.tokens import TOKEN_PROFILE
from zeno.constants.contracts import CONTRACT_ADDRESS


def get_collateral_address_asset_map(chain_id: int):
  address_asset_dict = {key: value["asset"]
                        for key, value in TOKEN_PROFILE[chain_id].items()}
  return address_asset_dict


def get_collateral_address_list(chain_id: int):
  address_list = list(set(val["address"]
                      for val in TOKEN_PROFILE[chain_id].values()))
  return address_list


def get_token_profile(chain_id: int):
  return TOKEN_PROFILE[chain_id]


def get_contract_address(chain_id: int):
  return CONTRACT_ADDRESS[chain_id]
