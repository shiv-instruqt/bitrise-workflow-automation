<div style="background:#1a1a2e;border-radius:8px;padding:24px 28px;color:#e0e4ef;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
  <span style="display:inline-block;background:#6b4eff;color:#fff;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;border-radius:3px;padding:2px 8px;margin-bottom:12px">WHY THIS MATTERS</span>
  <p style="font-size:15px;line-height:1.7;color:#c8cfe0">A CI pipeline that only runs tests catches bugs — but a pipeline that also scans for code quality issues, security vulnerabilities, and style violations catches them before they reach review.</p>
  <p style="font-size:15px;line-height:1.7;color:#c8cfe0;margin-top:12px">Bitrise has <strong style="color:#fff">330+ steps</strong> in its public step library. Adding one to your workflow takes seconds — no Dockerfile, no YAML to hand-write. The editor writes it for you.</p>
</div>

# Add a Code Quality Step

The primary workflow has 3 steps. Let's add a **Code Quality Scan** step using the visual editor, then verify it with the CLI.

## Step 1 — Open the Step Library

Open the **Workflow Editor** tab.

The **primary** workflow should be selected. At the bottom of the step list in the middle panel, click **+ Add Step**.

The step library opens with 10 pre-built steps available. Search for **"Code Quality"** or scroll to find **Code Quality Scan**.

Click **+ Add** next to **Code Quality Scan**. The step appears at the bottom of the workflow immediately.

> [!NOTE]
> In the real Bitrise Workflow Editor, adding a step here also updates your `bitrise.yml` in real time. The **Save changes** button in the top-right confirms the configuration is persisted.

## Step 2 — Verify in the Editor

You should now see **4 steps** in the primary workflow:

1. Git Clone Repository
2. Run Tests
3. Deploy to Bitrise.io
4. **Code Quality Scan** ← new

Click **Save changes** to confirm.

## Step 3 — Confirm via API

Switch to the **Terminal** tab.

Query the Workflow Editor API to confirm the step was added:

```bash,run
curl -s http://localhost:8080/api/workflows/primary | jq '.steps | length'
```

The output should be **4**.

Save it for the check script:

```bash,run
curl -s http://localhost:8080/api/workflows/primary | jq '.steps | length' > /tmp/step_count.txt
cat /tmp/step_count.txt
```

## Step 4 — Run the Updated Workflow

Run the workflow again to see all four steps execute:

```bash,run
cd /root/mobile-app && bitrise run primary 2>&1 | tail -20
```

<instruqt-task id="add_pipeline_step">
  Add the <strong>Code Quality Scan</strong> step to the <code>primary</code> workflow, then write the step count to <code>/tmp/step_count.txt</code>.
</instruqt-task>
