import backtrader
import datetime
from Strategy import TestStrategy_Example
from Strategy import TestSMA_Strategy
#
class Backtrader_main_():
    def _Backtrader_():
        #Start the Cerebro Library
        cerebro=backtrader.Cerebro()
        #Set a cash value to start investments with
        cerebro.broker.set_cash(1000)
        #Import oracle OHLC Data as an example
        data = backtrader.feeds.YahooFinanceCSVData(dataname='USO.csv',
                                            fromdate=datetime.datetime(2018, 1, 1),
                                            todate=datetime.datetime(2020, 1, 1),
                                            reverse=False
                                            )
        cerebro.adddata(data)
        #Run the strategy from Strategy.py
            #Test example buy and hold
        #cerebro.addstrategy(TestStrategy_Example)
            #Test SMA
        cerebro.addstrategy(TestSMA_Strategy)
        #Set # of shares to buy and sell
        cerebro.addsizer(backtrader.sizers.FixedSize,stake=50)
        #Starting Value
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        #Final Value
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        #matplotlib of returns
        cerebro.plot()