import pandas as pd
import os
import numpy as np
from pathlib import Path

def data_loading(datapath : Path, logger) -> pd.DataFrame:

    logger.info(f"Attempting to load dataset from: {datapath}")

    if not os.path.exists(datapath):
            _error = f"Input file not found at path: {datapath}"
            logger.error(_error)
            raise FileNotFoundError(_error)

    if os.path.getsize(datapath) == 0:
        _error = f"The input file at {datapath} is completely empty."
        logger.error(_error)
        raise ValueError(_error)
    
    try:
        raw = pd.read_csv(datapath)

    # Invalid CSV format 
    except pd.errors.ParserError as e:
        _error = f"Invalid CSV format or parsing error: {str(e)}"
        logger.error(_error)
        raise ValueError(_error)
    
    except Exception as e:
        _error = f"Unexpected file reading error: {str(e)}"
        logger.error(_error)
        raise
    
    # Double check if DataFrame loaded is empty (maybe just col titles with no rows)
    if raw.empty:
        _error = "Dataset validation failed: The loaded file contains no data rows."
        logger.error(_error)
        raise ValueError(_error)

    # validating required column
    if 'close' not in raw.columns:
        _error = "Dataset validation failed: Required column -close- is missing."
        logger.error(_error)
        raise KeyError(_error)

    logger.info(f"Dataset loaded and validated successfully. Total rows: {len(raw)}")
    return raw