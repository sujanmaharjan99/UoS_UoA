import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from cmath import exp
import numpy as np

def model(Q_given,I,A,c,e): #a function to simulate the model repeatedly
    Q_calc = []     #Discharge
    Q_calc.append(Q_given[0])   #Setting initial value as the initial outflow

    for i in range (1,len(I)):        #Calculate missing values
        Q_tplus1 = (c * A * I[i-1] / 1000 + (Q_calc[i-1] - c * A * I[i-1] / 1000) * e)
        Q_calc.append(Q_tplus1)
    return Q_calc

A= 247          #Area of the basin
Q_given=[0.402,0.454,0.798,0.817,3.25,5.07,5.32,5.23,4.57,4.05,4.26,4.09,3.54,3.16,2.72,2.38,1.97,1.45,1.03,0.623,0.307]        #Given discharge timeseries
I = [0,21.7,0.9,16.3,37.6,4.5,2,0.1,0.1,2.5,17.6,0.1,2,0.3,1.5,0,0,0,0,0,0.1]                                                   #Given Infiltration

n=100            #number of simulation
q_sim=[]        #results from n simulations

for i in range (n):
    c=np.random.uniform(0.1,0.8)    #Random Runoff coefficient
    Tr=np.random.uniform(1,10)      #Residence time in days
    e=np.exp(-1/(Tr))
    
    new=model(Q_given,I,A,c,e)  #calling the model function n number of times with random c and Tr
    q_sim.append(new)


df=pd.DataFrame(q_sim)
mean_of_simulation=df.mean()    #calculating a vector of mean of each timeseries in each timesetp
sd_of_simulation=df.std()       #calculating the standsrd deviation of each timeseries in each timestep

date=pd.date_range(start='6/15/2023', periods=21, freq='D')

#Plot of the Monte Carlo simulation
plt.fill_between(date,mean_of_simulation-2*sd_of_simulation,mean_of_simulation+2*sd_of_simulation,color='lightblue',label='Uncertainty range')
plt.plot(date,Q_given,label='Observed discharge')
plt.plot(date,mean_of_simulation,label='Mean of simulated discharge')
plt.xlabel('Date')
plt.xticks(rotation=30)
plt.ylabel('Discharge (m³/s)')
plt.title('Uncertainty plot with 2xSD')
plt.grid(True)
plt.legend()
plt.show()

# df=pd.DataFrame({'Date': pd.date_range(start='6/15/2023', periods=21, freq='D'),
#                  'Q calculated':Q_calc,
#                  'Q given':Q_given,
#                  'Infiltration':I
#                  })




# fig,ax1=plt.subplots()

# ax1.plot(df['Date'],df['Q calculated'],label='Q calculated',marker='o')
# ax1.plot(df['Date'],df['Q given'],label='Q given',marker='x')
# ax1.set_xlabel('Date')
# plt.xticks(rotation=30)
# ax1.set_ylabel('Discharge (m³/s)')
# ax1.set_title('c={:.3f} & Tr={:.2f} d \n RMSE:{:.2f}m³/s & NSE: {:.2f}'.format(c, Tr,rms,nse))
# ax1.grid(True)

# ax2 = ax1.twinx()
# ax2.bar(df['Date'], df['Infiltration'], color='green', alpha=0.5, label='Precipitation')
# ax2.set_ylabel('Infiltration (mm/day)')
# ax2.set_ylim(top=50)
# ax2.invert_yaxis()
# ax2.legend(loc=7)
# ax1.legend(loc=1)
# fig.tight_layout()
# plt.show()
