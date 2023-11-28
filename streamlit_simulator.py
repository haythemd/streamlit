import streamlit as st
import numpy as np
import pandas as pd
from datetime import time
import plotly.express as px

from app import Simulator



st.set_page_config(
    page_title="youree : Smart City",
    initial_sidebar_state="auto",
    layout = "wide"
)

#---------- App


with st.sidebar:
    col1, col2 = st.columns(2)
    col1.image('https://youreefleetweb.web.app/static/media/logo@2x.4aceb9046caa3b40e495.png' ,width=80)
    col2.title("Youree - Flexibility Simulation")
    
    st.write(":green[Parameters]")
    
    number_of_cars = st.number_input(label='Number of cars', value=50, step=2)
    col1, col2 = st.columns(2)
    with col1:
        capacity = st.number_input(label='Battery Capacity (Kwh)', value=75.0, step=0.5)
    with col2:
        charge_rate_station = st.number_input('Charging Power(Kw)',value=22,  step=5)
    charging_times = st.slider( "NoN - Charging hours :", value=(time(6, 00), time(19, 00)))
    soc_values = st.slider("SoC Levels (Start & End)", 0, 100, (20, 90))

    st.divider()
    
    charging_efficiency = st.number_input("Charging efficiency",value=90,  step=5)
    flexibiliyty_freq =  st.number_input('Flexibility Frequency (Hours/week)', value=3, step=1)
    flexibility_average_power_price = st.number_input('Flexibility Average Power Price (cts/Mwh)', value=250, step=10)
    provider_refund = st.number_input('Power Provider Compensation (cts/Mwh)', value=100, step=10)
    
    st.divider()
    col1, col2 = st.columns(2)
    on_peak_rate = col1.number_input('On-peak rate (cts/Kwh)', value=18, step=10)
    off_peak_rate = col2.number_input('Off-peak rate (cts/Kwh)', value=14, step=10)
    off_peak_period = st.slider( "On-peak Period :", value=(time(4, 00), time(22, 00)))

    #---- button
    #button = st.button("Simulate", use_container_width=True)

#---------- App

simulator = Simulator(
    number_evs=number_of_cars,
    battery_capacity=capacity,
    charge_rate_station=charge_rate_station,
    charging_hours_interval=charging_times,
    start_soc=soc_values[0],
    end_soc=soc_values[1],
    charging_efficiency=charging_efficiency,
    flexibiliyty_freq=flexibiliyty_freq,
    flexibility_average_power_price=flexibility_average_power_price,
    provider_refund=provider_refund,
    on_peak_rate=on_peak_rate,
    off_peak_rate=off_peak_rate,
    off_peak_period=off_peak_period
        )

#--- computings
simulator.get_energy_requested(add_efficiency=True)
simulator.get_charging_time()
simulator.get_smart_charging_savings()

simulator.get_flex_energy_reduced()
simulator.get_flex_saving()

#-----------

earnings_month_fleet = round(Simulator.at_fleet_scale(Simulator.week_to_month(simulator.global_flex_savings), cars_number=number_of_cars), 2)
energy_released_month_fleet = round(Simulator.at_fleet_scale(Simulator.week_to_month(simulator.energy_reduced_flex), cars_number=number_of_cars)/1000 , 2)
Net_Flexibility_Price_month_fleet = round(simulator.flexibility_average_power_price - simulator.provider_refund, 2)
Total_Weekly_Earnings = round(Simulator.at_fleet_scale(simulator.global_flex_savings, cars_number=number_of_cars), 2)
Total_Monthly_Flexibility_Earning_fleet = Simulator.week_to_month(Total_Weekly_Earnings)
youree_cashback_month_fleet = round(Simulator.at_fleet_scale(Simulator.week_to_month(simulator.flex_net_savings), cars_number=number_of_cars), 2)

Off_peak_Charging_Saving = simulator.on_peak_rate-simulator.off_peak_rate
total_weekly_savings_smart = round(  Simulator.at_fleet_scale(simulator.smart_charging_saving/100, cars_number=number_of_cars), 2)
total_monthly_savings_smart = round(Simulator.at_fleet_scale(Simulator.week_to_month(simulator.smart_charging_saving)/100, cars_number=number_of_cars), 2)


#------- DashBord
# Données

labels = ['Flexibility', 'Smart Charging']
values = [Total_Weekly_Earnings, total_weekly_savings_smart]
fig = px.pie(values=values, names=labels, title='Weekly Earning Overview', color_discrete_sequence=['blue', 'green'])
st.plotly_chart(fig)

#st.header('TOTAL : Flexibility & SmarCharging')
col1, col2, col3 = st.columns(3)
total_weekly_earnings_smart_flex = round(total_weekly_savings_smart + Total_Weekly_Earnings, 2)
total_monthy_earnings_smart_flex = total_weekly_earnings_smart_flex*4
col1.metric(label="Total Weekly Savings", value=f"{total_weekly_earnings_smart_flex} €")
col2.metric(label="Total Monthly Savings", value=f"{total_monthy_earnings_smart_flex} €")




st.divider()

st.header('Flexibility Earnings')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Energy Released", value=f"{energy_released_month_fleet} MWh")
    st.metric(label="Total Monthly Flexibility Earning", value=f"{Total_Monthly_Flexibility_Earning_fleet} €")
with col2:
    st.metric(label="Net Flexibility Price", value= f"{Net_Flexibility_Price_month_fleet} €/MWh")#----------------
    st.metric(label="Youree Cashback (per month)", value=f"{youree_cashback_month_fleet} €")
with col3:
    st.metric(label="Total Weekly Earnings", value=f"{Total_Weekly_Earnings} €")





st.divider() #----------- SMART CHARGING

st.header('Smart Charging Earnings')
st.caption('Additional savings can be made when flexibility events occur during on-peak periods ')

# add_smart_charging = st.checkbox('Include Smart charging Savaings')
# if add_smart_charging:
#     with st.expander("Variables"):
#         col1, col2 = st.columns(2)
#         with col1:
#             st.write('dsqfq')
#         with col2:
#             st.write('sfq')

st.metric(label="Earnings (per month)", value=f"{total_monthly_savings_smart} €")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Energy Released", value=f"{energy_released_month_fleet} MWh")
with col2:
    st.metric(label="Off-peak Charging Saving", value=f"{Off_peak_Charging_Saving} cts/kWh")
with col3:
    st.metric(label="Total Weekly Savings", value=f"{total_weekly_savings_smart} €")
#--------------------
