# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 13:56:13 2020

@author: mishk
"""
# Import the required modules
import streamlit as st
import plotly.graph_objs as go
import numpy as np
# import matplotlib.pyplot as plt
from scipy.integrate import odeint
#Initial values
P_init = st.number_input('Initial Population', value=1e6)
# P_init = 1e6 # 1million population

# E_init = 10000 # Exposed
E_init = st.number_input('Exposed', value=10000)

I_init=0 #initial infected
# I_init =  st.number_input('Initial infected', 0)

Is_init=0 # Initial isolated
# Is_init = st.number_input('Initial isolated',0)

C_init=0 # Initial cured
# C_init = st.number_input('Initial cured',0)

#Parameters
# beta = 1e-2 # Rate constant
beta = st.number_input('Rate Constant', 1e-2)

# tinc =  15 # 15 days incubation period
tinc =  st.number_input('Incubation period', 15)

# tinf = 15 # Patient is infectious for 15 days
tinf = st.number_input('Infection period patient', 15)

# tcure= 15 # Patient takes 15 days to recover
tcure = st.number_input('Recovery Time',15)
#P = [E I Is C]

def dP_dt(P, t):
    S =  P_init-P[0]-P[1]-P[2]-P[3]
    dE_dt= beta*P[1]*S/P_init-P[0]/tinc
    dI_dt = P[0]/tinc-P[1]/tinf-P[1]/(tinf+tcure)
    dIs_dt = P[1]/tinf-P[2]/tcure
    dC_dt = P[2]/tcure+P[1]/(tinf+tcure)
    return [dE_dt,dI_dt, dIs_dt,dC_dt ]

ts = np.linspace(0, 500, 1000)
P0 = [E_init, I_init, Is_init, C_init]
Ps = odeint(dP_dt, P0, ts)

exposed = Ps[:,0]
infect = Ps[:,1]
isol =  Ps[:,2]
cur =  Ps[:,3]

# """ plt.plot(ts, exposed, "+", label="Exposed")
# plt.plot(ts, infect, "x", label="Infected")
# plt.plot(ts, isol, "x", label="Isolated")
# plt.plot(ts, cur, "x", label="Cured")
# plt.xlabel("Time")
# plt.ylabel("Population")
# plt.legend()
# plt.show() """

st.title("SEIRD plot")

st.header("COVID Seird")

trace0 = go.Scatter(
    x=ts, 
    y =exposed, 
    name="Exposed",
    marker=dict(
        color='rgb(34,163,192)'
               ))# ,symbol="+", labels="Exposed"
trace1 = go.Scatter(
    x= ts, 
    y =infect, 
    name="Infected",
    marker=dict(
        color='rgb(100,0,0)'
               ))# , symbol="x", labels="Infected" 

trace2 = go.Scatter(
    x= ts, 
    y =isol, 
    name="Isolated",
    marker=dict(
        color='rgb(100,100,0)'
               ))# , symbol="x", labels="Infected" 
trace3 = go.Scatter(
    x= ts, 
    y =cur, 
    name="Cured",
    marker=dict(
        color='rgb(100,100,100)'
               ))# , symbol="x", labels="Infected" 

data = [trace0, trace1,trace2, trace3] #
layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
fig = go.Figure(data=data, layout=layout)
st.write(fig)

# # Bokeh plots
# from bokeh.plotting import figure, output_file, show
# from bokeh.io import output_notebook
# output to static HTML file
# output_file("lines.html")
#output_notebook()

S = P_init-exposed - infect - isol - cur

# create a new plot with a title and axis labels
# p = figure(title="Population", x_axis_label='Time (days)', y_axis_label='Population')

# p.circle(ts, S, line_width=2)
# show the results
# show(p)
trace1 = go.Scatter(x=ts, y=S, line_width=2)
data = [trace1]
layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
fig = go.Figure(data=data, layout=layout)

st.write(fig)
