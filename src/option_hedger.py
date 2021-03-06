import numpy as np
import pandas as pd
import src.black_scholes as bs
from typing import Callable, Union, List
import src.colnames as n


class OptionHedger:

    # (price, time_left) -> delta
    fun_delta: Callable[[float, float], float]

    rebalance_thresh: Union[List[float], float]
    _rebalance_thresh_levels: bool = False
    limit_ask: float = 0
    limit_bid: float = float('inf')
    limit_time: float = -1

    riskless_rate: float

    time_left: float
    price: float
    delta: float = 0
    cash: float = 0
    option_price: float
    nb_trades: int = 0

    # first position set?
    _initialized: bool = False

    def __init__(self,
                 fun_delta: Callable[[float, float], float],
                 time_left: float,
                 riskless_rate: float,
                 rebalance_thresh: Union[List[float], float],
                 rebalance_time_window_max: float = None) -> None:
        self.fun_delta = fun_delta
        self.time_left = time_left
        self.riskless_rate = riskless_rate
        if isinstance(rebalance_thresh, list):
            rebalance_thresh = [0, *sorted(rebalance_thresh), float('inf')]
            self._rebalance_thresh_levels = True
        self.rebalance_thresh = rebalance_thresh
        self.rebalance_time_window_max = rebalance_time_window_max

    def _update_rebalance_limits(self):
        if not self._rebalance_thresh_levels:
            mult = np.exp(self.rebalance_thresh)
            self.limit_ask = self.price * mult
            self.limit_bid = self.price / mult
        else:
            threshs = self.rebalance_thresh
            for i in range(len(threshs)):
                if self.price < threshs[i]:
                    break

            # avoir price at thresholds
            self.limit_bid = threshs[i -
                                     2] if self.price == threshs[i-1] else threshs[i-1]
            self.limit_ask = threshs[i +
                                     1] if self.price == threshs[i] else threshs[i]

        if self.rebalance_time_window_max:
            self.limit_time = self.time_left - self.rebalance_time_window_max

    def _update_state(self):
        self.valo = self.price * self.delta + self.cash

    def _rebalance(self, price: float, time_left: float):

        self.price = price
        self.time_left = time_left

        delta_tgt = self.fun_delta(price, time_left)
        delta_trd = delta_tgt - self.delta

        self.cash -= delta_trd * price
        self.delta = delta_tgt

        self.nb_trades += 1
        self._update_rebalance_limits()

    def _init_porfolio(self, price: float, time_left: float):
        self._rebalance(price, time_left)
        self.price = price
        self._update_state()
        self._initialized = True

    def update(self, price: float, time_left: float, way: int = 0):

        if not self._initialized:
            self._init_porfolio(price, time_left)
            return

        # update cash valo if time changes
        dt = self.time_left-time_left
        if dt > 0:
            self.time_left = time_left
            self.cash *= np.exp(dt * self.riskless_rate)
            self.nb_trades = 0

        if time_left > 0:
            if (self.limit_ask <= price) and (0 <= way):
                self._rebalance(self.limit_ask, time_left)
                self.update(price, time_left, 1)
            elif (price <= self.limit_bid) and (way <= 0):
                self._rebalance(self.limit_bid, time_left)
                self.update(price, time_left, -1)
            elif (self.time_left <= self.limit_time):
                self._rebalance(price, time_left)

        self.price = price
        self._update_state()

    def to_dict(self):
        return {
            n.Ttm: self.time_left,
            n.Price: self.price,
            n.Delta: self.delta,
            n.Cash: self.cash,
            n.LimAsk: self.limit_ask,
            n.LimBid: self.limit_bid,
            n.LimTime: self.limit_time,
            n.NbTrades: self.nb_trades,
            n.Valo: self.valo,
        }


def replicate_call(sigma, K, T, r, hedge_threshs, hedge_win, path, dt, store=False):

    if isinstance(dt, (list, pd.core.series.Series, np.ndarray)):
        if len(dt) != len(path):
            print("Please provide dt with same length than path (or single value).")
            exit()
    else:
        dt = np.full(fill_value=dt, shape=len(path))

    states = []

    hedger = OptionHedger(
        bs.call_delta_wrapper(sigma, K, r),
        T,
        r,
        hedge_threshs,
        hedge_win
    )

    time_left = T - dt[0]
    for price, time_step in zip(path, dt):
        time_left = max(time_left - time_step, 0.0)

        hedger.update(price, time_left)
        if store:
            states.append(hedger.to_dict())

        # if time_left <= 0:
        #     break

    if store:
        return states
    else:
        return hedger.to_dict()
