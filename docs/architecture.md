# System Architecture: Modernization-as-a-Service

## 1. High-Level Pipeline
The system follows a 5-stage pipeline designed for the IBM Cloud:

1.  **Ingestion & Normalization**: Raw COBOL is cleaned of legacy comments and column-fixed formatting.
2.  **Structural Extraction**: Regex-based analysis identifies SQL blocks, CALL statements, and Data Division structures.
3.  **Risk Intelligence (DNN)**: A Deep Neural Network (TensorFlow) classifies the program into Risk Tiers (LOW/MED/HIGH) based on 5 complexity features.
4.  **Generative Refactoring**: Metadata-grounded prompts guide the LLM to produce Java 17 code using Spring Boot 3 patterns (DI, Repositories).
5.  **Automated Audit**: The `Validator` module compares the output against source metadata to calculate a "Confidence Score."

## 2. Infrastructure
- **API Layer**: FastAPI provides asynchronous endpoints for single-file and batch modernization.
- **Scaling Layer**: PySpark RDDs enable horizontal scaling for enterprise-wide code scans.
- **Containerization**: Dockerized for seamless deployment on IBM OpenShift or Kubernetes.