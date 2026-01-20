# MARTINS-432-FLOW-2025 | Sistema de Ativação Vitrine
from core.loader import load_system_parameters
from core.engine import SigmaClock

def executar_sincronia():
    # 1. O Loader lê o Cérebro (config.yaml)
    diretrizes = load_system_parameters()
    
    if diretrizes:
        # 2. O Coração (engine.py) assume a frequência
        clock = SigmaClock()
        
        print(f"\n[ Grade {diretrizes['system']['name']} Iniciada ]")
        
        # 3. Teste de Atrito (Rede Neural vs Hardware em 432Hz)
        clock.check_friction(432.0, 432.0)

if __name__ == "__main__":
    executar_sincronia()
