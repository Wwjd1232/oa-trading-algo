from jqdata import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    log.info('Initialize function starts running and runs once globally')

    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003,
                             close_commission=0.0003, min_commission=5),
                   type='stock')

    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG')
    run_daily(market_open, time='open', reference_security='000300.XSHG')
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')

def before_market_open(context):
    log.info('Function run time (before_market_open): ' + str(context.current_dt.time()))
    g.security = '000001.XSHE'

def market_open(context):
    log.info('Function run time (market_open): ' + str(context.current_dt.time()))
    security = g.security
    close_data = get_bars(security, count=5, unit='1d', fields=['close'])
    MA5 = close_data['close'].mean()
    current_price = close_data['close'][-1]
    cash = context.portfolio.available_cash

    if (current_price > 1.01 * MA5) and (cash > 0):
        log.info("Price is 1% higher than MA5, buying %s" % (security))
        print(("Available cash: {0}, position_value: {1}".format(cash, context.portfolio.positions_value)))
        order_value(security, cash)
    elif current_price < MA5 and context.portfolio.positions[security].closeable_amount > 0:
        log.info("Price is lower than MA5, selling %s" % (security))
        order_target(security, 0)

def after_market_close(context):
    log.info(str('Function run time (after_market_close): ' + str(context.current_dt.time())))
    trades = get_trades()
    for _trade in list(trades.values()):
        log.info('Trade record: ' + str(_trade))
    log.info('End of day')
    log.info('##############################################################')