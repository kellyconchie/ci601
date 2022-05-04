# Pandas to manipulate the CSV files and data frames
import pandas as pd

# datetime to manipulate dates
from datetime import date, timedelta

from Download import DL
from Train import train


# Create file to store results
# Create file with column names
column_names = ['endtrain', 'av1', 'av2', 'per', 'traingain', 'trainratio', 'testgain', 'testratio']
df = pd.DataFrame(columns=column_names)
df.to_csv('csv/results.csv', index=False)


endtest = date(2022, 4, 30)
DL(endtest - timedelta(days=365), endtest)


mrec = 0

while mrec <= 180:
    train(mrec)
    print(mrec)
    mrec = mrec + 10
