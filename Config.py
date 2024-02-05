"""
/*******************************************************
 * Copyright (c) 2024 
 
 * Authors:
 *   - Janaka Wijekoon
 *   - Rashini Liyanarachchi
 *******************************************************/

"""
import subprocess
class Config:
  SEARCHKEY = '(Breast Cancer Treatment) AND (Radiology OR Radiotherapy) AND (Artificial Intelligence OR AI OR ML)'
  NUMRECORDS = 100
  
  # Install the modules which are missing
  def install_module(module_name):
    subprocess.check_call(["pip", "install", module_name])
