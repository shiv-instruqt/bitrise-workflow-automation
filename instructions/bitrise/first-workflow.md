<div style="background:#1a1a2e;border-radius:8px;padding:24px 28px;color:#e0e4ef;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
  <span style="display:inline-block;background:#6b4eff;color:#fff;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;border-radius:3px;padding:2px 8px;margin-bottom:12px">WHY THIS MATTERS</span>
  <p style="font-size:15px;line-height:1.7;color:#c8cfe0">Mobile teams waste hours on manual build-test-deploy cycles. One engineer triggers a release, another waits for test results, a third manually uploads to the app store — all sequential, all error-prone.</p>
  <p style="font-size:15px;line-height:1.7;color:#c8cfe0;margin-top:12px"><strong style="color:#fff">Bitrise</strong> replaces that chaos with a visual <strong style="color:#fff">Workflow Editor</strong> and a CLI runner that executes the exact same pipeline locally and in the cloud. Every step is versioned, every run is reproducible.</p>
  <ul style="font-size:14px;color:#c8cfe0;margin-top:12px;padding-left:18px;line-height:2">
    <li>Visual drag-and-drop workflow builder</li>
    <li>330+ pre-built steps (git clone, test runners, app store deploy)</li>
    <li>One <code style="background:#2a2a4a;padding:1px 5px;border-radius:3px">bitrise.yml</code> file drives both local and cloud builds</li>
  </ul>
</div>

# Your First Bitrise Workflow

The Workflow Editor is already running. Let's explore the pre-built pipeline for a mobile app.

## Step 1 — Explore the Workflow Editor

Open the **Workflow Editor** tab.

You'll see the **Bitrise CI Configuration** screen — the same interface your team uses to build and ship mobile apps.

The **left sidebar** is your navigation hub:

| Section | Purpose |
|---------|---------|
| **Workflows** | Visual pipeline builder (active now) |
| **Pipelines** | Chain workflows with dependencies |
| **Secrets** | Encrypted keys (API tokens, signing certs) |
| **Env Vars** | Shared variables across all workflows |
| **Triggers** | Auto-run on push, PR, or tag |

The **middle panel** shows the **primary** workflow — your default build pipeline. It has three steps already configured:

1. **Git Clone Repository** `8.5.1` — checks out your code
2. **Run Tests** `1.2.1` — executes your test suite
3. **Deploy to Bitrise.io** `2.25.0` — uploads artifacts and test reports

Click any step to see its **Configuration / Properties / Triggers** tabs in the right panel.

## Step 2 — Inspect the YAML

Click the **YAML** toggle at the top of the screen to switch from the visual view to the raw `bitrise.yml` configuration. This is what gets committed to your repository.

> [!NOTE]
> Every change you make in the visual editor is reflected instantly in the YAML. Toggle back to **Visual** when you're done.

## Step 3 — Run the Workflow

Switch to the **Terminal** tab.

Your project lives at `/root/mobile-app`. Navigate there and run the primary workflow:

```bash,run
cd /root/mobile-app && bitrise run primary
```

You'll see each step execute in sequence — clone, test, deploy — with coloured output showing pass/fail status.

## Step 4 — Capture the Output

Save the result so we can confirm the workflow completed:

```bash,run
bitrise run primary 2>&1 | tee /tmp/primary_output.txt
echo "Workflow done. Exit code: $?"
```

<instruqt-task id="first_workflow">
  Run the <code>primary</code> workflow and save its output to <code>/tmp/primary_output.txt</code>.
</instruqt-task>
