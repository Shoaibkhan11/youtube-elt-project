# 🎥 YouTube Data Engineering Pipeline

A complete **Data Engineering Project** that extracts YouTube channel statistics using the **YouTube API**, transforms raw data into a structured JSON format, and loads it into a **PostgreSQL Data Warehouse**. The entire workflow is orchestrated using **Apache Airflow**, containerized using **Docker**, and integrated with a **custom CI/CD pipeline** for automated validation on every commit.

---

## 📌 Project Overview

This project demonstrates an end-to-end **ETL/ELT Data Engineering pipeline** for ingesting and processing YouTube channel analytics data.

The pipeline:

* **Extracts** YouTube statistics using the **YouTube Data API**
* **Transforms** raw API responses into a clean, readable **JSON format**
* **Loads** transformed data into a **local PostgreSQL Data Warehouse**
* **Validates** data quality using **Soda tests**
* **Automates workflows** using **Apache Airflow DAG dependencies**
* **Implements CI/CD automation** for every commit

This project follows production-inspired data engineering practices, including orchestration, data validation, dependency handling, and containerization.

---

## 🏗️ Architecture

```text
        ┌────────────────────┐
        │    YouTube API     │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │   Airflow DAG 1    │
        │ Extract + Transform│
        │   (Python Tasks)   │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Readable JSON File │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │   Airflow DAG 2    │
        │ Load/Update DWH    │
        │    PostgreSQL      │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │   Airflow DAG 3    │
        │   Soda Data Tests  │
        └────────────────────┘
```

---

## ⚙️ Tech Stack

| Technology                    | Purpose                            |
| ----------------------------- | ---------------------------------- |
| Python                        | Data extraction and transformation |
| YouTube Data API              | Source data ingestion              |
| Apache Airflow                | Workflow orchestration             |
| PostgreSQL                    | Local Data Warehouse               |
| Docker                        | Containerization                   |
| Soda                          | Data quality testing               |
| GitHub Actions / Custom CI/CD | Automated validation               |

---

## 🔄 Workflow

### DAG 1 — Extract & Transform

The first Airflow DAG performs:

* Fetching channel and video statistics using the **YouTube API**
* Extracting relevant metadata and metrics
* Transforming raw responses into a **clean and readable JSON structure**
* Saving transformed output as a JSON file

#### Responsibilities

* API Extraction
* Data Cleaning
* JSON Transformation
* Intermediate Storage

---

### DAG 2 — Load Data Warehouse

The second DAG depends on **DAG 1** completion.

This DAG:

* Reads transformed JSON data
* Loads data into the **PostgreSQL Data Warehouse**
* Performs **incremental updates/upserts** to avoid duplicates
* Keeps warehouse data updated with latest statistics

#### Responsibilities

* Data Loading
* Incremental Updates
* Warehouse Synchronization

---

### DAG 3 — Soda Data Quality Tests

The third DAG performs **Soda tests** to validate data quality.

Checks include:

* Null validation
* Schema validation
* Data freshness checks
* Duplicate detection
* Data consistency verification

This ensures reliable and trustworthy warehouse data.

---

## 📂 Project Structure

```bash
project-root/
│
├── dags/ main.py                   # Airflow DAG definitions
│   
│
├── dags/api/                       # YouTube API logic and Data transformation scripts
│
│
├── dags/datawarehouse/             # PostgreSQL warehouse logic
│
├── dags/dataquality                # Soda validation files
│
├── data/                           # Generated JSON files
│
├── docker-compose.yml              # Docker services
├── Dockerfile                      # Docker setup
├── requirements.txt
│
└── .github/workflows/              # Custom CI/CD workflows
```



## 🔁 DAG Dependency Flow

```text
DAG 1 (produce_json)
<img width="936" height="186" alt="image" src="https://github.com/user-attachments/assets/7588da7e-d390-4068-9b95-5f8fa61ddf67" />

            ↓
DAG 2 (update_db)
<img width="977" height="222" alt="image" src="https://github.com/user-attachments/assets/40cb5ff9-ddc2-43c4-8469-f5b4252c52d0" />

            ↓
DAG 3 (data_quality)
<img width="637" height="156" alt="image" src="https://github.com/user-attachments/assets/494e7fae-42e6-4e42-bd2f-0cbe6e27d460" />


```

Each DAG depends on successful completion of the previous DAG to maintain data integrity.

---

## ✅ CI/CD Integration

This project includes a **custom CI/CD pipeline** that automatically executes on every commit pushed to the Git branch.

### CI/CD Workflow Includes

* Dependency validation
* Code quality checks
* Pipeline verification
* Automated testing
* Workflow consistency checks

This ensures project reliability and minimizes integration issues.

---

## 🐳 Docker Support

The project is fully containerized using **Docker** for easier deployment and reproducibility.

### Benefits

* One-command setup
* Isolated environment
* Simplified dependency management
* Better reproducibility across systems

---

## ✨ Key Features

✔ End-to-End Data Engineering Pipeline
✔ YouTube API Integration
✔ Airflow Workflow Orchestration
✔ JSON Data Transformation
✔ PostgreSQL Data Warehouse
✔ Incremental Data Updates
✔ Soda Data Quality Testing
✔ Custom CI/CD Pipeline
✔ Dockerized Environment

---

## 📈 Future Improvements

* Add dashboards using **Power BI** or **Tableau**
* Deploy warehouse to cloud (**AWS / Azure / GCP**)
* Add streaming ingestion with **Apache Kafka**
* Implement **dbt transformations**
* Add monitoring and alerting

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and create a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

---

**Built with Python, Airflow, PostgreSQL, Docker, and Data Engineering principles 🚀**
