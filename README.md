# Bitrise: Automate Your Mobile CI/CD — Instruqt Lab 2.0

A 1:1 port of the legacy Instruqt track `bitrise-workflow-automation` (`instruqt-abm`) to the
Instruqt Labs 2.0 HCL format.

## Structure

```
.
├── main.hcl                              # lab metadata, settings, chapter/page structure
├── layouts.hcl                           # two-column layout: tabs (67%) + instructions (33%)
├── sandbox.hcl                           # network, workstation container, provisioning exec
├── tabs.hcl                              # Workflow Editor service tab + terminal tab
├── pages.hcl                             # three pages, each bound to one task
├── tasks.hcl                             # three tasks with check + solve conditions
├── assets/
│   └── bitrise.png                       # lab icon
├── files/                                # mounted read-only at /opt/lab-files
│   ├── bitrise                           # Bitrise CLI wrapper (reads bitrise.yml, runs script steps)
│   ├── bitrise.yml                       # sample mobile app pipeline
│   └── bitrise_sim.py                    # FastAPI Workflow Editor simulation (port 8080)
├── instructions/bitrise/
│   ├── first-workflow.md
│   ├── add-pipeline-step.md
│   └── parallel-pipelines.md
└── scripts/
    ├── exec/setup_workstation/script.sh  # provisioning
    └── task/
        ├── first_workflow/{check,solve}.sh
        ├── add_pipeline_step/{check,solve}.sh
        └── parallel_pipelines/{check,solve}.sh
```

## Mapping from the legacy track

| Legacy (v1) | Labs 2.0 |
|---|---|
| `track.yml` (slug, title, teaser, description, icon, timers) | `resource "lab"` in `main.hcl` |
| `config.yml` containers | `resource "network"` + `resource "container"` in `sandbox.hcl` |
| `track_scripts/setup-workstation` | `resource "exec" "setup_workstation"` + `scripts/exec/setup_workstation/script.sh` |
| Challenge folder per step | `content.chapter.page` + `resource "page"` |
| Challenge `assignment.md` frontmatter `tabs:` | `resource "service"` / `resource "terminal"` in `tabs.hcl`, arranged in `layouts.hcl` |
| Challenge `notes:` intro panel | HTML block at the top of each instruction page |
| `check-workstation` + `fail-message` | `condition.check.script` + declarative `failure_message` in `tasks.hcl` |
| `solve-workstation` | `condition.solve.script` |
| `timelimit: 1800` / `idle_timeout: 400` | `settings.timelimit.duration = "30m"` / `settings.idle.timeout = "400s"` |
| `show_timer: true` / `hideStopButton: false` | `settings.timelimit.show_timer` / `settings.controls.show_stop` |

## Intentional differences

1. **Tab-switch buttons.** The legacy `[button label="..." variant="success"](tab-0)` shortcode has no
   documented equivalent in the 2.0 markdown syntax, so those lines became plain instructions
   ("Open the **Workflow Editor** tab"). Swap them for the editor's switch-tab block if you prefer.
2. **`level`, `tags`, `developers`, `owner`.** These are not part of the 2.0 `lab` resource schema —
   they are set on the lab in the Instruqt UI / project settings rather than in HCL.
3. **Payloads moved out of the setup script.** The CLI wrapper, `bitrise.yml`, and the FastAPI app were
   heredocs inside the legacy setup script. They are now real files under `files/`, bind-mounted
   read-only at `/opt/lab-files` and installed by the exec script.
4. **ANSI colour fix.** The legacy wrapper used `echo "\033[32m..."`, which printed the escape codes
   literally. Those lines now use `echo -e`, so the CLI output is actually coloured.
5. **Idempotent solves.** The solve scripts now check before mutating, so triggering a solve twice
   cannot push the step count past 4 or duplicate the deploy workflow.

## Verification performed

- All six `.hcl` files parse as valid HCL2.
- `bash -n` passes on every shell script and on the `bitrise` wrapper.
- `bitrise_sim.py` compiles; `bitrise.yml` parses as valid YAML.
- The simulation was booted and `bitrise run primary` / `bitrise run deploy` produce the expected output.
- Every task was run through the full cycle: check fails before solve, passes after, and stays
  passing when the solve is run a second time.

## Deploying

Labs 2.0 labs are published by connecting the repository to the Instruqt platform, not by a CLI
push — the platform syncs from Git. Commit this directory as the root of a repo (or as a
subdirectory pointed at by the lab's VCS settings), then connect it under the lab's version-control
settings in the Instruqt UI.

For CI validation, the same action the official `instruqt/lab-examples` repo uses works here:

```yaml
- uses: instruqt/cli/setup@v1
- uses: instruqt/cli/validate@v1
  with:
    path: ./bitrise-workflow-automation-lab-2.0
```

`instruqt lab init` is the CLI command that scaffolds a new lab locally if you want to compare this
layout against a fresh skeleton.
