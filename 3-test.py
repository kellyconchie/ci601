import pandas as pd

# os to remove old files and clean directories
import os

# Remove file
if os.path.isfile('../csv/testresult.csv'):
    os.remove('../csv/testresult.csv')
    print("testresult.csv removed")

# Create file
column_names = ['ticker', 'gain', 'av1', 'av2', 'per', 'pos', 'neg']
trav = pd.DataFrame(columns=column_names)
trav.to_csv('../csv/testresult.csv', index=False)

# Remove file
if os.path.isfile('../csv/testxch.csv'):
    os.remove('../csv/testxch.csv')
    print("testxch.csv removed")

# Create file
column_names = ['gain', 'av1', 'av2', 'per', 'pos', 'neg']
stav = pd.DataFrame(columns=column_names)
stav.to_csv('../csv/testxch.csv', index=False)

# Remove file
if os.path.isfile('../csv/test.csv'):
    os.remove('../csv/test.csv')
    print("test.csv removed")

# Create file for graphing
column_names = ['ticker', 'bdate', 'sdate']
test = pd.DataFrame(columns=column_names)
test.to_csv('../csv/test.csv', index=False)

# Read file
df = pd.read_csv('../csv/trainxch.csv')
mav = int(df.loc[0, 'av1'])
mav2 = int(df.loc[0, 'av2'])
mper = df.loc[0, 'per']

# Read files in test directory and insert columns in each file
dffor = pd.read_csv('../csv/test/forex.csv')
lfor = len(dffor)
ifor = 0
while ifor < lfor:
    mtic = dffor.loc[ifor, 'ticker']
    mtic = mtic + '.csv'
    tfor = pd.read_csv('../csv/test/XCH/' + mtic)
    if 'av1' in tfor.columns:
        print(' ')
    else:
        tfor.insert(4, 'av1', 0)
        tfor.insert(5, 'av2', 0)
    tfor.to_csv('../csv/test/XCH/' + mtic, index=False)
    ifor = ifor + 1


def sel(mtic, mav, mav2, mper, mbuy, msel, bdate, sdate):
    row = [mtic, bdate, sdate]
    mtest = pd.read_csv('../csv/test.csv')
    mtest.loc[len(mtest)] = row
    mtest.to_csv('../csv/test.csv', index=False)

    print(mtic, mbuy, msel)
    mgain = 100 / (mbuy / (msel - mbuy))

    dfav = pd.read_csv('../csv/testresult.csv')

    if ((dfav['ticker'] == mtic) & (dfav['av1'] == mav) & (dfav['av2'] == mav2) & (dfav['per'] == mper)).any():
        mtot = dfav['gain'][(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                            (dfav['av2'] == mav2) & (dfav['per'] == mper)]
        mpos = dfav['pos'][(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                           (dfav['av2'] == mav2) & (dfav['per'] == mper)]
        mneg = dfav['neg'][(dfav['ticker'] == mtic) & (dfav['av1'] == mav) &
                           (dfav['av2'] == mav2) & (dfav['per'] == mper)]
        mtot = mtot + mgain
        dfav.loc[(dfav['ticker'] == mtic) & (dfav['av1'] == mav) & (dfav['av2'] == mav2) &
                 (dfav['per'] == mper), 'gain'] = mtot
        if mgain >= 0:
            dfav.loc[(dfav['ticker'] == mtic) & (dfav['av1'] == mav) & (dfav['av2'] == mav2) &
                     (dfav['per'] == mper), 'pos'] = mpos + 1
        else:
            dfav.loc[(dfav['ticker'] == mtic) & (dfav['av1'] == mav) & (dfav['av2'] == mav2) &
                     (dfav['per'] == mper), 'neg'] = mneg + 1

    else:
        if mgain >= 0:
            row = [mtic, mgain, mav, mav2, mper, 1, 0]
            dfav.loc[len(dfav)] = row
        else:
            row = [mtic, mgain, mav, mav2, mper, 0, 1]
            dfav.loc[len(dfav)] = row

    dfav.to_csv('../csv/testresult.csv', index=False)

    trav = pd.read_csv('../csv/testxch.csv')

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

        trav.to_csv('../csv/testxch.csv', index=False)
    else:
        if mgain >= 0:
            row = [mgain, mav, mav2, mper, 1, 0]
        else:
            row = [mgain, mav, mav2, mper, 0, 1]

        trav.loc[len(trav)] = row
        trav.to_csv('../csv/testxch.csv', index=False)


def buy(mtic, mav, mav2, mper):
    dft = pd.read_csv('../csv/test/XCH/' + mtic)
    dft['av1'] = dft.iloc[:, 3].rolling(window=mav).mean()
    dft['av2'] = dft.iloc[:, 3].rolling(window=mav2).mean()
    dft.to_csv('../csv/test/XCH/' + mtic, index=False)
    dft = pd.read_csv('../csv/test/XCH/' + mtic)
    print(mtic)

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
        mdate = dft.loc[dfti, 'Date']

        tdprice = dft.loc[dfti, 'Realclose']

        if byav1 < yav1 and tdav1 < yav1 and byav2 < yav2 and tdav2 < yav2 and dfti + 5 < ldft and buy == 0:
            mbuy = tdprice
            bdate = mdate
            buy = 1
            pertot = mbuy

        if tdprice >= pertot and buy == 1:
            pertot = tdprice

        if pertot != tdprice and tdprice != 0 and pertot != 0:
            mmper = 100 / (pertot / (tdprice - pertot))
            mmper = mmper * -1

        if buy == 1 and mmper >= mper:
            msel = tdprice
            sdate = mdate
            sel(mtic, mav, mav2, mper, mbuy, msel, bdate, sdate)
            buy = 0

        if buy == 1 and dfti + 1 == ldft:
            msel = tdprice
            sdate = mdate
            sel(mtic, mav, mav2, mper, mbuy, msel, bdate, sdate)
            buy = 0

        dfti = dfti + 1


# Read forex file
dffor = pd.read_csv('../CSV/test/forex.csv')
lfor = len(dffor)
ifor = 0
while ifor < lfor:
    mtic = dffor.loc[ifor, 'ticker']
    mtic = mtic + '.csv'
    buy(mtic, mav, mav2, mper)
    ifor = ifor + 1

trav = pd.read_csv('../csv/testxch.csv')
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
trav.to_csv('../csv/testxch.csv', index=False)
