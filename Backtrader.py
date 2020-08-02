import backtrader
import datetime
from Strategy import Test_Strategy
import os
import pandas as pd
import numpy as np
#
class Backtrader_main_():
    def _Backtrader_():
        #Start the Cerebro Library
        cerebro=backtrader.Cerebro()
        #Set a cash value to start investments with
        cerebro.broker.set_cash(1000)
        #Import oracle OHLC Data as an example
        dataSymbol = 'SIFY'
        os.chdir('C:\Dan\Projects\TD_API\TD-AmeritradeStrategyCode\Backtrader .csv')
        data = backtrader.feeds.YahooFinanceCSVData(dataname= dataSymbol + '.csv',
                                            fromdate=datetime.datetime(2018, 1, 1),
                                            todate=datetime.datetime(2020, 5, 1),
                                            reverse=False
                                            )
        cerebro.adddata(data)
        cerebro.addstrategy(Test_Strategy)
        cerebro.addanalyzer(backtrader.analyzers.SharpeRatio, _name='sharpe_ratio')
        cerebro.addanalyzer(backtrader.analyzers.Transactions, _name='transactions')
        cerebro.addanalyzer(backtrader.analyzers.SQN, _name='sqn')
        #Set # of shares to buy and sell
        cerebro.addsizer(backtrader.sizers.FixedSize,stake=100)
        #Starting Value
        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        strat = cerebro.run()
        samStrat = strat[0]
        sharpeRatio = (samStrat.analyzers.sharpe_ratio.get_analysis())
        Transactions = (samStrat.analyzers.transactions.get_analysis())
        SQN = (samStrat.analyzers.sqn.get_analysis())
        print(sharpeRatio)
        print(SQN)
        tearSheet_df = pd.DataFrame(sharpeRatio, index = [dataSymbol], columns = sharpeRatio.keys())
        print(tearSheet_df)
        #Final Value
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        #matplotlib of returns
        cerebro.plot()