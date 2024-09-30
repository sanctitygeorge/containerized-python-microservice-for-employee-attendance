# User Attendance Microservice API

The **User Attendance Microservice API** is a Python-based web application designed for managing staff attendance, providing features for staff registration, attendance marking, and an admin dashboard for managing staff. The application is containerized using Docker and deployed to Azure Kubernetes Service (AKS) through Azure DevOps CI/CD pipelines.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
  - [Docker](#docker)
  - [Kubernetes](#kubernetes)
  - [CI/CD with Azure DevOps](#ci/cd-with-azure-devops)
- [Infrastructure](#infrastructure)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features
- **User Registration**: New staff members can register via a browser form.
- **Login & Attendance Marking**: Staff can log in and mark their attendance.
- **Admin Dashboard**: Admin users can view attendance records and manage staff.
- **REST API**: Exposes endpoints for integration with other services.
- **Security & Robustness**: Secured application with Azure best practices.

## Architecture

This application follows a microservice architecture with the following components:
- **Python Flask Application**: For managing the backend logic.
- **Docker**: Containerization of the application.
- **Azure Kubernetes Service (AKS)**: Orchestrates containers in production.
- **Azure DevOps**: For CI/CD, automating the build, testing, and deployment pipelines.

Below is a simplified diagram of the deployment workflow:

![Workflow Diagram](path/to/your/simplified-diagram.png)
![image](https://github.com/user-attachments/assets/a8fe1038-c8d5-4da3-ae22-45e7972a6044)


## Tech Stack
- **Language**: Python 3.11
- **Framework**: Flask
- **Database**: Azure SQL Database
- **Containerization**: Docker
- **Orchestration**: Kubernetes (AKS)
- **CI/CD**: Azure DevOps
- **Monitoring**: Prometheus, Grafana, DataDog (optional)

## Installation

### Prerequisites
- Python 3.11
- Docker
- Azure CLI
- Kubernetes CLI (kubectl)
- Terraform (for infrastructure as code)
  
### Cloning the Repository
```bash
git clone https://github.com/your-username/user-attendance-microservice-api.git
cd user-attendance-microservice-api
```

## Running Locally

1. Create a `.env` file in the root of the project with the following environment variables:
   ```bash
   DB_CONNECTION_STRING=your_db_connection_string
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:
   ```bash
   python run.py
   ```

4. Navigate to `http://localhost:5000` in your browser.

## Deployment

### Docker
To build and run the application inside a Docker container:
```bash
docker build -t attendance-microservice .
docker run -p 5000:5000 attendance-microservice
```

### Kubernetes
1. Build the Docker image:
   ```bash
   docker build -t <your-acr-name>.azurecr.io/attendance-microservice:latest .
   ```

2. Push the Docker image to Azure Container Registry (ACR):
   ```bash
   docker push <your-acr-name>.azurecr.io/attendance-microservice:latest
   ```

3. Apply the Kubernetes manifest files to deploy to AKS:
   ```bash
   kubectl apply -f kubernetes-deployment.yaml
   ```

### CI/CD with Azure DevOps

1. The CI/CD pipeline is defined in the `azure-pipelines.yml` file. The pipeline performs the following tasks:
   - Builds the Docker image.
   - Pushes the image to ACR.
   - Deploys the container to AKS.
  
2. Terraform is used to provision Azure resources like AKS, ACR, and a resource group.

3. For more details on setting up the CI/CD pipeline, refer to [this link](https://docs.microsoft.com/azure/devops/pipelines/).

## Infrastructure

Terraform is used to provision the following Azure resources:
- **Resource Group**
- **Azure Kubernetes Service (AKS)**
- **Azure Container Registry (ACR)**
  
To deploy the infrastructure:
```bash
cd terraform
terraform init
terraform apply
```

## Environment Variables

Ensure the following environment variables are configured:

```bash
DB_CONNECTION_STRING=your_azure_sql_db_connection_string
ACR_NAME=your_acr_name
AKS_CLUSTER_NAME=your_aks_cluster_name
```

## API Documentation

The REST API allows CRUD operations for managing staff attendance and users.

### Endpoints:
- **POST /register**: Register a new staff member.
- **POST /login**: Login an existing staff member.
- **POST /attendance**: Mark attendance for the logged-in user.
- **GET /attendance**: Admin view for all attendance records.
  
You can explore the API using tools like [Postman](https://www.postman.com/) or [Swagger](https://swagger.io/).

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any feature additions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links
- **GitHub Repository**: [Link to the project repository](https://github.com/sanctitygeorge/user-attendance-microservice-api)
