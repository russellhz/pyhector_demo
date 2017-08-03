import pyhector
from pyhector import rcp26, rcp45, rcp60, rcp85

# Input emissions
#print rcp26.head(5)

# Run rcp26 scenario and view default output
output = pyhector.run(rcp26)
#print output.head(5)

# Print out other outputs
output = pyhector.run(rcp26, outputs=['temperature.Tgav', 'simpleNbox.Ca', 'forcing.Ftot',
                                      'forcing.FCO2', 'ocean.Temp_HL'])
#print output.head(5)

# Calculate mean forcing 1850-1950
#print output['forcing.Ftot'].loc[1850:1950].mean()

# import matplotlib.pyplot as plt
#
# for rcp in [rcp26, rcp45, rcp60, rcp85]:
#     output = pyhector.run(rcp, {"core": {"endDate": 2100}})
#     temp = output["temperature.Tgav"]
#     # Adjust to 1850 - 1900 reference period
#     temp = temp.loc[1850:] - temp.loc[1850:1900].mean()
#     temp.plot(label=rcp.name.split("_")[0])
# plt.title("Global mean temperature")
# plt.ylabel("Degrees C over pre-industrial (1850-1900 mean)")
# plt.legend(loc="best")
# plt.show()

# Read in temp file to match
import pandas as pd
co2_file_to_match = "annual_avg_co2_GFDL-ESM2M_rcp45_r1i1p1.csv"
esm_co2_data = pd.read_csv(co2_file_to_match).rename(columns={"value.1...":"co2_value"}).set_index('year')
esm_co2 = esm_co2_data.co2_value * 1000000

#print esm_co2_data.head(5)
#print esm_co2.head(5)
from numpy import mean
from dplython import (DplyFrame, X, mutate)

CONCENTRATION_CO2 = "simpleNbox.Ca"
hector_co2 = pyhector.run(pyhector.rcp45)[CONCENTRATION_CO2].loc[esm_co2.index]
comp = DplyFrame({"hector": hector_co2, "esm": esm_co2})

def difference_quantifier(esm_series, hector_run_series):
    calculate_df = DplyFrame({"hector": hector_run_series, "esm": esm_series})
    calculate_df = calculate_df >> mutate(percentdiff=(X.hector - X.esm) / X.esm)
    return mean(abs(calculate_df.percentdiff))

#print difference_quantifier(esm_co2,hector_co2)

def hector_runner(params, comp_data, var):
    hector_output = pyhector.run(pyhector.rcp45, {"temperature": {"S": params[0]},
                                                 "simpleNbox":{"beta":params[1]},
                                                "simpleNbox":{"q10_rh":params[2]}})
    hector_co2 = hector_output[var].loc[comp_data.index]
    return difference_quantifier(comp_data, hector_co2)

#print hector_runner([4,1,1], esm_co2, CONCENTRATION_CO2)

#import scipy.optimize
#optim = scipy.optimize.fmin_powell(hector_runner, x0 = [5,2,2], args = (esm_co2,CONCENTRATION_CO2))
#print optim
#http://127.0.0.1:8888/notebooks/demo.ipynb

