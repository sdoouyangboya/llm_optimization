
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install gurobipy if not already installed
try:
    import gurobipy
except ImportError:
    install('gurobipy')
    import gurobipy
