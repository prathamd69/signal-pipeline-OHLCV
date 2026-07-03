import argparse
from src.utils import configLogger

def parse_arguments():

    parser = argparse.ArgumentParser(description="Signal Pipeline")
    
    parser.add_argument("--input", type=str, required=True, help="Path to the input OHLCV data.csv")
    parser.add_argument("--config", type=str, required=True, help="Path to the config.yaml file")
    parser.add_argument("--output", type=str, required=True, help="Path for metrics.json to be saved")
    parser.add_argument("--log-file", type=str, required=True, help="Path to write run.log")
    
    return parser.parse_args()

def main():
    args = parse_arguments()

    logger = configLogger("runs", args.log_file)
    logger.info("Job initialized and starting.")

if __name__ == "__main__":
    main()