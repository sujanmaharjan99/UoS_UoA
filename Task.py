import pandas as pd
from cmath import exp
import numpy as np

A= 247              #Area of the basin
c= 0.7            #Runoff coefficient
Tr=4       #Residence time in seconds
Q_calc = []         #Discharge
    

Q_given=[0.402,0.454,0.798,0.817,3.25,5.07,
         5.32,5.23,4.57,4.05,4.26,4.09,3.54,
         3.16,2.72,2.38,1.97,1.45,1.03,0.623,0.307]
I = [0,21.7,0.9,16.3,37.6,4.5,2,0.1,0.1,
     2.5,17.6,0.1,2,0.3,1.5,0,0,0,0,0,0.1]          #Infiltration

def model(Q_given,I,A,c,Tr):
    e=np.exp(-1/Tr)  
    Q_calc.append(Q_given[0])   #Setting initial value as the initial outflow

    for i in range (1,len(I)):        #Calculate missing values
        Q_tplus1 = (c * A * I[i-1] / 1000 + (Q_calc[i-1] - c * A * I[i-1] / 1000) * e)

        Q_calc.append(Q_tplus1)
  
    return Q_calc

Q_calc=model(Q_given,I,A,c,Tr)
df=pd.DataFrame({'Date': pd.date_range(start='6/15/2023', periods=21, freq='D'),
                    'Infiltration':I,
                    'Q given':Q_given,
                    'Q calculated':Q_calc,
                    })
print(df)
