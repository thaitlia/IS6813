# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 20:53:33 2025

@author: sabri
"""

#%%

sampled_orders = sampled_orders.drop('MATERIAL_ID', axis=1)
operating_hours = operating_hours.drop('FREQUENCY', axis=1)
cutoff_times = cutoff_times.drop('SALES_OFFICE', axis=1)
cutoff_times = cutoff_times.drop('DISTRIBUTION_MODE', axis=1)

#%%

#%%

customer.rename(columns={'CUSTOMER_NUMBER':'CUSTOMER_ID'}, inplace=True)

 # Inner merge (default): keeps only rows where 'customer_id' exists in both DataFrames
merged_df_inner = pd.merge(sampled_orders, sampled_google_analytics, on='CUSTOMER_ID', how='inner')
merged_df_inner = pd.merge(merged_df_inner, sampled_sales, on='CUSTOMER_ID', how='inner')
merged_df_inner = pd.merge(merged_df_inner, sampled_visit_plan, on='CUSTOMER_ID', how='inner')
merged_df_inner = pd.merge(merged_df_inner, customer, on='CUSTOMER_ID', how='inner')

#%%

#%%

operating_hours.rename(columns={'CUSTOMER_NUMBER':'CUSTOMER_ID'}, inplace=True)

sample_3000_combined = pd.merge(merged_df_inner, cutoff_times, on='PLANT_ID', how='inner')
sample_3000_combined = pd.merge(sample_3000_combined, material, on='MATERIAL_ID', how='inner')
sample_3000_combined = pd.merge(sample_3000_combined, operating_hours, on='CUSTOMER_ID', how='inner')

#%%

#%%

# Export the DataFrame to a CSV file
sample_3000_combined.to_csv('sample_3000_combined.csv', index=False) 

#%%


#%%

nan_counts = merged_df_inner.isna().sum()
print(nan_counts)


#%%

#%%

# Drop 'Column2'
merged_df_inner = merged_df_inner.drop('EVENT_PAGE_NAME', axis=1)

sample_3000_combined = sample_3000_combined.drop('EVENT_PAGE_NAME', axis=1)

#%%

#%%

# Sort the DataFrame by the 'Age' column in ascending order
sorted_df = merged_df_inner.sort_values(by='CUSTOMER_ID', ascending=True)


#%%

#%%

# Get unique values from the 'Name' column
unique_names = sorted_df['EVENT_NAME'].unique()

# Print the unique values
print("Unique values in the 'Name' column:")
print(unique_names)

#%%




#%%