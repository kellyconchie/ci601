# yfinance to download currency data from Yahoo
import yfinance as yf

# Pandas to manipulate the CSV files and data frames
import pandas as pd

# os to remove old files and clean directories
import os


def DL(st, td):
    # Check whether the specified path exists or not
    # If this is the first time of running the program it will create the directories necessary
    path = 'csv/XCH'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs('csv/XCH')
        os.makedirs('csv/GBP')
        print("The new directory is created!")

    # Clean Directories
    mydir = "csv/XCH"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))
    mydir = "csv/GBP"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))

    # Create a Forex.csv to record currency pairs used
    column_names = ['ticker', 'currency']
    dfor = pd.DataFrame(columns=column_names)
    dfor.to_csv('csv/forex.csv', index=False)

    # use ori.csv for currencies to be used
    df = pd.read_csv('csv/ori.csv')
    rn = len(df)
    i = 0

    # Download GBP files for currencies and dates to be used
    gbp = 'GBP'
    while i < rn:
        mquote = df.loc[i, 'code']
        data = yf.download(mquote + gbp + "=x", start=st, end=td)
        print(mquote, 'GBP data downloaded')
        df2 = pd.DataFrame(data)
        # Only date and closing price is being used
        # Delete unwanted columns from Data Frame
        del df2['Open']
        del df2['Volume']
        del df2['Adj Close']
        del df2['High']
        del df2['Low']
        df2.to_csv('csv/GBP/' + mquote + gbp + '=x.csv')
        i = i + 1

    # Dowload exchange files
    # use ori.csv for currencies to be used
    df = pd.read_csv('csv/ori.csv')
    rn = len(df)
    i = 0

    while i < rn:
        # Get base currency
        mbase = df.loc[i, 'code']
        bcur = df.loc[i, 'currency']
        print(bcur)

        ii = i + 1
        while ii < rn:
            # skip 1 get quote currency
            mquote = df.loc[ii, 'code']
            qcur = df.loc[ii, 'currency']
            print(qcur)

            # download data from Yahoo
            data = yf.download(mbase + mquote + "=x", start=st, end=td)
            print(mbase, mquote, ' data downloaded')
            df2 = pd.DataFrame(data)

            # Delete unwanted columns from Data Frame
            del df2['Open']
            del df2['Volume']
            del df2['Adj Close']
            del df2['High']
            del df2['Low']

            # Variable tic is the name of currency comparison file to be stored as csv file
            # Variable cur is the names of the currencies to be stored in the forex file listing the CSV files stored

            rn2 = len(df2)
            tic = mbase + mquote + "=x"
            cur = bcur + '-' + qcur

            # if dataframe contains more than 5 records. ie not empty.
            # save as csv file use base and quote names as file name in working directory
            # the working directory will either be the test or train directory
            # rn2 is the length of the downloaded file

            if rn2 > 5:
                df2.to_csv('csv/XCH/' + mbase + mquote + '=x.csv')
                df3 = pd.read_csv('csv/forex.csv')

                # check if file name already exists in the forex file. If not then add it
                if tic not in df3.values:
                    row = [tic, cur]
                    df3.loc[len(df3)] = row
                    df3.to_csv('csv/forex.csv', index=False)
            ii = ii + 1
        i = i + 1

    # repeat reversing base for quote currencies
    df = pd.read_csv('csv/ori.csv')
    rn = len(df)

    i = 0
    while i < rn:

        # Get quote currency
        mquote = df.loc[i, 'code']
        bcur = df.loc[i, 'currency']
        print(bcur)

        ii = i + 1
        while ii < rn:
            # skip 1 get base currency
            mbase = df.loc[ii, 'code']
            qcur = df.loc[ii, 'currency']
            print(qcur)

            # download data from Yahoo
            data = yf.download(mbase + mquote + "=x", start=st, end=td)
            print(mbase, mquote, 'data downloaded')
            df2 = pd.DataFrame(data)

            # Delete unwanted columns from Data Frame
            del df2['Open']
            del df2['Volume']
            del df2['Adj Close']
            del df2['High']
            del df2['Low']

            # Variable tic is the name of currency comparison file to be stored as csv file
            # Variable cur is the names of the currencies to be stored in the forex file listing the CSV files stored
            rn2 = len(df2)
            tic = mbase + mquote + "=x"
            cur = qcur + '-' + bcur

            # if dataframe contains more than 5 records. ie not empty.
            # save as csv file use base and quote names as file name in working directory
            if rn2 > 5:
                df2.to_csv('csv/XCH/' + mbase + mquote + '=x.csv')
                df3 = pd.read_csv('csv/forex.csv')

                # check if file name already exists in the forex file. If not then add it

                if tic not in df3.values:
                    row = [tic, cur]
                    df3.loc[len(df3)] = row
                    df3.to_csv('csv/forex.csv', index=False)
            ii = ii + 1
        i = i + 1

    # make 2 temporary files for testing and cleaning files
    column_names = ['ticker']
    dpc = pd.DataFrame(columns=column_names)
    dpc.to_csv('csv/gbpcheck.csv', index=False)

    column_names = ['ticker']
    dftc = pd.DataFrame(columns=column_names)
    dftc.to_csv('csv/tickclean.csv', index=False)

    # Check all GBP files to find ones with no data and remove files from GBP directory
    df = pd.read_csv('csv/ori.csv')
    rn = len(df)
    i = 0
    gbp = 'GBP'
    while i < rn:
        mquote = df.loc[i, 'code']
        mtic = mquote + gbp
        if os.path.isfile('csv/GBP/' + mtic + "=x.csv"):
            dff = pd.read_csv('csv/GBP/' + mtic + "=x.csv")
            rn2 = len(dff)
            print(mtic)
            if rn2 < 5:
                row = [mtic]
                dpc.loc[len(dpc)] = row
                dpc.to_csv('csv/gbpcheck.csv', index=False)
                os.remove('csv/GBP/' + mtic + "=x.csv")
                print(mtic + " removed")
        else:
            row = [mtic]
            dpc.loc[len(dpc)] = row
            dpc.to_csv('csv/gbpcheck.csv', index=False)

        i = i + 1

    # remove files from Train and test directories where we do not have a Quote-GBP comparison.
    # Remove reference to deleted files from Forex file.

    dpc = pd.read_csv('csv/gbpcheck.csv')
    i = 0
    rn = len(dpc)
    while i < rn:
        mtc = dpc.loc[i, 'ticker']
        mt2 = str(mtc)[0:3]
        dfor = pd.read_csv('csv/forex.csv')

        ii = 0
        rn2 = len(dfor)
        while ii < rn2:
            mticker = dfor.loc[ii, 'ticker']

            if str(mticker)[3:6] == mt2:
                row = [mticker]
                dftc.loc[len(dftc)] = row
                dftc.to_csv('csv/tickclean.csv', index=False)

            ii = ii + 1
        i = i + 1

    dftc = pd.read_csv('csv/tickclean.csv')
    i = 0
    ren = len(dftc)
    while i < ren:
        mtic = dftc.loc[i, 'ticker']
        if os.path.isfile('csv/XCH/' + mtic + '.csv'):
            os.remove('csv/XCH/' + mtic + '.csv')
            print(mtic, "tXCH removed")

        dfor = dfor.drop(dfor[dfor.ticker == mtic].index)
        dfor.to_csv('csv/forex.csv', index=False)

        i = i + 1

    # clean out temp csv files
    if os.path.isfile('csv/gbpcheck.csv'):
        os.remove("csv/gbpcheck.csv")
        print("gbpcheck.csv removed")

    if os.path.isfile('csv/tickclean.csv'):
        os.remove("csv/tickclean.csv")
        print("tickclean.csv removed")

    # Add extra column to exchange files to add the GBP exchange rate for the quote currency.
    df = pd.read_csv('csv/forex.csv')
    rn = len(df)
    i = 0
    while i < rn:
        mtic = df.loc[i, 'ticker']
        df2 = pd.read_csv('csv/XCH/' + mtic + '.csv')
        if 'GBPquote' in df2.columns:
            print(' ')
        else:
            df2.insert(2, 'GBPquote', 1)
            df2.insert(3, 'Realclose', 1)
        df2.to_csv('csv/XCH/' + mtic + '.csv', index=False)
        print('Column added to ' + mtic)
        i = i + 1

    rn = len(df)
    i = 0
    GBP = 'GBP'
    while i < rn:
        mtic = df.loc[i, 'ticker']
        mbase = str(mtic)[3:6]
        print(mtic)

        # Align indexes GBP exchange on Quote currency
        df2 = pd.read_csv('csv/XCH/' + mtic + '.csv')
        mtic2 = mbase + GBP + '=x.csv'
        df3 = pd.read_csv('csv/GBP/' + mtic2)
        lendf3 = len(df3)
        i2 = 0
        while i2 < lendf3:
            mdate = df3.loc[i2, 'Date']
            if mdate in df2['Date'].values:
                pass
            else:
                df3 = df3.drop(df3[df3['Date'] == mdate].index)
            i2 = i2 + 1
        # save as temporary files without index to keep originals in tact
        df2.to_csv('t1.csv', index=False)
        df3.to_csv('t2.csv', index=False)
        df2 = pd.read_csv('t1.csv')
        df3 = pd.read_csv('t2.csv')

        # updGBP exchange rate on quote price
        i3 = 0
        lendf3 = len(df3)
        print("updating" + mtic)
        while i3 < lendf3:
            mdate = df3.loc[i3, 'Date']
            mclose = df3.loc[i3, 'Close']
            df2.loc[(df2.Date == mdate), 'GBPquote'] = mclose
            df2.loc[(df2.Date == mdate), 'Realclose'] = df2.loc[(df2.Date == mdate), 'Close'] * mclose

            i3 = i3 + 1
        df2 = df2.drop(df2[df2.GBPquote == 1].index)
        df2.to_csv('csv/XCH/' + mtic + '.csv', index=False)

        i = i + 1

    # remove temporary files
    if os.path.isfile('t1.csv'):
        os.remove("t1.csv")
        print("t1.csv removed")
    if os.path.isfile('t2.csv'):
        os.remove("t2.csv")
        print("t2.csv removed")
