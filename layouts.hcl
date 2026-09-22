resource "layout" "workstation" {
  column {
    width = 67

    tab "workflow_editor" {
      title  = "Workflow Editor"
      target = resource.service.workflow_editor
      active = true
    }

    tab "terminal" {
      title  = "Terminal"
      target = resource.terminal.workstation
    }
  }

  column {
    width = 33

    instructions {
      title = "Instructions"
    }
  }
}
