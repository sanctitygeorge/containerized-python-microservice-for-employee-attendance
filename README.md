#  User Attendance Microservice API

This repository contains a Python-based web application for staff attendance management. The application features staff registration, login, attendance marking, and an admin dashboard for managing staff and viewing attendance records. This README provides instructions for setting up, developing, containerizing, and deploying the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup and Development](#setup-and-development)
- [Containerization](#containerization)
- [Deployment to Kubernetes](#deployment-to-kubernetes)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- [Python 3.8+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) with Kubernetes enabled
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) (for Azure deployment)
- [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) (for CI/CD pipeline)

## Setup and Development

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sanctitygeorge/user-attendance-microservice-api.git
   cd staff-attendance-app
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   Create a `.env` file in the root directory and add your environment variables:

   ```
   DB_CONNECTION_STRING="DRIVER={ODBC Driver 18 for SQL Server};SERVER=your-server;DATABASE=your-db;UID=your-username;PWD=your-password;"
   ```

5. **Run the Application Locally:**

   ```bash
   python run.py
   ```

   The application should now be accessible at `http://localhost:5000`.

## Containerization

1. **Create a Dockerfile:**

   Ensure your `Dockerfile` is in the root project directory and looks like this:

   ```Dockerfile
   # Use an official Python runtime as a parent image
   FROM python:3.8-slim

   # Set the working directory
   WORKDIR /app

   # Install ODBC Driver 18 for SQL Server
   RUN apt-get update && apt-get install -y \
       curl apt-transport-https gnupg \
       && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
       && curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/msprod.list \
       && apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools18 unixodbc-dev

   # Copy the current directory contents into the container at /app
   COPY . /app

   # Install any needed packages specified in requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt

   # Set environment variables
   COPY .env /app/.env
   RUN export $(cat /app/.env | xargs)

   # Make port 5000 available to the world outside this container
   EXPOSE 5000

   # Define the command to run the application
   CMD ["python", "run.py"]
   ```

2. **Create `docker-compose.yml`:**

   ```yaml
   version: '3'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - DB_CONNECTION_STRING=${DB_CONNECTION_STRING}
   ```

3. **Build and Run the Docker Container:**

   ```bash
   docker-compose up --build
   ```

   The application should now be running inside a Docker container, accessible at `http://localhost:5000`.

## Deployment to Kubernetes

1. **Prepare Kubernetes Manifest Files:**

   Create a `deployment.yml` file:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: attendance-microservice-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: attendance-microservice
     template:
       metadata:
         labels:
           app: attendance-microservice
       spec:
         containers:
         - name: attendance-app-container
           image: your-dockerhub-username/your-docker-image:latest
           ports:
           - containerPort: 5000
           env:
           - name: DB_CONNECTION_STRING
             value: "your-database-connection-string"
   ```

   Create a `service.yml` file:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: attendance-app-service
   spec:
     selector:
       app: attendance-microservice
     ports:
       - protocol: TCP
         port: 80
         targetPort: 5000
     type: LoadBalancer
   ```

2. **Deploy to Kubernetes:**

   ```bash
   kubectl apply -f deployment.yml
   kubectl apply -f service.yml
   ```

   Access the application via the external IP provided by the LoadBalancer.

## Monitoring

To monitor logs in real-time:

```bash
kubectl logs -f -l app=attendance-microservice
```

To monitor specific pods:

```bash
kubectl get pods
kubectl logs -f <pod-name>
```

## Troubleshooting

### Common Issues

- **ImagePullBackOff/Error ImagePull:**
  Ensure the Docker image name is correct and pushed to Docker Hub or the correct registry.

- **Application Not Accessible:**
  Ensure the service type is correctly configured and the external IP is accessible.

### Viewing Detailed Logs

If your application fails, detailed logs can be viewed by running:

```bash
kubectl logs -f <pod-name>
```

For any further issues, please refer to the Kubernetes and Docker documentation or open an issue on this repository.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your idea.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
