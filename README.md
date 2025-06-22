# ⚔️ Kubepwn – The Ultimate Kubernetes Red-Team Lab — Hack. Exploit. Own. like a Pro!!!

Kubepwn is a deliberately vulnerable Kubernetes lab environment designed for red teamers, penetration testers, and security researchers to simulate real-world attacks in a controlled, isolated cluster. It demonstrates the full kill chain — from web application exploitation to container breakout and potential node-level compromise — all within a local 'kind' cluster.

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Local%20Cluster-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-black?style=for-the-badge&logo=flask&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-Mapped-red?style=for-the-badge)

📌 Overview
Kubepwn provides:
- A Flask-based vulnerable web application
- Multiple attack surfaces
- Host-mounted container with 'privileged' access
- Realistic infrastructure using Kubernetes constructs
- Visual aids for MITRE ATT&CK and cyber kill chain

> ⚠️ For educational and research use only. Never deploy in production environments.

### 🧩 Lab Architecture
        kind (Kubernetes in Docker)
        └── kubepwn namespace
        └── kubepwn Pod (privileged)
        ├── Mounted host root filesystem (/)
        ├── Mounted containerd.sock
        └── Flask app running on port 8080

 💣 Attack Vectors
| Exploit                                   | Route / Trigger      | Description                                                                  |
| ----------------------------------------- | -------------------- | ---------------------------------------------------------------------------- |
| **Remote Code Execution (RCE)**           | `/rce`               | Execute arbitrary system commands via `subprocess` with unsanitized input.   |
| **Server-Side Template Injection**        | `/template`          | Exploit Jinja2 to run code via unsanitized user template input.              |
| **Server-Side Request Forgery (SSRF)**    | `/ssrf?url=...`      | Trigger backend server to request arbitrary internal/external URLs.          |
| **Insecure File Upload**                  | `/upload`            | Upload arbitrary files without validation, enabling script/webshell attacks. |
| **Sensitive Keys in Codebase**            | `/secrets`           | Exposes hardcoded secrets via insecure Python import (`secretdata.creds`).   |
| **Reverse Shell + Privilege Escalation**  | `/rce` with payload  | Obtain a reverse shell and escalate privileges using                         |
| **Kubernetes Enumeration (Post-Exploit)** | via reverse shell    | Enumerate container/host/K8s environment to pivot or escalate access.        |
| **Full Kubernetes compromise**            | via reverse shell    | compromise the full compromise after privilege escalation                    |


### 📦 File Structure
      Kubepwn/
      ├── app.py # Flask web application
      ├── deploy.py # Deployment helper (optional)
      ├── Dockerfile # Builds kubepwn-app image
      ├── kind-config.yaml # Kind cluster configuration
      ├── kubepwn-app.yaml # Kubernetes deployment/service manifest
      ├── static/ # Static assets (CSS, images)
      ├── templates/ # Jinja2 HTML templates
      └── README.md # This file


 ⚙️ Installation
# 1. Clone the repository
        git clone https://github.com/yourusername/kubepwn.git
        cd kubepwn

# 2. Pre-requisites
        >= python3.10

# Install kubectl
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/

# Install kind
        sudo apt update
        curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
        chmod +x kind
        sudo mv kind /usr/local/bin/
        sudo apt install docker.io docker-cli docker-compose 
        sudo systemctl enable docker
        sudo systemctl start docker
        sudo usermod -aG docker $USER
        sudo systemctl stop docker 
        sudo systemctl start docker
        sudo systemctl status docker

# 3. Deploy the lab
        python3 deploy.py

# 4. Access the Lab
        Navigate to: [http://localhost:8080](http://localhost:8080)


### 🎯 MITRE ATT\&CK Mapping
        Kubepwn aligns its techniques to the MITRE ATT\&CK for Containers framework.
                | Tactic               | Technique                                 |
                | -------------------- | ----------------------------------------- |
                | Initial Access       | Exploit Public-Facing Application (T1190) |
                | Execution            | Command and Scripting Interpreter (T1059) |
                | Privilege Escalation | Escape to Host (T1611)                    |
                | Discovery            | System Information Discovery (T1082)      |
                | Lateral Movement     | Kubernetes Exec into Container (T1609)    |
                | Collection           | Data from Local System (T1005)            |

Visual diagrams for both MITRE mapping and the cyber kill chain are available in the UI.

 📚 Learning Objectives
* Understand common container and Kubernetes misconfigurations
* Practice exploiting containers, clusters in a K8s
* Simulate container breakout via privileged access
* Map red team techniques to blue team detections

 🔐 Security Disclaimer
Kubepwn is intentionally insecure and must only be used in isolated, local environments for learning and ethical research.

* Do not expose to public or production clusters.
* Creator holds no liability for misuse or damage caused.

 👨‍💻 Author
Created with ❤️ by Deepanshu Khanna
🔗 [LinkedIn](https://www.linkedin.com/in/deepanshukhanna/) • 🛡️ Security Researcher

 📝 License
This project is licensed under the [MIT License](LICENSE).

## Support This Project

If you find **Kubepwn** useful and want to support its development, you can buy me a coffee:

**UPI ID:** "alivejatt@oksbi"


Or scan the QR code below using any UPI app (Google Pay, PhonePe, Paytm, etc.):
![UPI QR Code](https://api.qrserver.com/v1/create-qr-code/?data=upi://pay?pa=alivejatt@oksbi&size=200x200)

[![Pay via UPI](https://img.shields.io/badge/Pay%20via-UPI-blue?style=for-the-badge&logo=google-pay)](upi://pay?pa=alivejatt@oksbi&pn=Kubepwn+Support&cu=INR)
