#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.db import Base, engine
from src.model.lead import Lead
from src.model.lead_source_configuration import LeadSourceConfiguration

def init_database():
    """Cria todas as tabelas no banco de dados"""
    try:
        print("🗃️ Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se as tabelas foram criadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📋 Tabelas disponíveis: {tables}")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Inicializando banco de dados...\n")
    success = init_database()
    if success:
        print("\n🎉 Banco de dados pronto para uso!")
    else:
        print("\n💥 Falha na inicialização do banco de dados")
        sys.exit(1)