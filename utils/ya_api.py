import aiohttp
import asyncio
from typing import List, Dict

async def checkToken(business_id:str, oauth_token:str)-> bool: #проверка корректности токена
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

async def priceProduct(business_id:str, oauth_token:str, offer_id:str)-> int: #получение цены продукта
    url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings'

    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': 'application/json'
    }
    data={
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

async def setPriceYa(ParseYa:List[Dict[str, str]], business_id:str, oauth_token:str) -> None: #функция изменения цены
    for item in ParseYa:
        url = f'https://api.partner.market.yandex.ru/businesses/{business_id}/offer-mappings/update'

        headers = {
            'Authorization': f'Bearer {oauth_token}',
            'Content-Type': 'application/json'
        }
        newPrice = int(item["price"]) * 1.1 #повышение цены на 10 процентов
        data ={
                "offerMappings": [
                    {
                        "offer": {
                            "offerId": item["sku"],
                            "basicPrice": {
                                "value": newPrice,
                                "currencyId": "RUR"
                            },
                        },
                    }
                ]
            }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    print(f'Цена товара со sku: {item["sku"]} успешно обновлена')
                else:
                    print(f'Ошибка при обновлении цены на товар со sku: {item["sku"]}: {response.status} - {await response.text()}')


# Запуск асинхронных функций
asyncio.run(checkToken(business_id, oauth_token))
asyncio.run(priceProduct(business_id, oauth_token, offer_id))
asyncio.run(setPriceYa(product_dict,business_id, oauth_token))
