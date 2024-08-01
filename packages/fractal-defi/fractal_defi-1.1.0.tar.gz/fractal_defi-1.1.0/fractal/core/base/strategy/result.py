from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from fractal.core.base.entity import GlobalState, InternalState


@dataclass
class StrategyMetrics:
    """
    Default metrics of the strategy.
    """
    accumulated_return: float  # total return of the strategy
    apy: float                 # annualized return
    sharpe: float              # risk-adjusted return
    max_drawdown: float        # maximum drawdown


@dataclass
class StrategyResult:
    """
    Result of the strategy running.
    It contains the timestamps, internal states, global states of all entities
    and total balances

    Methods:
        get_metrics(data: pd.DataFrame) -> StrategyMetrics
        get_default_metrics() -> StrategyMetrics
        to_dataframe() -> pd.DataFrame
    """
    timestamps: List[datetime]
    internal_states: List[Dict[str, InternalState]]
    global_states: List[Dict[str, GlobalState]]
    balances: List[Dict[str, float]]

    def get_metrics(self, data: pd.DataFrame, notional_price: Optional[str | float] = None) -> StrategyMetrics:
        """
        Calculate metrics of the strategy by StrategyResult data.
        StrategyResult data can be generated by to_dataframe() method.

        Args:
            data (pd.DataFrame): DataFrame with the result.
            notional_price (Optional[str | float], optional): Notional price of the asset.
                If it is None, the notional price is 1.
                If it is a string, the notional price is column name of the DataFrame {entity}_{state_name}
                For example, if notional_price='SPOT_price', the notional price is price of global_state of SPOT.
                If it is a float, the notional price is the value of the float.

        Returns:
            StrategyMetrics: Metrics of the strategy.
        """
        data = data.sort_values('timestamp').copy()
        if notional_price is None:
            notional_price = 1
        elif isinstance(notional_price, str):
            notional_price = data[notional_price].values
        elif isinstance(notional_price, float):
            pass
        else:
            raise ValueError("notional_price must be None, str or float")
        data['net_balance'] /= notional_price
        accumulated_return: float = data['net_balance'].iloc[-1] / data['net_balance'].iloc[0] - 1
        total_seconds: float = (data['timestamp'].iloc[-1] - data['timestamp'].iloc[0]).total_seconds()
        total_years: float = total_seconds / (60 * 60 * 24 * 365)
        apy = accumulated_return / total_years
        data_frequency = len(data) / total_years

        net_balance_std = data['net_balance'].pct_change().std()
        if net_balance_std == 0:
            sharpe = 0
        else:
            sharpe = data['net_balance'].pct_change().mean() / net_balance_std
        sharpe *= np.sqrt(data_frequency)  # annualize sharpe

        net_balance = data['net_balance'].values
        cumulative_max = np.maximum.accumulate(net_balance)
        drawdowns = net_balance / cumulative_max - 1
        max_drawdown = np.min(drawdowns)

        return StrategyMetrics(
            accumulated_return=accumulated_return,
            apy=apy,
            sharpe=sharpe,
            max_drawdown=max_drawdown
        )

    def get_default_metrics(self) -> StrategyMetrics:
        """
        Calculate default metrics of the strategy.

        Returns:
            StrategyMetrics: Metrics of the strategy.
        """
        data = self.to_dataframe()
        return self.get_metrics(data)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the result to a DataFrame.

        Returns:
            pd.DataFrame: DataFrame with the result.
        """
        columns = ['timestamp']
        columns += [f"{entity_name}_{field}"
                    for entity_name in self.internal_states[0]
                    for field in self.internal_states[0][entity_name].__dict__]
        columns += [f"{entity_name}_{field}"
                    for entity_name in self.global_states[0]
                    for field in self.global_states[0][entity_name].__dict__]
        columns += [f"{entity_name}_balance" for entity_name in self.balances[0]]
        data = []
        for i, _ in enumerate(self.timestamps):
            row = [self.timestamps[i]]
            for entity_name in self.internal_states[i]:
                row += list(self.internal_states[i][entity_name].__dict__.values())
            for entity_name in self.global_states[i]:
                row += list(self.global_states[i][entity_name].__dict__.values())
            for entity_name in self.balances[i]:
                row.append(self.balances[i][entity_name])
            data.append(row)
        df = pd.DataFrame(data, columns=columns)
        df['net_balance'] = df[[col for col in df.columns if 'balance' in col]].sum(axis=1)
        return df
