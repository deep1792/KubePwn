from flask import Flask, jsonify
import os
import requests
import socket

app = Flask(__name__)

# Base Kubernetes API URL inside the cluster
K8S_API = "https://kubernetes.default.svc"

# Path to service account token & CA cert
TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"
CA_CERT_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

def get_k8s_token():
    with open(TOKEN_PATH, 'r') as f:
        return f.read()

def k8s_get(path):
    token = get_k8s_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{K8S_API}{path}"
    resp = requests.get(url, headers=headers, verify=CA_CERT_PATH)
    return resp.json() if resp.status_code == 200 else {"error": resp.text}

@app.route('/')
def hello():
    return "Hello, Metadata DB!"

@app.route('/hostname')
def hostname():
    return socket.gethostname()

@app.route('/pods')
def pods():
    # List pods in the default namespace
    return jsonify(k8s_get("/api/v1/namespaces/default/pods"))

@app.route('/nodes')
def nodes():
    # List all nodes
    return jsonify(k8s_get("/api/v1/nodes"))

@app.route('/secrets')
def secrets():
    # List secrets in the default namespace (if permitted)
    return jsonify(k8s_get("/api/v1/namespaces/default/secrets"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
