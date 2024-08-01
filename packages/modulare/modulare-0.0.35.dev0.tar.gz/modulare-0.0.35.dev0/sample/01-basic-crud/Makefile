# Definir o alvo de desenvolvimento
dev:
	@PYTHONPATH=src uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Definir o alvo de produção
prod:
	@PYTHONPATH=src uvicorn src.main:app --host 0.0.0.0 --port 8000
