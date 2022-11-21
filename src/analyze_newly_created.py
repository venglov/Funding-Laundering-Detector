import re
import requests

from src.config import NEWLY_CREATED_MAX_TRANSACTIONS_AMOUNT

headers_etherscan = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Referer': 'https://etherscan.io/txs',
    'Alt-Used': 'etherscan.io',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}


def get_the_amount_of_tx(address, chain_id):
    """
    This function is used to parse explorer to extract the number of transactions
    :param address:
    :param chain_id:
    :return: int
    """
    if chain_id == 1:
        base_url = "https://etherscan.io/address/"
    elif chain_id == 137:
        base_url = "https://polygonscan.com/address/"
    elif chain_id == 10:
        base_url = "https://optimistic.etherscan.io/address/"
    elif chain_id == 56:
        base_url = "https://bscscan.com/address/"
    elif chain_id == 250:
        base_url = "https://ftmscan.com/address/"
    elif chain_id == 42161:
        base_url = "https://arbiscan.io/address/"
    else:
        return 0

    try:
        response = requests.get(f'{base_url}{address.lower()}', headers=headers_etherscan)
        re_transactions_text = re.compile(r"title='Click to view full list'>[1234567890,]*</a> transactions")
        text = re_transactions_text.findall(response.text)
        if text:

            text = text[0]
            re_transactions = re.compile(r">[1234567890,]*<")
            amount_of_transactions = int(re.sub('[<>,]', '', re_transactions.findall(text)[0]))

        else:
            re_transactions_text = re.compile(r"from a total of \d* transactions")
            text = re_transactions_text.findall(response.text)[0]
            re_transactions = re.compile(r"f \d* t")
            amount_of_transactions = int(re.sub('[ft ]', '', re_transactions.findall(text)[0]))

    except Exception as e:
        print(f"Unable to get the amount of transactions for the address ({address}): {e}")
        amount_of_transactions = 0

    return amount_of_transactions


def is_newly_created(address, chain_id):
    amount_of_transactions = get_the_amount_of_tx(address, chain_id)

    if amount_of_transactions < NEWLY_CREATED_MAX_TRANSACTIONS_AMOUNT:
        return True
    else:
        return False
