from typing import Tuple
from pathlib import Path
from web3 import Web3
from eth_typing import HexAddress
from py_plugin_feeds.mapping.token_mapping import token_mapping
import json
import logging
logging.basicConfig(level=logging.INFO)

def get_abi(fname="token"):
    logging.info("***fetching abi details****")
    here = Path(__file__).resolve().parent
    abi_path = here / "abi" / Path(fname)
    with open(abi_path, "rt", encoding="utf-8") as f:
        abi = json.load(f)
    return abi

def get_contract(web3,fname,bytecode=None):
    logging.info("***fetching contract details internal****")
    contract_interface = get_abi(fname)
    abi = contract_interface["abi"]
    if bytecode is None:
        bytecode = contract_interface["bytecode"]
        if type(bytecode) == dict:
            bytecode = bytecode["object"]
        else:
            pass
    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    return Contract


def get_token_price(web3,pair,category,fname="token/token.json"):
    logging.info("***fetching token price****")
    address = token_mapping(pair)
    match web3.eth.chain_id:
        case 51:  # XDC Test net
            aggregator_address = address
        case 50:  # XDC Mainnet
            aggregator_address = address
        case 80002: # Amoy Testnet
            aggregator_address = address
        case 137: # Polygon Mainnet
            aggregator_address = address
        case _:
            logging.warning("***Unsupported chain****")
            raise NotImplementedError(f"Unsupported chain: {web3.eth.chain_id}. Please add aggregator mapping.")

    price = get_token_price_from_plugin_oracle(web3, aggregator_address,fname,category)
    return price


def get_token_price_from_plugin_oracle(    
    web3: Web3,
    aggregator_address: HexAddress,
    fname,
    category
):
    logging.info("***Internal final call to fetch price****")
    aggregator = get_deployed_contract(web3,aggregator_address,fname)
    match category:
        case "latestRoundData":
            data = aggregator.functions.latestRoundData().call()
        case "latestAnswer":
            data = aggregator.functions.latestAnswer().call()
        case "description":
            data = aggregator.functions.description().call()
        case "decimals":
            data = aggregator.functions.decimals().call()
        case "latestTimestamp":
            data = aggregator.functions.latestTimestamp().call()
        case _:
            logging.warning("***Unsupported methd****")
            raise NotImplementedError(f"Unsupported Method: {category}!!s")
    return data


def get_deployed_contract(web3,address,fname):
    logging.info("***Fetching deployed contract details****")    
    assert address, f"get_deployed_contract() address was None"
    address = Web3.to_checksum_address(address)
    Contract = get_contract(web3, fname)
    contract = Contract(address)
    return contract