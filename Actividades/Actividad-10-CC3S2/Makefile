# Flags comunes para pytest (puedes ampliarlas)
PYTEST_FLAGS ?= -q
COVERAGE_FLAGS ?= --cov=models --cov=tests --cov-report=term-missing --cov-fail-under=85
PY_WARNINGS  ?= ignore::DeprecationWarning

# Lint (modo "relajado" por defecto para desarrollo)
LINT_MAX_LINE ?= 88
LINT_IGNORE   ?= E501,W391,W293
# Ignora F401 en reexport del __init__ y E402 solo en archivos de tests
LINT_PER_FILE ?= src/models/__init__.py:F401,tests/*.py:E402

.PHONY: install
install:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt
	@if [ -f requirements-dev.txt ]; then \
		echo "Instalando dependencias de desarrollo..."; \
		pip install -r requirements-dev.txt; \
	fi

.PHONY: lint
lint:
	@echo "==> Formateando con Ruff..."
	ruff format .
	@echo "==> Ordenando imports (Ruff rule I)..."
	ruff check . --select I --fix
	@echo "==> Autofix de reglas con Ruff (whitespace, etc.)..."
	ruff check . --fix
	@echo "==> Lint con flake8 (relajado: ignora $(LINT_IGNORE); ancho $(LINT_MAX_LINE))..."
	flake8 . \
	    --max-line-length=$(LINT_MAX_LINE) \
	    --extend-ignore=$(LINT_IGNORE) \
	    --per-file-ignores="$(LINT_PER_FILE)"
	@echo "Lint OK"

.PHONY: test
test:
	@echo "Ejecutando pruebas"
	PYTHONWARNINGS="$(PY_WARNINGS)" pytest . $(PYTEST_FLAGS)


.PHONY: coverage
coverage:
	@echo "Ejecutando cobertura"
	@coverage erase
	PYTHONWARNINGS="$(PY_WARNINGS)" coverage run --source=. -m pytest . $(PYTEST_FLAGS) $(COVERAGE_FLAGS);
	@echo "Generando reporte"
	@coverage report -m
	@coverage html -d htmlcov

.PHONY: gates
gates: lint coverage
	@echo "Gates OK"

.PHONY: clean
clean:
	@echo "Eliminando archivos de caché y reportes..."
	# caches python/pytest
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	# coverage
	rm -rf .coverage htmlcov 2>/dev/null || true
	coverage erase || true
	@echo "Limpieza completa."

.PHONY: help
help:
	@echo "Uso: make [comando] [opciones]"
	@echo
	@echo "Comandos disponibles:"
	@echo "  install              Instala dependencias (requirements.txt y opcionalmente requirements-dev.txt)"
	@echo "  lint                 Formatea (ruff), ordena imports (ruff I), autofix y pasa flake8 relajado"
	@echo "  test                 Ejecuta pytest para el suite de pruebas"
	@echo "  coverage             Ejecuta pytest con cobertura para el suite de pruebas"
	@echo "  gates                Ejecuta lint y coverage como gate de calidad"
	@echo "  clean                Elimina archivos temporales, caches, etc."
	@echo
	@echo "Opciones:"
	@echo "  PYTEST_FLAGS='-q -k expr'  Banderas extra para pytest"