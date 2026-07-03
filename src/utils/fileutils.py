import yaml
import numpy as np

def setup_config(config_path: str, logger) -> dict:
    
    logger.info(f"Attempting to load configuration from: {config_path}")
    
    try:
    # Loading the file safely
        with open(config_path, 'r') as stream:
            config = yaml.safe_load(stream)

    except Exception as e:
        logger.error("Failed to read config file : %s", e)
        raise
        
    # validating the compulsory keys
    req_keys = {"seed", "window", "version"}
    if not config or not req_keys.issubset(config.keys()):
        _error = "Config missing required fields. Expected: {req_keys}"
        logger.error(_error)
        raise ValueError(_error)
    
    logger.info(f"Config loaded successfully: Version={config['version']}, Window={config['window']}, Seed={config['seed']}")
    
    np.random.seed(config["seed"])
    logger.debug(f"Global random seed set to {config['seed']}.")

    return config