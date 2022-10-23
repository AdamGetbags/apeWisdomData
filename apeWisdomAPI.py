# -*- coding: utf-8 -*-
"""
Sentiment/frequency data from 
Ape Wisdom API - https://apewisdom.io/api/
@author: adam getbags

"""

# import modules
import pandas as pd
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

# get filter from supported filter list
filterName =  'all-crypto' 
pageNbr = 1

# build url
url = f'https://apewisdom.io/api/v1.0/filter/{filterName}/page/{pageNbr}'

# make get request
res = requests.get(url)
# convert to dataframe
df = pd.read_json(res.text)

# assign number of pages
numPages = df.pages[0]

# if there is more than one page
if numPages > 1:

# loop through pages 2 through numPages    
    for i in range(2, numPages+1):
        time.sleep(.1)
# build url
        url = f'https://apewisdom.io/api/v1.0/filter/{filterName}/page/{i}'
# make get request
        res = requests.get(url)
# convert to dataframe
        temp = pd.read_json(res.text)
# concatenate dataframe 
        df = pd.concat([df, temp], ignore_index=True)

else: 
    pass

# dictionaries to dataframe
tickerData = df.results.apply(pd.Series)

tickerData = tickerData.apply(pd.to_numeric, errors='ignore')

# display results
print(tickerData)

fig = px.treemap(tickerData, 
                 path=[px.Constant("all"), 'ticker'],
                 values='mentions',
                 color='mentions',
                 color_continuous_scale='Blues',
                 color_continuous_midpoint=max(tickerData['mentions'])/2)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    
#open figure in browser
plot(fig, auto_open=True)
