import pandas as pd

import os

dataframes = []
folder_path = "data"

# make large dataframe to store all csv data
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder_path, file))
        dataframes.append(df)

final_df = pd.concat(dataframes, ignore_index=True)

#replace columns with better name
final_df.columns = final_df.columns.str.replace("obsw.cdh.telemetry.DataPool.platform.", "", regex=False)


#everything which is 1 either requires no multiplication or I need mor einfo before multiplying
# all battery currents and voltages need to be checked
EPSconstants = {"BAT1.batteryCurrent[0].value": 0.005237, "BAT1.batteryCurrent[1].value": 0.005327, "BAT1.batteryCurrent[2].value": 0.00207,
                "BAT1.batteryVoltage[0].value": 0.004311, "BAT1.batteryVoltage[1].value": 0.005685, "BAT1.batteryVoltage[2].value": 0.01349,
                "EPS.switchCurrents[0].value": 0.001328, "EPS.switchCurrents[1].value": 0.001328, "EPS.switchCurrents[2].value": 0.001328,
                "EPS.switchCurrents[3].value": 0.001328, "EPS.switchCurrents[4].value": 0.001328, "EPS.switchCurrents[5].value": 0.001328,
                "EPS.switchCurrents[6].value": 0.001328, "EPS.switchCurrents[7].value": 0.001328, "EPS.switchCurrents[8].value": 0.001328,
                "EPS.switchCurrents[9].value": 0.001328, "EPS.switchVoltages[0].value": 0.01349, "EPS.switchVoltages[1].value": 0.01349,
                "EPS.switchVoltages[2].value": 0.008993, "EPS.switchVoltages[3].value": 0.008993, "EPS.switchVoltages[4].value": 0.005865,
                "EPS.switchVoltages[5].value": 0.005865, "EPS.switchVoltages[6].value": 0.005865, "EPS.switchVoltages[7].value": 0.004311,
                "EPS.switchVoltages[8].value": 0.004311, "EPS.switchVoltages[9].value": 0.004311, "EPS.busCurrents[0].value": 0.005237,
                "EPS.busCurrents[1].value": 0.005237, "EPS.busCurrents[2].value": 0.005237, "EPS.busCurrents[3].value": 0.00207,
                "EPS.busVoltages[0].value": 0.008978, "EPS.busVoltages[1].value": 0.004311, "EPS.busVoltages[2].value": 0.005865,
                "EPS.busVoltages[3].value": 0.01349, "EPS.BcrOutputCurrent.value": 14.662757, "EPS.BcrOutputVoltage.value": 0.008993157}

#multiply only selected columsn by the EPS constants
EPScolumns = list(EPSconstants.keys())
final_df[EPScolumns] *= pd.Series(EPSconstants)

#split dataframe into charge and discharge dataframe using time (before 7:30 pm/19:30 is charge, after is discharge)
charge_df = final_df[final_df["Reception time"] < "19:30"]
discharge_df = final_df[final_df["Reception time"] >= "19:30"]

# Define output directory and file path
output_dir = "output"
output_file = os.path.join(output_dir, "charge.csv")
output_file2 = os.path.join(output_dir, "discharge.csv")

# Create directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save DataFrame as CSV
charge_df.to_csv(output_file, index=False)
discharge_df.to_csv(output_file2, index=False)

print(f"Charge DataFrame saved to {output_file}")
print(f"Discharge DataFrame saved to {output_file2}")