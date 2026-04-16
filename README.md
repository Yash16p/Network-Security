# Network Security - Phishing Detection ML Pipeline

A production-ready machine learning pipeline for detecting phishing attacks in network traffic. This project implements an end-to-end ML workflow with automated data ingestion, validation, transformation, model training, and deployment on AWS ECS with CI/CD via GitHub Actions.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Monitoring & Artifacts](#monitoring--artifacts)

## 🎯 Overview

This project detects phishing attacks using machine learning by analyzing network security data. It provides:

- **Automated ML Pipeline**: End-to-end data processing and model training
- **REST API**: FastAPI-based inference server for real-time predictions
- **Cloud Integration**: AWS S3 for artifact storage and ECS for containerized deployment
- **CI/CD Automation**: GitHub Actions for continuous integration and deployment
- **Experiment Tracking**: MLflow integration for model versioning and monitoring

## ✨ Features

- **Data Ingestion**: Automated data fetching from MongoDB with feature store creation
- **Data Validation**: Schema validation and data drift detection
- **Data Transformation**: Feature engineering and preprocessing with scikit-learn
- **Model Training**: Scikit-learn based classification models with hyperparameter tuning
- **Batch Predictions**: Process CSV files for bulk inference
- **Interactive UI**: HTML-based table visualization for prediction results
- **S3 Integration**: Automatic artifact and model syncing to AWS S3
- **Docker Support**: Containerized deployment ready for ECS
- **Comprehensive Logging**: Structured logging for debugging and monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                      │
│  (Lint → Test → Build Docker → Push to ECR → Deploy to ECS) │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ /train       │  │ /predict     │  │ /docs        │       │
│  │ (Pipeline)   │  │ (Inference)  │  │ (Swagger UI) │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  ML Training Pipeline                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Data         │  │ Data         │  │ Data         │       │
│  │ Ingestion    │→ │ Validation   │→ │ Transformation│      │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                              ↓                               │
│                    ┌──────────────────┐                      │
│                    │ Model Training   │                      │
│                    │ & Evaluation     │                      │
│                    └──────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AWS Cloud Storage                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ S3 Artifacts │  │ S3 Models    │  │ ECR Images   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
network-security/
├── networksecurity/              # Main package
│   ├── components/               # ML pipeline components
│   │   ├── data_ingestion.py     # MongoDB data fetching
│   │   ├── data_validation.py    # Schema & drift validation
│   │   ├── data_transformation.py # Feature engineering
│   │   └── model_trainer.py      # Model training & evaluation
│   ├── pipeline/                 # Orchestration
│   │   ├── training_pipeline.py  # End-to-end training workflow
│   │   └── batch_prediction.py   # Batch inference
│   ├── cloud/                    # AWS integration
│   │   └── s3_syncer.py          # S3 sync utilities
│   ├── entity/                   # Data models
│   │   ├── config_entity.py      # Configuration classes
│   │   └── artifact_entity.py    # Artifact definitions
│   ├── constant/                 # Constants & configs
│   ├── exception/                # Custom exceptions
│   ├── logging/                  # Logging setup
│   └── utlis/                    # Utility functions
├── app.py                        # FastAPI application
├── main.py                       # Entry point
├── Dockerfile                    # Container configuration
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── .github/workflows/main.yml    # CI/CD pipeline
├── final_model/                  # Trained models
│   ├── model.pkl                 # Serialized model
│   └── preprocessor.pkl          # Feature preprocessor
├── Artifacts/                    # Training artifacts (timestamped)
├── logs/                         # Application logs
├── mlruns/                       # MLflow experiment tracking
└── templates/                    # HTML templates
    └── table.html                # Prediction results UI
```

## 📦 Prerequisites

- Python 3.10+
- Docker & Docker Compose
- AWS Account with S3 and ECS access
- MongoDB Atlas cluster
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/network-security.git
cd network-security
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Package

```bash
pip install -e .
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=ClusterName
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

### AWS Configuration

Ensure your AWS credentials are configured:

```bash
aws configure
```

### GitHub Secrets

Add the following secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_REGION`: AWS region (e.g., us-east-1)
- `ECR_REPOSITORY_NAME`: ECR repository name
- `AWS_ECR_LOGIN_URI`: ECR login URI

## 💻 Usage

### Training the Model

#### Option 1: Via API

```bash
python app.py
# Then visit http://localhost:8000/train
```

#### Option 2: Direct Pipeline

```python
from networksecurity.pipeline.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline()
model_artifact = pipeline.run_pipeline()
```

### Making Predictions

#### Option 1: Via API (Web UI)

1. Start the application: `python app.py`
2. Navigate to `http://localhost:8000/docs`
3. Upload a CSV file to the `/predict` endpoint
4. View results in the interactive table

#### Option 2: Batch Prediction

```python
from networksecurity.pipeline.batch_prediction import BatchPredictionPipeline

batch_pipeline = BatchPredictionPipeline()
predictions = batch_pipeline.predict('path/to/data.csv')
```

## 🔌 API Endpoints

### 1. Training Endpoint

```
GET /train
```

Triggers the complete ML pipeline:
- Data ingestion from MongoDB
- Data validation
- Feature transformation
- Model training
- Artifact sync to S3

**Response**: `"Training is successful"`

### 2. Prediction Endpoint

```
POST /predict
Content-Type: multipart/form-data

file: <CSV file>
```

Accepts a CSV file and returns predictions with an HTML table visualization.

**Response**: HTML table with predictions

### 3. Documentation

```
GET /docs
```

Interactive Swagger UI for API exploration and testing.

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`main.yml`) implements a three-stage pipeline:

### Stage 1: Continuous Integration
- Checkout code
- Lint code
- Run unit tests

### Stage 2: Continuous Delivery
- Build Docker image
- Tag with latest version
- Push to Amazon ECR

### Stage 3: Continuous Deployment
- Pull latest image from ECR
- Run Docker container on self-hosted runner
- Expose service on port 8080
- Clean up old images

**Trigger**: Automatic on push to `main` branch (excluding README.md changes)

## 🐳 Deployment

### Local Docker Deployment

```bash
# Build image
docker build -t network-security:latest .

# Run container
docker run -d -p 8000:8000 \
  -e MONGO_DB_URL="your_mongo_url" \
  -e AWS_ACCESS_KEY_ID="your_key" \
  -e AWS_SECRET_ACCESS_KEY="your_secret" \
  -e AWS_REGION="us-east-1" \
  network-security:latest
```

### AWS ECS Deployment

The CI/CD pipeline automatically:
1. Builds Docker image
2. Pushes to Amazon ECR
3. Deploys to ECS on self-hosted runner
4. Exposes service on port 8080

**Environment Variables** are passed via GitHub Secrets during deployment.

## 📊 Monitoring & Artifacts

### MLflow Tracking

View experiment tracking:

```bash
mlflow ui
# Visit http://localhost:5000
```

### Artifacts Structure

Training artifacts are organized by timestamp:

```
Artifacts/
├── 02_26_2025_12_20_50/
│   ├── data_ingestion/
│   │   ├── feature_store/phisingData.csv
│   │   └── ingested/
│   │       ├── train.csv
│   │       └── test.csv
│   └── data_validation/
│       ├── drift_report/report.yaml
│       └── validated/
│           ├── train.csv
│           └── test.csv
```

### S3 Sync

Artifacts are automatically synced to S3:

```
s3://training-bucket/
├── artifact/{timestamp}/
└── final_model/{timestamp}/
```

### Logs

Application logs are stored with timestamps:

```
logs/
├── 02_26_2025_12_20_49.log/
└── ...
```

## 🔧 Key Components

### Data Ingestion
- Fetches data from MongoDB
- Creates feature store CSV
- Splits into train/test sets (80/20 default)

### Data Validation
- Schema validation against defined schema
- Data drift detection
- Generates validation reports

### Data Transformation
- Feature scaling and normalization
- Categorical encoding
- Handles missing values
- Saves preprocessor for inference

### Model Training
- Scikit-learn classification models
- Hyperparameter tuning
- Cross-validation
- Model evaluation and metrics
- Saves trained model for inference

## 📝 Logging

Comprehensive logging is implemented throughout:

```python
from networksecurity.logging.logger import logging

logging.info("Processing data...")
logging.error("Error occurred", exc_info=True)
```

## ⚠️ Exception Handling

Custom exception handling with context:

```python
from networksecurity.exception.exception import NetworkSecurityException

try:
    # code
except Exception as e:
    raise NetworkSecurityException(e, sys)
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Yash Pandey**
- Email: yashpandey1626@gmail.com

## 🙏 Acknowledgments

- MongoDB for data storage
- AWS for cloud infrastructure
- FastAPI for the web framework
- Scikit-learn for ML algorithms
- MLflow for experiment tracking
