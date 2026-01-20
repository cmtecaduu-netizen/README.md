# MARTINS-432-FLOW-2025 | Simulador de Sincronia V2
from core.engine import SigmaClock
import time

def executar_missao_nivel1():
    # Inicializa o Relógio Σ lendo o config.yaml
    relogio = SigmaClock()
    
    # Sequência de teste: 10 Ticks de observação
    # Simulando valores enviados pela "Rede Neural"
    observacoes = [
        432.0, 432.0,          # Estável
        432.5, 432.5, 432.5,  # RUÍDO (Deve ativar o Silêncio aqui)
        432.0, 432.0, 432.0,  # Recuperando (Ainda no Silêncio)
        432.0, 432.0           # Recuperado (Deve voltar ao Running)
    ]

    print(f"--- INICIANDO GRADE {relogio.target}Hz ---")
    
    for i, valor in enumerate(observacoes):
        print(f"\n[Tick {i+1}] Observado: {valor}")
        relogio.evaluate_tick(valor)
        time.sleep(0.5) # Pequena pausa para visualização

if __name__ == "__main__":
    executar_missao_nivel1()
