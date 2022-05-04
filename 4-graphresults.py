import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd


def graph(mtic, mdate, sdate):
    dft = pd.read_csv('../csv/test/xch/' + mtic)
    dft = dft.tail(10)

    plt.plot(dft['Date'], dft[['Realclose', 'av1', 'av2']])
    plt.xticks(rotation=90)

    mx = mdate
    mxx = sdate
    my = dft["Realclose"].mean()
    plt.axvline(x=mdate, color='b', label='axvline - full height')
    plt.text(mx, my, 'Buy Signal', fontsize=15, fontweight='bold', rotation=90, backgroundcolor='white')
    plt.axvline(x=sdate, color='r', label='axvline - full height')
    plt.text(mxx, my, 'Sell Signal', fontsize=15, fontweight='bold', rotation=90, backgroundcolor='white')
    plt.legend(['Close', 'Av1', 'Av2'])
    plt.title(mtic + mdate)

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


df = pd.read_csv('../csv/test.csv')

ldf = len(df)
i = 0

while i < ldf:
    mtic = df.loc[i, 'ticker']
    mdate = df.loc[i, 'bdate']
    sdate = df.loc[i, 'sdate']
    print(mtic)
    graph(mtic, mdate, sdate)
    i = i + 1
