# Splunk AI Install Agent

An AI-agent-driven reference implementation for planning, installing, configuring, and validating Splunk Enterprise on Linux.

> **Safety:** The agent defaults to plan/dry-run mode and requires explicit approval before privileged execution. Use only on systems you own or are authorized to administer.

## What it does

A request such as:

> "Install Splunk Enterprise on this RHEL server and enable it at boot."

is converted into a controlled workflow:

1. Collect host facts.
2. Validate prerequisites.
3. Generate a structured installation plan.
4. Apply policy/safety checks.
5. Require approval before privileged execution.
6. Execute deterministic installation tasks.
7. Verify the Splunk service and management port.
8. Produce a machine-readable report.

## Architecture

```text
User
  |
  v
AI Agent / Planner
  |
  +--> Host Facts
  +--> Safety / Policy Checks
  +--> Installation Plan
  +--> Approval Gate
  |
  v
Execution Tools
  |
  +--> Package handling
  +--> Splunk installation
  +--> systemd / boot-start
  +--> Health checks
  |
  v
Verification + Report
```

## Repository

```text
splunk-ai-install-agent/
├── agent/
│   ├── agent.py
│   ├── planner.py
│   ├── policy.py
│   ├── schemas.py
│   └── tools.py
├── config/
│   └── example.yaml
├── docs/
│   └── agent-flow.md
├── scripts/
│   └── install_splunk.sh
├── tests/
│   └── test_policy.py
├── .env.example
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

## Quick start

```bash
git clone https://github.com/<YOUR-ORG>/splunk-ai-install-agent.git
cd splunk-ai-install-agent

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Safe planning-only run:

```bash
python -m agent.agent \
  --request "Install Splunk Enterprise on this Linux server and enable it at boot" \
  --plan-only
```

The reference project does not automatically download Splunk binaries. Supply an approved package/archive path.

## Example request

```text
Install Splunk Enterprise on RHEL 9.
Use /opt/splunk as SPLUNK_HOME.
Enable Splunk at boot.
Do not change the firewall.
Validate that port 8089 is listening after installation.
```

Example structured plan:

```json
{
  "target_os": "linux",
  "actions": [
    "validate_os",
    "validate_package",
    "create_user",
    "install_splunk",
    "enable_boot_start",
    "verify_service",
    "verify_management_port"
  ],
  "firewall_changes": false,
  "requires_approval": true
}
```

## Security model

The important design principle is: **AI reasoning is separated from privileged execution.**

The LLM should propose structured actions; it should not receive unrestricted shell access.

Recommended production controls:

- Dedicated service account.
- Least-privilege sudo.
- Allowlisted package sources.
- Human approval for privileged/destructive actions.
- Complete command/result audit trail.
- Secrets stored in Vault or an equivalent secret manager.
- Change-ticket integration for production.

## Roadmap

- [ ] OpenAI-compatible agent planner
- [ ] Ansible execution backend
- [ ] SSH remote execution
- [ ] Splunk REST API validation
- [ ] Indexer / Search Head / Heavy Forwarder roles
- [ ] Universal Forwarder installation
- [ ] Cluster-aware deployment
- [ ] Post-install security hardening
- [ ] Vault integration
- [ ] ServiceNow approval integration
- [ ] MCP tool interface
- [ ] Multi-host deployment
- [ ] Deployment dashboard

Splunk is a trademark of Splunk LLC. This independent project is not affiliated with or endorsed by Splunk.
