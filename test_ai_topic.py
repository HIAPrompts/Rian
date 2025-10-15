from src.agent.core.humanized_writer import HumanizedWriter
from src.agent.core.automated_reviewer import AutomatedReviewer
from src.agent.core.director import Director

# Inicializar componentes
writer = HumanizedWriter()
reviewer = AutomatedReviewer()
director = Director(writer, reviewer)

# Gerar texto humanizado
topic = "Inteligência Artificial"
humanized_text = director.coordinate_process(topic)

print("=" * 80)
print("TEXTO HUMANIZADO GERADO:")
print("=" * 80)
print(humanized_text)
print("=" * 80)
