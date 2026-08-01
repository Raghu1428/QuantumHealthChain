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

## ✨ Key Features
* **Secure File Upload and Storage:** Patients, doctors, and hospitals can securely upload and store medical records like prescriptions and diagnostic results, protecting them from unauthorized access or modification.

* **Post-Quantum Encryption:** The system utilizes post-quantum cryptographic algorithms, specifically KYBER for key encapsulation and FALCON for signing, to encrypt patient files and protect them against both classical and future quantum computer attacks.

* **Blockchain-Based Logging:** All data transactions—including file uploads, downloads, and access actions—are recorded on a decentralized, tamper-proof blockchain network, ensuring transparency and traceability.

* **Secure File Sharing:** The platform enables the secure sharing of medical records between institutions and patients using encrypted session keys, preventing interception during transmission.

* **Access Control and Authentication:** Role-based access control ensures that only verified users (doctors, patients, and administrators) are granted appropriate permissions to access sensitive medical information.

* **Data Integrity and Privacy Protection:** The integration of blockchain and encryption ensures that patient data remains accurate and private, and any attempt to manipulate the stored information can be easily detected.

## ⚙️ Core System Modules
The primary workflows and operations managed by the system include:
* User Registration
* User Login
* Appointment Booking
* Prescription Generation
* View Report

## 👥 Project Team
This major project was developed at the Department of Information Technology, CMR Technical Campus:
* **A Sahithi** (227R1A1265)
* **K Raghunath** (227R1A1298)
* **B Nikhil** (227R1A1271)