from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn, json, copy

app = FastAPI()

INITIAL_STATE = {
    "workflows": {
        "primary": {
            "title": "Primary Build",
            "steps": [
                {"id": "git-clone", "title": "Git Clone Repository", "version": "8.5.1", "icon": "git", "color": "#e74c3c"},
                {"id": "run-tests", "title": "Run Tests", "version": "1.2.1", "icon": "test", "color": "#2c3e50"},
                {"id": "deploy", "title": "Deploy to Bitrise.io", "version": "2.25.0", "icon": "deploy", "color": "#3498db"}
            ]
        }
    },
    "secrets": [
        {"key": "GITHUB_TOKEN", "value": "***", "is_protected": True},
        {"key": "DEPLOY_KEY", "value": "***", "is_protected": True}
    ],
    "env_vars": [
        {"key": "APP_NAME", "value": "MyMobileApp"},
        {"key": "BUILD_ENV", "value": "production"}
    ],
    "triggers": [
        {"event": "push", "branch": "main", "workflow": "primary"},
        {"event": "pull_request", "branch": "*", "workflow": "primary"}
    ]
}

STATE = copy.deepcopy(INITIAL_STATE)

HTML_SPA = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bitrise — CI Configuration</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f5f5f5;color:#1a1a2e;font-size:14px}

/* Top bar */
.topbar{display:flex;align-items:center;justify-content:space-between;height:52px;background:#fff;border-bottom:1px solid #e5e5e5;padding:0 20px;position:fixed;top:0;left:0;right:0;z-index:100}
.topbar-brand{display:flex;align-items:center;gap:10px}
.topbar-logo{display:flex;align-items:center;flex-shrink:0}
.topbar-title{font-size:15px;font-weight:600;color:#1a1a2e}
.view-toggle{display:flex;background:#f0f0f0;border-radius:8px;padding:3px;gap:2px}
.view-btn{padding:5px 14px;border:none;background:transparent;border-radius:6px;font-size:13px;font-weight:500;cursor:pointer;color:#666;display:flex;align-items:center;gap:5px}
.view-btn.active{background:#fff;color:#6b4eff;box-shadow:0 1px 3px rgba(0,0,0,.12)}
.view-btn svg{width:14px;height:14px}
.topbar-actions{display:flex;gap:8px}
.btn-ghost{padding:6px 14px;border:1px solid #e0e0e0;background:#fff;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;color:#444}
.btn-save{padding:6px 14px;border:1px solid #6b4eff;background:#6b4eff;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;color:#fff}
.btn-save:hover{background:#5a3de8}

/* Layout */
.layout{display:flex;margin-top:52px;height:calc(100vh - 52px)}

/* Sidebar */
.sidebar{width:220px;background:#fff;border-right:1px solid #e5e5e5;display:flex;flex-direction:column;flex-shrink:0}
.sidebar-main{flex:1;padding:8px 0}
.sidebar-bottom{border-top:1px solid #e5e5e5;padding:8px 0}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 16px;cursor:pointer;border-radius:0;color:#444;font-size:13.5px;font-weight:500;transition:background .15s}
.nav-item:hover{background:#f8f6ff}
.nav-item.active{background:#f0ebff;color:#6b4eff}
.nav-item svg{width:16px;height:16px;flex-shrink:0;opacity:.7}
.nav-item.active svg{opacity:1;color:#6b4eff}

/* Middle panel */
.middle{width:330px;background:#fff;border-right:1px solid #e5e5e5;display:flex;flex-direction:column;flex-shrink:0}
.workflow-selector{padding:12px 14px;border-bottom:1px solid #f0f0f0}
.wf-select{width:100%;padding:8px 12px;border:1px solid #e0e0e0;border-radius:8px;font-size:13px;background:#fff;color:#1a1a2e;cursor:pointer;font-family:inherit}
.workflow-steps{flex:1;overflow-y:auto;padding:12px}
.wf-header{margin-bottom:12px}
.wf-name{font-size:15px;font-weight:700;color:#1a1a2e}
.wf-sub{font-size:12px;color:#888;margin-top:2px}
.step-item{display:flex;align-items:center;gap:10px;padding:10px 10px;border:1px solid #e8e8e8;border-radius:10px;margin-bottom:8px;background:#fff;cursor:pointer;transition:border-color .15s}
.step-item:hover{border-color:#6b4eff}
.step-item.selected{border-color:#6b4eff;background:#faf8ff}
.drag-handle{color:#ccc;font-size:13px;cursor:grab;user-select:none}
.step-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:14px}
.step-info{flex:1;min-width:0}
.step-title{font-size:13px;font-weight:600;color:#1a1a2e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.step-version{font-size:11px;color:#888;margin-top:1px}
.add-step-btn{display:flex;align-items:center;justify-content:center;gap:6px;padding:9px;border:1.5px dashed #d0d0d0;border-radius:10px;cursor:pointer;color:#888;font-size:13px;font-weight:500;margin-top:4px;transition:border-color .2s,color .2s}
.add-step-btn:hover{border-color:#6b4eff;color:#6b4eff}

/* Right panel */
.right{flex:1;overflow-y:auto;background:#f5f5f5;padding:20px}
.panel-card{background:#fff;border-radius:12px;border:1px solid #e5e5e5;overflow:hidden}
.panel-header{padding:18px 20px 0}
.panel-title{font-size:18px;font-weight:700;color:#1a1a2e}
.panel-sub{font-size:12px;color:#888;margin-top:4px}
.panel-tabs{display:flex;gap:0;padding:0 20px;border-bottom:1px solid #e8e8e8;margin-top:16px}
.tab-btn{padding:10px 16px;border:none;background:transparent;font-size:13.5px;font-weight:500;cursor:pointer;color:#888;border-bottom:2px solid transparent;margin-bottom:-1px}
.tab-btn.active{color:#6b4eff;border-bottom-color:#6b4eff}
.tab-content{padding:20px}
.accordion{border:1px solid #e8e8e8;border-radius:10px;overflow:hidden;margin-bottom:12px}
.accordion-header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;cursor:pointer;background:#fff;font-size:13.5px;font-weight:600}
.accordion-header:hover{background:#fafafa}
.accordion-body{padding:16px;border-top:1px solid #f0f0f0;background:#fafafa}
.env-row{display:flex;gap:8px;margin-bottom:8px;align-items:center}
.env-key{flex:1;padding:7px 10px;border:1px solid #e0e0e0;border-radius:7px;font-size:12.5px;font-family:monospace;background:#fff}
.env-val{flex:2;padding:7px 10px;border:1px solid #e0e0e0;border-radius:7px;font-size:12.5px;font-family:monospace;background:#fff}
.yaml-view{display:none;padding:20px}
.yaml-box{background:#1e1e2e;border-radius:10px;padding:20px;font-family:monospace;font-size:12.5px;line-height:1.7;color:#cdd6f4;overflow-x:auto;white-space:pre}
.yaml-key{color:#89b4fa}.yaml-str{color:#a6e3a1}.yaml-num{color:#fab387}.yaml-comment{color:#6c7086}

/* Step add modal */
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:200;align-items:center;justify-content:center}
.modal-overlay.open{display:flex}
.modal{background:#fff;border-radius:14px;width:520px;max-height:70vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.2)}
.modal-header{padding:20px 20px 16px;border-bottom:1px solid #f0f0f0;display:flex;align-items:center;justify-content:space-between}
.modal-title{font-size:16px;font-weight:700}
.modal-close{background:none;border:none;font-size:20px;cursor:pointer;color:#888;line-height:1}
.modal-search{padding:12px 20px;border-bottom:1px solid #f0f0f0}
.modal-search input{width:100%;padding:8px 12px;border:1px solid #e0e0e0;border-radius:8px;font-size:13px;font-family:inherit;outline:none}
.modal-search input:focus{border-color:#6b4eff}
.step-option{display:flex;align-items:center;gap:12px;padding:12px 20px;cursor:pointer;border-bottom:1px solid #f8f8f8}
.step-option:hover{background:#f8f6ff}
.step-option-icon{width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.step-option-info{flex:1}
.step-option-name{font-size:13.5px;font-weight:600}
.step-option-desc{font-size:12px;color:#888;margin-top:2px}
.step-option-version{font-size:11px;color:#aaa;margin-top:2px}
.step-option-add{padding:5px 14px;border:1px solid #6b4eff;border-radius:7px;background:#fff;color:#6b4eff;font-size:12px;font-weight:600;cursor:pointer}
.step-option-add:hover{background:#6b4eff;color:#fff}

/* New workflow modal */
.nw-modal{background:#fff;border-radius:14px;width:400px;box-shadow:0 20px 60px rgba(0,0,0,.2)}
.nw-body{padding:20px}
.nw-label{font-size:13px;font-weight:600;margin-bottom:6px;color:#444}
.nw-input{width:100%;padding:9px 12px;border:1px solid #e0e0e0;border-radius:8px;font-size:13px;font-family:inherit;outline:none}
.nw-input:focus{border-color:#6b4eff}
.nw-footer{display:flex;justify-content:flex-end;gap:8px;padding:12px 20px;border-top:1px solid #f0f0f0}
.chevron{transition:transform .2s}
.chevron.open{transform:rotate(180deg)}

/* Notifications */
.toast{position:fixed;bottom:24px;right:24px;background:#1a1a2e;color:#fff;padding:12px 18px;border-radius:10px;font-size:13px;font-weight:500;z-index:300;opacity:0;transition:opacity .3s;pointer-events:none}
.toast.show{opacity:1}
</style>
</head>
<body>

<!-- Top Bar -->
<div class="topbar">
  <div class="topbar-brand">
    <div class="topbar-logo">
      <!-- Bitrise robot mascot logo (inline SVG) -->
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="8" fill="#683DF5"/>
        <!-- Robot head outline -->
        <rect x="7" y="10" width="18" height="14" rx="3" fill="white"/>
        <!-- Eyes -->
        <rect x="11" y="14" width="4" height="4" rx="1" fill="#683DF5"/>
        <rect x="17" y="14" width="4" height="4" rx="1" fill="#683DF5"/>
        <!-- Mouth -->
        <rect x="11" y="20" width="10" height="1.5" rx="0.75" fill="#683DF5"/>
        <!-- Antenna -->
        <rect x="15.25" y="6" width="1.5" height="4" rx="0.75" fill="white"/>
        <circle cx="16" cy="6" r="1.5" fill="white"/>
        <!-- Ears -->
        <rect x="4" y="13" width="3" height="5" rx="1.5" fill="white"/>
        <rect x="25" y="13" width="3" height="5" rx="1.5" fill="white"/>
      </svg>
    </div>
    <span class="topbar-title">CI configuration</span>
  </div>
  <div class="view-toggle">
    <button class="view-btn active" id="btnVisual" onclick="setView('visual')">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="1" width="6" height="6" rx="1.5"/><rect x="9" y="1" width="6" height="6" rx="1.5"/><rect x="1" y="9" width="6" height="6" rx="1.5"/><rect x="9" y="9" width="6" height="6" rx="1.5"/></svg>
      Visual
    </button>
    <button class="view-btn" id="btnYaml" onclick="setView('yaml')">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 6l-3 2 3 2M12 6l3 2-3 2M9 4l-2 8"/></svg>
      YAML
    </button>
  </div>
  <div class="topbar-actions">
    <button class="btn-ghost" onclick="showDiff()">Show diff</button>
    <button class="btn-ghost" onclick="discard()">Discard</button>
    <button class="btn-save" onclick="saveChanges()">Save changes</button>
  </div>
</div>

<!-- Layout -->
<div class="layout">
  <!-- Sidebar -->
  <nav class="sidebar">
    <div class="sidebar-main">
      <div class="nav-item active" id="nav-workflows" onclick="showSection('workflows')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="3" r="2"/><circle cx="3" cy="13" r="2"/><circle cx="13" cy="13" r="2"/><path d="M8 5v3M8 8l-3 3M8 8l3 3"/></svg>
        Workflows
      </div>
      <div class="nav-item" id="nav-pipelines" onclick="showSection('pipelines')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="5" width="14" height="2.5" rx="1"/><rect x="1" y="8.5" width="14" height="2.5" rx="1"/><circle cx="4" cy="6.25" r="1" fill="currentColor"/><circle cx="4" cy="9.75" r="1" fill="currentColor"/></svg>
        Pipelines
      </div>
      <div class="nav-item" id="nav-stepbundles" onclick="showSection('stepbundles')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 1l6 3.5v7L8 15l-6-3.5v-7z"/></svg>
        Step bundles
      </div>
      <div class="nav-item" id="nav-secrets" onclick="showSection('secrets')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="7" width="10" height="8" rx="2"/><path d="M5 7V5a3 3 0 016 0v2"/></svg>
        Secrets
      </div>
      <div class="nav-item" id="nav-envvars" onclick="showSection('envvars')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6"/><path d="M6 8h4M8 6v4"/></svg>
        Env Vars
      </div>
      <div class="nav-item" id="nav-triggers" onclick="showSection('triggers')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 2L3 9h5l-1 5 8-7H9z"/></svg>
        Triggers
      </div>
      <div class="nav-item" id="nav-containers" onclick="showSection('containers')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="1" y="4" width="14" height="10" rx="2"/><path d="M1 8h14M5 4V2M11 4V2"/></svg>
        Containers
      </div>
    </div>
    <div class="sidebar-bottom">
      <div class="nav-item" onclick="alert('Opens YAML reference docs')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="1" width="12" height="14" rx="2"/><path d="M5 5h6M5 8h6M5 11h4"/></svg>
        YAML Reference
      </div>
      <div class="nav-item" onclick="alert('Browse Workflow Recipes')">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 2a4 4 0 014 4c0 3-4 8-4 8S4 9 4 6a4 4 0 014-4z"/><circle cx="8" cy="6" r="1.5" fill="currentColor"/></svg>
        Workflow Recipes
      </div>
    </div>
  </nav>

  <!-- Middle panel -->
  <div class="middle" id="middlePanel">
    <!-- Workflows view -->
    <div id="view-workflows-middle">
      <div class="workflow-selector">
        <select class="wf-select" id="wfSelect" onchange="selectWorkflow(this.value)"></select>
      </div>
      <div class="workflow-steps" id="stepList">
        <div class="wf-header">
          <div class="wf-name" id="wfTitle">primary</div>
          <div class="wf-sub">Not used by other Workflow</div>
        </div>
        <div id="steps"></div>
        <div class="add-step-btn" onclick="openAddStep()">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 2v10M2 7h10"/></svg>
          Add Step
        </div>
      </div>
    </div>
    <!-- Other section placeholders -->
    <div id="view-pipelines-middle" style="display:none;padding:20px">
      <div style="font-weight:700;font-size:15px;margin-bottom:8px">Pipelines</div>
      <div id="pipelineList"></div>
      <div class="add-step-btn" style="margin-top:8px" onclick="openNewWorkflow()">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 2v10M2 7h10"/></svg>
        New Workflow
      </div>
    </div>
    <div id="view-secrets-middle" style="display:none;padding:20px">
      <div style="font-weight:700;font-size:15px;margin-bottom:12px">Secrets</div>
      <div id="secretsList"></div>
    </div>
    <div id="view-envvars-middle" style="display:none;padding:20px">
      <div style="font-weight:700;font-size:15px;margin-bottom:12px">App Environment Variables</div>
      <div id="envVarsList"></div>
    </div>
    <div id="view-triggers-middle" style="display:none;padding:20px">
      <div style="font-weight:700;font-size:15px;margin-bottom:12px">Triggers</div>
      <div id="triggersList"></div>
    </div>
    <div id="view-stepbundles-middle" style="display:none;padding:20px">
      <div style="color:#888;font-size:13px;margin-top:40px;text-align:center">No step bundles defined yet.</div>
    </div>
    <div id="view-containers-middle" style="display:none;padding:20px">
      <div style="color:#888;font-size:13px;margin-top:40px;text-align:center">No custom containers configured.</div>
    </div>
  </div>

  <!-- Right panel -->
  <div class="right" id="rightPanel">
    <div id="yaml-view" class="panel-card" style="display:none">
      <div class="yaml-view" id="yamlContent"></div>
    </div>
    <div id="visual-right">
      <!-- Workflows config panel -->
      <div id="right-workflows" class="panel-card">
        <div class="panel-header">
          <div class="panel-title" id="rightTitle">primary</div>
          <div class="panel-sub">Not used by other Workflow</div>
        </div>
        <div class="panel-tabs">
          <button class="tab-btn active" id="tabConfig" onclick="showTab('config')">Configuration</button>
          <button class="tab-btn" id="tabProps" onclick="showTab('props')">Properties</button>
          <button class="tab-btn" id="tabTriggers" onclick="showTab('triggers')">Triggers</button>
        </div>
        <div class="tab-content" id="tabConfigContent">
          <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion('envAcc')">
              Env Vars
              <svg class="chevron" id="chevEnvAcc" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6l4 4 4-4"/></svg>
            </div>
            <div class="accordion-body" id="envAcc" style="display:none">
              <div class="env-row"><input class="env-key" value="APP_NAME" readonly><input class="env-val" value="MyMobileApp" readonly></div>
              <div class="env-row"><input class="env-key" value="BUILD_ENV" readonly><input class="env-val" value="production" readonly></div>
            </div>
          </div>
          <div class="accordion">
            <div class="accordion-header" onclick="toggleAccordion('stackAcc')">
              Stack & Machine
              <svg class="chevron" id="chevStackAcc" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6l4 4 4-4"/></svg>
            </div>
            <div class="accordion-body" id="stackAcc" style="display:none">
              <div style="font-size:13px;color:#666">Ubuntu 22.04 · Linux · 2 vCPU · 4 GB RAM</div>
            </div>
          </div>
        </div>
        <div class="tab-content" id="tabPropsContent" style="display:none">
          <div style="font-size:13px;color:#888">Workflow timeout: none<br>No utility workflows assigned.</div>
        </div>
        <div class="tab-content" id="tabTriggersContent" style="display:none">
          <div id="rightTriggersList" style="font-size:13px;color:#888"></div>
        </div>
      </div>
      <!-- Other section right panels -->
      <div id="right-secrets" style="display:none" class="panel-card">
        <div class="panel-header" style="padding-bottom:16px">
          <div class="panel-title">Secrets</div>
          <div class="panel-sub">Encrypted key-value pairs injected at build time</div>
        </div>
      </div>
      <div id="right-envvars" style="display:none" class="panel-card">
        <div class="panel-header" style="padding-bottom:16px">
          <div class="panel-title">App Environment Variables</div>
          <div class="panel-sub">Shared across all workflows in this app</div>
        </div>
      </div>
      <div id="right-triggers" style="display:none" class="panel-card">
        <div class="panel-header" style="padding-bottom:16px">
          <div class="panel-title">Triggers</div>
          <div class="panel-sub">Define when workflows run automatically</div>
        </div>
      </div>
      <div id="right-pipelines" style="display:none" class="panel-card">
        <div class="panel-header" style="padding-bottom:16px">
          <div class="panel-title">Pipelines</div>
          <div class="panel-sub">Chain multiple workflows with dependencies</div>
        </div>
      </div>
      <div id="right-other" style="display:none" class="panel-card">
        <div class="panel-header" style="padding-bottom:16px">
          <div class="panel-title" id="rightOtherTitle">Section</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Add Step Modal -->
<div class="modal-overlay" id="addStepModal">
  <div class="modal">
    <div class="modal-header">
      <span class="modal-title">Add Step</span>
      <button class="modal-close" onclick="closeAddStep()">&#x2715;</button>
    </div>
    <div class="modal-search">
      <input type="text" placeholder="Search steps..." id="stepSearch" oninput="filterSteps()" />
    </div>
    <div id="stepOptions"></div>
  </div>
</div>

<!-- New Workflow Modal -->
<div class="modal-overlay" id="newWfModal">
  <div class="nw-modal">
    <div class="modal-header">
      <span class="modal-title">New Workflow</span>
      <button class="modal-close" onclick="closeNewWorkflow()">&#x2715;</button>
    </div>
    <div class="nw-body">
      <div class="nw-label">Workflow name</div>
      <input class="nw-input" id="newWfName" placeholder="e.g. deploy" />
    </div>
    <div class="nw-footer">
      <button class="btn-ghost" onclick="closeNewWorkflow()">Cancel</button>
      <button class="btn-save" onclick="createWorkflow()">Create Workflow</button>
    </div>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
const STEP_LIBRARY = [
  {id:"git-clone", title:"Git Clone Repository", desc:"Clone your repository to the build machine", version:"8.5.1", icon:"🔴", color:"#e74c3c"},
  {id:"run-tests", title:"Run Tests", desc:"Execute your test suite with coverage reporting", version:"1.2.1", icon:"⬛", color:"#2c3e50"},
  {id:"deploy", title:"Deploy to Bitrise.io", desc:"Upload build artifacts and test reports", version:"2.25.0", icon:"🔵", color:"#3498db"},
  {id:"code-quality", title:"Code Quality Scan", desc:"Run static analysis and code quality checks", version:"1.0.0", icon:"🟢", color:"#27ae60"},
  {id:"slack-notify", title:"Send a Slack message", desc:"Post build status notifications to Slack", version:"3.2.1", icon:"🟣", color:"#9b59b6"},
  {id:"cache-push", title:"Bitrise.io Cache:Push", desc:"Push build cache to speed up future builds", version:"2.4.3", icon:"🟡", color:"#f39c12"},
  {id:"cache-pull", title:"Bitrise.io Cache:Pull", desc:"Restore build cache from previous builds", version:"2.4.3", icon:"🟡", color:"#f39c12"},
  {id:"android-build", title:"Android Build", desc:"Build your Android project with Gradle", version:"1.0.9", icon:"🟢", color:"#3ddc84"},
  {id:"xcode-build", title:"Xcode build for iOS", desc:"Build iOS project with Xcode", version:"2.3.0", icon:"⬛", color:"#555"},
  {id:"fastlane", title:"Fastlane", desc:"Run Fastlane lanes for iOS/Android automation", version:"3.3.15", icon:"🔶", color:"#e67e22"},
];

let state = null;
let currentWorkflow = "primary";
let currentView = "workflows";
let currentTab = "config";
let selectedStepIdx = null;

async function fetchState(){
  const r = await fetch('/api/state');
  state = await r.json();
}

function stepIconSvg(color){
  return `<div class="step-icon" style="background:${color}20;color:${color}">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="${color}" stroke-width="1.8"><rect x="2" y="2" width="12" height="12" rx="3"/><path d="M5 8h6M8 5v6"/></svg>
  </div>`;
}

function renderSteps(){
  if(!state) return;
  const wf = state.workflows[currentWorkflow];
  if(!wf) return;
  document.getElementById('wfTitle').textContent = currentWorkflow;
  document.getElementById('rightTitle').textContent = currentWorkflow;

  // Update workflow select
  const sel = document.getElementById('wfSelect');
  const wfKeys = Object.keys(state.workflows);
  sel.innerHTML = wfKeys.map(k => `<option value="${k}" ${k===currentWorkflow?'selected':''}>${k}</option>`).join('');

  const steps = document.getElementById('steps');
  steps.innerHTML = wf.steps.map((s, i) => `
    <div class="step-item ${selectedStepIdx===i?'selected':''}" onclick="selectStep(${i})">
      <span class="drag-handle">&#8942;&#8942;</span>
      ${stepIconSvg(s.color)}
      <div class="step-info">
        <div class="step-title">${s.title}</div>
        <div class="step-version">${s.version}</div>
      </div>
    </div>
  `).join('');
}

function renderPipelines(){
  const list = document.getElementById('pipelineList');
  const wfKeys = Object.keys(state.workflows);
  list.innerHTML = wfKeys.map(k => `
    <div class="step-item" onclick="selectWorkflow('${k}');showSection('workflows')">
      <div class="step-icon" style="background:#f0ebff;color:#6b4eff">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#6b4eff" stroke-width="1.8"><circle cx="8" cy="3" r="2"/><circle cx="3" cy="13" r="2"/><circle cx="13" cy="13" r="2"/><path d="M8 5v3M8 8l-3 3M8 8l3 3"/></svg>
      </div>
      <div class="step-info"><div class="step-title">${k}</div><div class="step-version">${state.workflows[k].steps.length} steps</div></div>
    </div>
  `).join('');
}

function renderSecrets(){
  document.getElementById('secretsList').innerHTML = state.secrets.map(s => `
    <div class="step-item">
      <div class="step-info">
        <div class="step-title" style="font-family:monospace">${s.key}</div>
        <div class="step-version">${s.is_protected ? '🔒 Protected' : s.value}</div>
      </div>
    </div>
  `).join('');
}

function renderEnvVars(){
  document.getElementById('envVarsList').innerHTML = state.env_vars.map(e => `
    <div class="env-row" style="margin-bottom:8px">
      <input class="env-key" value="${e.key}" readonly>
      <input class="env-val" value="${e.value}" readonly>
    </div>
  `).join('');
}

function renderTriggers(){
  document.getElementById('triggersList').innerHTML = state.triggers.map(t => `
    <div class="step-item">
      <div class="step-icon" style="background:#fff8e6;color:#f39c12">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#f39c12" stroke-width="1.8"><path d="M13 2L3 9h5l-1 5 8-7H9z"/></svg>
      </div>
      <div class="step-info">
        <div class="step-title">${t.event} → ${t.branch}</div>
        <div class="step-version">Workflow: ${t.workflow}</div>
      </div>
    </div>
  `).join('');
  document.getElementById('rightTriggersList').innerHTML = state.triggers.map(t =>
    `<div style="margin-bottom:6px">• ${t.event} on <code>${t.branch}</code> → <strong>${t.workflow}</strong></div>`
  ).join('');
}

function selectWorkflow(name){
  currentWorkflow = name;
  selectedStepIdx = null;
  renderSteps();
}

function selectStep(i){
  selectedStepIdx = i;
  renderSteps();
}

function showSection(sec){
  currentView = sec;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.getElementById('nav-'+sec)?.classList.add('active');

  // Middle panels
  ['workflows','pipelines','secrets','envvars','triggers','stepbundles','containers'].forEach(v => {
    const el = document.getElementById('view-'+v+'-middle');
    if(el) el.style.display = v===sec ? '' : 'none';
  });

  // Right panels
  ['workflows','secrets','envvars','triggers','pipelines'].forEach(v => {
    const el = document.getElementById('right-'+v);
    if(el) el.style.display = 'none';
  });
  document.getElementById('right-other').style.display = 'none';

  if(sec==='workflows') document.getElementById('right-workflows').style.display='';
  else if(sec==='secrets'){ renderSecrets(); document.getElementById('right-secrets').style.display=''; }
  else if(sec==='envvars'){ renderEnvVars(); document.getElementById('right-envvars').style.display=''; }
  else if(sec==='triggers'){ renderTriggers(); document.getElementById('right-triggers').style.display=''; }
  else if(sec==='pipelines'){ renderPipelines(); document.getElementById('right-pipelines').style.display=''; }
  else {
    document.getElementById('right-other').style.display='';
    document.getElementById('rightOtherTitle').textContent = sec.charAt(0).toUpperCase()+sec.slice(1);
  }
}

function showTab(tab){
  currentTab = tab;
  ['config','props','triggers'].forEach(t => {
    document.getElementById('tab'+t.charAt(0).toUpperCase()+t.slice(1)).classList.remove('active');
    document.getElementById('tabContent' in {config:1}?'tab'+t.charAt(0).toUpperCase()+t.slice(1)+'Content':'tab'+t.charAt(0).toUpperCase()+t.slice(1)+'Content').style.display='none';
  });
  const map = {config:'Config',props:'Props',triggers:'Triggers'};
  document.getElementById('tab'+map[tab]).classList.add('active');
  document.getElementById('tab'+map[tab]+'Content').style.display='';
}

function toggleAccordion(id){
  const body = document.getElementById(id);
  const chev = document.getElementById('chev'+id.charAt(0).toUpperCase()+id.slice(1));
  const open = body.style.display!=='none';
  body.style.display = open ? 'none' : '';
  if(chev) chev.classList.toggle('open', !open);
}

function setView(view){
  document.getElementById('btnVisual').classList.toggle('active', view==='visual');
  document.getElementById('btnYaml').classList.toggle('active', view==='yaml');
  document.getElementById('yaml-view').style.display = view==='yaml' ? '' : 'none';
  document.getElementById('visual-right').style.display = view==='visual' ? '' : 'none';
  if(view==='yaml') loadYaml();
}

async function loadYaml(){
  const r = await fetch('/api/yaml');
  const d = await r.json();
  document.getElementById('yamlContent').innerHTML = d.yaml
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/(^|\\n)(\w[^:]+):/gm, '$1<span class="yaml-key">$2</span>:')
    .replace(/: (["'][^"']*["'])/g, ': <span class="yaml-str">$1</span>');
}

// Add step modal
const ALL_STEPS = STEP_LIBRARY;
let filteredSteps = [...ALL_STEPS];

function openAddStep(){
  filteredSteps = [...ALL_STEPS];
  renderStepOptions();
  document.getElementById('stepSearch').value='';
  document.getElementById('addStepModal').classList.add('open');
}
function closeAddStep(){ document.getElementById('addStepModal').classList.remove('open'); }
function filterSteps(){
  const q = document.getElementById('stepSearch').value.toLowerCase();
  filteredSteps = ALL_STEPS.filter(s => s.title.toLowerCase().includes(q) || s.desc.toLowerCase().includes(q));
  renderStepOptions();
}
function renderStepOptions(){
  document.getElementById('stepOptions').innerHTML = filteredSteps.map(s => `
    <div class="step-option">
      <div class="step-option-icon" style="background:${s.color}20;color:${s.color}">${s.icon}</div>
      <div class="step-option-info">
        <div class="step-option-name">${s.title}</div>
        <div class="step-option-desc">${s.desc}</div>
        <div class="step-option-version">v${s.version}</div>
      </div>
      <button class="step-option-add" onclick="addStep('${s.id}')">+ Add</button>
    </div>
  `).join('');
}

async function addStep(stepId){
  const step = ALL_STEPS.find(s=>s.id===stepId);
  if(!step) return;
  await fetch('/api/steps', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({workflow: currentWorkflow, step_id: stepId, title: step.title, version: step.version, color: step.color})
  });
  await fetchState();
  renderSteps();
  closeAddStep();
  showToast('Step "'+step.title+'" added to '+currentWorkflow);
}

// New workflow modal
function openNewWorkflow(){ document.getElementById('newWfName').value=''; document.getElementById('newWfModal').classList.add('open'); }
function closeNewWorkflow(){ document.getElementById('newWfModal').classList.remove('open'); }

async function createWorkflow(){
  const name = document.getElementById('newWfName').value.trim();
  if(!name){ alert('Please enter a workflow name'); return; }
  await fetch('/api/workflows', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name})
  });
  await fetchState();
  currentWorkflow = name;
  showSection('workflows');
  renderSteps();
  closeNewWorkflow();
  showToast('Workflow "'+name+'" created');
}

function showDiff(){ showToast('No uncommitted changes'); }
function discard(){ showToast('Changes discarded'); }
function saveChanges(){ showToast('Configuration saved ✓'); }

function showToast(msg){
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'), 2800);
}

async function poll(){
  await fetchState();
  if(currentView==='workflows') renderSteps();
  else if(currentView==='pipelines') renderPipelines();
  else if(currentView==='secrets') renderSecrets();
  else if(currentView==='envvars') renderEnvVars();
  else if(currentView==='triggers') renderTriggers();
}

(async()=>{
  await fetchState();
  renderSteps();
  setInterval(poll, 5000);
})();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return HTML_SPA

@app.get("/api/state")
def get_state():
    return STATE

@app.get("/api/workflows")
def get_workflows():
    return {"workflows": {k: {"title": v.get("title", k), "steps": v["steps"]} for k, v in STATE["workflows"].items()}}

@app.get("/api/workflows/{name}")
def get_workflow(name: str):
    if name not in STATE["workflows"]:
        return JSONResponse({"error": "not found"}, status_code=404)
    return STATE["workflows"][name]

@app.post("/api/workflows")
async def create_workflow(request: Request):
    body = await request.json()
    name = body.get("name", "").strip().lower().replace(" ", "-")
    if not name:
        return JSONResponse({"error": "name required"}, status_code=400)
    STATE["workflows"][name] = {
        "title": name.replace("-", " ").title(),
        "steps": [
            {"id": "script", "title": "Script", "version": "1.2.1", "icon": "script", "color": "#6b4eff"}
        ]
    }
    return {"name": name, "steps": STATE["workflows"][name]["steps"]}

@app.post("/api/steps")
async def add_step(request: Request):
    body = await request.json()
    wf = body.get("workflow", "primary")
    if wf not in STATE["workflows"]:
        return JSONResponse({"error": "workflow not found"}, status_code=404)
    step = {
        "id": body.get("step_id", "script"),
        "title": body.get("title", "New Step"),
        "version": body.get("version", "1.0.0"),
        "icon": body.get("step_id", "script"),
        "color": body.get("color", "#6b4eff")
    }
    STATE["workflows"][wf]["steps"].append(step)
    return {"workflow": wf, "steps": STATE["workflows"][wf]["steps"]}

@app.get("/api/yaml")
def get_yaml():
    lines = ["format_version: '26'", "default_step_lib_source: https://github.com/bitrise-io/bitrise-steplib.git", "workflows:"]
    for wf_name, wf in STATE["workflows"].items():
        lines.append(f"  {wf_name}:")
        lines.append(f"    title: {wf.get('title', wf_name)}")
        lines.append("    steps:")
        for s in wf["steps"]:
            lines.append(f"    - script@1:")
            lines.append(f"        title: {s['title']}")
    return {"yaml": "\n".join(lines)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
