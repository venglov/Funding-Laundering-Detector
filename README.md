# **Funding Laundering Detector**

---

## Description

The goal of this agent is to identify mixers, bridges, exchanges generically, such that any funding and money laundering
activities from those protocols can be flagged. The bot analyzes each transaction and remembers the transfers of the 
native coin of the network or the ERC20 token. In the case of a large number of transfers, the address is recorded by 
the bot in the list of suspects, whether it is analyzed as a smart contract or EOA, and information about it is parsed 
from Internet resources (currently from one of the 6 network explorers on which the bot works). Based on the information 
received, the bot decides whether the address is a mixer, exchanger, dex or a bridge. Although this method works very 
well at the moment, it would be worthwhile to translate or improve the classification using machine learning in the 
future. Having addresses of bridges, exchangers and mixers, the bot monitors transfers of funds to these addresses 
(network native tokens and ERC20) and creates an alert if the amount in USD equivalent is more than the threshold 
specified in the settings. The type of alert depends on whether funds are being received or withdrawn from the 
exchanger. In each case, we try to determine whether the suspicious address is new or not. To do this, the bot parses 
the explorer of the corresponding network in the place that contains data on the number of transactions of this 
address, and if this number is less than the threshold specified in the settings, the address is considered new.


:warning: To enable DEX-related alerts please change `DEX_DISABLE` to `False` in `src/config.py`.


## Features

- Fully asynchronous local database to save the addresses in case of crash
- Bot is stable after the sudden restart
- 6 networks supported
- EOA detection
- high-precision type detection
- USD value of each transaction (native and ERC20)

## Chains

- Ethereum
- Polygon 
- Fantom
- BSC
- Optimism
- Arbitrum

## Settings

You can specify your own settings in the `src/config.py`:

## Alerts

- FLD_FUNDING
    - Fired when the account was funded by cex / dex / bridge / mixer'
    - Severity:
        - `Critical` - EOA is newly created or transfer in USD > Critical threshold
        - `High` - transfer in USD > High threshold
        - `Medium` - transfer in USD > Medium threshold
        - `Low` - transfer in USD < Medium threshold
    - Type is always set to "Suspicious"
    - Metadata contains:
        - `funded_address` - funded address
        - `newly_created` - is EOA newly created or not
        - `source_address` - address of cex / dex / bridge / mixer
        - `source_type` - centralized exchange / dex / bridge / mixer
        - `usd_volume` - transfer amount in USD
        - `tx_hash` - the hash of the transaction

- FLD_Laundering
    - Fired when the huge amount of assets in USD was transferred to cex / dex / bridge / mixer'
    - Severity:
        - `Critical` - transfer in USD > Critical threshold
        - `High` - transfer in USD > High threshold
        - `Medium` - transfer in USD > Medium threshold
        - `Low` - transfer in USD < Medium threshold
    - Type is always set to "Suspicious"
    - Metadata contains:
        - `laundering_address` - EOA address
        - `newly_created` - is EOA newly created or not
        - `target_address` - address of cex / dex / bridge / mixer
        - `source_type` - centralized exchange / dex / bridge / mixer
        - `usd_volume` - transfer amount in USD
        - `tx_hash` - the hash of the transaction

## Tests

Tests and test data use database preset `test/database_presets/test_14442765-14489802.db` that contains real collected
data. It should be moved to `./test.db` e.g.

```bash
cp ./test/database_presets/main.db ./main.db
```

There are 17 tests that should pass:

```python
test_returns_zero_finding_if_the_amount_is_small()
test_returns_critical_finding_if_the_amount_is_big_erc20_new_address_FLD_FUNDING()
test_returns_high_finding_if_the_amount_is_big_erc20_old_address_FLD_FUNDING()
test_returns_low_finding_if_the_amount_is_low_erc20_old_address_FLD_FUNDING()
test_returns_critical_finding_if_new_address_ETH_FLD_FUNDING()
test_returns_critical_finding_if_critical_amount_eth_old_address_FLD_FUNDING()
test_returns_high_finding_if_high_amount_eth_old_address_FLD_FUNDING()
test_returns_medium_finding_if_medium_amount_eth_old_address_FLD_FUNDING()
test_returns_low_finding_if_low_amount_eth_old_address_FLD_FUNDING()
test_returns_critical_finding_if_critical_amount_eth_old_address_FLD_Laundering()
test_returns_hight_finding_if_critical_amount_eth_old_address_FLD_Laundering()
test_returns_medium_finding_if_medium_amount_eth_old_address_FLD_Laundering()
test_returns_low_finding_if_low_amount_eth_old_address_FLD_Laundering()
test_returns_low_finding_if_the_amount_is_low_erc20_old_address_FLD_Laundering()
test_returns_medium_finding_if_the_amount_is_medium_erc20_old_address_FLD_Laundering()
test_returns_high_finding_if_the_amount_is_high_erc20_old_address_FLD_Laundering()
test_returns_critical_finding_if_the_amount_is_critical_erc20_old_address_FLD_Laundering()
```

## Test Data

Example of the alert:

```
1 findings for transaction 0x5e37371ddeb4f249fcae38ff0cfebc022467c04df5e5586fdf52536a013b719a {
  "name": "Laundering Alert",
  "description": "0x8bd9880db6ed9c140669731cb9bfd27caafd9649 is engaged in money laundering behavior using exchange 0x8bd9880db6ed9c140669731cb9bfd27caafd9649",
  "alertId": "FLD_Laundering",
  "protocol": "ethereum",
  "severity": "High",
  "type": "Suspicious",
  "metadata": {
    "laundering_address": "0x8bd9880db6ed9c140669731cb9bfd27caafd9649",
    "newly_created": false,
    "target_address": "0x28c6c06298d514db089934071355e5743bf21d60",
    "target_type": "exchange",
    "usd_volume": 97693.99334193398,
    "token": "USDC",
    "tx_hash": "0x5e37371ddeb4f249fcae38ff0cfebc022467c04df5e5586fdf52536a013b719a"
  },
  "addresses": []

1 findings for transaction 0xb8fae9fb9ed036e3ab08051323465ca6e2f110adaf1ccb7b56aab885d889f74d {
  "name": "Funding Alert",
  "description": "0x10ff52ca0559f50471db4fd42a10df2e987252e1 was funded using exchange 0x28c6c06298d514db089934071355e5743bf21d60",
  "alertId": "FLD_FUNDING",
  "protocol": "ethereum",
  "severity": "High",
  "type": "Suspicious",
  "metadata": {
    "funded_address": "0x10ff52ca0559f50471db4fd42a10df2e987252e1",
    "newly_created": false,
    "source_address": "0x28c6c06298d514db089934071355e5743bf21d60",
    "source_type": "exchange",
    "usd_volume": 6378.5421323,
    "token": "AAVE",
    "tx_hash": "0xb8fae9fb9ed036e3ab08051323465ca6e2f110adaf1ccb7b56aab885d889f74d"
  },
  "addresses": []
}

1 findings for transaction 0x8ef58e6aeca4eed871fe9725441e21071b40dd040f88ca110240d265d68a981e {
  "name": "Laundering Alert",
  "description": "0xf033bce292bcaaf998ca13755104a4b23c04af5c is engaged in money laundering behavior using exchange 0xf033bce292bcaaf998ca13755104a4b23c04af5c",
  "alertId": "FLD_Laundering",
  "protocol": "ethereum",
  "severity": "Critical",
  "type": "Suspicious",
  "metadata": {
    "laundering_address": "0xf033bce292bcaaf998ca13755104a4b23c04af5c",
    "newly_created": false,
    "target_address": "0x28c6c06298d514db089934071355e5743bf21d60",
    "target_type": "exchange",
    "usd_volume": 2013999.9999999998,
    "token": "USDT",
    "tx_hash": "0x8ef58e6aeca4eed871fe9725441e21071b40dd040f88ca110240d265d68a981e"
  },
  "addresses": []
}

1 findings for transaction 0x5d1560c856df18d7a139cd6d12e743252d19f7926742d8bca27a468f7e8c81b4 {
  "name": "Funding Alert",
  "description": "0xf7c005851f532d0a55270330e27398ee0b04537c was funded using exchange 0x28c6c06298d514db089934071355e5743bf21d60",
  "alertId": "FLD_FUNDING",
  "protocol": "ethereum",
  "severity": "Critical",
  "type": "Suspicious",
  "metadata": {
    "funded_address": "0xf7c005851f532d0a55270330e27398ee0b04537c",
    "newly_created": true,
    "source_address": "0x28c6c06298d514db089934071355e5743bf21d60",
    "source_type": "exchange",
    "usd_volume": 389.899636,
    "token": "MANA",
    "tx_hash": "0x5d1560c856df18d7a139cd6d12e743252d19f7926742d8bca27a468f7e8c81b4"
  },
  "addresses": []
}
}
```
