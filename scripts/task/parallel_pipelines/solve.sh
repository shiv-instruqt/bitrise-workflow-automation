#!/bin/bash
set -euxo pipefail

# Create the deploy workflow in the Workflow Editor if it does not exist yet.
if ! curl -s http://localhost:8080/api/workflows | jq -e '.workflows | has("deploy")' > /dev/null; then
  curl -s -X POST http://localhost:8080/api/workflows \
    -H "Content-Type: application/json" \
    -d '{"name":"deploy"}' > /dev/null
fi

# Add the deploy workflow to bitrise.yml if it is not already present.
if ! grep -q "^  deploy:" /root/mobile-app/bitrise.yml; then
  cat >> /root/mobile-app/bitrise.yml << 'EOF'
  deploy:
    title: Deploy to Production
    steps:
    - script@1:
        title: Deploy to App Store
        inputs:
        - content: |
            #!/bin/bash
            echo "Deploying ${APP_NAME} to App Store..."
            echo "Status: SUBMITTED"
EOF
fi

cd /root/mobile-app
bitrise run deploy 2>&1 | tee /tmp/deploy_output.txt
