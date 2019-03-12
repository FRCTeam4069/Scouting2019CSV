import base64
import pyperclip
import sys

file = open(sys.argv[1], "rb")
ret = base64.b64encode(file.read())
pyperclip.copy(str(ret)[2:-1])
print("Copied to clipboard!")
