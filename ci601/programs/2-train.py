import pandas as pd

# os to remove old files and clean directories
import os

if os.path.isfile('../csv/trainresult.csv'):
    os.remove('../csv/trainresult.csv')
    print("trainresult.csv removed")

# Create file with column names to record data
column_names = ['ticker', 'gain', 'av1', 'av2', 'per', 'pos', 'neg']
trav = pd.DataFrame(columns=column_names)
trav.to_csv('../csv/trainresult.csv', index=False)

# Remove old file
if os.path.isfile('../csv/trainxch.csv'):
    os.remove('../csv/trainxch.csv')
    print("trainxch.csv removed")

# Create file with column names
column_names = ['gain', 'av1', 'av2', 'per', 'pos', 'neg']
stav = pd.DataFrame(columns=column_names)
stav.to_csv('../csv/trainxch.csv', index=False)

# Read all file names in forex file
# In each file in the train directory insert two new columns
dffor = pd.read_csv('../csv/train/forex.csv')
lfor = len(dffor)
ifor = 0
while ifor < lfor:
    mtic = dffor.loc[ifor, 'ticker']
    mtic = mtic + '.csv'
    tfor = pd.read_csv('../csv/train/XCH/' + mtic)
    if 'av1' in tfor.columns:
        print(' ')
    else:
        tfor.insert(4, 'av1', 0)
        tfor.insert(5, 'av2', 0)
    tfor.to_csv('../csv/train/XCH/' + mtic, index=False)
    ifor = ifor + 1

# Declare variables
# sav1 : start of the first moving average; eav1: end of the first moving average
# sav2: start of the second moving average; eav2: end of the second moving average
# sper: start of the percentage drop, eper: end of the percentage drop

sav1 = 2
eav1 = 5
sav2 = 3
eav2 = 10
sper = .1
eper = .5


# Receive variable from function buy :
# (ticker name,1st moving average, 2nd moving average, percentage drop, buying price, selling price)
# The variable mgain is calculating the percentage gain or loss from the buying price
# The following if statements are just checking if a record exists and if it does exist,
# the gain, number of positives and number of negatives will be updated each time
# 'positives' is keeping a record of the number of positive outcomes (a profit has been made)
# 'negatives' is keeping a record of the number of negative outcomes (a loss has occurred)
# If it does not exists, a new record is created


def sel(mtic, mav, mav2, mper, mbuy, msel):
    print(mtic, mbuy, msel)
    mgain = 100 / (mbuy / (msel - mbuy))

    dfav = pd.read_csv('../csv/trainresult.csv')

    if ((dfav['ticker'] == mtic) & (dfav['av1'] == mav) & (dfav['av2'] == mav2) & (dfav['per'] == mper)).any():
        mtot = dfav['gain'][(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                            (dfav['av2'] == mav2) & (dfav['per'] == mper)]
        mpos = dfav['pos'][(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                           (dfav['av2'] == mav2) & (dfav['per'] == mper)]
        mneg = dfav['neg'][(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                           (dfav['av2'] == mav2) & (dfav['per'] == mper)]
        mtot = mtot + mgain
        dfav.loc[(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                 (dfav['av2'] == mav2) & (dfav['per'] == mper), 'gain'] = mtot
        if mgain >= 0:
            dfav.loc[(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                     (dfav['av2'] == mav2) & (dfav['per'] == mper), 'pos'] = mpos + 1
        else:
            dfav.loc[(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                     (dfav['av2'] == mav2) & (dfav['per'] == mper), 'neg'] = mneg + 1

    else:
        if mgain >= 0:
            row = [mtic, mgain, mav, mav2, mper, 1, 0]
            dfav.loc[len(dfav)] = row
        else:
            row = [mtic, mgain, mav, mav2, mper, 0, 1]
            dfav.loc[len(dfav)] = row

    dfav.to_csv('../csv/trainresult.csv', index=False)

    trav = pd.read_csv('../csv/trainxch.csv')

    if ((trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper)).any():
        mtot = trav['gain'][(trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper)]
        mtot = mtot + mgain
        trav.loc[(trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper), 'gain'] = mtot

        if mgain >= 0:
            mpos = trav['pos'][(trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper)]
            trav.loc[(trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper), 'pos'] = mpos + 1
        else:
            mneg = trav['neg'][(trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper)]
            trav.loc[(trav['av1'] == mav) & (trav['av2'] == mav2) & (trav['per'] == mper), 'neg'] = mneg + 1

        trav.to_csv('../csv/trainxch.csv', index=False)
    else:
        if mgain >= 0:
            row = [mgain, mav, mav2, mper, 1, 0]
        else:
            row = [mgain, mav, mav2, mper, 0, 1]

        trav.loc[len(trav)] = row
        trav.to_csv('../csv/trainxch.csv', index=False)


# Receive variables from perdrop (ticker name, 1st moving average, 2nd moving average, percentage drop)
# Get the mean for av1 and av2 and save to file
# Assign variable names
# While loop that will start at dfti and loop until the last record
# Get today, yesterday and the day before yesterday av1 and av2, along with todays price

# The if statements will determine when a buy signal should be executed
# The first if statement states that if before yesterday av1 is bigger than yesterdays av1 and
# todays av1 is bigger than yesterday av1, meaning that the av1 graph has changed direction, and
# yesterday av2 is bigger than yesterdays av2 and todays av2 is bigger than yesterday av2,
# the av2 graph has change direction and buy equals 0, meaning that there has not been a signal yet and
# dfti (the position in the dataframe) +5 must be smaller than the last record
# This has been added to give a 5 day period for a reaction, nothing can be bought in these last 5 days, but can be sold
# If the statement is true, the variable mbuy = is set to todays price as it is the price of when it was bought
# Set buy to 1 (as it is a buy a signal)
# The variable pertot is equal to mbuy as pertot will be used to record the highest achieved price prior to selling

# The next if statement states that if todays price is bigger or equal to pertot (record of the highest price achieved)
# and buy equals 1 (It has already been bought), set pertot to todays price as it wil be bigger than the recorded data

# The third if statement states that if pertot (record of the highest price achieved) is not equal to todays price
# Calculate the percentage drop and multiply by -1 to return a positive figure

# The fourth if statement states that if buy equal 1 (it has been bought)
# and mmper(either 0 or the calculated percentage drop) is bigger than mper (received variable from function perdrop)
# this is a sell sign so the variable msel is equal to todays price, variable get sent to the sel function
# and buy = 0 as it has been sold

# The last if statement states that if buy equals 1 (it has been bought) and dfti has reached the last record,
# send variables to sell, this will bring train to an end and  maximise profits
# If dfti reaches the last record without selling it is because the graph is still in an upwards direction


def buy(mtic, mav, mav2, mper):
    dft = pd.read_csv('../csv/train/XCH/' + mtic)
    dft['av1'] = dft.iloc[:, 3].rolling(window=mav).mean()
    dft['av2'] = dft.iloc[:, 3].rolling(window=mav2).mean()
    dft.to_csv('../csv/train/XCH/' + mtic, index=False)
    dft = pd.read_csv('../csv/train/XCH/' + mtic)

    ldft = len(dft)
    dfti = ldft - 10
    buy = 0
    mmper = 0
    pertot = 0

    while dfti < ldft:
        tdav2 = dft.loc[dfti, 'av2']
        yav2 = dft.loc[dfti - 1, 'av2']
        byav2 = dft.loc[dfti - 2, 'av2']
        tdav1 = dft.loc[dfti, 'av1']
        yav1 = dft.loc[dfti - 1, 'av1']
        byav1 = dft.loc[dfti - 2, 'av1']
        tdprice = dft.loc[dfti, 'Realclose']

        if byav1 > yav1 and tdav1 > yav1 and byav2 > yav2 and tdav2 > yav2 and dfti + 5 < ldft and buy == 0:
            mbuy = tdprice
            buy = 1
            pertot = mbuy

        if tdprice >= pertot and buy == 1:
            pertot = tdprice

        if pertot != tdprice:
            mmper = 100 / (pertot / (tdprice - pertot))
            mmper = mmper * -1

        if buy == 1 and mmper >= mper:
            msel = tdprice
            sel(mtic, mav, mav2, mper, mbuy, msel)
            buy = 0

        if buy == 1 and dfti + 1 == ldft:
            msel = tdprice
            sel(mtic, mav, mav2, mper, mbuy, msel)
            buy = 0

        dfti = dfti + 1


# The following function is being used to determine the best percentage drop to trigger a sell signal
# Receive variables from mav2 (ticker name, first moving average second moving average)
# set back to original state being .1, while loop until it reaches .5
# Round to one decimal place
# send variables to buy


def perdrop(mtic, mav, mav2):
    mper = sper
    while mper <= eper:
        mper = round(mper, 1)
        buy(mtic, mav, mav2, mper)
        mper = mper + 0.1


# Functions mav1 and mav2 are used to determine the two different moving averages
# AV1 will use the moving averages between 2 and 5 and AV2 will use the moving averages between 3 and 10

# Receive variables from mav1 (ticker name, first moving average)
# set back to original state being 3, loop until it reaches 10
# While loop to figure out starting position
# There is 0 value of keeping data before the highest moving average
# Send variables to function perdrop

def mav2(mtic, mav):
    mav2 = sav2
    while mav2 <= eav2:
        print(mav2)
        if mav2 == mav:
            mav2 = mav2 + 1
        perdrop(mtic, mav, mav2)
        print(mtic, mav, mav2)
        mav2 = mav2 + 1


# Receive variable ticker name, set mav back to original being 2, loop until it reaches 5
# send variables (ticker name and moving average (between 2 and 5) to function mav2

def mav1(mtic):
    mav = sav1
    while mav <= eav1:
        mav2(mtic, mav)
        mav = mav + 1


# Read Forex file and loop through file to send ticker (file) name to function mav1


dffor = pd.read_csv('../CSV/train/forex.csv')
lfor = len(dffor)
ifor = 0
while ifor < lfor:
    mtic = dffor.loc[ifor, 'ticker']
    mtic = mtic + '.csv'
    mav1(mtic)
    ifor = ifor + 1

# Once all of the functions have been executed
# Insert three columns into trainxch.csv file
# riseratio is the ratio between the number of negative and positive outcomes
# avrise is the average rise -> the gain divided by the sum of postives and negative outcomes
# best is the average rise multiplied by the rise ratio
# The best will be used to order the file in a descending order as it will be the best outcome overall

trav = pd.read_csv('../csv/trainxch.csv')
if 'riseratio' in trav.columns:
    print(' ')
else:

    trav.insert(6, 'riseratio', 0)
    trav.insert(7, 'avrise', 0)
    trav.insert(8, 'best', 0)

tlen = len(trav)
i = 0
while i < tlen:
    mp = trav.loc[i, 'pos']
    mn = trav.loc[i, 'neg']
    mg = trav.loc[i, 'gain']
    mt = mp + mn
    if mn == 0:
        trav.loc[i, 'riseratio'] = mp
    else:
        trav.loc[i, 'riseratio'] = mp / mn
    trav.loc[i, 'avrise'] = mg / mt
    ma = trav.loc[i, 'avrise']
    mr = trav.loc[i, 'riseratio']
    trav.loc[i, 'best'] = ma * mr

    i = i + 1

trav = trav.sort_values(by='best', ascending=False)
trav.to_csv('../csv/trainxch.csv', index=False)
