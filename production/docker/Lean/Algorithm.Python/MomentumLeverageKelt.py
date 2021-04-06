from clr import AddReference

AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Indicators")
AddReference("QuantConnect.Common")

from QuantConnect import *
from QuantConnect.Parameters import *
from QuantConnect.Benchmarks import *
from QuantConnect.Brokerages import *
from QuantConnect.Util import *
from QuantConnect.Interfaces import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Selection import *
from QuantConnect.Algorithm.Framework.Alphas import *
from QuantConnect.Algorithm.Framework.Portfolio import *
from QuantConnect.Algorithm.Framework.Execution import *
from QuantConnect.Algorithm.Framework.Risk import *
from QuantConnect.Indicators import *
from QuantConnect.Data import *
from QuantConnect.Data.Consolidators import *
from QuantConnect.Data.Custom import *
from QuantConnect.Data.Fundamental import *
from QuantConnect.Data.Market import *
from QuantConnect.Data.UniverseSelection import *
from QuantConnect.Notifications import *
from QuantConnect.Orders import *
from QuantConnect.Orders.Fees import *
from QuantConnect.Orders.Fills import *
from QuantConnect.Orders.Slippage import *
from QuantConnect.Scheduling import *
from QuantConnect.Securities import *
from QuantConnect.Securities.Equity import *
from QuantConnect.Securities.Forex import *
from QuantConnect.Securities.Interfaces import *
from datetime import date, datetime, timedelta
from QuantConnect.Python import *
from QuantConnect.Storage import *

QCAlgorithmFramework = QCAlgorithm
QCAlgorithmFrameworkBridge = QCAlgorithm

VAR_CASH = 100000
START_YEAR = 2020
START_MONTH = 1
START_DAY = 1
END_YEAR = 2021
END_MONTH = 1
END_DAY = 1


class MomentumLeverage(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start/end dates for your algorithm.
            All algorithms must initialized. We also initialize indicators for the algorithm components.
           '''

        # Set Start Date
        self.SetStartDate(START_YEAR, START_MONTH, START_DAY)

        # Set End Date
        self.SetEndDate(END_YEAR, END_MONTH, END_DAY)

        # Set starting cash
        self.SetCash(VAR_CASH)

        # Define symbols
        self.NAS = "TQQQ"
        self.SPY = "UPRO"
        self.RUS = "TNA"
        self.DOW = "UDOW"

        # Initialize possible universe assets their resolutions
        self.universe = [self.NAS, self.SPY, self.RUS, self.DOW]
        self.current_universe = []
        nas_data = self.AddEquity(self.NAS, Resolution.Daily)
        spy_data = self.AddEquity(self.SPY, Resolution.Daily)
        rus_data = self.AddEquity(self.RUS, Resolution.Daily)
        dow_data = self.AddEquity(self.DOW, Resolution.Daily)

        # Declare time varibles for enforcing algorithm time rules
        self.current = datetime.min
        self.current_sold = None

        # Declare a rolling window for price history
        self.window_NAS = RollingWindow[float](6)
        self.window_SPY = RollingWindow[float](6)
        self.window_RUS = RollingWindow[float](6)
        self.window_DOW = RollingWindow[float](6)

        # define strategy indicators: keltner bands, adx, momentum and momentum percent, regression channel
        self.kelt_NAS = self.KCH(self.NAS, 20, 1, MovingAverageType.Exponential, Resolution.Daily)
        self.kelt_NAS_sell = self.KCH(self.NAS, 20, 2, MovingAverageType.Exponential, Resolution.Daily)
        self.adx_NAS = self.ADX(self.NAS, 10, Resolution.Daily)
        self.mom_NAS = self.MOM(self.NAS, 100, Resolution.Daily)
        self.momp_NAS = self.MOMP(self.NAS, 100, Resolution.Daily)
        self.rc_NAS = self.RC(self.NAS, 100, 1, Resolution.Daily)

        self.kelt_SPY = self.KCH(self.SPY, 20, 1, MovingAverageType.Exponential, Resolution.Daily)
        self.kelt_SPY_sell = self.KCH(self.SPY, 20, 2, MovingAverageType.Exponential, Resolution.Daily)
        self.adx_SPY = self.ADX(self.SPY, 10, Resolution.Daily)
        self.mom_SPY = self.MOM(self.SPY, 100, Resolution.Daily)
        self.momp_SPY = self.MOMP(self.SPY, 100, Resolution.Daily)
        self.rc_SPY = self.RC(self.SPY, 100, 1, Resolution.Daily)

        self.kelt_RUS = self.KCH(self.RUS, 20, 1, MovingAverageType.Exponential, Resolution.Daily)
        self.kelt_RUS_sell = self.KCH(self.RUS, 20, 2, MovingAverageType.Exponential, Resolution.Daily)
        self.adx_RUS = self.ADX(self.RUS, 10, Resolution.Daily)
        self.mom_RUS = self.MOM(self.RUS, 100, Resolution.Daily)
        self.momp_RUS = self.MOMP(self.RUS, 100, Resolution.Daily)
        self.rc_RUS = self.RC(self.RUS, 100, 1, Resolution.Daily)

        self.kelt_DOW = self.KCH(self.DOW, 20, 1, MovingAverageType.Exponential, Resolution.Daily)
        self.kelt_DOW_sell = self.KCH(self.DOW, 20, 2, MovingAverageType.Exponential, Resolution.Daily)
        self.adx_DOW = self.ADX(self.DOW, 10, Resolution.Daily)
        self.mom_DOW = self.MOM(self.DOW, 100, Resolution.Daily)
        self.momp_DOW = self.MOMP(self.DOW, 100, Resolution.Daily)
        self.rc_DOW = self.RC(self.DOW, 100, 1, Resolution.Daily)

        # Initialize warm up for indicators
        self.SetWarmUp(timedelta(100))

        # Monthly Universe Selection
        self.Schedule.On(self.DateRules.On(START_YEAR, START_MONTH, START_DAY),
                         self.TimeRules.BeforeMarketClose("TQQQ", 10), self.RebalanceUniverse)

        # Initial Universe Selection
        self.Schedule.On(self.DateRules.WeekStart("TQQQ", 0), self.TimeRules.BeforeMarketClose("TQQQ", 10),
                         self.RebalanceUniverse)

    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.

        Arguments:
            data: Slice object keyed by symbol containing the stock data
        '''

        # add data to rolling window
        self.window_NAS.Add(self.Securities[self.NAS].Price)
        self.window_SPY.Add(self.Securities[self.SPY].Price)
        self.window_RUS.Add(self.Securities[self.RUS].Price)
        self.window_DOW.Add(self.Securities[self.DOW].Price)

        # If the algorithm has a position
        if self.HavePosition() is True:

            # If risk management function returns True a sell order was made.
            if self.ManageRisk() is True: return

        # Else there is no position, we can check for a buy signal.
        else:

            # Check if enough time has passed to consider buying again.
            if self.WaitPeriod() is False: return

            # Position represents a ticker for a symbol with a buy signal. if the function returns None, there are no buy signals above threshold, so return.
            position = self.BuySignal()
            if position is None: return

            # If there is a buy signal for a position, make an order and set the time.
            self.SetHoldings(position, 1)
            self.current = self.Time

    def BuySignal(self):
        ''' The buy signal component of the algorithm. Determines based on the universe and buy signal indicators if we should take a position.
        '''

        # Declare empty arrays for filling.
        buy_universe = [0, 0, 0, 0]
        adx_uni = [0, 0, 0, 0]
        momp_uni = [0, 0, 0, 0]
        mom_uni = [0, 0, 0, 0]
        rc_uni = [0, 0, 0, 0]

        # if the universe is empty, return.
        if self.current_universe is None or not self.current_universe: return

        # Fill arrays with indicators
        adx_uni[0] = self.adx_NAS.Current.Value
        adx_uni[1] = self.adx_SPY.Current.Value
        adx_uni[2] = self.adx_RUS.Current.Value
        adx_uni[3] = self.adx_DOW.Current.Value

        mom_uni[0] = self.mom_NAS.Current.Value
        mom_uni[1] = self.mom_SPY.Current.Value
        mom_uni[2] = self.mom_RUS.Current.Value
        mom_uni[3] = self.mom_DOW.Current.Value

        momp_uni[0] = self.momp_NAS.Current.Value
        momp_uni[1] = self.momp_SPY.Current.Value
        momp_uni[2] = self.momp_RUS.Current.Value
        momp_uni[3] = self.momp_DOW.Current.Value

        rc_uni[0] = self.rc_NAS.Slope.Current.Value
        rc_uni[1] = self.rc_SPY.Slope.Current.Value
        rc_uni[2] = self.rc_RUS.Slope.Current.Value
        rc_uni[3] = self.rc_DOW.Slope.Current.Value

        # Based on the indicators values and current universe, buy if the current asset price crosses the upper keltner buy band
        # as well as the asset must have adx above a threshold.

        if self.current_universe[0] == self.NAS:
            if self.Securities[
                self.NAS].Price - self.kelt_NAS.UpperBand.Current.Value > 0 and self.adx_NAS.Current.Value > 12:
                return self.current_universe[0]

        elif self.current_universe[0] == self.SPY:
            if self.Securities[
                self.SPY].Price - self.kelt_SPY.UpperBand.Current.Value > 0 and self.adx_SPY.Current.Value > 12:
                return self.current_universe[0]

        elif self.current_universe[0] == self.RUS:
            if self.Securities[
                self.RUS].Price - self.kelt_RUS.UpperBand.Current.Value > 0 and self.adx_RUS.Current.Value > 12:
                return self.current_universe[0]

        elif self.current_universe[0] == self.DOW:
            if self.Securities[
                self.DOW].Price - self.kelt_DOW.UpperBand.Current.Value > 0 and self.adx_DOW.Current.Value > 12:
                return self.current_universe[0]

        # No signal.
        return None

    def HavePosition(self):
        ''' Determines if the algorithm currently has any positions open'''

        # Return true if we currently have an open position
        if self.Portfolio[self.NAS].Quantity > 0 or self.Portfolio[self.SPY].Quantity > 0 or self.Portfolio[
            self.RUS].Quantity > 0 or self.Portfolio[self.DOW].Quantity > 0:
            return True

        # return false if we have no open positions.
        return False

    def WaitPeriod(self):
        ''' Wait a period of time before checking for a buy signal after selling'''

        # Return true if the minimum number of waiting days has passed.
        if (self.current_sold is None or (self.Time - self.current_sold).days >= 2):
            return True

        # Otherwise return false.
        return False

    def ManageRisk(self):
        ''' Function to manage the risk of the position.'''

        # if invested and price crosses the lower band of the sell signal, liquidate.
        if self.Portfolio[self.NAS].Quantity > 0:
            if self.Securities[self.NAS].Price - self.kelt_NAS_sell.LowerBand.Current.Value < 0:
                self.Liquidate()
                self.current_sold = self.Time
                return True

            # Else if 5 days has passed and price has not moved a certain percentage, liquidate.
            elif (self.Time - self.current).days >= 5:
                if self.Securities[self.NAS].Price < 1.03 * self.window_NAS[5]:
                    self.Liquidate()
                    self.current_sold = self.Time
                    return True



        elif self.Portfolio[self.SPY].Quantity > 0:
            if self.Securities[self.SPY].Price - self.kelt_SPY_sell.LowerBand.Current.Value < 0:
                self.Liquidate()
                self.current_sold = self.Time
                return True

            elif (self.Time - self.current).days >= 5:
                if self.Securities[self.SPY].Price < 1.03 * self.window_SPY[5]:
                    self.Liquidate()
                    self.current_sold = self.Time
                    return True


        elif self.Portfolio[self.RUS].Quantity > 0:
            if self.Securities[self.RUS].Price - self.kelt_RUS_sell.LowerBand.Current.Value < 0:
                self.Liquidate()
                self.current_sold = self.Time
                return True

            elif (self.Time - self.current).days >= 5:
                if self.Securities[self.RUS].Price < 1.03 * self.window_RUS[5]:
                    self.Liquidate()
                    self.current_sold = self.Time
                    return True


        elif self.Portfolio[self.DOW].Quantity > 0:
            if self.Securities[self.DOW].Price - self.kelt_DOW_sell.LowerBand.Current.Value < 0:
                self.Liquidate()
                self.current_sold = self.Time
                return True

            elif (self.Time - self.current).days >= 5:
                if self.Securities[self.DOW].Price < 1.03 * self.window_DOW[5]:
                    self.Liquidate()
                    self.current_sold = self.Time
                    return True

        # Return false if no sell signal was shown after checking the position.
        return False

    def RebalanceUniverse(self):
        ''' Function to check longer term indicators in order to reevaluate the universe.'''
        self.current_universe = []

        # Declare empty arrays for indicators.
        adx_uni = [0, 0, 0, 0]
        momp_uni = [0, 0, 0, 0]
        mom_uni = [0, 0, 0, 0]
        rc_uni = [0, 0, 0, 0]

        # Fill arrays with current indicator values
        adx_uni[0] = self.adx_NAS.Current.Value
        adx_uni[1] = self.adx_SPY.Current.Value
        adx_uni[2] = self.adx_RUS.Current.Value
        adx_uni[3] = self.adx_DOW.Current.Value

        mom_uni[0] = self.mom_NAS.Current.Value
        mom_uni[1] = self.mom_SPY.Current.Value
        mom_uni[2] = self.mom_RUS.Current.Value
        mom_uni[3] = self.mom_DOW.Current.Value

        momp_uni[0] = self.momp_NAS.Current.Value
        momp_uni[1] = self.momp_SPY.Current.Value
        momp_uni[2] = self.momp_RUS.Current.Value
        momp_uni[3] = self.momp_DOW.Current.Value

        rc_uni[0] = self.rc_NAS.Slope.Current.Value
        rc_uni[1] = self.rc_SPY.Slope.Current.Value
        rc_uni[2] = self.rc_RUS.Slope.Current.Value
        rc_uni[3] = self.rc_DOW.Slope.Current.Value

        # Select based on local maximum for longer term regression channel slope.
        if rc_uni.index(max(rc_uni)) == 0:
            self.current_universe = [self.NAS]

        elif rc_uni.index(max(rc_uni)) == 1:
            self.current_universe = [self.SPY]

        elif rc_uni.index(max(rc_uni)) == 2:
            self.current_universe = [self.RUS]

        elif rc_uni.index(max(rc_uni)) == 3:
            self.current_universe = [self.DOW]