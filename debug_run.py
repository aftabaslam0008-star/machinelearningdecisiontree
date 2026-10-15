import traceback
import sys

print("Python version:", sys.version)

try:
    print("Reading task1_titanic.py...")
    with open('task1_titanic.py') as f:
        code = f.read()
    print("Executing code...")
    exec(code, {'__name__': '__main__', '__file__': 'task1_titanic.py'})
    print("Executed successfully!")
except BaseException:
    traceback.print_exc()
