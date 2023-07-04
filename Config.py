import subprocess
class Config:
  SEARCHKEY = "Blister Blight and  Tea leafe and  Machine Learning"
  NUMRECORDS = 5
  
  # Install the modules whic are missing
  def install_module(module_name):
    subprocess.check_call(["pip", "install", module_name])