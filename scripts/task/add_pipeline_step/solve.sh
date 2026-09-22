#!/bin/bash
set -euxo pipefail

# Only add the step if it is not already in the primary workflow, so the
# solve stays idempotent and the step count lands on exactly 4.
present="$(curl -s http://localhost:8080/api/workflows/primary | jq -r '[.steps[].id] | index("code-quality")')"

if [ "${present}" = "null" ]; then
  curl -s -X POST http://localhost:8080/api/steps \
    -H "Content-Type: application/json" \
    -d '{"workflow":"primary","step_id":"code-quality","title":"Code Quality Scan","version":"1.0.0","color":"#27ae60"}' > /dev/null
fi

curl -s http://localhost:8080/api/workflows/primary | jq '.steps | length' > /tmp/step_count.txt
cat /tmp/step_count.txt
