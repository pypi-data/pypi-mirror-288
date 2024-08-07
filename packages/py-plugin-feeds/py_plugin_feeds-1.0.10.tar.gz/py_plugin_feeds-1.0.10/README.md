[![PyPI version](https://img.shields.io/pypi/v/py-plugin-feeds.svg)](https://pypi.org/project/py-plugin-feeds/)


# py-plugin-feeds

py-plugin-feeds (`py_plugin_feeds`) Python package provides high level modules for smart contracts, with prepackaged ABI files for data feeds and the aggregator address,The package aims for robustness, high quality of the code and documentation.

This package helps users/developers/customers to extract the price from Plugin a decentralized Oracle in few lines of python program. User can navigate their preferred index pair to retrieve and provide the method to access the value.

## Install

```sh
pip install py-plugin-feeds
```

## Example to pull the price XDC/USDT 

```python

from web3 import HTTPProvider, Web3
from py_plugin_feeds import get_token_price

def main():
    json_rpc_url = "https://erpc.xinfin.network"
    pair = "XDC/USDT"
    method = "latestAnswer"
    web3 = Web3(HTTPProvider(json_rpc_url))
    web3.middleware_onion.clear()
    result= get_token_price(web3,pair,"latestAnswer")
    print("result:::",result)

if __name__ == "__main__":
    main()

```

## Example to pull the price CIFI/USDT 

```python

from web3 import HTTPProvider, Web3
from py_plugin_feeds import get_token_price

def main():
    json_rpc_url = "https://rpc-amoy.polygon.technology"
    pair = "BTC/USDT"
    method = "latestRoundData"
    web3 = Web3(HTTPProvider(json_rpc_url))
    web3.middleware_onion.clear()
    result= get_token_price(web3,pair,method)
    print("result:::",result)

if __name__ == "__main__":
    main()

```



## Example to pull the price PLI/USDT 

```python

from web3 import HTTPProvider, Web3
from py_plugin_feeds import get_token_price

def main():
    json_rpc_url = "https:/erpc.xinfin.network"
    pair = "PLI/USDT"
    method = "description"
    web3 = Web3(HTTPProvider(json_rpc_url))
    web3.middleware_onion.clear()
    result= get_token_price(web3,pair,method)
    print("result:::",result)

if __name__ == "__main__":
    main()

```

## Pairs available on XDC Mainnet


```
{
    "CIFI/USDT" : "0xf699C9049B3fF0983bBDCFc115f7E86687a17Ee4",
    "BTC/USDT" : "0x49CD12b8daa769b2fEc36C669b10a0f7bfd352E8",
    "ETH/USDT" : "0xD9B592729c7b7Cbed0A817d4bF2896aB83b01b9E",
    "PRNT/USD" : "0x3Ea54753e3Eb29ce0013C2eb9F57c636037c4f8f",
    "USTY/USD" : "0x607E64B7B72a861440190E3Df8B536CE6380879c",
    "EURS/USDC" : "0xEceC25C2bd99EA806A7aE3e84eDAC69a42a591fe",
    "PLI/USDT" : "0x8F5fcf7f9110A44AC2f55f1a2B6538Df75e4B24b",
    "WTK/USDT" : "0x08477Fab6cEa95df426e7DB1F9042d3BB1558e36",
    "CGO/USDT" : "0xf048DD8CF78504842ADe9af2b5b4c809DCDE819C",
    "FXD/USD" : "0x61Fe25F89FD88510d4de35a4e26BB545872f9F86",
    "XDC/USDT" : "0x896CC6fE8AD04dF9f481332606c445768e286076",
    "PLI/XDC" : "0xc0aD46d667f7d257617de5EDf725BC8059d16bB3",
    "GBEX/USDT" : "0x70d252A13784EA98cB5825c10a025311C4e5b4fe",
    "XSP/USDT" : "0x4A835d097E3432Eccf4F01Cc4cdB8Bb04cFa4Cd4",
    "XTT/USDT" : "0x6733871153Ea1e316dBf0c5193CabcB79840905B"
  }
  

```

## List of methods you can invoke

  ```
  latestAnswer
  latestRoundData
  decimals
  description
  lastRound
  latestTimestamp
  ```

## Explore our data feeds platform 

- explorer now - https://feeds.goplugin.co 
- explore the data source details(Single / aggregator) and choose the appropriate index pair
- data you fetch doesn't requires gas fee, as it is just GET Method
- frequency of this data (last update value)

## Enterprise level access

- Submit your request in feeds platform


## What's Next

- Method to invoke oracle to fetch new data will be added
- VRF functions 
- To raise the right exceptions when data is not available for the index pair