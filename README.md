# ⚔️ Kubepwn – The Ultimate Kubernetes Red & Blue Team Lab  
### Hack. Exploit. Own. Detect. Like a Pro.

> 🧨 **APT-Style Attack Simulations** (🔴 Red Team) + 🎯 **Realistic Threat Hunting & Detection** (🟢 Blue Team) — All in One Lab!

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-KIND%20Cluster-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![MITRE ATT&CK](https://img.shields.io/badge/ATT%26CK-Mapped-red?style=for-the-badge)
![Falco](https://img.shields.io/badge/Falco-Enabled-0052CC?style=for-the-badge&logo=falco)

---

![Kubepwn Banner](https://github.com/deep1792/KubePwn/blob/main/static/images/banner-final.png)

---

## 📌 What is Kubepwn?

**Kubepwn** is a purpose-built, deliberately vulnerable Kubernetes lab for advanced adversarial simulation, post-exploitation, and blue team detection engineering — all within a local kind (Kubernetes in Docker) cluster.

        - ✅ Simulate real-world APT tactics & misconfigurations  
        - ✅ Map attacks to **MITRE ATT&CK** + **Cyber Kill Chain**  
        - ✅ Practice real-world *K8s miscofigurations**, **privilege escalations**, **lateral movement**, **persistence**  
        - ✅ Detect threats with **Falco + Loki + Grafana dashboards**  

---

## 🚀 Key Features
        
        - 🧪 Vulnerable Flask app (RCE, SSRF, SSTI, file upload)
        - 🐳 Kubernetes-native misconfigurations: hostPath, containerd.sock, default SA tokens
        - 👣 Full red team kill chain: exploit → pivot → cluster compromise
        - 📡 Lateral movement & secret dumping
        - 🧙‍♂️ DaemonSet backdoors & persistence
        - 🛡️ SIEM stack: **Falco + Promtail + Loki + Grafana**
        - 🗺️ ATT&CK-mapped & CKC-mapped scenario matrix
        - ⚙️ One-command deploy/teardown scripts

---

## 🧠 Learning Objectives

        - 🔓 Exploit vulnerable containerized apps
        - 🔒 Escalate to host / access Kubernetes API
        - 🧰 Understand attacker TTPs inside K8s
        - 🔍 Detect, alert, visualize attacks in Grafana
        - 🛡️ Build defender muscle memory with Falco/Loki rules

---

## 🗡️ Attack Simulation Scenarios

        | Exploit Technique         | Attack Route            | Description                                               |
        |--------------------------|--------------------------|-----------------------------------------------------------|
        | RCE                      | `/rce`                   | Command injection via subprocess abuse                    |
        | SSRF                     | `/ssrf?url=...`          | Access internal services (e.g., metadata, pods)           |
        | SSTI                     | `/template`              | Server-Side Template Injection (Jinja2)                   |
        | File Upload              | `/upload`                | Arbitrary file upload to public dir                       |
        | Secrets Exposure         | `/secrets`               | Hardcoded credentials exposure                            |
        | Git Repo Leak            | `.git` exposed directory | Credential leak via dumped Git repo                       |
        | Container Escape         | privileged pod + hostPath| Escape to host with `chroot /host` or `containerd.sock`   |
        | Lateral Movement         | SA token abuse           | Use pod token to list secrets, exec into other pods       |
        | DaemonSet Backdoor       | DaemonSet implant         | Full-cluster persistence with shell & reverse shell      |

---

## 🛡️ Detection & Monitoring Stack

        | Tool        | Role                                               |
        |-------------|----------------------------------------------------|
        | **Falco**   | Syscall-based runtime threat detection             |
        | **Loki**    | Central log aggregation from containers/nodes      |
        | **Promtail**| Log shipper to Loki                                |
        | **Grafana** | SIEM-style dashboards with alert queries           |

🧪 Example Detections:

        | Attack                 | Detected By   | Example Trigger                                 |
        |------------------------|---------------|-------------------------------------------------|
        | RCE via `/rce`         | Falco + Loki  | `bash` or `nc` child process under Flask pod    |
        | Webshell Upload        | Loki          | File write event in `/uploads` dir              |
        | Token Abuse            | Loki          | Read from `serviceaccount/token` path           |
        | DaemonSet Backdoor     | Falco         | Suspicious container in kube-system             |
        | DIND Escape            | Falco + Loki  | Access to `docker.sock`, `host mount`           |

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

## 🏗️ Lab Architecture

        kind (Kubernetes in Docker)
        └── kubepwn namespace
        ├── kubepwn Pod (privileged)
        │   ├── Host-mounted /
        │   ├── containerd.sock
        │   └── Flask app (port 8080)
        ├── DaemonSet (reverse shell)
        ├── Detection Stack (Falco, Loki, Promtail)
        └── Grafana Dashboard (port 3000)

---

## ⚙️ Installation

### 1. Clone the Repo

        git clone https://github.com/deep1792/kubepwn.git
        cd kubepwn

### 2. Install Requirements

        * Python ≥ 3.10
        * Docker
        * kind
        * kubectl
        * helm

### 3. Deploy the Lab

        python3 deploy.py


☑️ This deploys:

        * Flask app
        * Detection stack
        * Backdoor DaemonSet
        * Kind cluster

---

## 🔍 Access Points

        | Component         | URL                                                    |
        | ----------------- | ------------------------------------------------------ |
        | Kubepwn App       | [http://localhost:8080](http://localhost:8080)         |
        | Grafana Dashboard | [http://localhost:3000](http://localhost:3000)         |
        | Upload Dir        | [http://localhost/uploads/](http://localhost/uploads/) |

🔐 **Get Grafana Password:**

        kubectl get secret -n monitoring loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode


---

## 🧼 Teardown

        python3 cleanup.py

---

## 📚 Use Cases

        ✅ Red & Blue Team Training
        ✅ SOC Analyst Simulation Lab
        ✅ Container Security Workshops
        ✅ Detection Engineering Lab
        ✅ MITRE ATT\&CK Emulation

---

## ❗ License

        Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
        
        > ❗ For educational/research use only.
        > ❌ Do not deploy in production or expose to internet.
        > 💰 Not for resale or SaaS redistribution.

---

## 👨‍💻 Author

        Created with ❤️ by [Deepanshu Khanna](https://www.linkedin.com/in/deepanshukhanna/)
        🛡️ Security Researcher | Red Teamer | Threat Hunter

---

## ☕ Support the Project
        
If you found this useful, buy me a coffee 💙
        
![UPI QR Code](https://api.qrserver.com/v1/create-qr-code/?data=upi://pay?pa=alivejatt@oksbi\&size=200x200)
        
[![UPI](https://img.shields.io/badge/Buy%20Me%20Coffee-UPI-blue?style=for-the-badge\&logo=google-pay)](upi://pay?pa=alivejatt@oksbi&pn=Kubepwn+Support&cu=INR)

---

## 🧷 Disclaimer

        Kubepwn is for **educational and research** use only.
        Test responsibly.
        Don't be that person. ☠️
