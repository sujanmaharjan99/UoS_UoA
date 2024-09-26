import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from cmath import exp
import numpy as np

A= 247              #Area of the basin
c= 1             #Runoff coefficient
Tr= 0.1             #Residence time in seconds
Q_calc = []         #Discharge
e=np.exp(-1/(Tr))

Q_given=[0.402,0.454,0.798,0.817,3.25,5.07,
         5.32,5.23,4.57,4.05,4.26,4.09,3.54,
         3.16,2.72,2.38,1.97,1.45,1.03,0.623,0.307]
I = [0,21.7,0.9,16.3,37.6,4.5,2,0.1,0.1,
     2.5,17.6,0.1,2,0.3,1.5,0,0,0,0,0,0.1]          #Infiltration

Q_calc.append(Q_given[0])   #Setting initial value as the initial outflow

for i in range (1,len(I)):        #Calculate missing values
    Q_tplus1 = (c * A * I[i-1] / 1000 + (Q_calc[i-1] - c * A * I[i-1] / 1000) * e)
    Q_calc.append(Q_tplus1)

df=pd.DataFrame({'Date': pd.date_range(start='6/15/2023', periods=21, freq='D'),
                 'Q calculated':Q_calc,
                 'Q given':Q_given,
                 'Infiltration':I
                 })

rms = np.sqrt(mean_squared_error(df['Q given'], df['Q calculated']))

def NSE(a1,a2):
    denominator = np.sum((a1 - np.mean(a1)) ** 2)
    numerator = np.sum((a2 - a1) ** 2)
    nse_val = 1 - numerator / denominator
    return nse_val

nse=NSE(df['Q given'],df['Q calculated'])


fig,ax1=plt.subplots()

ax1.plot(df['Date'],df['Q calculated'],label='Q calculated',marker='o')
ax1.plot(df['Date'],df['Q given'],label='Q given',marker='x')
ax1.set_xlabel('Date')
plt.xticks(rotation=30)
ax1.set_ylabel('Discharge (m³/s)')
ax1.set_title('c={:.3f} & Tr={:.2f} d \n RMSE:{:.2f}m³/s & NSE: {:.2f}'.format(c, Tr,rms,nse))
ax1.grid(True)

ax2 = ax1.twinx()
ax2.bar(df['Date'], df['Infiltration'], color='green', alpha=0.5, label='Precipitation')
ax2.set_ylabel('Infiltration (mm/day)')
ax2.set_ylim(top=50)
ax2.invert_yaxis()
ax2.legend(loc=7)
ax1.legend(loc=1)
fig.tight_layout()
plt.show()
