import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

CRITICAL_ERROR_THRESHOLD = 5
MIN_EFFICIENCY = 70.0
MAINTENANCE_HOURS = 500


class Machine:
    def __init__(self, _machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed):
        self._machine_id = _machine_id
        self._type = _type
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
    def __init__(self, _machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed):
        super().__init__(_machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed)
        self._speed_target = 60
        self._noise = self.calc_noise()
        self._speed = self.calc_speed()
        self._efficiency = self.calc_efficiency()

    def calc_noise(self):
        _noise = self._rng.uniform(-2.0, 2.0)
        return _noise

    def calc_speed(self):
        speed = min(self._units_produced / (self._hours_run * self._speed_target), 1.0)
        return speed

    def calc_efficiency(self):
        efficiency = (0.7 * self._quality + 0.3 * self._speed) * 100 + self._noise
        return efficiency


class AssemblyMachine(Machine):
    def __init__(self, _machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed):
        super().__init__(_machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed)
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
    def __init__(self, _machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed):
        super().__init__(_machine_id, _type, _hours_run, _units_produced, _units_rejected, _error_count, seed )
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
    print(CuttingMachine(_machine_id="turtle", _type="cut", _hours_run=1, _units_produced=1, _units_rejected=1, _error_count=1, seed=1).__dict__)


def main():

    while True:
        factory_name = input("Enter factory name: ")
        if not factory_name:
            print("Error: input cannot be empty.")
            continue
        else:
            break

    while True:
        log_file_name = input("Enter log file name (e.g., factory_log.txt): ")
        if not log_file_name:
            print("Error: input cannot be empty.")
            continue
        else:
            log_data = read_log_file(log_file_name, factory_name)

            if log_data is None:
                continue
            else:
                break


def read_log_file(log_file_name, factory_name):
    machines = []
    try:
        with open(log_file_name) as f:

            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',')

                if len(parts) != 7:
                    continue

                try:
                    m_id = parts[0].strip()
                    m_type = parts[1].strip().lower()
                    hours_run = float(parts[2].strip())
                    units_produced = int(parts[3].strip())
                    units_rejected = int(parts[4].strip())
                    error_count = int(parts[5].strip())
                    seed = int(parts[6].strip())

                except ValueError:
                    continue

                if m_type == 'cutting':
                    machine = CuttingMachine(m_id, hours_run, units_produced, units_rejected, error_count, seed)
                elif m_type == 'assembly':
                    machine = AssemblyMachine(m_id, hours_run, units_produced, units_rejected, error_count, seed)
                elif m_type == 'quality':
                    machine = QualityChecker(m_id, hours_run, units_produced, units_rejected, error_count, seed)
                else:
                    continue

                machines.append(machine)

            print(f"{factory_name} loaded successfully.")
            print(machines)
            return machines

    except FileNotFoundError:
        print(f"Error: Cannot find '{log_file_name}'. Please check the spelling and try again.")
        return None


main()

