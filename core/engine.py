# MARTINS-432-FLOW-2025 | Core Engine - Sigma Clock V2.5 (Soberania Temporal)
import yaml, os
from enum import Enum

class SigmaState(Enum):
    RUNNING, SILENCE, FAULT = "running", "silence", "fault"

class SigmaClock:
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config.yaml")

        try:
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)
                sigma_cfg = cfg["sigma_clock"]
            self.target, self.tolerance = sigma_cfg["target_value"], sigma_cfg["tolerance"]
            self.silence_after, self.recovery_window = sigma_cfg["silence_after"], sigma_cfg["recovery_window"]
        except:
            self.target, self.tolerance, self.silence_after, self.recovery_window = 432.0, 0.001, 3, 5

        self.state, self.failure_count, self.stable_count = SigmaState.RUNNING, 0, 0
        self.friction_history = [] # Ajuste 2: Histórico de Atrito
        self.window_size = 5

    def evaluate_tick(self, observed_value):
        friction = abs(observed_value - self.target)
        
        # Gestão de Memória Temporal
        self.friction_history.append(friction)
        if len(self.friction_history) > self.window_size:
            self.friction_history.pop(0)

        # Defesa Nível 3+: Analisa Amplitude e Repetição
        if self._analyze_trajectory():
            self._force_silence("Trajetória Artificial Detectada")
            return False
        
        return self._handle_silence(friction) if self.state == SigmaState.SILENCE else self._handle_running(friction)

    def _analyze_trajectory(self):
        """Ajuste 1: Detecta se a variação na janela é baixa demais para ser natural."""
        if len(self.friction_history) < self.window_size: return False
        
        # Se a amplitude (Máximo - Mínimo) for quase zero e o erro for alto
        amplitude = max(self.friction_history) - min(self.friction_history)
        is_too_perfect = amplitude < 1e-7 and self.friction_history[-1] > self.tolerance
        
        return is_too_perfect

    def _force_silence(self, reason):
        self.state, self.failure_count, self.stable_count = SigmaState.SILENCE, self.silence_after, 0
        print(f"🚨 DEFESA TEMPORAL: {reason}.")

    def _handle_running(self, friction):
        if friction <= self.tolerance:
            self.failure_count = 0
            print("✔ Tick Σ Autorizado.")
            return True
        self.failure_count += 1
        print(f"⚠ Atrito: {friction:.4f} ({self.failure_count}/{self.silence_after})")
        if self.failure_count >= self.silence_after: self._force_silence("Limite de Falhas")
        return False

    def _handle_silence(self, friction):
        print(f"--- SILÊNCIO --- Atrito: {friction:.4f}")
        if friction <= self.tolerance:
            self.stable_count += 1
            print(f"✨ Estabilidade ({self.stable_count}/{self.recovery_window})")
            if self.stable_count >= self.recovery_window:
                self.state, self.failure_count, self.friction_history = SigmaState.RUNNING, 0, []
                print("♻ RECONEXÃO: Relógio Σ retomado.")
        else: self.stable_count = 0
        return False
