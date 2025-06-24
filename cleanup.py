import subprocess

def run_cmd(cmd, exit_on_fail=False):
    print(f"\n$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"⚠️ Command failed: {cmd}")
        if exit_on_fail:
            exit(1)
    return result

def cleanup():
    print("[*] Cleaning up Helm releases and namespaces...")
    run_cmd("helm uninstall falco -n falco")
    run_cmd("kubectl delete namespace falco")

    run_cmd("helm uninstall loki -n monitoring")
    run_cmd("kubectl delete namespace monitoring")

    print("[*] Deleting Kind cluster 'kubepwn'...")
    run_cmd("kind delete cluster --name kubepwn")

    print("[*] Deleting kubepwn namespace and all resources inside...")
    run_cmd("kubectl delete namespace kubepwn")

    print("[*] Deleting kubepwn namespace and all resources inside...")
    run_cmd("kubectl delete namespace kubepwn")

    print("[*] Deleting kubepwn namespace and all resources inside...")
    run_cmd("kubectl delete namespace kubepwn")

    print("[*] Delete all the docker volumes to release memory...")
    run_cmd("docker system prune -a --volumes")

    print("[*] Cleanup complete. You can now rerun deploy.py for a fresh start.")

if __name__ == "__main__":
    cleanup()
