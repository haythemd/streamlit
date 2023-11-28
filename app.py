import numpy as np
import pandas as pd
import datetime

class Simulator:
    
    def __init__(self,
        charging_hours_interval,
        off_peak_period, 
        
        number_evs:int,
        battery_capacity:float,
        charge_rate_station:float,
        #charging_hours_interval:tuple(datetime),
        start_soc:float,
        end_soc:float,
        charging_efficiency:float,
        flexibiliyty_freq:float,
        flexibility_average_power_price:float,
        provider_refund:float,
        
        #---- smart charging
        on_peak_rate:float,
        off_peak_rate:float,
        #off_peak_period:tuple(datetime) 
                                    ) -> None:
        self.number_evs = number_evs
        self.battery_capacity = battery_capacity
        self.charge_rate_station = charge_rate_station
        self.charging_hours_interval = charging_hours_interval #( debut, fin ) en datetime.time
        self.start_soc = start_soc
        self.end_soc = end_soc
        self.charging_efficiency = charging_efficiency
        self.flexibiliyty_freq = flexibiliyty_freq
        self.flexibility_average_power_price = flexibility_average_power_price
        self.provider_refund = provider_refund
        self.on_peak_rate = on_peak_rate
        self.off_peak_rate = off_peak_rate
        self.off_peak_period = off_peak_period
        
        
    
    def get_energy_requested(self, add_efficiency:bool=True):
        """ L'energie réelement soutirée pour atteindre le pourcentage requis. Cela inclus le perte d'éfficatié"""
        if add_efficiency:
            energy_req = (self.battery_capacity *(self.end_soc - self.start_soc)) / self.charging_efficiency
        else:
            energy_req = self.battery_capacity *(self.end_soc - self.start_soc)/100 
        self.energy_req = energy_req


    def get_charging_time(self):
        self.charging_time = self.energy_req / self.charge_rate_station


    def get_smart_charging_savings(self):
        """ renvoie le saving pour une voiture donné  """
        off_peak_cost = self.energy_req * self.off_peak_rate
        on_peak_cost = self.energy_req * self.on_peak_rate
        self.smart_charging_saving = on_peak_cost-off_peak_cost
    
    
    #--------- NEBEF
    
    def get_flex_energy_reduced(self):
        """ l'energie non consommée pour un evenement de flex donné sur un interval """
        # start_time , end_time = self.charging_hours_interval
        
        # # Convertir les heures en objets datetime pour le calcul
        # start_datetime = datetime.datetime.combine(datetime.date.today(), start_time)
        # end_datetime = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), end_time)

        # # Calculer la différence
        # duration = end_datetime - start_datetime

        # Obtenir la durée en heures
        self.energy_reduced_flex = self.charge_rate_station * self.flexibiliyty_freq


    def get_flex_saving(self):
        """ savings en euros par weeks pour un véhicule donné. 
        """
        #-- ce qu'on reçoit de nebef
        self.global_flex_savings = self.energy_reduced_flex*self.flexibility_average_power_price/1000
        #-- compensation à payer de notre poche
        self.flex_savings_compensation = self.energy_reduced_flex*self.provider_refund /1000
        #-- ce qu'on reçoit net pour youree
        self.flex_net_savings =  self.global_flex_savings - self.flex_savings_compensation
    
    
    @staticmethod
    def week_to_month(value):
        return value*4
    
    @staticmethod
    def at_fleet_scale(value, cars_number):
        return value*cars_number
    
    