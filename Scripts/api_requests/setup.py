import subprocess
import sys
print(subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]))

