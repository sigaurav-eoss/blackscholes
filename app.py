import numpy as np
from scipy.stats import norm
from fastapi import FastAPI

# Define Model Variables
# Description based on National Stock Exchange, India
# r = 0.052 # Rate of interest is the relevant MIBOR 
# S = 16220
# K = 16200
# T = 4/365
# sigma = 0.181

app = FastAPI()

# Implementing black scholes model
@app.get('/')
def echo():
    return {'message':'echo'}

@app.get('/price')
def blackScholes(r:float, S:int, K:int, T:float, sigma:float, type:str):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma * np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    try:
        if type == 'C':
            optionPrice = S * norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
            return optionPrice
        elif type == 'P':
            optionPrice = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)
            return optionPrice
    except Exception as e:
        print(e)   
    