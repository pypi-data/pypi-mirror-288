# import pandas as pd
# class DerivativeData:
#     def __init__(self, data) -> None: 
#         self.__private_attribute: pd.DataFrame = data
#         self.TotalMatchVolume: int 
#         self.MarketStatus: str 
#         self.TradingDate: str 
#         self.MatchType: str 
#         self.ComGroupCode: str
#         self.DerivativeCode: str 
#         self.ReferencePrice: float 
#         self.OpenPrice: float 
#         self.ClosePrice: float 
#         self.CeilingPrice: float 
#         self.FloorPrice: float 
#         self.HighestPrice: float 
#         self.LowestPrice: float 
#         self.MatchPrice: float 
#         self.PriceChange: float 
#         self.PercentPriceChange: float 
#         self.MatchVolume: int 
#         self.MatchValue: float 
#         self.TotalMatchValue: float 
#         self.TotalBuyTradeVolume: int 
#         self.TotalSellTradeVolume: int 
#         self.DealPrice: float 
#         self.TotalDealVolume: int 
#         self.TotalDealValue: float 
#         self.ForeignBuyVolumeTotal: int
#         self.ForeignBuyValueTotal: float
#         self.ForeignSellVolumeTotal: int 
#         self.ForeignSellValueTotal: float 
#         self.ForeignTotalRoom: int 
#         self.ForeignCurrentRoom: int
#         self.OpenInterest: int 
#     def get_data(self) -> pd.DataFrame: ...
    

import pandas as pd
class DerivativeData:
    def __init__(self, data) -> None: 
        self.__private_attribute: pd.DataFrame = data
        self.TotalMatchVolume: str 
        self.MarketStatus: str 
        self.TradingDate: str 
        self.MatchType: str 
        self.ComGroupCode: str
        self.DerivativeCode: str 
        self.ReferencePrice: str 
        self.OpenPrice: str 
        self.ClosePrice: str 
        self.CeilingPrice: str 
        self.FloorPrice: str 
        self.HighestPrice: str 
        self.LowestPrice: str 
        self.MatchPrice: str 
        self.PriceChange: str 
        self.PercentPriceChange: str 
        self.MatchVolume: str 
        self.MatchValue: str 
        self.TotalMatchValue: str 
        self.TotalBuyTradeVolume: str 
        self.TotalSellTradeVolume: str 
        self.DealPrice: str 
        self.TotalDealVolume: str 
        self.TotalDealValue: str 
        self.ForeignBuyVolumeTotal: str
        self.ForeignBuyValueTotal: str
        self.ForeignSellVolumeTotal: str 
        self.ForeignSellValueTotal: str 
        self.ForeignTotalRoom: str 
        self.ForeignCurrentRoom: str
        self.OpenInterest: str 
    def get_data(self) -> pd.DataFrame: ...
    