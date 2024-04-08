import aiohttp
import asyncio
import json
import time


CRYPTOCURRENCIES = ['GRIMACEUSDT', 'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'LINKUSDT', 'ARBUSDT', 'TRXUSDT', 'DOGEUSDT', 'DOTUSDT', 'NEARUSDT']

class Money:
    def __init__(self, cryptocurrencies) -> None:
        self.cryptocurrencies = cryptocurrencies
        self.data = {"bitget": {}, "binance": {}, "huobi": {}}
        self.peres = {"bitget": [], "binance": [], "huobi": []}

    async def requests_processing(self, currencie, session):
        try:
            async with session.get('https://api.bitget.com/api/v2/spot/market/orderbook', ssl=False, params={"symbol": currencie}) as response:
                text = await response.json()
                print(f'bitget : {currencie}')
                if text.get("msg") == "success":
                    self.peres["bitget"].append(currencie)
                    self.data["bitget"][currencie] = text

            async with session.get('https://api.binance.com/api/v3/depth', ssl=False, params={"symbol": currencie}) as response:
                text = await response.json()
                print(f'binance : {currencie}')
                if not text.get("msg") == "Invalid symbol.":
                    self.peres["binance"].append(currencie)
                    self.data["binance"][currencie] = text

            async with session.get(f"https://api.huobi.pro/market/depth?symbol={currencie.lower()}&depth=20&type=step0", ssl=False) as response:
                text = await response.json()
                print(f'huobi : {currencie}')
                if text.get("status") == "ok":
                    self.peres["huobi"].append(currencie)
                    self.data['huobi'][currencie] = text
                    
        except Exception as e:
            print(f"Произошла ошибка для {currencie}: {e}")

    async def gather(self):
        async with aiohttp.ClientSession(read_timeout=2, conn_timeout=2) as session:
            await asyncio.gather(*[self.requests_processing(currencie, session) for currencie in self.cryptocurrencies])

        await self.saving()

    async def saving(self):
        with open('orderbook.json', 'w') as file:
            json.dump(self.data, file)

if __name__ == '__main__':
    start = time.time()
    test = Money(CRYPTOCURRENCIES)
    asyncio.run(test.gather())
    print(time.time() - start)
