#!/usr/bin/env bash
set -euo pipefail

# Deterministic installation helper.
# Run only on an authorized Linux host.
#
# Usage:
#   sudo ./install_splunk.sh /tmp/splunk-package.tgz /opt/splunk

PACKAGE_PATH="${1:?Package path required}"
SPLUNK_HOME="${2:-/opt/splunk}"

if [[ ! -f "$PACKAGE_PATH" ]]; then
  echo "ERROR: package not found: $PACKAGE_PATH" >&2
  exit 1
fi

if [[ "$(id -u)" -ne 0 ]]; then
  echo "ERROR: run with root privileges." >&2
  exit 1
fi

getent group splunk >/dev/null || groupadd --system splunk
id splunk >/dev/null 2>&1 || useradd --system --gid splunk \
  --home-dir "$SPLUNK_HOME" --shell /bin/bash splunk

mkdir -p "$(dirname "$SPLUNK_HOME")"

if [[ -d "$SPLUNK_HOME" ]]; then
  echo "Splunk home already exists: $SPLUNK_HOME"
else
  tar -xzf "$PACKAGE_PATH" -C "$(dirname "$SPLUNK_HOME")"
fi

chown -R splunk:splunk "$SPLUNK_HOME"

if [[ -x "$SPLUNK_HOME/bin/splunk" ]]; then
  "$SPLUNK_HOME/bin/splunk" enable boot-start -user splunk \
    --accept-license --answer-yes
  systemctl daemon-reload || true
  systemctl enable Splunkd || true
  systemctl start Splunkd || true
else
  echo "ERROR: Splunk executable not found at $SPLUNK_HOME/bin/splunk" >&2
  exit 1
fi

echo "Installation helper completed."
