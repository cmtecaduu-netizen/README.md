# MARTINS-432-FLOW-2025 | Configuration Loader
# Este script conecta as leis (YAML) à máquina (Python)

import yaml

def load_system_parameters():
    try:
        # Busca o arquivo de configuração que você já criou
        with open("core/config.yaml", "r") as file:
            config = yaml.safe_load(file)
            print(f"--- SISTEMA INICIALIZADO ---")
            print(f"Protocolo: {config['system']['name']}")
            print(f"Frequência Alvo: {config['physics']['target_frequency']}Hz")
            return config
    except FileNotFoundError:
        print("ERRO: Configuração Soberana não encontrada.")
        return None

if __name__ == "__main__":
    load_system_parameters()
