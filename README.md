# Crypto-Currency Blockchain Backend API

This project implements a fully functional blockchain backend API for a cryptocurrency, built using Flask (Python), Pub/Sub for real-time communication, Elliptic Curve Digital Signature Algorithm (ECDSA) for secure transactions, and includes comprehensive unit tests.

## Features

* **Blockchain Core:**
    * Implements a decentralized blockchain data structure.
    * Includes block creation, validation, and chain management.
    * Handles transaction processing and block mining.
* **Mining and Reward System:**
    * Implements a Proof-of-Work (PoW) mining algorithm.
    * Distributes block rewards to miners.
    * Difficulty adjustment for consistent block generation times.
* **Transaction Management:**
    * Creates and verifies transactions.
    * Uses ECDSA for secure transaction signing and verification.
    * Manages transaction pools.
* **Real-time Communication (Pub/Sub):**
    * Utilizes Pub/Sub (e.g., Redis Pub/Sub, Google Cloud Pub/Sub) for real-time updates.
    * Broadcasts new blocks and transactions to connected nodes.
* **Flask API:**
    * Provides RESTful API endpoints for interacting with the blockchain.
    * Endpoints for retrieving blockchain data, submitting transactions, and mining.
* **Security:**
    * Employs ECDSA for secure transaction signing and verification.
    * Protects against tampering and double-spending.
* **Unit Tests:**
    * Includes 40+ comprehensive unit tests covering all core functionalities.
    * Ensures code reliability and stability.

## Prerequisites

* Python 3.8+
* pip (Python package installer)
* Virtual environment (recommended)
* Redis or Google Cloud Pub/Sub (for real-time communication)

**Activate the env**
```
conda activate block
```


**Install all the packages**
```
conda install -r requirment.txt
```


**To Run Tests: ACTIVATE ENVIRMENT FIRST**
```
python -m pytest backend/tests
```


**Run the application and API after activating the env**
```
python -m backend.py
```


**Run the frontend** 
```
cd ./frontend/ && npm run start
```
* **API Endpoints:**
    * Refer to the API documentation (e.g., Swagger or Postman collection) for details on available endpoints.
    * Examples:
        * `/blockchain`: Retrieve the blockchain.
        * `/transaction`: Submit a transaction.
        * `/mine`: mine a new block.
* **Real-time Updates:**
    * Connect to the Pub/Sub channels to receive real-time updates on new blocks and transactions.
* **Wallet Management:**
    * The wallet class handles the creation of public and private keys, and the signing of transactions.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

[Specify your license here, e.g., MIT License]

## Future Enhancements

* Implement a more robust consensus algorithm (e.g., Proof-of-Stake).
* Add support for smart contracts.
* Improve API documentation.
* Implement a more sophisticated wallet management system.
* Add more extensive logging and monitoring.
* Implement a peer-to-peer network layer.
* Add a user authentication system.
* Working on a front end with React website to interact with the API.
