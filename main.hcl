resource "lab" "bitrise_workflow_automation" {
  title = "Bitrise: Automate Your Mobile CI/CD"

  description = <<-EOF
    Build, test, and deploy mobile apps automatically — from a single visual workflow
    editor to the CLI that powers every Bitrise build machine.

    Experience how Bitrise orchestrates mobile CI/CD with a visual Workflow Editor
    and a powerful CLI runner. In 18 minutes you will explore a pre-built pipeline,
    add a code quality step, and run parallel workflows — all without a Bitrise account.
  EOF

  icon = "/assets/bitrise.png"

  settings {
    timelimit {
      duration   = "30m"
      show_timer = true
    }

    idle {
      enabled      = true
      timeout      = "400s"
      show_warning = true
    }

    controls {
      show_stop = true
    }
  }

  layout = resource.layout.workstation

  content {
    title = "Bitrise Workflow Automation"

    chapter "bitrise" {
      title = "Bitrise Workflow Automation"

      page "first_workflow" {
        title     = "Your First Bitrise Workflow"
        reference = resource.page.first_workflow
      }

      page "add_pipeline_step" {
        title     = "Add a Code Quality Step"
        reference = resource.page.add_pipeline_step
      }

      page "parallel_pipelines" {
        title     = "Run Parallel Workflows"
        reference = resource.page.parallel_pipelines
      }
    }
  }
}
