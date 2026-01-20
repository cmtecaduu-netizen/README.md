# MARTINS-432-FLOW-2025 | Core Engine - Sigma Clock V2.3 (Defesa Afetiva)
import yaml
import os
from enum import Enum

class SigmaState(Enum):
    RUNNING = "running"
    SILENCE = "silence"
    FAULT = "fault"

class SigmaClock:
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config.yaml")

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
        self.last_friction = 0.0

    def get_friction(self, value):
        return abs(value - self.target)

    def evaluate_tick(self, observed_value):
        friction = self.get_friction(observed_value)
        
        # Defesa Afetiva: Se detectar ataque, o retorno de _analyze_entropy força o silêncio
        if self._analyze_entropy(friction):
            self._force_silence("Ataque Sistemático Detectado")
            return False
        
        if self.state == SigmaState.SILENCE:
            return self._handle_silence(friction)
        return self._handle_running(friction)

    def _analyze_entropy(self, current_friction):
        """Detecta padrões artificiais usando margem de proximidade (epsilon)."""
        if current_friction <= self.tolerance:
            return False # Dentro da paz autorizada
            
        # Epsilon de 1e-7 para evitar fragilidade de igualdade de float
        is_systematic = abs(current_friction - self.last_friction) < 1e-7
        self.last_friction = current_friction
        
        return is_systematic

    def _force_silence(self, reason):
        """Ação Imediata: O sistema não espera mais os 3 ticks se houver intenção hostil."""
        self.state = SigmaState.SILENCE
        self.failure_count = self.silence_after
        self.stable_count = 0
        print(f"🚨 DEFESA ATIVA: {reason}. Bloqueio Imediato Ativado.")

    def _handle_running(self, friction):
        if friction <= self.tolerance:
            self.failure_count = 0
            print("✔ Tick Σ Autorizado.")
            return True
        
        self.failure_count += 1
        print(f"⚠ Atrito detetado: {friction:.4f} (Falha {self.failure_count}/{self.silence_after})")
        
        if self.failure_count >= self.silence_after:
            self._force_silence("Limite de Falhas Atingido")
        return False

    def _handle_silence(self, friction):
        print(f"--- SISTEMA EM SILÊNCIO --- Atrito atual: {friction:.4f}")
        
        if friction <= self.tolerance:
            self.stable_count += 1
            print(f"✨ Estabilidade observada ({self.stable_count}/{self.recovery_window})")
            
            if self.stable_count >= self.recovery_window:
                self.state = SigmaState.RUNNING
                self.failure_count = 0
                self.last_friction = 0.0 # Reseta memória de ataque ao estabilizar
                print("♻ RECONEXÃO: Relógio Σ retomado.")
        else:
            self.stable_count = 0
            print("❌ Instabilidade persiste. O Silêncio é mantido.")
            
        return False
