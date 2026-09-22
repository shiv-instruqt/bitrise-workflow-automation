resource "page" "first_workflow" {
  title = "Your First Bitrise Workflow"
  file  = "instructions/bitrise/first-workflow.md"

  activities = {
    "first_workflow" = resource.task.first_workflow
  }
}

resource "page" "add_pipeline_step" {
  title = "Add a Code Quality Step"
  file  = "instructions/bitrise/add-pipeline-step.md"

  activities = {
    "add_pipeline_step" = resource.task.add_pipeline_step
  }
}

resource "page" "parallel_pipelines" {
  title = "Run Parallel Workflows"
  file  = "instructions/bitrise/parallel-pipelines.md"

  activities = {
    "parallel_pipelines" = resource.task.parallel_pipelines
  }
}
