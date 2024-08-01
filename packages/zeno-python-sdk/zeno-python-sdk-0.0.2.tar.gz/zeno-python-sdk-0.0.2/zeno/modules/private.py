from eth_abi.packed import encode_packed
from eth_keys import keys
from web3 import Web3, Account
from web3.middleware.signing import construct_sign_and_send_raw_middleware
from zeno.constants.contracts import (
  CROSS_MARGIN_HANDLER_ABI_PATH,
  LIMIT_TRADE_HANDLER_ABI_PATH,
  VAULT_STORAGE_ABI_PATH,
  PERP_STORAGE_ABI_PATH,
  CONFIG_STORAGE_ABI_PATH,
  ERC20_ABI_PATH,
  CALCULATOR_ABI_PATH
)
from zeno.constants.common import (
  ADDRESS_ZERO,
  DAYS,
  EXECUTION_FEE,
  BPS,
  MAX_UINT54,
  MINUTES
)
from zeno.constants.intent import (
  INTENT_TRADE_API,
)
from eth_account import Account

from eth_account.messages import encode_typed_data, encode_defunct
from time import time
from zeno.helpers.contract_loader import load_contract
from simple_multicall_v6 import Multicall
from zeno.helpers.mapper import (
  get_contract_address,
  get_token_profile,
  get_collateral_address_asset_map,
  get_collateral_address_list
)
from zeno.helpers.util import check_sub_account_id_param, from_number_to_e30, int_to_byte32
from zeno.modules.oracle.oracle_middleware import OracleMiddleware
import decimal
import math
import requests as r
import json

decimal.getcontext().prec = 15
decimal.getcontext().rounding = "ROUND_HALF_DOWN"


class Private(object):

  def __init__(self, chain_id: int, eth_provider: Web3,
               eth_signer: Account, oracle_middleware: OracleMiddleware):
    self.chain_id = chain_id
    self.eth_provider = eth_provider
    self.eth_signer = eth_signer
    self.oracle_middleware = oracle_middleware
    self.eth_provider.middleware_onion.add(
      construct_sign_and_send_raw_middleware(self.eth_signer))
    self.contract_address = get_contract_address(chain_id)
    self.collateral_address_asset_map = get_collateral_address_asset_map(
      chain_id)
    self.collateral_address_list = get_collateral_address_list(chain_id)
    self.token_profile = get_token_profile(chain_id)
    self.intent_trade_api = INTENT_TRADE_API[chain_id]
    # load contract
    self.limit_trade_handler_instance = load_contract(
      self.eth_provider, self.contract_address["LIMIT_TRADE_HANDLER_ADDRESS"], LIMIT_TRADE_HANDLER_ABI_PATH)
    self.perp_storage_instance = load_contract(
      self.eth_provider, self.contract_address["PERP_STORAGE_ADDRESS"], PERP_STORAGE_ABI_PATH)
    self.config_storage_instance = load_contract(
      self.eth_provider, self.contract_address["CONFIG_STORAGE_ADDRESS"], CONFIG_STORAGE_ABI_PATH)
    self.vault_storage_instance = load_contract(
      self.eth_provider, self.contract_address["VAULT_STORAGE_ADDRESS"], VAULT_STORAGE_ABI_PATH)
    self.cross_margin_handler_instance = load_contract(
      self.eth_provider, self.contract_address["CROSS_MARGIN_HANDLER_ADDRESS"], CROSS_MARGIN_HANDLER_ABI_PATH)
    self.calculator_instance = load_contract(
      self.eth_provider, self.contract_address["CALCULATOR_ADDRESS"], CALCULATOR_ABI_PATH
    )
    self.multicall_instance = Multicall(w3=self.eth_provider,
                                        custom_address=self.contract_address["MULTICALL_ADDRESS"])

  def deposit_erc20_collateral(self, sub_account_id: int, token_address: str, amount: float):
    '''
    Deposit ERC20 token as collateral.

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param token_address: required
    :type token_address: str in list COLLATERALS

    :param amount: required
    :type amount: float
    '''
    if token_address not in self.collateral_address_list:
      raise Exception("Invalid collateral address")
    check_sub_account_id_param(sub_account_id)

    amount_wei = int(
      amount * 10 ** self.token_profile[token_address]["decimals"])
    token_instance = load_contract(
      self.eth_provider, token_address, ERC20_ABI_PATH)

    CROSS_MARGIN_HANDLER_ADDRESS = self.contract_address["CROSS_MARGIN_HANDLER_ADDRESS"]

    allowance = token_instance.functions.allowance(
        self.eth_signer.address, CROSS_MARGIN_HANDLER_ADDRESS).call()
    if allowance < amount_wei:
      tx = token_instance.functions.approve(
          CROSS_MARGIN_HANDLER_ADDRESS, amount_wei).transact({"from": self.eth_signer.address, "gasPrice": self.eth_provider.eth.gas_price})
      self.eth_provider.eth.wait_for_transaction_receipt(tx)

    return self.cross_margin_handler_instance.functions.depositCollateral(
      sub_account_id,
      token_address,
      amount_wei,
      False
    ).transact({"from": self.eth_signer.address, "gasPrice": self.eth_provider.eth.gas_price})

  def withdraw_collateral(self, sub_account_id: int, token_address: str, amount: float, wrap: bool = False):
    '''
    Withdraw ERC20 token as collateral.

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param token_address: required
    :type token_address: str in list COLLATERALS

    :param amount: required
    :type amount: float
    '''
    if token_address not in self.collateral_address_list:
      raise Exception("Invalid collateral address")
    check_sub_account_id_param(sub_account_id)
    wrap = wrap if self.token_profile[token_address]['symbol'] == "WETH" else False

    amount_wei = int(
      amount * 10 ** self.token_profile[token_address]["decimals"])

    return self.cross_margin_handler_instance.functions.createWithdrawCollateralOrder(
      sub_account_id,
      token_address,
      amount_wei,
      EXECUTION_FEE,
      wrap
    ).transact({"value": EXECUTION_FEE, "from": self.eth_signer.address, "gasPrice": self.eth_provider.eth.gas_price})

  def deposit_eth_collateral(self, sub_account_id: int, amount: float):
    '''
    Deposit ETH as collateral.

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param amount: required
    :type amount: float
    '''
    check_sub_account_id_param(sub_account_id)

    amount_wei = int(amount * 10 ** 18)

    eth_token = self.token_profile['WETH']['address']

    return self.cross_margin_handler_instance.functions.depositCollateral(
      sub_account_id,
      eth_token,
      amount_wei,
      True
    ).transact({"from": self.eth_signer.address, "value": amount_wei})

  def create_market_order(self, sub_account_id: int, market_index: int, buy: bool, size: float, reduce_only: bool, tp_token: str = ADDRESS_ZERO):
    '''
    Post a market order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param market_index: required
    :type market_index: int in list MARKET

    :param buy: required
    :type buy: bool

    :param size: required
    :type size: float

    :param reduce_only: required
    :type reduce_only: bool

    :param tp_token
    :type tp_token: str in list COLLATERALS address
    '''
    check_sub_account_id_param(sub_account_id)
    return self.__create_intent_trade_order(sub_account_id, market_index, buy, size, reduce_only, tp_token)

  def create_trigger_order(self, sub_account_id: int, market_index: int, buy: bool, size: float, trigger_price: float, trigger_above_threshold: bool, reduce_only: bool, tp_token: str = ADDRESS_ZERO, expire_time: int = 30 * DAYS):
    '''
    Post a trigger order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param market_index: required
    :type market_index: int in list MARKET

    :param buy: required
    :type buy: bool

    :param size: required
    :type size: float

    :param trigger_price: required
    :type trigger_price: float

    :param trigger_above_threshold: required
    :type trigger_above_threshold: bool

    :param reduce_only: required
    :type reduce_only: bool

    :param tp_token
    :type tp_token: str in list COLLATERALS address
    '''
    check_sub_account_id_param(sub_account_id)
    return self.__create_intent_trigger_order(sub_account_id, market_index, buy, size, trigger_price, trigger_above_threshold, reduce_only, expire_time, tp_token)

  def cancel_trigger_order(self, sub_account_id: int, market_index: int, order_index: int):
    '''
    Cancel a trigger order

    :param sub_account_id: required
    :type sub_account_id: int between 0 and 255

    :param order_index: required
    :type order_index: int
    '''

    return self.__cancel_intent_trade_order(market_index, order_index)

  def __add_slippage(self, value: float):
    return decimal.Decimal(value) * (BPS + 25) / BPS

  def __sub_slippage(self, value: float):
    return decimal.Decimal(value) * (BPS - 25) / BPS

  def __create_intent_trigger_order(self, sub_account_id: int, market_index: int, buy: bool, size: float, trigger_price: float, trigger_above_threshold: bool, reduce_only: bool, expire_time: int, tp_token: str = ADDRESS_ZERO):
    created_timestamp = math.floor(time())
    expired_timestamp = created_timestamp + expire_time

    acceptable_price = self.__add_slippage(
      trigger_price) if buy else self.__sub_slippage(trigger_price)
    acceptable_price = from_number_to_e30(acceptable_price)

    trigger_price = from_number_to_e30(trigger_price)

    # trunc to e8
    size = from_number_to_e30(size)

    json_body = json_body = self.__encode_and_build_trade_order(
      market_index, size, buy, trigger_price, acceptable_price, trigger_above_threshold, reduce_only, tp_token, created_timestamp, expired_timestamp, sub_account_id)

    return self.__upsert_intent_trade_orders_api(json_body)

  def __create_intent_trade_order(self, sub_account_id: int, market_index: int, buy: bool, size: float, reduce_only: bool, tp_token: str = ADDRESS_ZERO):
    created_timestamp = math.floor(time())
    expired_timestamp = created_timestamp + 5 * MINUTES

    acceptable_price = MAX_UINT54 if buy else 0
    trigger_price = 0

    # trunc to e8
    size = from_number_to_e30(size)

    json_body = self.__encode_and_build_trade_order(
      market_index, size, buy, trigger_price, acceptable_price, True, reduce_only, tp_token, created_timestamp, expired_timestamp, sub_account_id)

    return self.__upsert_intent_trade_orders_api(json_body)

  def __upsert_intent_trade_orders_api(self, req):
    return r.post(f'{self.intent_trade_api}/v1/intent-handler/orders.upsert', headers={'Content-Type': 'application/json'}, data=req)

  def __encode_and_build_trade_order(self, market_index: int, size: int, buy: bool, trigger_price: int, acceptable_price: int, trigger_above_threshold: bool, reduce_only: bool, tp_token: str, created_timestamp: int, expired_timestamp: int, sub_account_id: int):
    full_message = {
      "domain": {
        "name": "IntentHander",
        "version": "1.0.0",
        "chainId": self.chain_id,
        "verifyingContract": get_contract_address(self.chain_id)['INTENT_HANDLER_ADDRESS']
      },
      "types": {
        "TradeOrder": [
          {"name": "marketIndex", "type": "uint256"},
          {"name": "sizeDelta", "type": "int256"},
          {"name": "triggerPrice", "type": "uint256"},
          {"name": "acceptablePrice", "type": "uint256"},
          {"name": "triggerAboveThreshold", "type": "bool"},
          {"name": "reduceOnly", "type": "bool"},
          {"name": "tpToken", "type": "address"},
          {"name": "createdTimestamp", "type": "uint256"},
          {"name": "expiryTimestamp", "type": "uint256"},
          {"name": "account", "type": "address"},
          {"name": "subAccountId", "type": "uint8"}
        ]
      },
      "primaryType": "TradeOrder",
      "message": {
        "marketIndex": market_index,
        "sizeDelta": str(size if buy else size * -1),
        "triggerPrice": str(trigger_price),
        "acceptablePrice": str(acceptable_price),
        "triggerAboveThreshold": trigger_above_threshold,
        "reduceOnly": reduce_only,
        "tpToken": tp_token,
        "createdTimestamp": created_timestamp,
        "expiryTimestamp": expired_timestamp,
        "account": self.eth_signer.address,
        "subAccountId": sub_account_id
      }
    }

    encoded_data = encode_typed_data(full_message=full_message)

    sign_data = Account.sign_message(encoded_data, self.eth_signer.key)

    signature = encode_packed(['bytes32', 'bytes32', 'uint8'], [
        int_to_byte32(sign_data.r), int_to_byte32(sign_data.s), sign_data.v])

    pk = keys.PrivateKey(self.eth_signer.key)

    pubkey = pk.public_key

    str_pubkey = str(pubkey)

    # convert to secp256k1 format
    pubkey_ser = str_pubkey[:2] + "04" + str_pubkey[2:]

    req_body = {
      "chainId": self.chain_id,
      "intentTradeOrders": [
        {
          "marketIndex": market_index,
          "sizeDeltaE30": str(size if buy else size * -1),
          "triggerPriceE30": str(trigger_price),
          "acceptablePriceE30": str(acceptable_price),
          "triggerAboveThreshold": trigger_above_threshold,
          "reduceOnly": reduce_only,
          "tpToken": tp_token,
          "createdTimestamp": created_timestamp,
          "expiryTimestamp": expired_timestamp,
          "account": self.eth_signer.address,
          "subAccountId": sub_account_id,
          "signature": "0x" + signature.hex(),
          "digest": sign_data.messageHash.hex(),
          "publicKey": pubkey_ser,
        }
      ]
    }
    json_body = json.dumps(req_body)

    return json_body

  def get_public_address(self):
    '''
    Get the public address of the signer.
    '''
    return self.eth_signer.address

  def __encode_and_build_cancel_trade_order(self, market_index: int, order_index: int, created_timestamp: int):
    order_key = self.__get_order_key_from_order_index(order_index)
    raw_message = f'Cancel_{order_key}_{created_timestamp}'

    encoded_message = encode_defunct(text=raw_message)
    pk = keys.PrivateKey(self.eth_signer.key)
    pubkey = pk.public_key

    str_pubkey = str(pubkey)

    # convert to secp256k1 format
    pubkey_ser = str_pubkey[:2] + "04" + str_pubkey[2:]
    sign_data = Account.sign_message(
      encoded_message, pk)

    signature = encode_packed(['bytes32', 'bytes32', 'uint8'], [
        int_to_byte32(sign_data.r), int_to_byte32(sign_data.s), sign_data.v])

    cancel_order = {
      "id": order_index,
      "marketIndex": market_index,
      "cancelOrderSignature": "0x" + signature.hex(),
      "cancelTimestamp": created_timestamp,
      "publicKey": pubkey_ser,
      "_rawMessage": raw_message
    }

    req_body = {
      "chainId": self.chain_id,
        "intentTradeOrders": [cancel_order]
    }

    json_body = json.dumps(req_body)

    return json_body

  def __cancel_intent_trade_order_api(self, req):
    return r.post(f'{self.intent_trade_api}/v1/intent-handler/orders.cancel', headers={'Content-Type': 'application/json'}, data=req)

  def __cancel_intent_trade_order(self, market_index: int, order_index: int):
    created_timestamp = math.floor(time())
    json_body = self.__encode_and_build_cancel_trade_order(
      market_index, order_index, created_timestamp)
    return self.__cancel_intent_trade_order_api(json_body)

  def __get_order_key_from_order_index(self, order_index: int):
    order_response = self.__get_intent_trade_orders(
      self.eth_signer.address, [0, 1, 2, 3, 4])

    order_object = {}

    order_list = [
        x for y in order_response.values() for x in y]

    for order in order_list:
      order_object[order['id']] = order['key']

    return order_object[order_index]

  def __get_intent_trade_orders_api(self, address: str, sub_account_id: int):
    response = r.get(
        f'{self.intent_trade_api}/v1/intent-handler/{address}/{sub_account_id}/trade-orders', params={'chainId': self.chain_id, 'status': 'pending'})
    return response.json()

  def __get_intent_trade_orders(self, address: str, sub_account_ids: int):
    active_trade_orders = {}
    for sub_account_id in sub_account_ids:
      active_trade_orders[sub_account_id] = self.__get_intent_trade_orders_api(
        address, sub_account_id)['data']['intentTradeOrders']

    return active_trade_orders
