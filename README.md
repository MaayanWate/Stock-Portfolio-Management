# Stock Portfolio Manager

Stock Portfolio Manager is a microservices-based system for managing stock portfolios, calculating capital gains, and ensuring persistent data storage. The system is built with **Docker Compose**, **NGINX**, and **MongoDB**, providing a scalable and reliable architecture.

---

## Features

- **Stock Management**:
  - View and manage multiple stock portfolios.
  - Retrieve details of individual stocks.
- **Capital Gains Calculation**:
  - Calculate total and filtered capital gains.
- **Data Persistence**:
  - All stock data is stored in **MongoDB**.
- **Failover Recovery**:
  - Services automatically restart after failure.
- **Load Balancing**:
  - NGINX implements weighted round-robin load balancing.

---

## Prerequisites

Before running the application, ensure you have the following installed:
1. [Docker](https://www.docker.com/)
2. [Docker Compose](https://docs.docker.com/compose/)

---

## Setup and Deployment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Start the application**:
   Run the following command to build and start the containers:
   ```bash
   docker-compose up -d
   ```

3. **Verify that the containers are running**:
   Use the following command to list all running containers:
   ```bash
   docker ps
   ```

4. **Access the services**:
   - **stocks1** API: `http://localhost/stocks1`
   - **stocks2** API: `http://localhost/stocks2`
   - **Capital Gains** API: `http://localhost/capital-gains`

---

## API Endpoints

### Stocks Service
- **GET /stocks1**: Returns a list of stocks in the first portfolio.
- **GET /stocks1/{id}**: Returns details of a stock in the first portfolio by ID.
- **GET /stocks2**: Returns a list of stocks in the second portfolio.
- **GET /stocks2/{id}**: Returns details of a stock in the second portfolio by ID.

### Capital Gains Service
- **GET /capital-gains**: Calculates total capital gains across all portfolios.
- **GET /capital-gains?portfolio=stocks1&numsharesgt=10**:
  - Filters capital gains based on:
    - `portfolio`: `stocks1` or `stocks2`.
    - `numsharesgt`: Greater than a specified number of shares.
    - `numshareslt`: Less than a specified number of shares.

---

## Persistence and Recovery

- **Data Persistence**:  
  All stock data is stored in **MongoDB**, ensuring it is retained even after container restarts.

- **Failover Recovery**:  
  Docker Compose automatically restarts services in case of failure using the `restart: always` policy.

---

## Load Balancing

NGINX implements weighted round-robin load balancing:
- **stocks1**:
  - Instance A: Handles 3 requests for every 1 request to Instance B.
- **stocks2**:
  - Single instance (no load balancing).

---

## Project Structure

```
.
├── docker-compose.yml        # Orchestrates all services
├── stocks1/                  # Microservice for stocks1
├── stocks2/                  # Microservice for stocks2
├── capital-gains/            # Microservice for capital gains
├── nginx/                    # NGINX configuration files
├── mongo-init/               # MongoDB initialization scripts
└── README.md                 # Project documentation
```

---

## Authors

- **Maayan Wate**
- **May Bourshan**

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

