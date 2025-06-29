# ⚔️ Kubepwn – The Ultimate Kubernetes Red & Blue Team Lab — Hack. Exploit. Own. Detect. like a Pro!!!
        📡 APT-Style Attack Simulations (🔴 Offensive) and 🎯Hunt & Detect Like a Pro Threat Hunter (🕵️‍♂️ Defensive)

Kubepwn is a deliberately vulnerable Kubernetes lab environment designed for red teamers, penetration testers, and security researchers to simulate real-world attacks in a controlled, isolated cluster. It demonstrates the full kill chain — from web application exploitation to container breakout and potential node-level compromise — all within a local 'kind' cluster.

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Local%20Cluster-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-black?style=for-the-badge&logo=flask&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-Mapped-red?style=for-the-badge)

📌 Overview
Kubepwn provides:
- 🧪 A Flask-based vulnerable web application
- 🎯 Multiple attack surfaces
- 🐳 Host-mounted container with 'privileged' access
- 🔐 Host Mounts + containerd.sock exposure
- 📡 Lateral Movement simulation via `ServiceAccount` token theft
- 🐙 DaemonSet backdoor persistence
- 🎯 MITRE ATT&CK + Cyber Kill Chain Mapping
- 📈 Detection via Falco, Loki, and Grafana
- 🧹 Cleanup script for easy teardown
- 🏗️ Realistic infrastructure using Kubernetes constructs
- 🛰️ Visual aids for MITRE ATT&CK and Cyber Kill Chain


> ⚠️ For educational and research use only. Never deploy in production environments.


🛡️ Integrated Detection & Forensics Stack (🟢 Defensive)

⚙️ New! Full Detection Stack Integration

Kubepwn now integrates a production-grade detection and monitoring suite, combining open-source observability tools:

        |   Tool   |                   Purpose                       |
        | ---------| ----------------------------------------------- |
        | Falco    | Runtime threat detection for container activity |
        | Grafana  | Visual dashboard for real-time alerting         |
        | Loki     | Log aggregation for forensics & timeline        |
        | Promtail | Log shipping from pods/nodes                    |


### 🧩 Lab Architecture
        kind (Kubernetes in Docker)
        └── kubepwn namespace
        └── kubepwn Pod (privileged)
        ├── Mounted host root filesystem (/)
        ├── Mounted containerd.sock
        └── Flask app running on port 8080


---

## 💣 Attack Vectors
        
        |           Exploit Type            |     Route/Vector         | Description                                                                |
        | ----------------------------------| ----------------------- | --------------------------------------------------------------------------- |
        | **RCE**                           | `/rce`                  | Arbitrary command execution via unsanitized `subprocess` call               |
        | **SSTI**                          | `/template`             | Server-Side Template Injection in Jinja2                                    |
        | **SSRF**                          | `/ssrf?url=...`         | SSRF attack to internal/external URLs                                       |
        | **Insecure File Upload**          | `/upload`               | Uploads arbitrary files to `/var/www/html/uploads`                          |
        | **Secrets Exposure**              | `/secrets`              | Hardcoded Python imports leak credentials                                   |
        | **Reverse Shell + PrivEsc**       | `/rce` payload           | Shell access + host breakout with `privileged` pod                         |
        | **Lateral Movement (APT style)**  | `lateral-movement.yaml` | SA token theft used to exec into other pods                                 |
        | **DaemonSet Backdoor**            | `daemonset-backdoor.yaml`| Persistence via hidden DaemonSet shell backdoor                            |

---

## 📦 File Structure
        Kubepwn/
        ├── app.py # Vulnerable Flask app
        ├── deploy.py # Automated deployment (lab + detection)
        ├── cleanup.py # Teardown script
        ├── kind-config.yaml # Kind cluster configuration
        ├── kubepwn-app.yaml # App deployment + service
        ├── daemonset-backdoor.yaml # DaemonSet backdoor persistence
        ├── lateral-movement.yaml # Simulated lateral movement
        ├── promtail-values.yaml # Promtail Helm values for logging
        ├── Dockerfile
        ├── static/
        ├── templates/
        └── README.md


 ⚙️ Installation
# 1. Clone the repository
        git clone https://github.com/deep1792/kubepwn.git
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
        
        This sets up:
        Flask vulnerable app
        Kind cluster
        DaemonSet backdoor + Lateral movement vectors
        Apache for webshell access
        Falco + Loki + Grafana stack via Helm

# 4. Access the Lab
        Navigate to: 
        | Component              | URL                                                           |
        | ---------------------- | ------------------------------------------------------------- |
        | Kubepwn Lab            | [http://localhost:8080](http://localhost:8080)                |
        | Uploaded Webshells     | [http://localhost/uploads/](http://localhost/uploads/)        |
        | Grafana Dashboard      | [http://localhost:3000](http://localhost:3000)                |
        | Port Forward (Grafana) | `kubectl port-forward -n monitoring svc/loki-grafana 3000:80` |

### 🔐 Decode Grafana Admin Password: 
        kubectl get secret -n monitoring loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode && echo

### 🎯 MITRE ATT\&CK Mapping

        Kubepwn aligns its techniques to the MITRE ATT\&CK for Containers framework.
        | Tactic               | Technique                                 |
        | -------------------- | ----------------------------------------- |
        | Initial Access       | T1190 - Exploit Public-Facing Application |
        | Execution            | T1059 - Command and Scripting Interpreter |
        | Privilege Escalation | T1611 - Escape to Host                    |
        | Discovery            | T1082 - System Information Discovery      |
        | Lateral Movement     | T1609 - Kubernetes Exec into Container    |
        | Collection           | T1005 - Data from Local System            |
        | Persistence          | T1499 - DaemonSet/Cluster-wide Implant    |

🛡️ Integrated Detection & Forensics Stack (🟢 Defensive)

        ⚙️ Full Threat Detection Stack Integration (NEW!)
        Kubepwn now ships with a powerful detection + monitoring stack tailored for incident response and threat             hunting in Kubernetes:

        Tool	Role in Detection Workflow
        Falco	Real-time runtime security monitoring (system calls, process, execve, file access)
        Loki	Aggregates logs from Kubernetes pods (attack timeline, IOC correlation)
        Grafana	Visualizes logs, detection alerts, dashboards, metrics
        Promtail	Collects and ships pod logs to Loki

📊 Example Dashboards in Grafana:

        Real-Time Attack Timelines
        
        Falco Syscall Alerts (e.g., reverse shell, container escape)
        
        Suspicious Container Behaviors (e.g., bash, nc, curl inside a pod)

🧪 Example Detection Scenarios:

        ATTACK	DETECTED BY	FALCO RULE TRIGGERED
        RCE via Flask /rce	Falco + Logs (Loki)	Process spawned in container
        Lateral Movement	Falco + Loki	kubectl exec or suspicious SA token
        DaemonSet Backdoor	Falco	Hidden container deployment
        File Upload + Web Shell	Loki logs	Unusual file created

🔐 How to Access:

        📺 Grafana: http://localhost:3000 (Login: admin, password via kubectl get secret)
        📜 View Falco alerts: kubectl logs -n falco <falco-pod-name>


Visual diagrams for both MITRE mapping and the cyber kill chain are available in the UI.

 📚 Learning Objectives
 
        * 🧠 Understand Kubernetes misconfigurations
        * 🔍 Practice real-world attack techniques
        * 💥 Escape containers & compromise nodes
        * 📊 Monitor and detect attacks using open-source tools
        * ⚔️ Map attacks to MITRE ATT&CK for better blue team correlation

 🔐 Security Disclaimer
     
        Kubepwn is intentionally insecure and must only be used in isolated, local environments for learning and              ethical research.

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
