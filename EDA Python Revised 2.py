# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 09:37:30 2025

@author: sabri
"""
#%%
#libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, timedelta, date, time
import random

#%%

#reading in the necessary csv files - this section has the massive files

google_analytics = pd.read_csv('google_analytics.csv')
orders = pd.read_csv('orders.csv')
sales = pd.read_csv('sales.csv')
visit_plan = pd.read_csv('visit_plan.csv')

#%%

#reading in the necessary csv files - this section has the smaller files files

customer = pd.read_csv('customer.csv')
cutoff_times = pd.read_csv('cutoff_times.csv')

material = pd.read_csv('material.csv') #not using material for my success metric
operating_hours = pd.read_csv('operating_hours.csv') #not using as it contains the most
#recent anchor date info and I need it for a whole year which is what the visit plan 
#table has it as

#%%

#calling out the specific customer ids to sample - randomly chosen

specific_customer_ids = customer['CUSTOMER_NUMBER'].to_list()
specific_customer_ids = random.sample(specific_customer_ids, 50)

#from the massive data tables - pulling the specific customer id information, all rows 

sampled_google_analytics = google_analytics[google_analytics['CUSTOMER_ID'].isin(specific_customer_ids)]
sampled_visit_plan = visit_plan[visit_plan['CUSTOMER_ID'].isin(specific_customer_ids)]
sampled_orders = orders[orders['CUSTOMER_ID'].isin(specific_customer_ids)]
sampled_sales = sales[sales['CUSTOMER_ID'].isin(specific_customer_ids)]

#%%

#sort the sampled data tables just to understand how the groupings work in each one
sorted_google_analytics = sampled_google_analytics.sort_values(by='CUSTOMER_ID')
sorted_orders = sampled_orders.sort_values(by='CUSTOMER_ID')
sorted_sales = sampled_sales.sort_values(by='CUSTOMER_ID')
sorted_visit_plan = sampled_visit_plan.sort_values(by='CUSTOMER_ID')

#%%

#this section is to convert local cutoff times to EST as per the ppt

#extract the last two characters and create a new column to show state
cutoff_times['STATE'] = cutoff_times['SALES_OFFICE'].str.slice(-2)

#convert 'time' column to datetime objects (handling only time part)
#cutoff_times['CUTOFFTIME__C'] = pd.to_datetime(cutoff_times['CUTOFFTIME__C'], format='%H:%M:%S').dt.time

#convert cutofftimes to EST as they are local to customer
cutoff_times['adjusted_time'] = cutoff_times['CUTOFFTIME__C']

#add two hours to 'adjusted_time' where 'STATE' is a state that lies in an MST zone
#convert time objects back to datetime for calculation, then extract time again
cutoff_times.loc[cutoff_times['STATE'] == 'CO', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'CO', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time
    
cutoff_times.loc[cutoff_times['STATE'] == 'UT', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'UT', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time
    
cutoff_times.loc[cutoff_times['STATE'] == 'ID', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'ID', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time

cutoff_times.loc[cutoff_times['STATE'] == 'NE', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'NE', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time

cutoff_times.loc[cutoff_times['STATE'] == 'WY', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'WY', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time
    
cutoff_times.loc[cutoff_times['STATE'] == 'AZ', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'AZ', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time    
    
cutoff_times.loc[cutoff_times['STATE'] == 'NM', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'NM', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=2)).dt.time    
    
#add three hours to 'adjusted_time' where 'STATE' is a state that lies in an PST zone
#convert time objects back to datetime for calculation, then extract time again
cutoff_times.loc[cutoff_times['STATE'] == 'NV', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'NV', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=3)).dt.time    
    
cutoff_times.loc[cutoff_times['STATE'] == 'OR', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'OR', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=3)).dt.time 
    
cutoff_times.loc[cutoff_times['STATE'] == 'WA', 'adjusted_time'] = \
    (pd.to_datetime(cutoff_times.loc[cutoff_times['STATE'] == 'WA', 'adjusted_time'].astype(str)) + 
     pd.Timedelta(hours=3)).dt.time 
    
#%%

#per the ppt, joining cutoff times to visit plan on SALES_OFFICE, SHIPPING_CONDITION_TIME
#and DISTRIBUTION_MODE

#creating dictionary so all data is encoded the same way across the tables
appendix_distribution_mode = {'OFS':'OF','Rapid Delivery':'RD','E Pallet':'EZ',
                              'Sideload':'SL','Night Sideload':'NS','Full Service':'FS',
                              'Night Rapid Delivery':'NR','Night OFS':'NO',
                              'Special Events':'SE','Bulk Distribution':'BK',
                              'Tell Sell':'TS','Nights Bulk':'NB'}

#need to update cutoff_times DISTRIBUTION_MODE to the abbreviations above to match visit_plan table
cutoff_times['DISTRIBUTION_MODE'] = cutoff_times['DISTRIBUTION_MODE'].replace(appendix_distribution_mode)

#need to update cutoff_times to numeric hours to match visit_plan table and update column name
cutoff_times['SHIPPING_CONDITION_TIME'] = cutoff_times['SHIPPING_CONDITION_TIME'].str[:2]
cutoff_times.rename(columns={'SHIPPING_CONDITION_TIME':'SHIPPING_CONDITIONS_DESC'}, inplace=True)

#need to update visit_plan to the abbreviations above
sampled_visit_plan['SHIPPING_CONDITIONS_DESC'] = sampled_visit_plan['SHIPPING_CONDITIONS_DESC'].str[:2]

#need to update cutoff_times column name to match visit_plan
cutoff_times.rename(columns={'SALES_OFFICE':'SALES_OFFICE_DESC'}, inplace=True)

#merge the cutoff_times and sampled_visit_plan tables together - inner join
merged = pd.merge(sampled_visit_plan, cutoff_times, on=['SALES_OFFICE_DESC',
                                                'SHIPPING_CONDITIONS_DESC',
                                                'DISTRIBUTION_MODE'], how='inner')

#%%

#sort the sampled data tables just to understand how the groupings work in each one
sorted_merged = merged.sort_values(by='CUSTOMER_ID')

#%%

#removing duplicate column information in customer table and merging with merged table
customer = customer.drop('SALES_OFFICE', axis=1)
customer = customer.drop('SALES_OFFICE_DESCRIPTION', axis=1)
customer = customer.drop('DISTRIBUTION_MODE_DESCRIPTION', axis=1)
customer = customer.drop('SHIPPING_CONDITIONS_DESCRIPTION', axis=1)

customer.rename(columns={'CUSTOMER_NUMBER':'CUSTOMER_ID'}, inplace=True)

merged = pd.merge(merged, customer, on=['CUSTOMER_ID'], how='inner')

#%%

#sort the sampled data tables just to understand how the groupings work in each one
sorted_merged = merged.sort_values(by='CUSTOMER_ID')

#%%

#NOT USING THIS SECTION FOR ANYTHING CURRENTLY - PULL SALES IN LATER?

#removing unwanted columns in sales table and merging with merged table - I don't want it for my
#purposes so omitting
sampled_sales = sampled_sales.drop('POSTING_DATE', axis=1)
sampled_sales = sampled_sales.drop('MATERIAL_ID', axis=1)
sampled_sales = sampled_sales.drop('GROSS_PROFIT_DEAD_NET', axis=1)

#%%

#combining google analytics table with orders assuming that CREATED_DATE_UTC in
#the orders table matches up with the google analytics table EVENT_TIMSTAMP

#removing unwanted columns in orders table and merging with google analytics

sampled_orders = sampled_orders.drop('CREATED_DATE_UTC', axis=1)
sampled_orders = sampled_orders.drop('PLANT_ID', axis=1)

#%%



#Calculating Order Window

#%%

#using the merged sampled_visit_plan and cutoff_times table from above

#Getting the most recent anchor date for each customer
sampled_visit_plan = merged

#convert 'ANCHOR_DATE' to datetime objects
sampled_visit_plan['ANCHOR_DATE'] = pd.to_datetime(sampled_visit_plan['ANCHOR_DATE'])

#find the most recent date for each customer
most_recent_dates = sampled_visit_plan.groupby('CUSTOMER_ID')['ANCHOR_DATE'].max()

#merge back to the original DataFrame (optional)
sampled_visit_plan = sampled_visit_plan.merge(most_recent_dates.rename('MostRecentOrderDate'), on='CUSTOMER_ID', how='left')

#%%

#need to change 'Every Week On' and 'Every Second Week On' and etc. to a numeric value
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Week On', 1)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Second Week On', 2)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Third Week On', 3)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Fourth Week On', 4)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Fifth Week On', 5)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Sixth Week On', 6)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Seventh Week On', 7)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Eighth Week On', 8)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Ninth Week On', 9)
sampled_visit_plan['FREQUENCY'] = sampled_visit_plan['FREQUENCY'].replace('Every Tenth Week On', 10)

#convert frequency column to numeric 
sampled_visit_plan['FREQUENCY'] = pd.to_numeric(sampled_visit_plan['FREQUENCY'])

#%%

#Calculating order window by finding a range of dates from ANCHOR_DATE and then the periodic 
#frequency
sampled_visit_plan['end_date'] = sampled_visit_plan['ANCHOR_DATE'] + pd.to_timedelta(sampled_visit_plan['FREQUENCY'], unit='W')

#%%

#continuation of above

#need a dummy date for the adjusted_time column in order to convert to datetime, then
#I will extract the time needed

my_date = date(2025, 10, 25)

#combine them to create a dummy datetime object
#combine the date and time, then convert to datetime objects
sampled_visit_plan['adjusted_time_dummy'] = pd.to_datetime(my_date.isoformat() + ' ' + sampled_visit_plan['adjusted_time'].astype(str))

sampled_visit_plan['adjusted_time_dummy'] = pd.to_datetime(sampled_visit_plan['adjusted_time_dummy'])

#extract date from 'datetime_col_with_date' and update the time with the time from
#the adjusted_time_dummy table

sampled_visit_plan['end_date_time'] = sampled_visit_plan.apply(lambda row: row['end_date'].replace(
    hour=row['adjusted_time_dummy'].hour,
    minute=row['adjusted_time_dummy'].minute,
    second=row['adjusted_time_dummy'].second,
    microsecond=row['adjusted_time_dummy'].microsecond
   ), axis=1)

#%%

#determining if customer made a purchase

#replace NaN values in 'EVENT_PAGE_NAME' with "Not Available"
sampled_google_analytics['EVENT_PAGE_NAME'] = sampled_google_analytics['EVENT_PAGE_NAME'].fillna('not available')

substring_to_find = 'Purchase Success'
sampled_google_analytics['made_a_purchase'] = np.where(sampled_google_analytics['EVENT_PAGE_NAME'].str.contains(substring_to_find, case=False), 1, 0)

#%%

#sort the sampled data tables just to understand how the groupings work in each one
sorted_google_analytics = sampled_google_analytics.sort_values(by=['CUSTOMER_ID', 'EVENT_DATE'])

#%%

#in the sampled google analytics table - several transaction in one day - give me unique for 
#CUSTOMER_ID, EVENT_DATE, and made_a_purchase - want both for information for modeling and 
#prediction

#also if order by date never had any transaction to begin with then customer never even
#attempted to use MyCoke360 to order or otherwise - so does not count as abandoned

sampled_google_analytics = sampled_google_analytics.drop_duplicates(subset=['CUSTOMER_ID', 'EVENT_DATE', 'made_a_purchase'])

#%%

#sort the sampled data tables just to understand how the groupings work in each one
sorted_google_analytics = sampled_google_analytics.sort_values(by=['CUSTOMER_ID', 'EVENT_DATE'])

#%%

def calculate_customer_dates(customer_data):
    
    all_customer_dates = []
    
    for index, row in customer_data.iterrows():
        customer_id = row['CUSTOMER_ID']
        start_date = pd.to_datetime(row['end_date_time'])
        weekly_frequency = row['FREQUENCY']
        
        #define the overall data range for filtering
        start_2024 = pd.to_datetime('2024-05-31')
        end_2025 = pd.to_datetime('2025-05-26')
        
        num_weeks_to_generate = int((end_2025 - start_date).days / 7) + 52
        
        if num_weeks_to_generate < 0:
            num_weeks_to_generate = 0
        
        dates_for_customer = pd.date_range(start=start_date, 
                                           periods=num_weeks_to_generate * weekly_frequency + 1, 
                                           freq=f'{7/weekly_frequency}D')
        
        filtered_dates = dates_for_customer[(dates_for_customer >= start_2024) & (dates_for_customer <= end_2025)]
        
        for date in filtered_dates:
            all_customer_dates.append({'CUSTOMER_ID': customer_id, 'date': date})
    
    return pd.DataFrame(all_customer_dates)


#taking one unique instance of each CUSTOMER_ID in the sample_visit_plan - function will auto
#cut it between the dates I want
unique_sampled_visit_plan = sampled_visit_plan.drop_duplicates(subset=['CUSTOMER_ID'])

customer_date_ranges = calculate_customer_dates(unique_sampled_visit_plan)

#%%

#appending orders to the table for more accounts of not abandoned carts - just used 
#different means of creating an order

#need to drop rows where MYCOKE360 was used as that is accounted for in the google_analytics table
column_to_search = 'ORDER_TYPE'
substring_to_detect = 'MYCOKE360'

#drop rows where the substring is found in the specified column
#the '~' inverts the boolean Series, keeping rows where the substring is NOT found
clean_sampled_orders = sampled_orders[~sampled_orders[column_to_search].str.contains(substring_to_detect, na=False)]

#CREATED_DATE_EST is the same as EVENT_DATE in the google_analytics table (imo)
clean_sampled_orders = clean_sampled_orders.rename(columns={'CREATED_DATE_EST': 'EVENT_DATE'})

#create a column as every order is made_a_purchase =1 
clean_sampled_orders['made_a_purchase'] = 1

#join the cleaned_sampled_orders table with the sorted_google_analytics table
#any missing info from either or will be a inserted as NA
join_sampled_ga_orders = pd.merge(sorted_google_analytics,
                                  clean_sampled_orders, 
                                  on=['CUSTOMER_ID', 'EVENT_DATE', 'made_a_purchase'], 
                                  how='outer')

#%%

df1 = join_sampled_ga_orders
df1 = df1.rename(columns={'EVENT_DATE':'event_date_df1'})

df2 = customer_date_ranges
df2 = df2.rename(columns={'date':'transaction_date_df2'})

df1['event_date_df1'] = pd.to_datetime(df1['event_date_df1'])
df2['transaction_date_df2'] = pd.to_datetime(df2['transaction_date_df2'])

df2_sorted = df2.sort_values(by='transaction_date_df2')
df1_sorted = df1.sort_values(by='event_date_df1')

merged_df = pd.merge_asof(
    df2_sorted,
    df1_sorted,
    left_on='transaction_date_df2',
    right_on='event_date_df1',
    by='CUSTOMER_ID',
    direction='nearest',
    tolerance=pd.Timedelta('7 days')
    )

sorted_merged_df = merged_df.sort_values(by=['CUSTOMER_ID','transaction_date_df2'])

#%%

cleaned_sorted_merged_df = sorted_merged_df.dropna(subset=['made_a_purchase'])

#calculate the proportions of each value in 'made_a_purchase'
proportions = sorted_merged_df['made_a_purchase'].value_counts(normalize=True)

#%%

#replace all NaN values with "Not Available"
cleaned_sorted_merged_df = cleaned_sorted_merged_df.fillna('not available given order type')

cleaned_sorted_merged_df.to_csv('IS 6813 Final Output for Modeling.csv', index=False)

#%%


































