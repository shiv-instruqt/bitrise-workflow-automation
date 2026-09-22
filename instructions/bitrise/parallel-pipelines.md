<div style="background:#1a1a2e;border-radius:8px;padding:24px 28px;color:#e0e4ef;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
  <span style="display:inline-block;background:#6b4eff;color:#fff;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;border-radius:3px;padding:2px 8px;margin-bottom:12px">WHY THIS MATTERS</span>
  <p style="font-size:15px;line-height:1.7;color:#c8cfe0">A single build-test-deploy workflow works for small teams. Larger mobile teams split responsibilities — one workflow for CI (build + test on every PR), a separate workflow for CD (deploy only on merge to main).</p>
  <p style="font-size:15px;line-height:1.7;color:#c8cfe0;margin-top:12px">With Bitrise, each workflow has <strong style="color:#fff">its own trigger</strong>, its own step set, and its own machine configuration. You can run them in <strong style="color:#fff">parallel</strong> on separate build machines — shipping faster without waiting for tests to finish.</p>
</div>

# Run Parallel Workflows

You have a `primary` CI workflow. Let's create a `deploy` workflow for production releases, then run both.

## Step 1 — Create the Deploy Workflow

Open the **Workflow Editor** tab.

In the left sidebar, click **Pipelines**. The middle panel shows all your workflows.

Click **+ New Workflow** at the bottom. Enter the name **deploy** and click **Create Workflow**.

The editor switches to the new `deploy` workflow — it starts with a single **Script** step.

> [!NOTE]
> In a real project, you'd add steps like **Fastlane**, **Deploy to App Store**, and **Send a Slack message**. For this lab the Script step is enough to demonstrate parallel execution.

## Step 2 — Confirm Both Workflows Exist

Switch to the **Terminal** tab.

List your workflows via the API:

```bash,run
curl -s http://localhost:8080/api/workflows | jq '.workflows | keys'
```

You should see both `["deploy", "primary"]`.

## Step 3 — Add the Deploy Workflow to bitrise.yml

Update your local `bitrise.yml` to include the deploy workflow:

```bash,run
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
            echo "Build: $(date +%Y%m%d.%H%M)"
            echo "Status: SUBMITTED"
EOF
```

## Step 4 — Run Both Workflows

Run both workflows to see parallel pipeline execution:

```bash,run
cd /root/mobile-app && bitrise run primary 2>&1 | tail -5
```

```bash,run
cd /root/mobile-app && bitrise run deploy 2>&1 | tee /tmp/deploy_output.txt
echo "Deploy workflow complete."
```

## Step 5 — View the Pipelines View

Open the **Workflow Editor** tab again.

Click **Pipelines** in the left sidebar. You'll see both workflows — `primary` and `deploy` — ready to be chained or triggered independently.

In a real Bitrise account, each workflow runs on its own cloud machine simultaneously, cutting your total pipeline time by up to 50%.

<instruqt-task id="parallel_pipelines">
  Create the <code>deploy</code> workflow and run it, saving the output to <code>/tmp/deploy_output.txt</code>.
</instruqt-task>

<instruqt-completion heading="You have completed the lab!" finish-button-label="Stop & Exit"></instruqt-completion>
