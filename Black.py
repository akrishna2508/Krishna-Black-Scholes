from math import log, sqrt, exp
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import norm
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#imported all libraries to use necesary functions

def bs(S, K, T, r, sigma, option_type='call'): #bs= black scholes formula function
    d1 = (log(S / K) + (r + ((sigma ** 2) * 0.5) * T)) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        messagebox.showerror("Error", "Invalid option type selected")
        return

    return option_price

def getval(): #geting values from gui
    S = float(spot_price_entry.get())
    K = float(strike_price_entry.get())
    T = float(maturity_entry.get())
    r = float(interest_rate_entry.get())
    sigma = float(volatility_entry.get())
    option_type = option_type_var.get()

    option_price = bs(S, K, T, r, sigma, option_type)
    messagebox.showinfo("Option Price", f"The {option_type} option price is: {option_price}")

def heatmap(): #heat map production
    S = float(spot_price_entry.get())
    r = float(interest_rate_entry.get())
    sigma = float(volatility_entry.get())

    strike_prices = np.arange(80, 121, 5)
    maturities = np.arange(0.1, 1, 0.1)

    K, T = np.meshgrid(strike_prices, maturities)
    option_prices = np.vectorize(bs)(S, K, T, r, sigma, 'call')

    plt.figure(figsize=(10, 6))
    plt.contourf(K, T, option_prices, cmap='viridis')
    plt.colorbar(label='Option Price')
    plt.title('Option Price Heatmap')
    plt.xlabel('Strike Price')
    plt.ylabel('Time to Maturity (Years)')
    plt.show()

root = tk.Tk() #gui through tkinter
root.geometry('600x400') #size of the window
root.title("Black Scholes Option Price Calculator") #heading of the gui

tk.Label(root, text="Spot Price (S):").grid(row=0, column=0) #input spot price
spot_price_entry = tk.Entry(root)
spot_price_entry.grid(row=0, column=1)

tk.Label(root, text="Strike Price (K):").grid(row=1, column=0) #Strike price (price at which you can buy the security when call option, or at which you sell when put.)
strike_price_entry = tk.Entry(root)
strike_price_entry.grid(row=1, column=1)

tk.Label(root, text="Time to Maturity in years (T):").grid(row=2, column=0) #input  time to maturity
maturity_entry = tk.Entry(root)
maturity_entry.grid(row=2, column=1)

tk.Label(root, text="Risk-free Interest Rate (r)(enter as decimal percentage):").grid(row=3, column=0) # input risk free interest rate
interest_rate_entry = tk.Entry(root)
interest_rate_entry.grid(row=3, column=1)

tk.Label(root, text="Volatility (sigma)(enter as decimal percentage):").grid(row=4, column=0) #input the volatility (sigma value) annualized standard deviation of the return on the asset
volatility_entry = tk.Entry(root)
volatility_entry.grid(row=4, column=1)

option_type_var = tk.StringVar(value='call') #getting option type
tk.Label(root, text="Option Type:").grid(row=5, column=0)
tk.Radiobutton(root, text="Call", variable=option_type_var, value='call').grid(row=5, column=1)
tk.Radiobutton(root, text="Put", variable=option_type_var, value='put').grid(row=5, column=2)

tk.Button(root, text="Calculate", command=getval).grid(row=6, columnspan=3) #option to generate value, from where  
tk.Button(root, text="Generate Heatmap", command=heatmap).grid(row=7, columnspan=3) #option to generate heat map

lbl = Label(root, text = "By Krishna Lal Agarwal")
lbl.grid()

root.mainloop() # for the gui
