from web3 import HTTPProvider, Web3
from py_plugin_feeds import get_token_price

def main():
    json_rpc_url = "https://rpc-amoy.polygon.technology"
    pair = "BTC/USDT"
    method="latestAnswer"
    web3 = Web3(HTTPProvider(json_rpc_url))
    web3.middleware_onion.clear()
    result= get_token_price(web3,pair,method)
    print("result:::",result)

if __name__ == "__main__":
    main()