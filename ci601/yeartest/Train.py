import pandas as pd


from Test import test

def train(mrec):
    print('start ', mrec)

    column_names = ['date', 'gain', 'av1', 'av2', 'per', 'pos', 'neg']
    stav = pd.DataFrame(columns=column_names)
    stav.to_csv('csv/trainxch.csv', index=False)

    # Read all file names in forex file
    # In each file in the train directory insert two new columns
    dffor = pd.read_csv('csv/forex.csv')
    lfor = len(dffor)
    ifor = 0
    while ifor < lfor:
        mtic = dffor.loc[ifor, 'ticker']
        print(mtic)
        mtic = mtic + '.csv'
        tfor = pd.read_csv('csv/XCH/' + mtic)
        if 'av1' in tfor.columns:
            print(' ')
        else:
            tfor.insert(4, 'av1', 0)
            tfor.insert(5, 'av2', 0)
        tfor.to_csv('csv/XCH/' + mtic, index=False)
        ifor = ifor + 1

    sav1 = 2
    eav1 = 5
    sav2 = 3
    eav2 = 10
    sper = .1
    eper = .5

    def sel(chkdate, mav, mav2, mper, mbuy, msel):
        print('sell ', chkdate)
        mgain = 100 / (mbuy / (msel - mbuy))

        trav = pd.read_csv('csv/trainxch.csv')

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

            trav.to_csv('csv/trainxch.csv', index=False)
        else:
            if mgain >= 0:
                row = [chkdate, mgain, mav, mav2, mper, 1, 0]
            else:
                row = [chkdate, mgain, mav, mav2, mper, 1, 0]

            trav.loc[len(trav)] = row
            trav.to_csv('csv/trainxch.csv', index=False)

    def buy(mtic, mrec, mav, mav2, mper):
        print('buy ', mrec)
        print('Training ', mtic, ' ', mrec)
        dft = pd.read_csv('csv/XCH/' + mtic)
        dft['av1'] = dft.iloc[:, 3].rolling(window=mav).mean()
        dft['av2'] = dft.iloc[:, 3].rolling(window=mav2).mean()
        dft.to_csv('csv/XCH/' + mtic, index=False)
        dft = pd.read_csv('csv/XCH/' + mtic)

        dfti = mrec + 15
        ldft = dfti + 25
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
            chkdate = dft.loc[mrec, 'Date']
            print(mrec, ' ', chkdate)
            print('train ', mrec)

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
                sel(chkdate, mav, mav2, mper, mbuy, msel)
                buy = 0

            if buy == 1 and dfti + 1 == ldft:
                msel = tdprice
                sel(chkdate, mav, mav2, mper, mbuy, msel)
                buy = 0

            dfti = dfti + 1

    def perdrop(mtic, mrec, mav, mav2):
        mper = sper
        while mper <= eper:
            mper = round(mper, 1)
            print('perdrop ', mrec)
            buy(mtic, mrec, mav, mav2, mper)
            mper = mper + 0.1

    def mav2(mtic, mrec, mav):
        mav2 = sav2
        while mav2 <= eav2:
            print(mav2)
            if mav2 == mav:
                mav2 = mav2 + 1
            print('mav2 ', mrec)
            perdrop(mtic, mrec, mav, mav2)
            print(mtic, mrec, mav, mav2)
            mav2 = mav2 + 1

    def mav1(mtic, mrec):
        mav = sav1
        while mav <= eav1:
            print('mav1 ', mrec)
            mav2(mtic, mrec, mav)
            mav = mav + 1

    dffor = pd.read_csv('csv/forex.csv')
    lfor = len(dffor)
    ifor = 0
    while ifor < lfor:
        mtic = dffor.loc[ifor, 'ticker']
        mtic = mtic + '.csv'
        print('ticker ', mrec)
        mav1(mtic, mrec)
        ifor = ifor + 1


    trav = pd.read_csv('csv/trainxch.csv')
    mchk = trav.loc[0, 'av1']
    if mchk > 0:
        if 'riseratio' in trav.columns:
            print(' ')
        else:

            trav.insert(7, 'riseratio', 0)
            trav.insert(8, 'avrise', 0)
            trav.insert(9, 'best', 0)

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
        trav.to_csv('csv/trainxch.csv', index=False)
        df = pd.read_csv('csv/trainxch.csv')

        mgain = df.loc[0, 'gain']
        mratio = df.loc[0, 'riseratio']
        mav1 = df.loc[0, 'av1']
        mav2 = df.loc[0, 'av2']
        mper = df.loc[0, 'per']
        chkdate = df.loc[0, 'date']

        dff = pd.read_csv('csv/results.csv')
        row = [chkdate, mav1, mav2, mper, mgain, mratio, 0, 0, ]
        dff.loc[len(df)] = row
        dff.to_csv('csv/results.csv', index=False)

        test(mrec)
