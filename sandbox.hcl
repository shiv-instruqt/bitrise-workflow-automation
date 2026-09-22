resource "network" "main" {
  subnet = "10.0.10.0/24"
}

resource "container" "workstation" {
  image {
    name = "ubuntu:22.04"
  }

  # ubuntu:22.04 has no long-running entrypoint, so keep the container alive.
  command = ["sleep", "infinity"]

  resources {
    cpu    = 1000
    memory = 1024
  }

  network {
    id = resource.network.main.meta.id
  }

  # The Workflow Editor simulation listens here; resource.service.workflow_editor proxies it.
  port {
    local    = 8080
    host     = 8080
    protocol = "tcp"
  }

  # Lab payloads (CLI wrapper, sample bitrise.yml, Workflow Editor simulation)
  # are mounted read-only and installed by resource.exec.setup_workstation.
  volume {
    source      = "./files"
    destination = "/opt/lab-files"
    type        = "bind"
    read_only   = true
  }
}

resource "exec" "setup_workstation" {
  target  = resource.container.workstation
  script  = "scripts/exec/setup_workstation/script.sh"
  timeout = "300s"
}
