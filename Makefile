# ==========================
#        CONFIGURATION
# ==========================

PYTHON := python
PYTEST := pytest
COVERAGE := coverage

SRC := src/triangulator

# ==========================
#        COMMANDES
# ==========================

# Lancer tous les tests
test:
	$(PYTEST)

# Tests unitaires uniquement (on exclut les perfs)
unit_test:
	$(PYTEST) -k "not performance"

# Tests de performance uniquement
perf_test:
	$(PYTEST) -k "performance"

# Couverture de code + rapport HTML
coverage:
	$(COVERAGE) run -m pytest
	$(COVERAGE) html
	@echo "Rapport généré : htmlcov/index.html"

# Linting avec ruff
lint:
	ruff check .

# Génération de documentation
doc:
	pdoc --html $(SRC) --output-dir docs --force
	@echo "Documentation disponible dans docs/"

# Nettoyage
clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache htmlcov docs
