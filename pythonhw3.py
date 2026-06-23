import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
CRITICAL_ERROR_THRESHOLD = 5
MIN_EFFICIENCY = 70.0
MAINTENANCE_HOURS = 500
class Machine:
    def __init__(self, _machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed):
        self._machine_id = _machine_id
        self._type =_type
        self._hours_run = _hours_run
        self._units_produced = _units_produced
        self._units_rejected = _units_rejected
        self._error_count = _error_count
        self._rng = random.Random(seed) #to put in spec class
        self._quality = self.calc_quality()
    def calc_quality(self):
        quality = (self._units_produced - self._units_rejected) / self._units_produced
        return quality

class CuttingMachine(Machine):
    def __init__(self,_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed):
        super().__init__(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed)
        self._speed_target = 60
        self._noise = self.calc_noise()
        self._speed = self.calc_speed()
        self._efficiency = self.calc_efficiency()

    def calc_noise(self):
        _noise = self._rng.uniform(-2.0, 2.0)
        return _noise
    def calc_speed(self):
        speed = min(self._units_produced / (self._hours_run * self._speed_target),1.0)
        return speed

    def calc_efficiency(self):
        efficiency = (0.7 * self._quality + 0.3 * self._speed) * 100 + self._noise
        return efficiency

class AssemblyMachine(Machine):
    def __init__(self,_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed):
        super().__init__(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed)
        self._error_penalty = 3
        self._noise = self.calc__noise()
        self._efficiency = self.calc_efficiency()

    def calc__noise(self):
        _noise = self._rng.uniform(-1.5, 1.5)
        return _noise
    def calc_efficiency(self):
        efficiency = self._quality * 100 - self._error_count * self._error_penalty + self._noise
        return efficiency

class QualityChecker(Machine):
    def __init__(self,_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed):
        super().__init__(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed )
        self._error_penalty = 2
        self._scan_target = 80
        self._noise = self.calc_noise()
        self._throughput = self.calc_throughput()
        self._efficiency = self.calc_efficiency()

    def calc_noise(self):
        noise = self._rng.uniform(-1.0, 1.0)
        return noise

    def calc_throughput(self):
        throughput = min(self._units_produced / (self._hours_run * self._scan_target),1.0)
        return throughput

    def calc_efficiency(self):
        efficiency = self._throughput * 100 - self._error_count * self._error_penalty + self._noise
        return efficiency
class Factory:
    def __init__(self,file_path,name):
        self._machines = []
        self.name = name
        self._report = file_path
    def add_machine(self,_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed):
        if _type == "cutting":
            print("Found a cutting machine")
            self._machines.append(CuttingMachine(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed))
        if _type == "assembly":
            print("Found a assembly machine")
            self._machines.append(AssemblyMachine(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed))
        if _type == "quality":
            print("Found a quality machine")
            self._machines.append(QualityChecker(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed))
factory = Factory(file_path=0,name="Ariel's factory")
factory.add_machine(_machine_id=1,_type="cutting",_hours_run=1,_units_produced=3,_units_rejected=1,_error_count=0,seed=3)
factory.add_machine(_machine_id=2,_type="assembly",_hours_run=1,_units_produced=3,_units_rejected=1,_error_count=0,seed=3)
factory.add_machine(_machine_id=3 ,_type="quality",_hours_run=1,_units_produced=3,_units_rejected=1,_error_count=0,seed=3)
for i in factory._machines:
    print(i.__dict__)