import aiohttp

card_req = "https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1252448&spp=30&nm="


async def parse(links: list[str]) -> list[tuple[int, int]]:
    res = []
    for link in links:
        nm = 0
        for link_part in link.split('/'):
            if link_part.isdigit():
                nm = link_part
        card_link = f'{card_req}{nm}'
        async with aiohttp.ClientSession() as session:
            async with session.get(card_link) as resp:
                try:
                    product = (await resp.json())["data"]["products"][0]
                    id = int(product["id"])
                    price = product["sizes"][0]["price"]["total"]
                    res.append((id, price // 100))
                except:
                    print(f"Ошибочка ((")

    return res
