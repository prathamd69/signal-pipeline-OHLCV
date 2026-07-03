import argparse
from pathlib import Path
from src.utils import (configLogger,
                       setup_config)

def parse_arguments():

    parser = argparse.ArgumentParser(description="Signal Pipeline")
    
    parser.add_argument("--input", type=Path, required=True, help="Path to the input OHLCV data.csv")
    parser.add_argument("--config", type=Path, required=True, help="Path to the config.yaml file")
    parser.add_argument("--output", type=Path, required=True, help="Path for metrics.json to be saved")
    parser.add_argument("--log-file", type=Path, required=True, help="Path to write run.log")
    
    return parser.parse_args()

def main():
    args = parse_arguments()

    #setting up logger
    logger = configLogger("runs", args.log_file)
    logger.info("Job initialized and starting.")

    #setting up config file
    config = setup_config(args.config, logger)

if __name__ == "__main__":
    main()