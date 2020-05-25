#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install plotly_express


# In[4]:


# !pip install pandas_profiling


# In[5]:


# conda install -c conda-forge altair 


# In[6]:


import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt
from matplotlib import style
import seaborn as sns
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas_profiling
import altair as alt
from altair.expr import datum


# In[7]:


data = pd.read_csv("/Users/frj/Desktop/pythondata/Border_Crossing_Entry_Data.csv")
data.head(2)


# In[8]:


print(data.info()) # inspect data


# In[10]:


# The column 'date' is object. Now, let's change is to datetime format:
data['Date'] = pd.to_datetime(data['Date'])
data.head(2)


# In[11]:


# Now let's change columns name to lower case to make it easy: 
data.columns = data.columns.str.lower()


# In[12]:


# Rename 'port name' to make all letters attached
data.rename(columns={'port name': 'port_name'},inplace=True)


# In[13]:


# reset dataframe: add year & day of the week column, using python datetime function: 
data['year'] = data['date'].dt.strftime('%Y')
data['day_of_week'] = data['date'].dt.day_name()

data.head(3)


# In[14]:


# Which border is the busiest? 

# Create new dataframe and sort in descending order:
busy_border = data.groupby("border").value.sum().reset_index()
busy_border.sort_values(["value"], axis=0, 
                 ascending=[False], inplace=True)  
busy_border


# In[41]:


# pie chart visualization
border_value = busy_border['value']
border_name = busy_border['border']

explode = (0, 0.1)   #only explode the 2nd slice
colors = ['indianred','lightblue']

fig1, ax1 = plt.subplots(figsize=(12,7))

ax1.pie(border_value, autopct='%d%%', labels=border_name, explode=explode, colors=colors, shadow=True, startangle=90,
       textprops={'fontsize': 14})

plt.title('US inbound crossing percentage', size=16, fontweight="bold", color="steelblue")
ax1.axis('equal') 
plt.legend(border_name, loc= "upper left", fancybox=True, framealpha=1, shadow=True, fontsize=13)

plt.show()


# In[16]:


# The transportation way of inbound crossing for each US border
# visualization with Seaborn

border_tick=range(2)

fig2, ax2 = plt.subplots(figsize=(18,8))

ax2 = sns.barplot(x=data['border'], y=data['value'], hue=data['measure'], data=data, log=True)
ax2.set_xlabel('US borders', size=14, fontweight='bold')
ax2.set_ylabel('Inbound crossing value', size=14, fontweight='bold')
plt.legend(loc="upper left", frameon=False, ncol=3, fontsize=12)
plt.title("US inbound crossing analysis: Measure VS Border", size=17, color="indianred", fontweight='bold')

# bar chart styling
sns.despine(left=True)  # remove upper and left line

ax2.set_axisbelow(True)  
ax2.yaxis.grid(True, color='#EEEEEE')
ax2.xaxis.grid(False)

plt.show()


# In[42]:


# Treemap breakdown with Plotly express
fig = px.treemap(data, path=['border','state','measure'], values='value',
                  color='value', hover_data=['state'],
                  color_continuous_scale='RdBu')

fig.update_layout(title="US inbound crossing with Canada and Mexico: State level",
                  width=1000, height=700, uniformtext=dict(minsize=10, mode='hide'))  

fig.show()


# In[18]:


# Time series analysis

# rearrange new dataframe
time_line = data.groupby(['date', 'year', 'border', 'day_of_week']).value.sum().reset_index()
time_line.head(2)


# In[19]:


# time series: yearly

fig, ax = plt.subplots(figsize=(20,8))

ax = sns.lineplot(data=time_line, x='year',y='value', hue='border')
plt.title('US inbound Crossings 1996-2020', fontweight='bold', color='indianred', fontsize=18)

ax.set_xlabel('year from 1996 to 2020', size=14, fontweight='bold')
ax.set_ylabel('Inbound crossing value', size=14, fontweight='bold')
plt.legend(fontsize='14', frameon=False)

sns.despine(left=True)
ax.set_axisbelow(True)  #styling
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

plt.show()


# In[20]:


# time series detail

fig, ax = plt.subplots(figsize=(18, 8))

sns.pointplot(ax=ax, data=time_line, x="date", y="value", hue="border")
plt.title('US inbound crossing 1966-2020', fontsize=18, fontweight='bold', color='indianred')
ax.set_xlabel('year from 1966 to 2020', size=13)
ax.set_ylabel('value', size=13)
plt.legend(fancybox=True, shadow=True, fontsize=14)

# set xlabels as the datetime data for the given labelling frequency
ax.set_xticklabels(time_line.iloc[::12].date.dt.year.unique())

# set the xticks at the same frequency as the xlabels
xtix = ax.get_xticks()
ax.set_xticks(xtix[::12])

sns.despine(left=True)
ax.set_axisbelow(True)  # styling
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

plt.show()


# In[21]:


# state level yearly transportation evolution
tran = data.groupby(['measure', 'state','year']).value.sum().reset_index()
tran.head(10)


# In[43]:


# Plotly facet chart visualization
fig = px.scatter(tran, x="year", y="value", color="measure", facet_col="state",
       facet_col_wrap=5)

fig.update_layout(title="US inbound crossing measure from Canada and Mexico border 1996-2020", 
                  width=1000, height=700)

fig.update_xaxes(showgrid=False)

fig.show()


# In[23]:


# day of week analysis
# regroup related data

week_table = data.groupby(['border', 'day_of_week']).value.count().reset_index()
week_table.head(5)


# In[24]:


# Create pivot table

pivot_week = pd.pivot_table(data, 'value', ['border','state','year'], 'day_of_week')
pivot_week.head()

# Reorder column
pivot_week = pivot_week[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']]
pivot_week.head()


# In[25]:


# State level inbound crossing for each day of week
sns.set()
pd.pivot_table(data, 'value', ['state'], 'day_of_week').plot(kind= 'bar', width=0.9, alpha=0.9, figsize=(22, 10), title="US inbound crossing weekday level", fontsize=15)
plt.ylabel("crossing number", fontsize=18, color='indianred', fontweight='bold')
plt.xlabel("US states", fontsize=18, color='indianred', fontweight='bold')
plt.title('US inbound crossing weekday level', fontsize=25, color='indianred', fontweight='bold')
plt.legend(fancybox=True, shadow=True, fontsize=16)

# Monday has a noticeable high rate of border crossing while Friday is realtively flat. Hypothesis: People enters US for work, then go back for weekend.


# In[26]:


# legal VS illegal crossing analysis: border level

# create new column and fill its value with lambda function: 
data['law'] = data.measure.apply(lambda x: 'illegal' if x == 'Truck Containers Empty' or x == 'Truck Containers Full' or x =='Rail Containers Empty' or x == 'Rail Containers Full' else 'legal')
data.head()


# In[27]:


# extract categorical data: illegal crossing
illegal_data = data[data.law == 'illegal']
illegal_data2 = illegal_data.groupby(['year', 'border']).value.sum().reset_index()
illegal_data2.head()


# In[28]:


# stacked area visualization

alt.Chart(illegal_data2).mark_area(opacity=0.34).encode(
    x="year:T",
    y=alt.Y("value:Q", stack=None),
    color="border:N", tooltip=['value', 'year', 'border']).properties(title='US illegal inbound crossing', height=400, width=800)


# In[29]:


# legal VS illegal crossing analysis: state level

measure_ill = data[data.law == 'illegal']
measure_ill = measure_ill.groupby(['border', 'measure', 'state', 'year']).value.sum().reset_index()
measure_ill.head()


# In[30]:


# set pivot table: columns should be illega crossing measure
pivot_illegal = pd.pivot_table(measure_ill, 'value', ['state'], 'measure')
pivot_illegal.head(5)


# In[31]:


# plot pivot table outcome with Seaborn

sns.set()
pd.pivot_table(measure_ill, 'value', ['state'], 'measure').plot(kind= 'bar', width=0.88, figsize=(22, 10), title="US inbound crossing weekday level", fontsize=15)
plt.ylabel("crossing number", fontsize=18, color='indianred', fontweight='bold')
plt.xlabel("US states", fontsize=18, color='indianred', fontweight='bold')
plt.title('US inbound crossing illegal transportation', fontsize=25, color='indianred', fontweight='bold')
plt.legend(fancybox=True, shadow=True, fontsize=16)

# Truck is the most popular transportation.
# Most illegal crossing states: Michegan, Texas, New York 


# In[32]:


# Among legal crossings: private VS public
# Extract legal dataset
all_legal = data[data.law == 'legal']
all_legal.head()


# In[33]:


# Regroup and rename measure elements in dataset

all_legal.loc[(all_legal['measure'] == 'Bus Passengers') | (all_legal['measure'] == 'Train Passengers') | (all_legal['measure'] == 'Buses') | (all_legal['measure'] == 'Trains'), 'measure'] = 'public'
all_legal.loc[(all_legal['measure'] == 'Personal Vehicle Passengers') | (all_legal['measure'] == 'Personal Vehicles') | (all_legal['measure'] == 'Pedestrians') | (all_legal['measure'] == 'Trucks'), 'measure'] = 'private'
all_legal.head()


# In[34]:


# create finalsorted table: pu_pri
pu_pri = all_legal[['year', 'state', 'measure', 'value']]
pu_pri.head(5)


# In[35]:


# create pivot table show private & public
pivot_pupri = pd.pivot_table(pu_pri, 'value', ['state','year'], 'measure')
pivot_pupri.head(3)


# In[36]:


pivot_pupri = pivot_pupri.reset_index()
pivot_pupri.head()   # reconvert pivot table to dataframe


# In[37]:


# Calculate percentage of public 
pivot_pupri['per_public'] = pivot_pupri.apply(lambda row: row['public']/(row['private']+row['public']), axis=1)
pivot_pupri.head()


# In[38]:


# Now, visualize public measure percentage

fig = px.scatter(pivot_pupri, x="year", y="per_public", facet_col="state",
       facet_col_wrap=5)

fig.update_layout(title="public transportation percentage from 1966 to 2020", 
                  width=1000, height=700)

fig.layout.yaxis2.update(matches=None)  # matches=none, reset y value
fig.update_xaxes(showgrid=False)
fig.show()

# Wow! Alaska has an outstanding high level of public transportation VS private


# In[39]:


# Explore Alaska data

alaska = data.groupby(['year', 'measure', 'state']).value.sum().reset_index()
alaska.head()

alaska = alaska[alaska.state == 'AK'].reset_index()
alaska.head()

ooo = alaska[(alaska.year == '2017') | (alaska.year == '2018') | (alaska.year == '2019')]
nnn = ooo[(ooo.measure == 'Bus Passengers') | (ooo.measure == 'Train Passengers') | (ooo.measure == 'Buses') | (ooo.measure == 'Trains')]  
nnn.head(12)


# train & bus passengers are increasing largely from 2017 to 2019!


# In[40]:


# Create pivot table

AK = pd.pivot_table(nnn, 'value', ['year', 'state'], 'measure').reset_index()
AK.head()

# Many people enter Alaska by bus! 
# Why Alaska has a high public transportation rate? Because it's hard to drive on ice... 

