import hashlib
import json
import sys
from pathlib import Path

# Protocolo MARTINS-432-FLOW-2025
# Script de Verificação de Integridade de Nível 1

def sha256(file_path):
    h = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    except FileNotFoundError:
        return None

def main():
    # Carrega o manifesto oficial (a fonte da verdade)
    manifest_path = Path("integrity/manifest.json")
    if not manifest_path.exists():
        print("❌ ERRO: manifest.json não encontrado na pasta /integrity.")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    errors = []

    # Verifica cada documento crítico do protocolo
    for file_name, expected_hash in manifest["documents"].items():
        current_hash = sha256(file_name)
        
        if current_hash is None:
            errors.append(f"[AUSENTE] O arquivo {file_name} foi removido.")
        elif current_hash != expected_hash:
            errors.append(f"[VIOLADO] O arquivo {file_name} foi alterado ilegalmente.")

    if errors:
        print("❌ FALHA DE INTEGRIDADE DETECTADA:")
        for e in errors:
            print(" -", e)
        print("\nO uso comercial deste fork não está autorizado pelo protocolo SSA.")
        sys.exit(1)
    else:
        print("✅ INTEGRIDADE CONFIRMADA: Protocolo Oficial MARTINS-432-FLOW.")
        print("Release assinado por: Leandro Martins (SSA)")

if __name__ == "__main__":
    main()
