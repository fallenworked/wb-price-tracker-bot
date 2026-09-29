import httpx
import logging
import re
from typing import Optional, Dict, Any

class WBParser:
    @staticmethod
    def extract_article(text: str) -> Optional[int]:
        """Извлекает артикул Wildberries из ссылки или обычного текста"""
        text = text.strip()
        if text.isdigit():
            return int(text)
        
        # Поиск артикула в ссылках вида https://www.wildberries.ru/catalog/123456789/detail.aspx
        match = re.search(r'catalog/(\d+)/detail', text)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    async def get_product_info(article: int) -> Optional[Dict[str, Any]]:
        """Получает информацию о товаре напрямую через публичное API Wildberries"""
        url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "*/*",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    products = data.get("data", {}).get("products", [])
                    if products:
                        prod = products[0]
                        # Цена WB указывается в копейках, делим на 100
                        price = prod.get("sizes", [{}])[0].get("price", {}).get("total", 0) // 100
                        if price == 0:
                            price = prod.get("salePriceU", 0) // 100

                        return {
                            "article": article,
                            "title": prod.get("name", "Товар Wildberries"),
                            "brand": prod.get("brand", "Без бренда"),
                            "price": price,
                            "rating": prod.get("reviewRating", 0),
                            "url": f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
                        }
            except Exception as e:
                logging.error(f"Ошибка при запросе WB API для артикула {article}: {e}")
        return None
