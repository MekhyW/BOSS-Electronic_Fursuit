import os
Pitch = -200
Bass = 10
os.system("play '|rec -d pitch {} bass {}'".format(Pitch, Bass))