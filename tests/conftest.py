import sys
from pathlib import Path

# Agregar el directorio raiz del proyecto al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
