
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


dataframe = pd.read_csv(filename , low_memory=False)
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
