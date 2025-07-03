# ⚔️ Kubepwn – The Ultimate Kubernetes Red & Blue Team Lab  
### Hack. Exploit. Own. Detect. Like a Pro.

> 🧨 **APT-Style Attack Simulations** (🔴 Red Team) + 🎯 **Realistic Threat Hunting & Detection** (🟢 Blue Team) — All in One Lab!

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-KIND%20Cluster-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/ATT%26CK-Mapped-red?style=for-the-badge)
![Falco](https://img.shields.io/badge/Falco-Enabled-0052CC?style=for-the-badge&logo=falco)

---

## 📌 What is Kubepwn?

**Kubepwn** is a purpose-built, deliberately vulnerable Kubernetes lab for advanced adversarial simulation, post-exploitation, and blue team detection engineering — **all within a local kind (Kubernetes in Docker) cluster**.

        ✅ Simulate real-world TTPs  
        ✅ Map attacks to both **MITRE ATT&CK** and **Cyber Kill Chain**  
        ✅ Practice **container breakout**, **privilege escalation**, and **cluster persistence**  
        ✅ Monitor and detect threats using **Falco, Loki, and Grafana**

---

## 🚀 Key Features

        - 🧪 Flask-based web app with multiple vulnerabilities (RCE, SSRF, SSTI, file upload)
        - 🎯 Realistic Kubernetes-native misconfigurations (hostPath, containerd.sock, ServiceAccount)
        - 🐙 DaemonSet-based persistence via shell backdoors
        - 📡 Lateral movement via ServiceAccount token theft
        - 📈 Full threat detection stack: **Falco + Loki + Promtail + Grafana**
        - 🗺️ Visual mapping to **MITRE ATT&CK for Containers** + **Cyber Kill Chain**
        - 🧹 One-command setup & teardown scripts

---

## 🧠 Learning Objectives

        - 🔓 Exploit containerized apps and break out to host
        - 🧰 Understand K8s attack surfaces and misconfigurations
        - 🔒 Practice defense using open-source runtime detection tools
        - 🧭 Map actions to attacker TTPs using ATT&CK + CKC
        - 💣 Build muscle memory for both offensive and blue team playbooks

---

## 🗡️ Attack Simulation Scenarios

        |     Exploit Technique   |      Route/Vector           |                 Description                            |
        |-------------------------|--------------------------   |--------------------------------------------------------|
        | **RCE (Command Exec)**  | `/rce`                      | Unsanitized `subprocess` call leads to OS command exec |
        | **SSTI (Jinja2)**       | `/template`                 | Template injection using user-controlled input         |
        | **SSRF**                | `/ssrf?url=...`             | SSRF attack to internal metadata and pods              |
        | **File Upload**         | `/upload`                   | Upload arbitrary files to web-accessible directory     |
        | **Secrets Exposure**    | `/secrets`                  | Hardcoded Python credentials exposed in app logic      |
        | **Container Escape**    | `/rce` + `privileged` pod   | Break out using host mount or containerd.sock          |
        | **Lateral Movement**    | `lateral-movement.yaml`     | SA token theft + remote `kubectl exec`                 |
        | **Persistence **        | `daemonset-backdoor.yaml`   | Hidden DaemonSet backdoor with reverse shell           |

---

## 🛡️ Detection & Monitoring Stack

        |     Tool     |                 Purpose                          |
        |--------------|--------------------------------------------------|
        | **Falco**    | Real-time syscall-based runtime threat detection |
        | **Loki**     | Log aggregation + timeline reconstruction        |
        | **Grafana**  | Dashboard visualizations & alerts                |
        | **Promtail** | Log shipping agent (pods, nodes)                 |

🧪 Example Detections:

        | Attack                   | Detected By | Trigger Example                        |
        |--------------------------|-------------|----------------------------------------|
        | RCE via Flask `/rce`     | Falco + Loki| Suspicious `bash`/`nc` process spawn   |
        | Webshell Upload          | Loki        | Unusual file write under `/uploads`    |
        | Lateral Movement         | Falco       | `kubectl exec` detected from pod       |
        | DaemonSet Backdoor       | Falco       | New hidden container with shell        |

---

## 🗺️ MITRE ATT&CK Mapping (Containers)

        | Tactic               | Technique                                 |
        |----------------------|-------------------------------------------|
        | Initial Access       | T1190 - Exploit Public-Facing Application |
        | Execution            | T1059 - Command and Scripting Interpreter |
        | Privilege Escalation | T1611 - Escape to Host                    |
        | Discovery            | T1082 - System Information Discovery      |
        | Lateral Movement     | T1609 - Kubernetes Exec into Container    |
        | Collection           | T1005 - Data from Local System            |
        | Persistence          | T1499 - DaemonSet/Cluster-wide Implant    |

---

## 🏗️ Architecture
        kind (Kubernetes in Docker)
        └── kubepwn namespace
            ├── kubepwn Pod (privileged)
            │   ├── Host-mounted filesystem (/)
            │   ├── containerd.sock bind
            │   └── Flask app (port 8080)
            └── DaemonSet + Backdoor + Detection Stack


---

## ⚙️ Installation

### 1. Clone Repo

        git clone https://github.com/deep1792/kubepwn.git
        cd kubepwn


### 2. Pre-requisites

        * ✅ Python ≥ 3.10
        * ✅ Docker
        * ✅ `kubectl`, `kind`, `helm` (basic k8s tools)

> 🐧 For Linux setup:


        sudo apt update
        sudo apt install docker.io docker-compose
        curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64 && chmod +x kind && sudo mv kind /usr/local/bin/
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl && sudo mv kubectl /usr/local/bin/


### 3. Deploy Lab

        python3 deploy.py


> This spins up:

        * Vulnerable Flask App
        * Detection Stack (Falco, Loki, Grafana)
        * DaemonSet backdoor
        * Kind cluster

---

## 🔍 Access Points

        | Component           | URL                                                    |
        | ------------------- | ------------------------------------------------------ |
        | Kubepwn App         | [http://localhost:8080](http://localhost:8080)         |
        | Web Shell Directory | [http://localhost/uploads/](http://localhost/uploads/) |
        | Grafana Dashboard   | [http://localhost:3000](http://localhost:3000)         |

🔐 **Get Grafana Admin Password**

        kubectl get secret -n monitoring loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode

---

## 📚 Use Cases

        ✅ Adversary Emulation & Purple Team
        ✅ Blue Team Detection Engineering
        ✅ MITRE ATT\&CK/CKC Based Learning
        ✅ Container Escape & Privilege Escalation
        ✅ SOC Analyst Training / Lab Challenges

---

## ❗ License & Usage

        📝 Licensed under Creative Commons Attribution-NonCommercial 4.0 International License. https://creativecommons.org/licenses/by-nc/4.0/ 
        This project is intended for educational and research purposes only.

> **Kubepwn is NOT licensed for resale or commercial hosting.**
> It is free to use for personal, academic, research, and internal enterprise learning purposes only.

        * 🔓 You **can** fork, modify, and use for workshops or internal demos.
        * 💰 You **cannot** sell, SaaS, or redistribute this lab commercially.
        * ☣️ Never deploy Kubepwn in a production or internet-facing environment.

---

## 👨‍💻 Author

Created with ❤️ by [Deepanshu Khanna](https://www.linkedin.com/in/deepanshukhanna/)
        🛡️ Security Researcher | Red Teamer | Threat Hunter

---

## ☕ Support the Project

If you love **Kubepwn**, then buy me a coffee:

![UPI QR Code](https://api.qrserver.com/v1/create-qr-code/?data=upi://pay?pa=alivejatt@oksbi\&size=200x200)

[![Pay via UPI](https://img.shields.io/badge/Buy%20Me%20Coffee-UPI-blue?style=for-the-badge\&logo=google-pay)](upi://pay?pa=alivejatt@oksbi&pn=Kubepwn+Support&cu=INR)

---

## 🧼 Teardown

        python3 cleanup.py


---

## 🧷 Note

        Kubepwn is for **ethical, educational, and research** purposes only.
        Use responsibly. Abuse = 🚫 permanent ban from the internet (just kidding... or not).
