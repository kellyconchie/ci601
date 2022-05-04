# Pandas to manipulate the CSV files and data frames
import pandas as pd

# os to remove old files and clean directories
import os

# check that both the train and list list of exchange rates are the same

dftr = pd.read_csv('../csv/train/forex.csv')
dfts = pd.read_csv('../csv/test/forex.csv')

# make a temp file to compare files and delete unwanted files
column_names = ['ticker']
temp = pd.DataFrame(columns=column_names)
temp.to_csv('../csv/temp.csv', index=False)

# remove mismatched files from train directory
i = 0
ml = len(dftr)
while i < ml:
    mtic = dftr.loc[i, 'ticker']
    if (dfts['ticker'] == mtic).any():
        print('matched', mtic)
    else:
        row = [mtic]
        temp.loc[len(temp)] = row
        mtf = "../csv/train/XCH/"
        mtf2 = ".csv"
        mtf3 = mtf + mtic + mtf2
        if os.path.isfile(mtf3):
            os.remove(mtf3)
            print(mtic, "removed")
    i = i + 1

# remove file references from train forex file
i = 0
ml = len(temp)
while i < ml:
    mtic = temp.loc[i, 'ticker']
    dftr = dftr.drop(dftr[dftr['ticker'] == mtic].index)
    dftr.to_csv('../csv/train/forex.csv', index=False)
    i = i + 1

# make a temp file to compare files and delete unwanted files
column_names = ['ticker']
temp = pd.DataFrame(columns=column_names)
temp.to_csv('../csv/temp.csv', index=False)

# remove mismatched files from test directory
i = 0
ml = len(dfts)
while i < ml:
    mtic = dfts.loc[i, 'ticker']
    if (dftr['ticker'] == mtic).any():
        print('matched', mtic)
    else:
        row = [mtic]
        temp.loc[len(temp)] = row
        mtf = "../csv/test/XCH/"
        mtf2 = ".csv"
        mtf3 = mtf + mtic + mtf2
        if os.path.isfile(mtf3):
            os.remove(mtf3)
            print(mtic, "removed")
    i = i + 1

# remove file references from test forex file
i = 0
ml = len(temp)
while i < ml:
    mtic = temp.loc[i, 'ticker']
    dfts = dfts.drop(dfts[dfts['ticker'] == mtic].index)
    dfts.to_csv('../csv/test/forex.csv', index=False)
    i = i + 1

# Remove temp file
os.remove('../csv/temp.csv')
