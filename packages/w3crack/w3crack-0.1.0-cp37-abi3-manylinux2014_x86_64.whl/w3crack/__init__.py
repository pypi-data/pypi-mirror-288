import os
import sys

cur_file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_file_dir)
prev_dir = os.getcwd()
os.chdir(cur_file_dir)

from wcrack import *

os.chdir(prev_dir)