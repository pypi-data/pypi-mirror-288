class CoveredWarrantData:
    def __init__(self, data):
        self.__private_attribute = data
        self.TotalMatchVolume = data['TotalMatchVolume'].values[0]
        self.MarketStatus = data['MarketStatus'].values[0]
        self.TradingDate = data['TradingDate'].values[0]
        self.MatchType = data['MatchType'].values[0]
        self.ComGroupCode = data['ComGroupCode'].values[0]
        self.OrganCode = data['OrganCode'].values[0]
        self.Ticker = data['Ticker'].values[0]
        self.ReferencePrice = data['ReferencePrice'].values[0]
        self.OpenPrice = data['OpenPrice'].values[0]
        self.ClosePrice = data['ClosePrice'].values[0]
        self.CeilingPrice = data['CeilingPrice'].values[0]
        self.FloorPrice = data['FloorPrice'].values[0]
        self.HighestPrice = data['HighestPrice'].values[0]
        self.LowestPrice = data['LowestPrice'].values[0]
        self.MatchPrice = data['MatchPrice'].values[0]
        self.PriceChange = data['PriceChange'].values[0]
        self.PercentPriceChange = data['PercentPriceChange'].values[0]
        self.MatchVolume = data['MatchVolume'].values[0]
        self.MatchValue = data['MatchValue'].values[0]
        self.TotalMatchValue = data['TotalMatchValue'].values[0]
        self.TotalBuyTradeVolume = data['TotalBuyTradeVolume'].values[0]
        self.TotalSellTradeVolume = data['TotalSellTradeVolume'].values[0]
        self.DealPrice = data['DealPrice'].values[0]
        self.TotalDealVolume = data['TotalDealVolume'].values[0]
        self.TotalDealValue = data['TotalDealValue'].values[0]
        self.ForeignBuyVolumeTotal = data['ForeignBuyVolumeTotal'].values[0]
        self.ForeignBuyValueTotal = data['ForeignBuyValueTotal'].values[0]
        self.ForeignSellVolumeTotal = data['ForeignSellVolumeTotal'].values[0]
        self.ForeignSellValueTotal = data['ForeignSellValueTotal'].values[0]
        self.ForeignTotalRoom = data['ForeignTotalRoom'].values[0]
        self.ForeignCurrentRoom = data['ForeignCurrentRoom'].values[0]

    def get_data(self):
        return self.__private_attribute
    



