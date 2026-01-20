# MARTINS-432-FLOW-2025 | Core Engine - Sigma Clock V2.2 (Defesa Ativa Nível 2)
import yaml
import os
from enum import Enum

class SigmaState(Enum):
    RUNNING = "running"
    SILENCE = "silence"
    FAULT = "fault"

class SigmaClock:
    def __init__(self, config_path=None):
        # 1. Blindagem de Caminho: Localiza a raiz do projeto automaticamente
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config.yaml")

        # 2. Conexão Real com o Cérebro (YAML)
        try:
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)
                sigma_cfg = cfg["sigma_clock"]
                
            self.target = sigma_cfg["target_value"]
            self.tolerance = sigma_cfg["tolerance"]
            self.silence_after = sigma_cfg["silence_after"]
            self.recovery_window = sigma_cfg["recovery_window"]
            print(f"--- Cérebro Conectado: {config_path} ---")
        except Exception as e:
            print(f"⚠ Alerta: Usando parâmetros de emergência. Erro: {e}")
            self.target, self.tolerance = 432.0, 0.001
            self.silence_after, self.recovery_window = 3, 5

        self.state = SigmaState.RUNNING
        self.failure_count = 0
        self.stable_count = 0
        
        # 3. Módulo de Defesa Ativa (Nível 2)
        self.last_friction = 0.0

    def get_friction(self, value):
        """Calcula o atrito lógico entre a observação e o alvo."""
        return abs(value - self.target)

    def evaluate_tick(self, observed_value):
        """O Coração do Relógio: Avalia se o avanço é autorizado."""
        friction = self.get_friction(observed_value)
        
        # Verifica padrões de ataque antes de tratar o estado
        self._analyze_entropy(friction)
        
        if self.state == SigmaState.SILENCE:
            return self._handle_silence(friction)
        return self._handle_running(friction)

    def _analyze_entropy(self, current_friction):
        """Analisa se o atrito atual repete um padrão de desvio."""
        if current_friction > self.tolerance and current_friction == self.last_friction:
            print("🚨 ALERTA DE DEFESA: Ataque de desvio sistemático detectado!")
        self.last_friction = current_friction

    def _handle_running(self, friction):
        """Comportamento em estado de operação normal."""
        if friction <= self.tolerance:
            self.failure_count = 0
            print("✔ Tick Σ Autorizado.")
            return True
        
        self.failure_count += 1
        print(f"⚠ Atrito detetado: {friction:.4f} (Falha {self.failure_count}/{self.silence_after})")
        
        if self.failure_count >= self.silence_after:
            self.state = SigmaState.SILENCE
            self.stable_count = 0
            print("🛑 BLOQUEIO: Entrando em SILÊNCIO OPERACIONAL")
        return False

    def _handle_silence(self, friction):
        """O 'Deep Freeze': Proteção contra instabilidade persistente."""
        print(f"--- SISTEMA EM SILÊNCIO --- Atrito atual: {friction:.4f}")
        
        if friction <= self.tolerance:
            self.stable_count += 1
            print(f"✨ Estabilidade observada ({self.stable_count}/{self.recovery_window})")
            
            if self.stable_count >= self.recovery_window:
                self.state = SigmaState.RUNNING
                self.failure_count = 0
                print("♻ RECONEXÃO: Saindo do silêncio. Relógio Σ retomado.")
        else:
            self.stable_count = 0
            print("❌ Instabilidade persiste. O Silêncio é mantido.")
            
        return False
