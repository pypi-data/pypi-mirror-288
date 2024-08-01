        
class IndexData:
    def __init__(self,data, index):
        self.__private_attribute = data
        self.Index = index
        self.TotalMatchVolume = data['TotalMatchVolume'].values[0]
        self.MarketStatus = data['MarketStatus'].values[0]
        self.TradingDate = data['TradingDate'].values[0]
        self.ComGroupCode = data['ComGroupCode'].values[0]
        self.ReferenceIndex = data['ReferenceIndex'].values[0]
        self.OpenIndex = data['OpenIndex'].values[0]
        self.CloseIndex = data['CloseIndex'].values[0]
        self.HighestIndex = data['HighestIndex'].values[0]
        self.LowestIndex = data['LowestIndex'].values[0]
        self.IndexValue = data['IndexValue'].values[0]
        self.IndexChange = data['IndexChange'].values[0]
        self.PercentIndexChange = data['PercentIndexChange'].values[0]
        self.MatchVolume = data['MatchVolume'].values[0]
        self.MatchValue = data['MatchValue'].values[0]
        self.TotalMatchValue = data['TotalMatchValue'].values[0]  
        self.TotalDealVolume = data['TotalDealVolume'].values[0]
        self.TotalDealValue = data['TotalDealValue'].values[0]
        self.TotalStockUpPrice = data['TotalStockUpPrice'].values[0]
        self.TotalStockDownPrice = data['TotalStockDownPrice'].values[0]
        self.TotalStockNoChangePrice = data['TotalStockNoChangePrice'].values[0]
        self.TotalStockOverCeiling = data['TotalStockOverCeiling'].values[0]
        self.TotalStockUnderFloor = data['TotalStockUnderFloor'].values[0]
        self.ForeignBuyVolumeTotal = data['ForeignBuyVolumeTotal'].values[0]
        self.ForeignBuyValueTotal = data['ForeignBuyValueTotal'].values[0]
        self.ForeignSellVolumeTotal = data['ForeignSellVolumeTotal'].values[0]
        self.ForeignSellValueTotal = data['ForeignSellValueTotal'].values[0]
        self.VolumeBu = data['VolumeBu'].values[0]
        self.VolumeSd = data['VolumeSd'].values[0]
    def get_data(self):
        return self.__private_attribute 
    