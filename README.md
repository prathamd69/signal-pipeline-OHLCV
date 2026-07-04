# Signal-pipeline-OHLCV

A minimal, deployment-ready MLOps batch job that calculates binary trading signals from OHLCV market data using a deterministic, Dockerized Python pipeline.

---

## Architecture & Features

- **Reproducibility**: Guarantees deterministic behavior by applying a global random seed directly through runtime configuration (`config.yaml`).
- **Robust Ingestion**: Employs an armored data-loading component that automatically isolates, re-aligns, and parses maliciously "squashed" CSV input strings.
- **Vectorized Engine**: Utilizes lightning-fast NumPy vectorization (`np.where`) to evaluate rolling thresholds under strict boundary condition context handling.
- **Zero-Pollution Observability**: Routes granular debugging and lifecycle milestones exclusively to `run.log`, leaving `stdout` perfectly clear for automated system consumers.
- **Automated CI/CD**: Integrated with GitHub Actions to continuously test Docker builds and container executions on any push or PR to the `main` branch.

---

## Local Run Instructions

### 1. Installation
Ensure you have Python 3.9+ installed, establish a virtual environment, and load dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Pipeline

Execute the application using the required CLI layout:

```bash python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log ```

### 3. Docker Build & Run

The environment is fully containerized to ensure platform-independent execution and eliminate hardcoded paths.

### Build the Image

```bash docker build -t mlops-task . ```

### Run the Container

The container executes automatically via a default command configuration, printing final metrics JSON to stdout and exiting cleanly.

```bash   docker run --rm mlops-task   ```

Example Outputs
---------------

### Example metrics.json (Successful Run)

When executed successfully, the system logs and saves the precise JSON structure required for downstream aggregation:

```JSON
  { "version": "v1",      
    "rows_processed": 10000,      
    "metric": "signal_rate",      
    "value": 0.4989,      
    "latency_ms": 59,      
    "seed": 42,      
    "status": "success"  
  }   
```

### Example metrics.json (Unsuccessful Run)

```JSON
  { "version": "v1",            
    "status": "error",
    "error_message": "what went wrong"
  }   
```