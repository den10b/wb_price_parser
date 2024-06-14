import aiohttp


async def checkToken(business_id: str, oauth_token: str) -> bool:
    """
    Проверка корректности токена.

    """
    try:
        url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings'

        headers = {
            'Authorization': f'Bearer {oauth_token}',
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return True
                elif response.status == 401:
                    return False
                else:
                    print(f'Неожиданный статус: {response.status} - {await response.text()}')
                    return False
    except:
        return False


async def priceProduct(business_id: str, oauth_token: str, offer_id: str) -> int:
    """
    Получение цены продукта.

    """
    try:
        url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings'

        headers = {
            'Authorization': f'Bearer {oauth_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "offerIds": [
                offer_id
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, json=data) as response:
                if response.status == 200:
                    card = await response.json()
                    offer_mappings = card.get('result', {}).get('offerMappings', [])
                    if offer_mappings:
                        basic_price = offer_mappings[0].get('offer', {}).get('basicPrice', {}).get('value', 0)
                        return basic_price
                    return 0
                else:
                    print(f'Error: {response.status} - {await response.text()}')
                    return 0
    except:
        return 0


async def setPriceYa(item_id: str, business_id: str, oauth_token: str,
                     new_price: int) -> bool:
    """
    Функция изменения цены.

    """
    try:
        url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings/update'

        headers = {
            'Authorization': f'Bearer {oauth_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "offerMappings": [
                {
                    "offer": {
                        "offerId": item_id,
                        "basicPrice": {
                            "value": new_price,
                            "currencyId": "RUR"
                        },
                    },
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    print(f'Цена товара со sku: {item_id} успешно обновлена')
                else:
                    print(
                        f'Ошибка при обновлении цены на товар со sku: {item_id}: {response.status} - {await response.text()}')
                    return False
        return True
    except:
        return False
