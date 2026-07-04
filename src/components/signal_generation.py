import pandas as pd
import numpy as np
import logging

def rolling_mean(series: pd.Series, window: int) -> pd.Series:
    """
    Boundary Condition Handling:
    We use standard pandas rolling logic, which leaves the first (window - 1) rows 
    as NaN. We deliberately leave these as NaN here because our vectorized 
    signal generator will safely evaluate (close > NaN) as False, cleanly 
    defaulting those initial boundary rows to a signal of 0 without dropping them.
    """

    return series.rolling(window=window).mean()

def binary_signals(series: pd.Series, rolling_mean_series: pd.Series) -> pd.Series:
    """
    Internal helper to vectorize the signal generation logic.
    Returns a pd.Series of integers (1 if close > rolling_mean, else 0),
    preserving the input index and alignment.
    """
    result = np.where(series > rolling_mean_series, 1, 0)
    return pd.Series(result, index=series.index, name="signal").astype(int)

def compute_pipeline_signals(df: pd.DataFrame, window: int, logger: logging.Logger) -> pd.DataFrame:
    """The public interface called by run.py."""
    
    logger.info(f"Initiating signal generation pipeline. Window size: {window}")
    processed_df = df.copy()

    logger.debug("Calculating rolling mean on 'close' column.")
    processed_df['rolling_mean'] = rolling_mean(processed_df['close'], window)

    logger.debug("Evaluating threshold for binary signals.")
    processed_df['signal'] = binary_signals(processed_df['close'], processed_df['rolling_mean'])
    
    logger.info("Signal pipeline execution successful.")
    return processed_df