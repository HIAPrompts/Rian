import json
import os

class ClientStyleMemory:
    def __init__(self, base_path="config/style_fewshots"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save_few_shots(self, client_id: str, few_shots: dict) -> None:
        """Salva few-shots de estilo para um cliente."""
        with open(f"{self.base_path}/{client_id}.json", "w") as f:
            json.dump(few_shots, f, indent=2)

    def load_few_shots(self, client_id: str) -> dict:
        """Carrega few-shots de estilo de um cliente."""
        with open(f"{self.base_path}/{client_id}.json", "r") as f:
            return json.load(f)
