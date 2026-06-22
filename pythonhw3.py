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
        self.rng = random.Random(seed) #to put in spec class
    def calc_quality(self):
        quality = (self.units_produced - self.units_rejected) / self.units_produced
        return quality

class CuttingMachine(Machine):
    def __init__(self):
        super().__init__()
        self.speed_target = 60
        self.noise = self.calc_noise()
        self.speed = self.calc_speed()
        self.efficiency = self.calc_efficiency()

    def calc_noise(self):
        noise = self.rng.uniform(-2.0, 2.0)
        return noise
    def calc_speed(self):
        speed = min(self.units_produced / (self.hours_run * self.speed_target),1.0)
        return speed

    def calc_efficiency(self):
        efficiency = (0.7 * self.quality + 0.3 * self.speed) * 100 + self.noise

class AssemblyMachine:
    def __init__(self):
        super().__init__()
        self.error_penalty = 3
        self.noise = self.calc_noise()
        self.efficiency = self.calc_efficiency()

    def calc_noise(self):
        noise = self.rng.uniform(-1.5, 1.5)
    def calc_efficiency(self):
        efficiency = self.quality * 100 - self.error_count * self.error_penalty + self.noise

class QualityChecker:
    def __init__(self):
        super().__init__()
        self.error_penalty = 2
        self.scan_target = 80
        self.noise = self.calc_noise()
        self.throughput = self.calc_throughput()
        self.efficiency = self.calc_efficiency()

    def calc_noise(self):
        noise = self.rng.uniform(-1.0, 1.0)
        return noise

    def calc_throughput(self):
        throughput = min(self.units_produced / (self.hours_run * self.scan_target),1.0)
        return throughput

    def calc_efficiency(self):
        efficiency = self.throughput * 100 - self.error_count * self.error_penalty + self.noise
        return efficiency