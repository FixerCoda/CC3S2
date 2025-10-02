#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-miapp.local}"
PORT="${PORT:-8080}"
LAT_MS_MAX="${LAT_MS_MAX:-500}"   # umbral 0.5s

# HTTP readiness y liveness
curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null
curl -fsS "http://127.0.0.1:${PORT}/ready"  >/dev/null

# DNS local
getent hosts "${HOST}" | grep -qE '(^127\.0\.0\.1\s+)'

# TLS y headers
OUT_TLS="$(openssl s_client -connect ${HOST}:443 -servername ${HOST} -brief </dev/null || true)"
grep -q 'Protocol  : TLSv1.3' <<<"$OUT_TLS" || { echo "No TLSv1.3"; exit 1; }
curl -kI "https://${HOST}/" | grep -qi 'strict-transport-security' || { echo "Sin HSTS"; exit 1; }

# Latencia
LAT_S="$(curl -kso /dev/null -w '%{time_total}\n' "https://${HOST}/")"
LAT_MS="$(awk -v s="$LAT_S" 'BEGIN{printf("%.0f", s*1000)}')"
echo "latency_ms=$LAT_MS"
test "$LAT_MS" -le "$LAT_MS_MAX" || { echo "Latencia > ${LAT_MS_MAX}ms"; exit 1; }

echo "PREDEPLOY CHECKS: OK"
