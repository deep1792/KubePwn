import os
import subprocess
import shutil

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

                        An Intentional Offensive Red-Team Lab
                            Created by: Deepanshu Khanna  
    """)

def setup_apache_php():
    print("\n[*] Ensuring Apache and PHP are installed...")
    run_cmd("sudo apt update")
    run_cmd("sudo apt install apache2 php libapache2-mod-php -y")

    print("[*] Creating upload directory for webshells...")
    upload_path = "/var/www/html/uploads"

    # Use sudo to make and chmod the folder
    run_cmd(f"sudo mkdir -p {upload_path}")
    run_cmd(f"sudo chmod -R 777 {upload_path}")

    print("[*] Restarting Apache server...")
    run_cmd("sudo systemctl restart apache2")

    print("[+] Apache is ready. Webshells will execute via: http://localhost/uploads/<filename>.php")

def setup_kubepwn():
    print("\n[*] Starting Kubepwn Setup...")

    if not os.path.exists("kubepwn-app.yaml"):
        print("❌ Error: kubepwn-app.yaml not found.")
        exit(1)

    if not os.path.exists("/home/j0ck3r/Desktop/kubepwn/k8s_phase2"):
        print("⚠️  Warning: Phase 2 manifests directory not found. Skipping those.")

    print("[*] Building Docker image...")
    run_cmd("docker build -t kubepwn-app:latest .")

    print("[*] Checking kind cluster...")
    clusters = subprocess.check_output("kind get clusters", shell=True).decode().split()
    if "kubepwn" not in clusters:
        print("🌀 Creating kind cluster...")
        run_cmd("kind create cluster --config kind-config.yaml --name kubepwn")
    else:
        print("✅ Kind cluster 'kubepwn' already exists.")

    print("[*] Loading image into kind cluster...")
    run_cmd("kind load docker-image kubepwn-app:latest --name kubepwn")

    print("[*] Deploying application...")
    run_cmd("kubectl apply -f kubepwn-app.yaml")

def main():
    banner()
    setup_apache_php()
    setup_kubepwn()
    print("\n🚀 Kubepwn is live at: http://localhost:8080")
    print("⚠️  For lab use only. Do not expose to public networks.\n")

if __name__ == "__main__":
    main()
