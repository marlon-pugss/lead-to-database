#!/bin/bash

echo "🔄 Parando processos na porta 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "Nenhum processo encontrado na porta 8000"

echo "🚀 Iniciando servidor via módulo leads..."
./venv/bin/python -m src.leads