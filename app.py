import numpy as np
from scipy.stats import norm
from fastapi import FastAPI
from pydantic import BaseModel

# Define Model Variables
# Description based on National Stock Exchange, India
# r = 0.052 # Rate of interest is the relevant MIBOR 
# S = 16220
# K = 16200
# T = 4/365
# sigma = 0.181

app = FastAPI()

class blackScholes(BaseModel):

    r : float
    S : int
    K : int
    T : float
    sigma : float
    type : str

# Implementing black scholes model
@app.get('/')
def echo():
    return {'message':'echo'}

@app.post('/price')
def blackScholes(item:blackScholes):
    d1 = (np.log(item.S/item.K) + (item.r + item.sigma**2/2)*item.T)/(item.sigma * np.sqrt(item.T))
    d2 = d1 - item.sigma*np.sqrt(item.T)
    
    try:
        if item.type == 'C':
            optionPrice = item.S * norm.cdf(d1, 0, 1) - item.K*np.exp(-item.r*item.T)*norm.cdf(d2, 0, 1)
            return optionPrice
        elif item.type == 'P':
            optionPrice = item.K*np.exp(-item.r*item.T)*norm.cdf(-d2, 0, 1) - item.S * norm.cdf(-d1, 0, 1)
            return optionPrice
    except Exception as e:
        print(e)   
    