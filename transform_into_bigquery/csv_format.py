def create_csv(data, id):
        coin_data = data['data'][id]
        circulating_supply = coin_data['circulating_supply']
        price = coin_data['quote']['USD']['price']
        volume_change_24h = coin_data['quote']['USD']['volume_change_24h']
        percent_change_1h = coin_data['quote']['USD']['percent_change_1h']
        market_cap = coin_data['quote']['USD']['market_cap']
        fully_diluted_market_cap = coin_data['quote']['USD']['fully_diluted_market_cap']

        data_dict = {
        'Circulating_Supply': [circulating_supply],
        'Price': [price],
        'Volume_Change_24h': [volume_change_24h],
        'Percent_Change_1h': [percent_change_1h],
        'Market_Cap': [market_cap],
        'Fully_Diluted_Market_Cap': [fully_diluted_market_cap]
        }
        return data_dict