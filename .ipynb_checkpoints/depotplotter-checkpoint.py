
# coding: utf-8


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time


#TODO: GUI


#colors for plotting:

colors = ['#845EC2', '#D65DB1', '#FF6F91', '#FF9671', '#FFC75F', '#F9F871', '#5EADC2', '#4AC2C6', '#54D6BB',
          '#7FE6A4', '#B8F288', '#F9F871', '#282F44', '#453A49', '#6D3B47', '#FFD8BE', '#FFEEDD']



def manualmode():
    stocknumber = 'placeholder'
    stocknumber = input('How many positions do you have in your Portfolio? ')
    stocknumber=int(stocknumber)
    stocknames = []
    stockvalues = []
    stockshares = []

    for stock in range(stocknumber):
        stocknames.append(input('Please fill in the Name of Position Nr. {}: '.format(stock+1)))
        stockvalues.append(float(input('Please fill in the actual Value per stock of Position Nr. {}: '.format(stock+1))))
        stockshares.append(float(input('How many shares do you own of Position Nr. {}: '.format(stock+1))))
    for i in range(stocknumber):           #cut down namelenght
        if len(stocknames[i])>7:
            stocknames[i] = stocknames[i][0:6]
        else:
            pass
    df = pd.DataFrame(list(zip(stocknames, stockvalues, stockshares)), columns=['Stock', 'Value', 'Shares'])
    df['TotalValue'] = df['Value'] * df['Shares']
    df.sort_values("TotalValue", axis = 0, ascending = False, 
                 inplace = True, na_position ='last')
    return df

def automaticmode():
    df = pd.read_excel('depot.xls', encoding='latin1')
    df = df.drop(labels=['ISIN', 'Kategorie', 'Börse', 'Zeit', 'Unnamed: 22', 'Unnamed: 6', 'Unnamed: 4',
                    'Unnamed: 12', 'Unnamed: 14', '+/- Vortag', 'Unnamed: 16', 'Sperre/Lagerst.', 'in %',
                    'Unnamed: 18', 'Unnamed: 24', 'Datum', 'Unnamed: 20'], axis=1)
    df = df.rename(columns={"Bezeichnung": "Stock", "Stk./Nominale": "Shares", 'Aktueller Wert': 'TotalValue', 
                       'Akt. Kurs': 'Value'})
    df.sort_values("TotalValue", axis = 0, ascending = False, 
                   inplace = True, na_position ='last')
    for i in range(df.shape[0]):           #cut down namelenght
        if len(df['Stock'][i])>12:
            df['Stock'][i] = df['Stock'][i][0:11]
        else:
            pass
        
        
    return df

def plot(df):
    
    labels = df['Stock']
   # labellist = list(labels)
    numbers = df['TotalValue']
    y_pos = np.arange(len(labels))
    # Plot
    fig = plt.figure(figsize=(15,8))
    ax1 = fig.add_subplot(1,2,1)
    ax1.set_ylabel('Absolute Value')
    ax2 = fig.add_subplot(1,2,2)
    ax1.bar(y_pos, numbers, edgecolor='blue', color=colors)
    ax1.set_xticks(y_pos)
    ax1.set_xticklabels(labels, rotation='vertical')
    ax2.pie(numbers, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, colors = colors)
    circle = plt.Circle((0,0),0.70,fc='white')
    ax2.add_artist(circle)
    ax2.text(0.39, 0.53, getdate(), transform=ax2.transAxes, fontsize=15, verticalalignment='top')
    fig.tight_layout(pad=4.5)
    fig.savefig('portfolio_'+str(getdate())+'.jpg')
    fig.show()
    
    
def getdate():
    datestring = time.strftime("%d.%m.%Y")
    return datestring

#lets start:

#lets start:

print('Welcome to the Portfolio Plotter!')
mode = 2 

while(mode!=0 and mode!=1):
    mode = int(input('Type 0 for manual submitting stock information or 1 for reading in a csv file: '))
    if (mode!=0 and mode!=1):
        print("You entered a false character, please try again! \n")

if mode == 0:
    df = manualmode()
else:
    df = automaticmode()
    
print(df)
plot(df)