import backtrader
import datetime
class Test_Strategy(backtrader.Strategy):
    lines = ('macd', 'signal', 'histo')
    params = (('period_me1', 12),
              ('period_me2', 26),
              ('period_signal', 9),
              ('pfast', 5),
              ('pslow', 11),
              ('period',14),
              ('upperband',70),
              ('lowerband',30),
              ('devfactor',2.0)
             )
    plotlines = dict(period_signal=dict(_name='macdSignal', alpha=0.50))
    plotlines = dict(pfast=dict(_name='pfast', alpha=0.50))
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        self.order = None
        me1 = backtrader.indicators.EMA(self.data, period=self.p.period_me1, plot=False)
        me2 = backtrader.indicators.EMA(self.data, period=self.p.period_me2, plot=False)
        macd = backtrader.indicators.MACD(self.data, period_me1=self.p.period_me1, period_me2=self.p.period_me2, period_signal=self.p.period_signal, subplot=True, plotname='MACD')
        self.l.macd = me1 - me2
        self.l.signal = backtrader.indicators.EMA(self.l.macd, period=self.p.period_signal, plot=False)
        self.l.histo = self.l.macd - self.l.signal
        self.crossoverMACD = backtrader.indicators.CrossOver(self.l.macd, self.l.signal,plot=False)
        slowSMA = backtrader.indicators.SMA(period=self.p.pslow)#, plot=False)
        fastSMA = backtrader.indicators.SMA(period=self.p.pfast)#, plot=False)
        self.crossoverSMA = backtrader.indicators.CrossOver(slowSMA,fastSMA,plot=False)
        self.rsi = backtrader.indicators.RSI_SMA(self.data, period=self.p.period, upperband=self.p.upperband, lowerband=self.p.lowerband, subplot=True, plotname='RSI')
        self.bollingerBands = backtrader.indicators.BBands(self.data, period=self.p.period_me2, devfactor=self.p.devfactor)
        self.dataclose = self.datas[0].close
        self.dataVolume = self.datas[0].volume
    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log(('SELL EXECUTED {}'.format(order.executed.price)))
            self.bar_executed = len(self)
        self.order = None
    def next(self):
        if self.order:
            return
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        elif self.rsi > 70:
            self.order = self.sell()