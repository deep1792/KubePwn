import os
import subprocess

def run_cmd(cmd, exit_on_fail=True):
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        if exit_on_fail:
            exit(1)
    return result

def banner():
    print(r"""
   ,--.                                 ,-.----.                                   
   ,--/  /|                                 \    /  \                                  
,---,': / '               ,---,             |   :    \                                 
:   : '/ /          ,--,,---.'|             |   |  .\ :       .---.      ,---,         
|   '   ,         ,'_ /||   | :             .   :  |: |      /. ./|  ,-+-. /  |        
'   |  /     .--. |  | ::   : :      ,---.  |   |   \ :   .-'-. ' | ,--.'|'   |        
|   ;  ;   ,'_ /| :  . |:     |,-.  /     \ |   : .   /  /___/ \: ||   |  ,"' |        
:   '   \  |  ' | |  . .|   : '  | /    /  |;   | |`-'.-'.. '   ' .|   | /  | |        
|   |    ' |  | ' |  | ||   |  / :.    ' / ||   | ;  /___/ \:     '|   | |  | |        
'   : |.  \:  | : ;  ; |'   : |: |'   ;   /|:   ' |  .   \  ' .\   |   | |  |/         
|   | '_\.''  :  `--'   \   | '/ :'   |  / |:   : :   \   \   ' \ ||   | |--'          
'   : |    :  ,      .-./   :    ||   :    ||   | :    \   \  |--" |   |/              
;   |,'     `--`----'   /    \  /  \   \  / `---'.|     \   \ |    '---'               
'---'                   `-'----'    `----'    `---`      '---"                         

          Kubepwn: Kubernetes Red Team & Blue Lab — Hack. Exploit. Own. & Detect.
                 Created by: Deepanshu Khanna  
                 License: MIT
    """)

def setup_apache_php():
    print("\n[*] Ensuring Apache and PHP are installed...")
    run_cmd("sudo apt update")
    run_cmd("sudo apt install apache2 php libapache2-mod-php -y")
    run_cmd("sudo mkdir -p /var/www/html/uploads && sudo chmod -R 777 /var/www/html/uploads")
    run_cmd("sudo systemctl restart apache2")
    print("[+] Webshells accessible via http://localhost/uploads/<filename>.php")

def install_prerequisites():
    print("\n[*] Installing Docker, Kind, and kubectl...")

    # Docker
    run_cmd("sudo apt install docker.io docker-cli docker-compose -y")
    run_cmd("sudo systemctl enable docker && sudo systemctl start docker")
    run_cmd("sudo usermod -aG docker $USER")

    # Kind - install from official release if apt version not good
    kind_installed = subprocess.run("which kind", shell=True, stdout=subprocess.DEVNULL).returncode == 0
    if not kind_installed:
        print("[*] Installing kind from official release")
        run_cmd("curl -Lo kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64 && chmod +x kind && sudo mv kind /usr/local/bin/")
    else:
        print("[+] Kind already installed")

    # kubectl - install via apt or official binary if needed
    kubectl_installed = subprocess.run("which kubectl", shell=True, stdout=subprocess.DEVNULL).returncode == 0
    if not kubectl_installed:
        print("[*] Installing kubectl")
        run_cmd("sudo apt install kubectl -y")
    else:
        print("[+] kubectl already installed")

def setup_kubepwn_cluster():
    print("\n[*] Building and deploying Kubepwn app...")

    if not os.path.exists("kubepwn-app.yaml"):
        print("❌ kubepwn-app.yaml not found.")
        exit(1)

    run_cmd("docker build -t kubepwn-app:latest .")

    clusters = subprocess.getoutput("kind get clusters").split()
    if "kubepwn" not in clusters:
        run_cmd("kind create cluster --config kind-config.yaml --name kubepwn")
    else:
        print("✅ Kind cluster 'kubepwn' already exists.")

    run_cmd("kind load docker-image kubepwn-app:latest --name kubepwn")
    run_cmd("kubectl apply -f kubepwn-app.yaml")

def deploy_metadata_db():
    print("\n[*] Building and deploying metadata-db service...")

    # Build the Docker image from the metadata-db directory
    run_cmd("docker build -t metadata-db:latest ./bonus")

    # Load image into kind cluster
    run_cmd("kind load docker-image metadata-db:latest --name kubepwn")

def deploy_apt_attacks():
    print("\n[*] Deploying APT-style attacks...")

    run_cmd("kubectl apply -f bonus/lateral-movement.yaml")
    run_cmd("kubectl apply -f bonus/backdoor.yaml")
    run_cmd("kubectl apply -f bonus/dind-vuln.yaml")
    run_cmd("kubectl apply -f bonus/rbac-misconfigurations.yaml")
    run_cmd("kubectl apply -f bonus/git-leak.yaml")
    run_cmd("kubectl apply -f bonus/ssrf.yaml")
    run_cmd("kubectl apply -f bonus/metadata-db.yaml")    

def deploy_detection_stack():
    print("\n[*] Setting up Falco + Loki + Grafana stack...")

    # Pull images and load into kind cluster
    images = [
        "grafana/grafana:10.3.3",
        "grafana/loki:2.6.1",
        "grafana/promtail:2.9.3",
        "quay.io/kiwigrid/k8s-sidecar:1.19.2"
    ]
    for image in images:
        run_cmd(f"docker pull {image}")
        run_cmd(f"kind load docker-image {image} --name kubepwn")

    # Install Helm if not installed
    helm_installed = subprocess.run("which helm", shell=True, stdout=subprocess.DEVNULL).returncode == 0
    if not helm_installed:
        print("[*] Installing Helm...")
        run_cmd("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash")
    else:
        print("[+] Helm already installed")

    # Add repos and update
    run_cmd("helm repo add falcosecurity https://falcosecurity.github.io/charts")
    run_cmd("helm repo add grafana https://grafana.github.io/helm-charts")
    run_cmd("helm repo update")

    # Deploy Falco
    run_cmd("helm upgrade --install falco falcosecurity/falco --namespace falco --create-namespace")

    # Deploy Loki Stack (includes Grafana, Loki, and Promtail)
    # Use your promtail-values.yaml file here for the promtail configuration
    promtail_values_path = "promtail-values.yaml"
    if not os.path.exists(promtail_values_path):
        print(f"❌ {promtail_values_path} not found. Please create it before running this script.")
        exit(1)

    # The loki-stack includes loki, promtail, and grafana
    run_cmd(
        f"helm upgrade --install loki grafana/loki-stack "
        f"--namespace monitoring --create-namespace "
        f"--set grafana.enabled=true "
        f"--set promtail.enabled=true "
        f"-f {promtail_values_path}"
    )

    print("🔍 Grafana available at http://localhost:3000 ")

def main():
    banner()
    setup_apache_php()
    install_prerequisites()
    setup_kubepwn_cluster()
    deploy_apt_attacks()
    deploy_detection_stack()
    deploy_metadata_db() 

    print("\n Kubepwn is live at: http://localhost:8080")
    print(" Monitor attacks at: http://localhost:3000\n")
    print(" To forward the Grafana dashboard port run:")
    print("  kubectl port-forward -n monitoring svc/loki-grafana 3000:80\n")
    print(' To decode the Grafana admin password run:')
    print('  kubectl get secret -n monitoring loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode && echo\n')

if __name__ == "__main__":
    main()
