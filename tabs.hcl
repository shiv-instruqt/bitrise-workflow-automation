resource "service" "workflow_editor" {
  target = resource.container.workstation
  scheme = "http"
  port   = 8080
  path   = "/"
}

resource "terminal" "workstation" {
  target            = resource.container.workstation
  shell             = "/bin/bash"
  user              = "root"
  group             = "root"
  working_directory = "/root/mobile-app"
}
