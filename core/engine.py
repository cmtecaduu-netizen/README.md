# MARTINS-432-FLOW-2025 | Core Engine - Sigma Clock V2.4 (Janela de Variância)
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
        except:
            self.target, self.tolerance = 432.0, 0.001
            self.silence_after, self.recovery_window = 3, 5

        self.state = SigmaState.RUNNING
        self.failure_count = 0
        self.stable_count = 0
        
        # --- NOVIDADE V2.4: Janela de Histórico ---
        self.history = []
        self.window_size = 5 

    def get_friction(self, value):
        return abs(value - self.target)

    def evaluate_tick(self, observed_value):
        friction = self.get_friction(observed_value)
        
        # Atualiza histórico (mantém apenas os últimos W valores)
        self.history.append(observed_value)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        # Defesa Nível 3: Analisa a trajetória (Variância)
        if self._analyze_trajectory():
            self._force_silence("Trajetória Artificial Detectada")
            return False
        
        if self.state == SigmaState.SILENCE:
            return self._handle_silence(friction)
        return self._handle_running(friction)

    def _analyze_trajectory(self):
        """Detecta estabilidade 'perfeita demais' ou desvios sistemáticos."""
        if len(self.history) < self.window_size:
            return False

        # Se todos os valores no histórico forem idênticos (Epsilon 1e-7)
        # e estiverem fora da tolerância, é um ataque persistente
        diffs = [abs(self.history[i] - self.history[i-1]) for i in range(1, len(self.history))]
        is_static_attack = all(d < 1e-7 for d in diffs) and abs(self.history[-1] - self.target) > self.tolerance
        
        return is_static_attack

    def _force_silence(self, reason):
        self.state = SigmaState.SILENCE
        self.failure_count = self.silence_after
        self.stable_count = 0
        print(f"🚨 DEFESA NÍVEL 3: {reason}. Bloqueio Imediato.")

    def _handle_running(self, friction):
        if friction <= self.tolerance:
            self.failure_count = 0
            print("✔ Tick Σ Autorizado.")
            return True
        
        self.failure_count += 1
        print(f"⚠ Atrito: {friction:.4f} (Falha {self.failure_count}/{self.silence_after})")
        if self.failure_count >= self.silence_after:
            self._force_silence("Limite de Falhas")
        return False

    def _handle_silence(self, friction):
        print(f"--- SILÊNCIO --- Atrito: {friction:.4f}")
        if friction <= self.tolerance:
            self.stable_count += 1
            print(f"✨ Estabilidade ({self.stable_count}/{self.recovery_window})")
            if self.stable_count >= self.recovery_window:
                self.state = SigmaState.RUNNING
                self.failure_count = 0
                self.history = [] # Limpa histórico para nova fase
                print("♻ RECONEXÃO: Relógio Σ retomado.")
        else:
            self.stable_count = 0
        return False
