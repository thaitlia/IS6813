# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 13:12:57 2025

@author: sabri
"""

#%%
#libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, timedelta

#%%

#%%

#import modeling csv from R into Python

inner_joined_df = pd.read_csv('inner_joined_df.csv')


#%%

#%%

import scikit_learn as sk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier #Or RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report #For evaluation


#%%