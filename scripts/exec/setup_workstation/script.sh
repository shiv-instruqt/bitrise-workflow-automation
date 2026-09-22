#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

# Use a short timeout so apt-get fails fast on network issues rather than hanging.
apt-get -o Acquire::http::Timeout=15 -o Acquire::https::Timeout=15 update -qq 2>/dev/null || true

# curl and jq are NOT in the ubuntu:22.04 base image.
apt-get install -y -qq --no-install-recommends curl jq python3-pip 2>/dev/null || {
  # Fallback: bootstrap pip via wget (wget IS in the ubuntu:22.04 base image).
  if ! command -v pip3 >/dev/null 2>&1; then
    wget -qO- https://bootstrap.pypa.io/get-pip.py | python3
  fi
}

# Bitrise CLI wrapper: reads bitrise.yml and runs script steps.
# A wrapper avoids the ~85MB binary download while producing identical output.
install -m 0755 /opt/lab-files/bitrise /usr/local/bin/bitrise

# Workflow Editor simulation dependencies.
pip3 install fastapi uvicorn 2>/dev/null

# Sample mobile app project.
mkdir -p /root/mobile-app
install -m 0644 /opt/lab-files/bitrise.yml /root/mobile-app/bitrise.yml
install -m 0644 /opt/lab-files/bitrise_sim.py /root/bitrise_sim.py

# Start the Workflow Editor simulation on port 8080.
nohup python3 /root/bitrise_sim.py > /var/log/bitrise_sim.log 2>&1 &
disown || true

# Wait for the server to accept connections before the lab hands over to the learner.
for _ in $(seq 1 60); do
  if curl -sf http://localhost:8080/ > /dev/null 2>&1; then
    break
  fi
  sleep 1
done

# Fail provisioning loudly if the editor never came up.
curl -sf http://localhost:8080/ > /dev/null
bitrise --version
