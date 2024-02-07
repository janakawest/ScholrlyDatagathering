"""
/*******************************************************
 * General Public License 2024 
 
 * Authors:
 *   - Janaka Wijekoon
 *   - Rashini Liyanarachchi

 * Feel free to make any modifications to the code. If you make any changes, kindly add your name to the authors list.
 *******************************************************/

"""
import subprocess
class Config:
  SEARCHKEY = '(Breast Cancer Treatment) AND (Radiology OR Radiotherapy) AND (Artificial Intelligence OR AI OR ML)'
  NUMRECORDS = 100
  
  # Install the modules which are missing
  def install_module(module_name):
    subprocess.check_call(["pip", "install", module_name])
