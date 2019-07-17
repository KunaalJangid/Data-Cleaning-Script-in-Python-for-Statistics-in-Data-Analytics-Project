import pandas as pd
import numpy as np
import matplotlib as plt

df1 = pd.read_csv("Country_Basic_Water_Data.csv")
df2 = pd.read_csv("Cholera_Percentage.csv")
df3 = pd.read_csv("Country_Sanitation_Data.csv")

#Cleaning df1 Data

country_col = df1.iloc[:,0]
country_col = pd.DataFrame(country_col)
country_col.columns = ['Country']
country_col = country_col.drop(country_col.index[[0,1]])
country_col.index = pd.RangeIndex(len(country_col.index))
country_col.index = range(len(country_col.index))

df1.rename(columns={'Unnamed: 0':'Country'}, inplace=True)
df1 = df1[['Country', '2015.2', '2014.2', '2013.2', '2011.2', '2010.2', '2009.2',
                                   '2008.2', '2007.2', '2006.2', '2005.2', '2004.2', '2003.2', 
                                   '2002.2', '2001.2', '2000.2']].copy()

numeric_columns = df1.drop(df1.columns[0],axis=1)
numeric_columns = numeric_columns.drop(numeric_columns.index[[0,1]])
numeric_columns.fillna(0, inplace = True)
numeric_columns = numeric_columns.astype(int)
basic_drinking_water_averages = numeric_columns.mean(axis=1)
basic_drinking_water_averages = pd.DataFrame(basic_drinking_water_averages)
basic_drinking_water_averages.columns = ['Basic_Drinking_Water_Averages']
basic_drinking_water_averages.index = pd.RangeIndex(len(basic_drinking_water_averages.index))
basic_drinking_water_averages.index = range(len(basic_drinking_water_averages.index))
dataframe1 = country_col.join(basic_drinking_water_averages)

#Cleaning df2 Data
df2 = df2[df2.Year > 2000]
country_list = df2['Country'].unique()
df2['Country'].value_counts()

df2.dtypes
list(df2)
#Renaming Columns
df2.columns = ['Country', 'Year', 'Cases']

#Removing blank spaces from Cases Column
df2.Cases = df2.Cases.str.replace(' ', '')

df2 = df2[df2.Cases != 'Unknown']

#Converting Cases column to Numeric
df2.Cases = df2.Cases.astype(float)


#Creating a new Column with Sum of Unique Cases
df2['TotalCases'] = df2.groupby('Country')['Cases'].transform('sum')

#Merging and Aggregating Rows
df2_new = df2['Year'].groupby([df2.Country, df2.TotalCases]).apply(list).reset_index()

#Remove Column from df2
df2_new= df2_new.drop("Year", axis=1)

#Cleaning df3 Data

df3.rename(columns={'Unnamed: 0':'Country'}, inplace=True)

df3 = df3[['Country', '2015.2', '2014.2', '2013.2', '2011.2', '2010.2', '2009.2',
                                   '2008.2', '2007.2', '2006.2', '2005.2', '2004.2', '2003.2', 
                                   '2002.2', '2001.2', '2000.2']].copy()
numeric_columns3 = df3.drop(df3.columns[0],axis=1)
numeric_columns3 = numeric_columns3.drop(numeric_columns3.index[[0,1]])
numeric_columns3.fillna(0, inplace = True)
numeric_columns3 = numeric_columns3.astype(int)
basic_sanitation_service_averages = numeric_columns3.mean(axis=1)
basic_sanitation_service_averages = pd.DataFrame(basic_sanitation_service_averages)
basic_sanitation_service_averages.columns = ['Basic_Sanitation_Averages']
basic_sanitation_service_averages.index = pd.RangeIndex(len(basic_sanitation_service_averages.index))
basic_sanitation_service_averages.index = range(len(basic_sanitation_service_averages.index))
dataframe3 = country_col.join(basic_sanitation_service_averages)
#Combining Datasets
dataset = pd.merge(dataframe1, dataframe3, on='Country')
dataset = pd.merge(dataset, df2_new, on='Country')

dataset.to_csv("Multiple_Regression.csv")
