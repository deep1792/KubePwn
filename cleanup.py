import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),                    # Print to console
        logging.FileHandler("cleanup.log", mode='w') # Save to file
    ]
)

def run_cmd(cmd, exit_on_fail=False):
    logging.info(f"$ {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(result.stdout.decode().strip())
        return result
    except subprocess.CalledProcessError as e:
        logging.warning(f"⚠️ Command failed: {cmd}")
        logging.debug(e.stderr.decode().strip())
        if exit_on_fail:
            exit(1)
        return e

def cleanup():
    logging.info("🚮 Starting cleanup of Helm releases, namespaces, and Kind cluster...")

    # Run independent commands in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(run_cmd, "helm uninstall falco -n falco || true")
        executor.submit(run_cmd, "kubectl delete namespace falco")
        executor.submit(run_cmd, "helm uninstall loki -n monitoring || true")
        executor.submit(run_cmd, "kubectl delete namespace monitoring")
        executor.submit(run_cmd, "kubectl delete namespace kubepwn")

    # Delete Kind cluster
    logging.info("🧨 Deleting Kind cluster 'kubepwn'...")
    run_cmd("kind delete cluster --name kubepwn")

    # Clean up Docker volumes
    logging.info("🧼 Pruning Docker volumes and unused data...")
    run_cmd("docker system prune -a --volumes -f")

    logging.info("✅ Cleanup complete. You can now rerun deploy.py for a fresh start.")

if __name__ == "__main__":
    cleanup()
