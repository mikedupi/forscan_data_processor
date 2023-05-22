# forscan_data_processor
A collection of tools that process OBD II / OBD 2 logs from FORScan. The intention behind this tool was initially to display data, then I needed to generate a lookup table for Turbo Programming and so I added in functionality for calculating the look up table.

This Data Processor can be used to visualise any data from a CSV File, it specifically caters to data from the Power Control Module (PCM) and I have included column name substitutions for the columns I used (more can definitely be added).

Since I was interested in comparing actual turbo behaviour to the programmed turbo behaviour - I built a table which mimics that during ECU Programming in a Ford Ranger with a hybrid turbo.

The graphing tool I chose was Plotly since it supports zooming and hover values, enabling a layman easier inspection of the data using just the mouse.

Below is an example of the Turbo Table: (DMP = Demanded Manifold Pressure , MAP = Manifold Absolute Pressure)

```
# Maximum Turbo Boost from log data, in the format DMP/MAP
# +------------------------------+----------------+----------------+----------------+----------------+----------------+
# | Measured RPM & Engine Torque |  0Nm - 100Nm   | 100Nm - 200Nm  | 200Nm - 300Nm  | 300Nm - 400Nm  | 400Nm - 500Nm  |
# +------------------------------+----------------+----------------+----------------+----------------+----------------+
# |        500 - 1000 rpm        | 107.3 / 107.8  | 109.0 / 109.8  |   nan / nan    |   nan / nan    |   nan / nan    |
# |       1000 - 1500 rpm        | 139.3 / 137.0  | 133.0 / 132.8  | 143.5 / 145.0  |   nan / nan    |   nan / nan    |
# |       1500 - 2000 rpm        | 179.8 / 178.0  | 225.3 / 204.5  | 238.0 / 234.8  | 254.3 / 252.8  | 254.3 / 257.8  |
# |       2000 - 2500 rpm        | 228.3 / 214.8  | 233.8 / 243.5  | 251.5 / 264.5  | 269.0 / 266.0  | 278.8 / 272.5  |
# |       2500 - 3000 rpm        | 232.8 / 224.5  | 249.0 / 245.5  | 251.5 / 259.5  | 263.5 / 264.5  | 275.0 / 271.8  |
# |       3000 - 3500 rpm        | 230.3 / 195.8  | 236.0 / 223.3  | 241.8 / 246.8  | 247.3 / 251.8  | 256.8 / 255.5  |
# |       3500 - 4000 rpm        | 180.5 / 184.3  | 193.5 / 204.3  | 208.8 / 227.8  | 221.8 / 232.0  | 248.8 / 244.8  |
# +------------------------------+----------------+----------------+----------------+----------------+----------------+
```
