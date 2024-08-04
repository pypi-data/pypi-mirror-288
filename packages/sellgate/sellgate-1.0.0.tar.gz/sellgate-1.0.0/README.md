# Sellgate Python SDK

This is the Sellgate Python SDK. It is a simple SDK to use the Sellgate API. 

Sellgate provides an API service that allows sellers and developers to easily integrate crypto payments into their applications or payment flows. Using our service has several benefits:

- Low transaction fees, just 1%.
- No authentication required for any usage: No API keys, no accounts.
- Examples for quick implementation on our docs.
- Support for bug fixes, extra features and integration assistance.

For further documentation, please refer to the [Sellgate docs](https://sellgate.io/docs)

## Installation

```bash
pip install sellgate
```	

## Usage

```python
from sellgate import sellgate

checkout = sellgate().create_checkout({
  "price": '10',
  "crypto": [
    {
      "network": "ETH",
      "coin": "ETH",
      "address": "0xB1DA646D1cD015d205a99198e809724D5C78109d"
    }
  ]
})

address = sellgate().create_address({
  "crypto": 
    {
      "network": "ETH",
      "coin": "ETH",
      "address": "0xB1DA646D1cD015d205a99198e809724D5C78109d"
    },
  "webhook": "https://webhook.site/1234567890"
})

print(checkout)
print(address)
```
