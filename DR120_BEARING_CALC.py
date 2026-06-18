import pandas as pd
import numpy as np

# read excel file
df = pd.read_excel("D120 BEARING SELECTION.xlsx")

# sort collumns
selected = df[
    [
        "K",
        "Inner",
        "Outer",
        "Bore D in",
        "OD D in",
        "Width in",
        "C1 lbf"
    ]
].dropna()

# rear bearings
rear = selected.iloc[:12]

Rear_K = rear["K"].to_numpy()
Rear_Inner = rear["Inner"].to_numpy()
Rear_Outer = rear["Outer"].to_numpy()
Rear_Bore_D_in = rear["Bore D in"].to_numpy()
Rear_OD_D_in = rear["OD D in"].to_numpy()
Rear_Width_in = rear["Width in"].to_numpy()
Rear_C1_lbf = rear["C1 lbf"].to_numpy()

# front bearings
front = selected.iloc[-12:]

Front_K = front["K"].to_numpy()
Front_Inner = front["Inner"].to_numpy()
Front_Outer = front["Outer"].to_numpy()
Front_Bore_D_in = front["Bore D in"].to_numpy()
Front_OD_D_in = front["OD D in"].to_numpy()
Front_Width_in = front["Width in"].to_numpy()
Front_C1_lbf = front["C1 lbf"].to_numpy()

print(f"Rear bearings: {len(Rear_K)}")
print(f"Front bearings: {len(Front_K)}")

# variables

Fae = 7792 #lbf
FrA = 127137.06 #lbf
FrB = 133069.54 #lbf

Fae_dir = -1
m = -1

results = []

for i in range(len(Front_K)):
    for j in range(len(Rear_K)):

        K_front = Front_K[i]
        K_rear = Rear_K[j]

        TV1 = (0.47 * FrA) / K_front
        TV2 = (0.47 * FrB) / K_rear
        TV3 = m * Fae_dir * Fae

        LV1 = TV1
        LV2 = TV2 - TV3

        if LV1 < LV2:
            FaA = TV2 - TV3
            FaB = TV2
            Pa = 0.4 * FrA + K_front * FaA
            Pb = FrB
            condition = "Condition 1"
        else:
            FaA = TV1
            FaB = TV1 + TV3
            Pa = FrA
            Pb = 0.4 * FrB + K_rear * FaB
            condition = "Condition 2"

        FOS_Front = Front_C1_lbf[i] / Pa
        FOS_Rear = Rear_C1_lbf[j] / Pb

        results.append([
            i + 1,
            j + 1,
            f"{Front_Inner[i]} / {Front_Outer[i]}",
            f"{Rear_Inner[j]} / {Rear_Outer[j]}",
            FOS_Front,
            FOS_Rear
        ])

results_df = pd.DataFrame(results, columns=[
    "Front #",
    "Rear #",
    "Front Bearing",
    "Rear Bearing",
    "FOS Front",
    "FOS Rear"
])

results_df["FOS Front"] = results_df["FOS Front"].round(3)
results_df["FOS Rear"] = results_df["FOS Rear"].round(3)

print(results_df.to_string(index=False))

results_df.to_excel("Bearing_Results.xlsx", index=False)