import requests

# Сейчас это адрес мока на постмане, далее нужно изменить на реальный url wb
wb_url = 'https://6803f9f0-a1e0-4d1f-96e8-63eaf66dd520.mock.pstmn.io'


def wb_check_token(wb_token) -> bool:
    response = requests.get(url=f'{wb_url}/api/v2/list/goods/filter', headers={'Authorization': wb_token},
                            json={'limit': 10})
    if response.ok:
        return True
    return False


def wb_check_current_price(wb_token, wb_nm_id) -> int:
    response = requests.get(url=f'{wb_url}/api/v2/list/goods/filter', headers={'Authorization': wb_token},
                            json={'nmID': wb_nm_id, 'limit': 1})
    if response.ok:
        return response.json()['data']['listGoods'][0]['sizes'][0]['price']
    return 0


def wb_change_price(wb_token, wb_nm_id, target_price) -> bool:
    response = requests.post(url=f'{wb_url}/api/v2/upload/task', headers={'Authorization': wb_token},
                             json={'data': [{'nmID': wb_nm_id, 'price': target_price, 'discount': 0}]})
    if response.ok:
        return True
    return False
