## Module load ##

import sys
import os
sys.path.append(os.getcwd()+'/extract')
sys.path.append(os.getcwd()+'/transform')
sys.path.append(os.getcwd()+'/linkagepackages/graphical-record-linkage/python-encapsulation')
from extract import Extract
from transform import *
