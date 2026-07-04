import argparse
from pathlib import Path
import json
import yaml
import time
from typing import Dict, Any
import sys
import numpy as np
from src.utils import (configLogger,
                       setup_config)
from src.components import (compute_pipeline_signals,
                            data_loading)

def parse_arguments():

    parser = argparse.ArgumentParser(description="Signal Pipeline")
    
    parser.add_argument("--input", type=Path, required=True, help="Path to the input OHLCV data.csv")
    parser.add_argument("--config", type=Path, required=True, help="Path to the config.yaml file")
    parser.add_argument("--output", type=Path, required=True, help="Path for metrics.json to be saved")
    parser.add_argument("--log-file", type=Path, required=True, help="Path to write run.log")
    
    return parser.parse_args()

def write_metrics(output_path: Path, metrics: Dict[str, Any]) -> None:
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(json.dumps(metrics, indent=4))


def main():
    start_time_ns = time.perf_counter_ns()

    args = parse_arguments()

    #setting up logger
    logger = configLogger("runs", args.log_file)
    logger.info("Job initialized and starting.")

    #setting up config file
    config = setup_config(args.config, logger)
    logger.info("Reading config for parameters.")

    seed = config['seed']
    window = config['window']
    version = config['version']

    #just to be safe.
    np.random.seed(seed)

    try:
        df = data_loading(args.input, logger)

        processed_df = compute_pipeline_signals(df, window, logger)

        rows_processed = len(processed_df)
        signal_rate = float(processed_df['signal'].mean())

        end_time_ns = time.perf_counter_ns()
        latency_ms = int((end_time_ns - start_time_ns) / 1e6)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }
        
        logger.info(f"Pipeline execution complete. Writing metrics at {args.output}")
        write_metrics(args.output, metrics)
        sys.exit(0)

    except Exception as e:
        logger.error("Pipeline execution failed: %s", e)

        metrics = {
            "version": version,
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, metrics)
        sys.exit(1)

if __name__ == "__main__":
    main()