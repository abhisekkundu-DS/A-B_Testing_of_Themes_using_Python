# -*- coding: utf-8 -*-
"""A/B Testing_on_them.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J0bZZzo82z4i8dg4iZBzsqp4WNXP8apT
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.stats.proportion import proportions_ztest

data = pd.read_csv('/content/website_ab_test.csv')

data.head()

print(data.isnull().sum())

data.info()

data.describe()

#Scatter plot for click through rate and conversion rate
fig = px.scatter(data,x = 'Click Through Rate',y='Conversion Rate',color='Theme',title='CTR vs Conversion Rate', trendline='ols')
fig.show()

#Extract data for eich them
light_theme_data = data[data['Theme'] == 'Light Theme']
dark_theme_data = data[data['Theme'] == 'Dark Theme']

#Create grouped bar chart Click Through Rate
fig = go.Figure()

fig.add_trace(go.Histogram(x = light_theme_data['Click Through Rate'],name = 'Light Theme'))
fig.add_trace(go.Histogram(x = dark_theme_data['Click Through Rate'],name = 'Dark Theme'))

fig.update_layout(title_text = 'Click Through Rate',barmode = 'group',xaxis_title_text = 'Click Through Rate',yaxis_title_text='Frequency',bargap=0.1)
fig.show()

fig = go.Figure()
fig.add_trace(go.Box(y = light_theme_data['Bounce Rate'],name = 'Light Theme'))
fig.add_trace(go.Box(y = dark_theme_data['Bounce Rate'],name = 'Dark Theme'))

fig.update_layout(
    title_text='Bounce Rate by Theme',
    yaxis_title_text='Bounce Rate',
)

fig.show()

# A/B testing for purchses
light_theme_conversions = light_theme_data[light_theme_data['Purchases'] == 'Yes'].shape[0]
light_theme_total = light_theme_data.shape[0]

dark_theme_conversions = dark_theme_data[dark_theme_data['Purchases'] == 'yes'].shape[0]
dark_theme_total = dark_theme_data.shape[0]

conversion_counts = [light_theme_conversions ,dark_theme_conversions]
sample_sizes = [light_theme_total,dark_theme_total]

light_theme_conversion_rate = light_theme_conversions / light_theme_total
dark_theme_conversion_rate = dark_theme_conversions / dark_theme_total

#perform two-saple proposition test
zstat , pvl = proportions_ztest(conversion_counts,sample_sizes)
print('Light Theme Conversion Rate :',light_theme_conversion_rate)
print('Dark Theme Conversion Rate :',dark_theme_conversion_rate)
print('P-value :',pvl)

import scipy.stats as stats
light_theme_session_duration = light_theme_data['Session_Duration']
dark_theme_seassion_duration = dark_theme_data['Session_Duration']

# Calculate the average session duration for both themes
light_theme_avg_duration = light_theme_session_duration.mean()
dark_theme_avg_duration = dark_theme_seassion_duration.mean()

# Print the average session duration for both themes
print("Light Theme Average Session Duration:", light_theme_avg_duration)
print("Dark Theme Average Session Duration:", dark_theme_avg_duration)

# Perform two-sample t-test for session duration
tstat, pval = stats.ttest_ind(light_theme_session_duration, dark_theme_seassion_duration)
print("A/B Testing for Session Duration - t-statistic:", tstat, " p-value:", pval)