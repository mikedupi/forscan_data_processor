
# Includes
# Imports (May contain some unnecessary ones) 
# __requires__ = ["sqlalchemy==1.4.46"]
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

import pkg_resources
# pkg_resources.require("sqlalchemy==1.4.46")
# import sqlalchemy

from sqlalchemy import create_engine
from datetime import timedelta, date, datetime, time
import time
from pytz import timezone
import matplotlib.dates as mdates
import matplotlib.transforms as mtransforms
from matplotlib.pyplot import yticks
from matplotlib.patches import Rectangle
import json

# !pip install --upgrade pandas
# !pip install sqlalchemy==1.4.46
# !pip install matplotlib


# Interactive graphing
# !pip install plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot, iplot

from prettytable import PrettyTable
import os
from itertools import (takewhile,repeat)

# Function needed for line counting
def rawincount(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )

# Config:
# Setup

print('This file needs to be configured, choose between using local files or files stored on Google Drive')
option = input("Please input 'local' or 'Google':\n")

if(option == 'local'):
    filename = input("Please insert filename:\n")
    
elif(option == 'Google'):
    link = input("Please insert the Google Drive Sharing Link:\n")
    # Assumes link is in the format 'https://drive.google.com/file/d/some_id/view?usp=share_link
    fluff , id_fluff = link.split('/d/')
    id , fluff = id_fluff.split('/')

    # Create local file 
    filename = 'Filename.csv'
    downloaded = drive.CreateFile({'id':id}) 
    downloaded.GetContentFile(filename)

else:
    print("Invalid option, exitting...")
    exit()

print()
file_stats = os.stat(filename)
file_size = round(file_stats.st_size / (1024 * 1024) , 2)
line_count = rawincount(filename)

print("Your file is {} MB and has {} lines in it\n".format(file_size, line_count))
print("If your CSV Files are larger than 5MB then I recommend that you split the CSV up into sections to speed up data navigation")
large_file = input("How many lines would you like in each section? (press enter to skip this):\n")

if(large_file == ""):
    dataframe = pd.read_csv(filename , low_memory=False)

else:
    dataframe_list = []
    for chunk in pd.read_csv(filename , low_memory=False, chunksize = int(large_file)):
        dataframe_list.append(chunk)

    chunk_index = input("You have {} chunks, which chunk would you like to inspect? (from 1 - {})\n".format(len(dataframe_list) , len(dataframe_list)))
    dataframe = dataframe_list[int(chunk_index) - 1]
    
# Dataset is now stored in a Pandas Dataframe

# Might make better UI in future, Tool selection:
bool_display_graphs = False
bool_build_turbo_lut = True

# Globals
key_name_dict = {
  'time(ms)' : 'time_ms' ,
  'BAP(V)' : 'Boost_Absolute_pressure__Raw_Sensor_voltage' ,
  'BARO(kPa)' : 'Barometric_Pressure_kPa' ,
  'ACT(°C)' : 'Air_Charge_Temperature_C' ,
  'APP1 [APP_D](%)' : 'Accelerator_pedal_D_percent' ,
  'APP2 [APP_E](%)' : 'Accelerator_pedal_E_percent' ,
  'APP_D(%)' : 'Accelerator_pedal_position_D_percent' ,
  'APP_E(%)' : 'Accelerator_pedal_position_E_percent' ,
  'BOOST_PRES(%)' : 'BOOST_PRES_actuator_percent' ,
  'BPA_OUT(%)' : 'BOOST_PRES_actuator_OUT_percent' ,
  'BPA_POS(%)' : 'BOOST_PRES_actuator_POS_measured_percent' ,
  'CACRP(kPa)' : 'Corrected_Air_Conditioning_Refrigerant_Pressure_kPa' ,
  'CBACB1(%)' : 'Comanded_Boost_Actuator_Control_Bank_1_percent' ,
  'CET(Nm)' : 'Calculated_Engine_Torque_Nm' ,
  'DMP(kPa)' : 'Demanded_Manifold_Pressure_kPa' ,
  'DP_DPF(kPa)' : 'Exhaust_Gas_Differential_Pressure_kPa' ,
  'EGT13(°C)' : 'Exhaust_Gas_Temp_C' ,
  'EOT(°C)' : 'Engine_Oil_Temperature_C' ,
  'FRP(kPa)' : 'Fuel_Rail_Pressure_kPa' ,
  'FRPD(kPa)' : 'Fuel_Rail_Pressure_Desired_kPa' ,
  'IAT(°C)' : 'Intake_Air_Temp_C' ,
  'LOAD(%)' : 'LOAD_percent' ,
  'LOW_OIL' : 'LOW_OIL' ,
  'LP_FUEL_SW' : 'Low_Pressure_FUEL_System_Switch' ,
  'MAF(g/s)' : 'Mass_Air_Flow_g_per_s' ,
  'MAP(kPa)' : 'Manifold_Absolute_Pressure_kPa' ,
  'RPM(1/min)' : 'RPM__per_min' ,
  'SELTESTDTC( )' : 'Diagnostic_Trouble_Codes' ,
  'TAC_PCT(%)' : 'Demanded_Throttle_actuator_Control_percent' ,
  'TURBO_BYP_MES(%)' : 'TURBO_Bypass_Valve_position_Measured_percent' ,
  'VNTP(%)' : 'Variable_Nozzle_Turbo_Position_percent' ,
  'WG_POS(V)' : 'Waste_Gate_Position_sensor_V' ,
}

# Data Cleaning
dataframe.rename(columns = key_name_dict, inplace = True)

# Program Operations:
if(bool_build_turbo_lut == True):
    # Make new DF, only holds columns needed for turbo config Look Up Table (LUT)

    columns_of_interest = ['time_ms','Calculated_Engine_Torque_Nm','Demanded_Manifold_Pressure_kPa','Manifold_Absolute_Pressure_kPa','RPM__per_min']
    turbo_dataframe = dataframe[columns_of_interest].copy()

    # Remove starting not-populated values
    # In my case, RPM is logged last and therefore just removing those ones makes my entire DF clean
    turbo_dataframe = (turbo_dataframe[turbo_dataframe.RPM__per_min != '-'])

    # Ensure types are correct as we need to do math
    turbo_dataframe = turbo_dataframe.astype({"time_ms":"int","Calculated_Engine_Torque_Nm":"float" , "Demanded_Manifold_Pressure_kPa":"float" , "Manifold_Absolute_Pressure_kPa":"float" , "RPM__per_min":"int"})

    # Add a column which represents the difference between Demanded_Manifold_Pressure_kPa & Manifold_Absolute_Pressure_kPa (this is for interest sake, if needed)
    turbo_dataframe['Manifold_Absolute_Pressure_Differential_kPa'] = turbo_dataframe['Demanded_Manifold_Pressure_kPa'] - turbo_dataframe['Manifold_Absolute_Pressure_kPa']

    # Now build your LUT
    # Group the data by RPM, into 500 rmp increments, first one doesn't make sense from 500rpm since idle is at 800rpm
    turbo_df_rpm_list = []

    df_1000_rpm = turbo_dataframe.loc[(turbo_dataframe['RPM__per_min'] < 1000) & (turbo_dataframe['RPM__per_min'] >= 796)]
    turbo_df_rpm_list.append([df_1000_rpm])

    for index in range(1000,4000,500):
        new_rpm_df = turbo_dataframe.loc[(turbo_dataframe['RPM__per_min'] < (index + 500)) & (turbo_dataframe['RPM__per_min'] >= index)]
        turbo_df_rpm_list.append([new_rpm_df])

    # Now split by engine torque ranges (100Nm increments)
    for rpm_split in range(0, len(turbo_df_rpm_list)):
        for torque in range(100,600,100):
            new_rpm_df = turbo_df_rpm_list[rpm_split][0].loc[(turbo_df_rpm_list[rpm_split][0]['Calculated_Engine_Torque_Nm'] < (torque)) & (turbo_df_rpm_list[rpm_split][0]['Calculated_Engine_Torque_Nm'] >= (torque - 100))]
            turbo_df_rpm_list[rpm_split].append(new_rpm_df)

    row_list = ["Measured RPM & Engine Torque"]
    for torque_index in range(1, len(turbo_df_rpm_list[0])):
        row_list.append("{}Nm - {}Nm".format((torque_index-1)* 100 , (torque_index)* 100))

    # First row in table represents columns, this is done using the PrettyTable constructor function
    tab = PrettyTable(row_list)

    # Now add each row to the table
    for rpm_index in range(0, len(turbo_df_rpm_list)):
        row_list = ["{} - {} rpm".format((rpm_index+1)* 500 , (rpm_index+2)* 500)]

        for torque_index in range(1, len(turbo_df_rpm_list[rpm_index])):
            df_in_question = turbo_df_rpm_list[rpm_index][torque_index]

            calc_dmp = df_in_question.loc[:, 'Demanded_Manifold_Pressure_kPa'].describe()["max"]
            calc_map = df_in_question.loc[:, 'Manifold_Absolute_Pressure_kPa'].describe()["max"]

            row_list.append("{} / {} ".format(calc_dmp , calc_map))
        
        tab.add_row(row_list)
    
    # Print your table
    print("Maximum Turbo Boost from log data, in the format DMP/MAP")
    print(tab)

if(bool_display_graphs == True):
    print("Available metrics:")
    print(dataframe.columns)
    print()
    # Make graph
    # Interactive Graph setup
    trace = []
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Graph RPM
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.RPM__per_min,
        name = "RPM__per_min",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ) , secondary_y=True
    )
    # Graph Engine Load
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.LOAD_percent,
        name = "LOAD_percent",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ) , secondary_y=False
    )

    # Graph Measured Manifold Pressure (Turbo Boost)
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.Manifold_Absolute_Pressure_kPa,
        name = "Manifold_Absolute_Pressure_kPa",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ), secondary_y=False
    )

    # Graph Desired Manifold Pressure (Turbo Boost)
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.Demanded_Manifold_Pressure_kPa,
        name = "Demanded_Manifold_Pressure_kPa",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ) , secondary_y=False
    )

    # Graph Turbo Boost Pressure Percentage
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.BOOST_PRES_actuator_percent,
        name = "BOOST_PRES_actuator_percent",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ) , secondary_y=False
    )

    # Graph Turbo Boost Pressure Percentage
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.BOOST_PRES_actuator_OUT_percent,
        name = "BOOST_PRES_actuator_OUT_percent",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ) , secondary_y=False
    )

    # Graph Turbo Boost Pressure Percentage
    fig.add_trace( 
        go.Scatter(
        x = dataframe.time_ms ,   
        y = dataframe.BOOST_PRES_actuator_POS_measured_percent,
        name = "BOOST_PRES_actuator_POS_measured_percent",
        hoverinfo = 'y+name',
        mode = "lines+markers",
        marker = dict( size = 2 ),
        line = dict( width = 0.4 ),
        
    ) , secondary_y=False
    )

    # make look pretty
    fig['layout'].update(height = 800, width = 1500, title = "OBD Data Graph" ,showlegend=True )
    fig.update_yaxes(title_text="<b>Other</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>RPM</b>", secondary_y=True)
    fig.update_layout(autotypenumbers='convert types')



    # show us what you got
    fig.show()
