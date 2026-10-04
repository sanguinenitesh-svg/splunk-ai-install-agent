# AI Agent Flow

## 1. Understand
The user describes the desired deployment in natural language.

## 2. Plan
The AI converts the request into a structured `InstallPlan`.

## 3. Policy
The policy engine rejects unsupported or unsafe actions.

## 4. Approve
Production deployments should require explicit approval before privileged execution.

## 5. Execute
Use a deterministic backend such as Ansible, restricted SSH, or a deployment service.

## 6. Verify
Validate Splunk service status, TCP 8089, TCP 8000 where applicable,
SPLUNK_HOME ownership, boot-start configuration, and basic REST/API health.

## 7. Report
Return structured JSON containing host facts, intent, approved plan,
actions performed, verification results, errors, and remediation guidance.
