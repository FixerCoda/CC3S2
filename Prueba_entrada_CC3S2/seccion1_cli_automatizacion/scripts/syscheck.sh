#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[ERROR] Falló en línea $LINENO" >&2' ERR

mkdir -p reports

# TODO: HTTP-guarda headers y explica código en 2-3 líneas al final del archivo
{
  echo "curl -I example.com"
  curl -Is https://example.com | sed '/^\r$/d'
  echo
  echo "Explicación: El código de estado de la respuesta HTTP es 200, lo que indica un resultado exitoso. Se muestran headers con información importante como las fechas de consulta (date) y modificación (last-modified). Además, se revisan headers relacionados con mecanismos de caché como la expiración de la validez de la respuesta tras 86000 segundos (cache-control) y una forma de revisar si se tiene la versión más reciente de una respuesta (etag)."
} > reports/http.txt

# TODO: DNS — muestra A/AAAA/MX y comenta TTL
{
  echo "A";    dig A example.com +noall +answer
  echo "AAAA"; dig AAAA example.com +noall +answer
  echo "MX";   dig MX example.com +noall +answer
  echo
  echo "Nota: La selección del TTL se debe realizar según las prioridades respecto a recursos y disponibilidad. Un TTL alto implica una reducción en el número de consultas, pues el registro tiene validez por mayor tiempo, lo que ahorra recursos. Por otro lado, un TTL bajo agiliza la implementación de cambios al no tener que esperar a la expiración del mismo."
} > reports/dns.txt

# TODO: TLS - registra versión TLS
{
  echo "TLS via curl -Iv"
  curl -Iv https://example.com 2>&1 | sed -n '1,20p'
} > reports/tls.txt

# TODO: Puertos locales - lista y comenta riesgos
{
  echo "ss -tuln"
  ss -tuln || true
  echo
  echo "Riesgos: Puertos abiertos innecesarios pueden representar una vulnerabilidad en la seguridad, debido a que estos puertos pueden revelar información sensible del sistema que un atacante puede aprovechar. Se debe seguir una aproximación similar al principio de "least privilege" y exponer solo los puertos que se necesiten y asignar permisos de uso a únicamente los endpoints autorizados."
} > reports/sockets.txt

echo "Reportes generados en ./reports"
