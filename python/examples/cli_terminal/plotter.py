import tradingeconomics as te
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# read api key
load_dotenv()
# NOTE: the dotenv library only support files named .env and not env, so i added .env to gitignore
# you will need to add your own .env file and paste your key in there
# example: key="your_api_key"
key = os.getenv("key")

# check key provided, if not exists then use guest key
if key == None:
    key = "guest:guest"

te.login(key)

country = input("\nEnter country to analyze: ").lower().title() # capitalize country
indi = input("\nEnter indicator to analyze: ").lower()

# get forecasts
forecasts = te.getForecastData(indicator=indi, output_type='df') # i choose df as output bc its easiest to work with

# search for matching country
row = forecasts.loc[forecasts['Country'] == country]

# null checking
if row.empty: 
    print("No countries found matching \"", country, "\"")
    exit()

points = row.loc[:, "YearEnd":"YearEnd3"].values
current = row["LatestValue"].values
currDate = row["LatestValueDate"].values[0][:4] # get first 4 digits of the date line to get the year

currDate = int(currDate)

xvalues = [currDate, currDate + 1, currDate + 2, currDate + 3]
yvalues = np.append(current, points[0])

plt.plot(xvalues, yvalues)

plt.xlabel("Year")
plt.ylabel(indi)
plt.title("Forecast of " + indi + " for " + country)

plt.show()
