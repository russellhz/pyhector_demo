import pyhector
from pyhector import rcp26, rcp45, rcp60, rcp85

# Input emissions
print rcp26.head(5)

# Run rcp26 scenario and view default output
output = pyhector.run(rcp26)
print output.head(5)

# Print out other outputs
output = pyhector.run(rcp26, outputs=['temperature.Tgav', 'simpleNbox.Ca', 'forcing.Ftot',
                                      'forcing.FCO2', 'ocean.Temp_HL'])
print output.head(5)

#http://127.0.0.1:8888/notebooks/demo.ipynb

