import pandas as pd
# class IndexData:
#     def __init__(self, data, index) -> None:
#         self.__private_attribute: pd.DataFrame
#         self.Index: str
#         self.TotalMatchVolume: int
#         self.MarketStatus: str
#         self.TradingDate: str
#         self.ComGroupCode: str
#         self.ReferenceIndex: float
#         self.OpenIndex: float
#         self.CloseIndex: float
#         self.HighestIndex: float
#         self.LowestIndex: float
#         self.IndexValue: float
#         self.IndexChange: float
#         self.PercentIndexChange: float
#         self.MatchVolume: int
#         self.MatchValue: float
#         self.TotalMatchValue: float
#         self.TotalDealVolume: int
#         self.TotalDealValue: float
#         self.TotalStockUpPrice: int
#         self.TotalStockDownPrice: int
#         self.TotalStockNoChangePrice: int
#         self.TotalStockOverCeiling: int
#         self.TotalStockUnderFloor: int
#         self.ForeignBuyVolumeTotal: int
#         self.ForeignBuyValueTotal: float
#         self.ForeignSellVolumeTotal: int
#         self.ForeignSellValueTotal: float
#         self.VolumeBu: int
#         self.VolumeSd: int

#     def get_data(self) -> pd.DataFrame: 
#         ...

class IndexData:
    def __init__(self, data, index) -> None:
        self.__private_attribute: pd.DataFrame
        self.Index: str
        self.TotalMatchVolume: str
        self.MarketStatus: str
        self.TradingDate: str
        self.ComGroupCode: str
        self.ReferenceIndex: str
        self.OpenIndex: str
        self.CloseIndex: str
        self.HighestIndex: str
        self.LowestIndex: str
        self.IndexValue: str
        self.IndexChange: str
        self.PercentIndexChange: str
        self.MatchVolume: str
        self.MatchValue: str
        self.TotalMatchValue: str
        self.TotalDealVolume: str
        self.TotalDealValue: str
        self.TotalStockUpPrice: str
        self.TotalStockDownPrice: str
        self.TotalStockNoChangePrice: str
        self.TotalStockOverCeiling: str
        self.TotalStockUnderFloor: str
        self.ForeignBuyVolumeTotal: str
        self.ForeignBuyValueTotal: str
        self.ForeignSellVolumeTotal: str
        self.ForeignSellValueTotal: str
        self.VolumeBu: str
        self.VolumeSd: str

    def get_data(self) -> pd.DataFrame: 
        ...