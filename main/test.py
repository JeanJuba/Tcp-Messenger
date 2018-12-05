import datetime
import sys,os
sys.path.append(os.getcwd())

print(os.getcwd())
print(datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S'))