import pandas as pd


def test(mrec):
    mrec = mrec + 10
    print(mrec)

    # Create file
    column_names = ['gain', 'pos', 'neg']
    df = pd.DataFrame(columns=column_names)
    df.to_csv('csv/testxch.csv', index=False)
    df = pd.read_csv('csv/testxch.csv')
    row = [0, 0, 0]
    df.loc[len(df)] = row
    df.to_csv('csv/testxch.csv', index=False)

    # Read file
    df = pd.read_csv('csv/trainxch.csv')
    mav = int(df.loc[0, 'av1'])
    mav2 = int(df.loc[0, 'av2'])
    mper = df.loc[0, 'per']

    def sel(mbuy, msel):

        mgain = 100 / (mbuy / (msel - mbuy))
        trav = pd.read_csv('csv/testxch.csv')
        mmgain = trav.loc[0, 'gain']
        if mgain >= 0:
            mpos = trav.loc[0, 'pos']
            trav.loc[0, 'pos'] = mpos + 1
            trav.loc[0, 'gain'] = mgain + mmgain
        else:
            mneg = trav.loc[0, 'neg']
            trav.loc[0, 'neg'] = mneg + 1
            trav.loc[0, 'gain'] = mgain + mmgain
        trav.to_csv('csv/testxch.csv', index=False)

    def buy(mtic, mrec, mav, mav2, mper):
        dft = pd.read_csv('csv/XCH/' + mtic)
        dft['av1'] = dft.iloc[:, 3].rolling(window=mav).mean()
        dft['av2'] = dft.iloc[:, 3].rolling(window=mav2).mean()
        dft.to_csv('csv/XCH/' + mtic, index=False)
        dft = pd.read_csv('csv/XCH/' + mtic)
        print(mtic)

        # Change date into a string for searching

        dfti = mrec + 15
        ldft = dfti + 25
        buy = 0
        mmper = 0
        pertot = 0
        print(mrec)

        while dfti < ldft:
            print(dfti)
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

            if pertot != tdprice and tdprice != 0 and pertot != 0:
                mmper = 100 / (pertot / (tdprice - pertot))
                mmper = mmper * -1

            if buy == 1 and mmper >= mper:
                msel = tdprice

                sel(mbuy, msel)
                buy = 0

            if buy == 1 and dfti + 1 == ldft:
                msel = tdprice
                sel(mbuy, msel)
                buy = 0

            dfti = dfti + 1

    # Read forex file
    dffor = pd.read_csv('csv/forex.csv')
    lfor = len(dffor)
    ifor = 0
    while ifor < lfor:
        mtic = dffor.loc[ifor, 'ticker']
        mtic = mtic + '.csv'
        buy(mtic, mrec, mav, mav2, mper)
        ifor = ifor + 1

    trav = pd.read_csv('csv/testxch.csv')
    mp = trav.loc[0, 'pos']
    mn = trav.loc[0, 'neg']
    if mp + mn > 0:
        mlen = len(trav)
        if mlen > 0:
            mp = trav.loc[0, 'pos']
            mn = trav.loc[0, 'neg']
            if 'riseratio' in trav.columns:
                print(' ')
            else:
                trav.insert(3, 'riseratio', 0)
                trav.insert(4, 'avrise', 0)

            trav.loc[0, 'riseratio'] = mp / mn
            mgain = trav.loc[0, 'gain']
            mratio = trav.loc[0, 'riseratio']

            df = pd.read_csv('csv/results.csv')
            lrec = len(df) - 1
            df.loc[lrec, 'testgain'] = mgain
            df.loc[lrec, 'testratio'] = mratio

            df.to_csv('csv/results.csv', index=False)
