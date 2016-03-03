import sys
import os

baseline_path = os.path.join(os.getcwd()[:-1], 'en600.468')

f = open('README.md', 'r')
print f.readline()
