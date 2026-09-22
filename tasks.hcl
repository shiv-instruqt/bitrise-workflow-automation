resource "task" "first_workflow" {
  description     = "Run the pre-built primary workflow with the Bitrise CLI and capture its output."
  success_message = "Nice — you ran a full Bitrise workflow end to end."

  config {
    target            = resource.container.workstation
    user              = "root"
    group             = "root"
    working_directory = "/root/mobile-app"
    timeout           = "60s"
  }

  condition "primary_workflow_ran" {
    description = "The `primary` workflow has been run and its output saved to `/tmp/primary_output.txt`"

    check {
      script          = "scripts/task/first_workflow/check.sh"
      failure_message = "Run 'bitrise run primary 2>&1 | tee /tmp/primary_output.txt' in the terminal first."
    }

    solve {
      script = "scripts/task/first_workflow/solve.sh"
    }
  }
}

resource "task" "add_pipeline_step" {
  description     = "Add the Code Quality Scan step to the primary workflow and confirm it via the API."
  success_message = "The primary workflow now has four steps."

  config {
    target            = resource.container.workstation
    user              = "root"
    group             = "root"
    working_directory = "/root/mobile-app"
    timeout           = "60s"
  }

  condition "step_count_is_four" {
    description = "The `primary` workflow contains 4 steps and the count is saved to `/tmp/step_count.txt`"

    check {
      script          = "scripts/task/add_pipeline_step/check.sh"
      failure_message = "Expected 4 steps in the primary workflow. Add the Code Quality Scan step via the Workflow Editor's '+ Add Step' button, then re-run the curl command that writes /tmp/step_count.txt."
    }

    solve {
      script = "scripts/task/add_pipeline_step/solve.sh"
    }
  }
}

resource "task" "parallel_pipelines" {
  description     = "Create a deploy workflow alongside primary and run it."
  success_message = "Both workflows exist and the deploy workflow has run."

  config {
    target            = resource.container.workstation
    user              = "root"
    group             = "root"
    working_directory = "/root/mobile-app"
    timeout           = "60s"
  }

  condition "deploy_workflow_ran" {
    description = "The `deploy` workflow has been run and its output saved to `/tmp/deploy_output.txt`"

    check {
      script          = "scripts/task/parallel_pipelines/check.sh"
      failure_message = "Deploy workflow output not found. Run: cd /root/mobile-app && bitrise run deploy 2>&1 | tee /tmp/deploy_output.txt"
    }

    solve {
      script = "scripts/task/parallel_pipelines/solve.sh"
    }
  }
}
