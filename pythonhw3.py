import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
CRITICAL_ERROR_THRESHOLD = 5
MIN_EFFICIENCY = 70.0
MAINTENANCE_HOURS = 500

class Machine:
    def __init__(self, machine_id , type , hours_run , units_produced , units_rejected , error_count , seed):
        self.machine_id = machine_id
        self.type =type
        self.hours_run = hours_run
        self.units_produced = units_produced
        self.units_rejected = units_rejected
        self.error_count = error_count
        self.seed = seed #to put in spec class
