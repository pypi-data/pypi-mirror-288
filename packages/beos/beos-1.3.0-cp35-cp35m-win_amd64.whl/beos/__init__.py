# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                 BEOS                           #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Top-level compatibility interface for BEOS as a standalone python package.
 
@note: BEOS
Created on 04.08.2024

@version: 1.0
----------------------------------------------------------------------------------------------
@requires:
       - 

@change: 
       -    
                           
@author: garb_ma                                                     [DLR-SY,STM Braunschweig]
----------------------------------------------------------------------------------------------
"""

## @package BEOS
# Top-level compatibility interface for BEOS as a standalone python package.
## @authors 
# Marc Garbade
## @date
# 04.08.2024
## @par Notes/Changes
# - Added documentation // mg 04.08.2024

import os, sys

# Add local path to global search path
sys.path.insert(0,os.path.dirname(__file__))

from _beos import *

if __name__ == '__main__':
    sys.exit()
    pass
