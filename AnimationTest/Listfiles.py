import os
files = os.listdir('.')
files.sort()
for filename in files:
    tag = filename.split("_")[0]
    if tag == 'box':
        print(filename)