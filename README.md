# QuantumHealthChain: A Post-Quantum KYBER-FALCON Key Exchange and Blockchain-Backed Framework for TamperProof Electronic Health Records

A robust, enterprise-grade healthcare management framework that integrates **Post-Quantum Cryptography (Kyber)** with **Ethereum Blockchain technology** to protect Electronic Health Records (EHR) against future quantum computing vulnerabilities.

---

## 📌 Project Overview
Traditional cryptographic algorithms (such as RSA and ECC) are vulnerable to decryption by quantum computers utilizing Shor's algorithm. **QuantumHealthChain** addresses this threat by combining lattice-based post-quantum key exchange mechanisms (`Kyber.py`, `QuantumEncryption.py`) with decentralized smart contracts (`Healthcare.sol`) deployed on a local Ethereum network. This guarantees confidentiality, integrity, and tamper-proof storage of medical records, appointments, and prescriptions.

---

## 🛠️ Tech Stack & Architecture
* **Backend Framework:** Python, Django (`manage.py`, `HealthcareApp/`)
* **Blockchain & Web3:** Solidity (`Healthcare.sol`), Web3.py, Compiled Contract ABI (`Healthcare.json`)
* **Post-Quantum Security:** Custom Kyber and Quantum Encryption modules (`Kyber.py`, `QuantumEncryption.py`)
* **Database & Storage:** SQLite (`db.sqlite3`) / Secure Local Encrypted Storage
* **Execution & Deployment Utilities:** Batch scripts (`runServer.bat`)

---

## 📁 Repository Structure
```text
QuantumHealthChain/
│
├── __pycache__/                # Python compiled bytecode cache
├── Healthcare/                 # Django project core configuration files (settings, wsgi, urls)
├── HealthcareApp/              # Core application module (views, templates, static files)
├── Batch-17 Document.pdf       # Comprehensive project report and technical documentation
├── concept.txt                 # Project concept and abstract details
├── db.sqlite3                  # Local database for user authentication and records
├── execution.mp4               # Project demonstration and execution video
├── Healthcare.json             # Compiled smart contract ABI configuration
├── Healthcare.sol              # Smart contract source code for EHR management
├── Kyber.py                    # Post-quantum Kyber key exchange implementation
├── Major Project.pptx          # Technical presentation slides
├── manage.py                   # Django command-line utility
├── QuantumEncryption.py        # Quantum-resistant encryption and decryption utilities
├── README.md                   # Project documentation and setup guide
├── requirements.txt            # Python package dependencies
└── runServer.bat               # Windows batch script for quick server startup