#!/usr/bin/env bash
set -euo pipefail

# ops.sh — a tiny ops toolkit with subcommands.
# usage: ./ops.sh cpu|ram|disk|restart <svc>|logs <svc>|ports

usage() {
  echo "usage: $0 cpu|ram|disk|restart <svc>|logs <svc>|ports"
}

cmd="${1:-}"

case "$cmd" in
  cpu)
    # current CPU load summary
    top -bn1 | grep "Cpu(s)"
    ;;
  ram)
    # memory usage, human-readable
    free -h
    ;;
  disk)
    # filesystem usage, then the biggest directories under /var
    df -h
    echo
    du -sh /var/* 2>/dev/null | sort -rh | head
    ;;
  restart)
    # changes state — restart a service and confirm it came back up
    svc="${2:?usage: $0 restart <svc>}"
    sudo systemctl restart "$svc" && systemctl is-active "$svc"
    ;;
  logs)
    # last hour of logs for a service, most recent 50 lines
    svc="${2:?usage: $0 logs <svc>}"
    journalctl -u "$svc" --since "1 hour ago" --no-pager | tail -n 50
    ;;
  ports)
    # everything listening, with the owning process
    ss -tulpn
    ;;
  *)
    usage
    exit 1
    ;;
esac
