import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CRITICAL_ERROR_THRESHOLD = 5
MIN_EFFICIENCY = 70.0
MAINTENANCE_HOURS = 500


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
            factory = Factory(log_file_name, factory_name)
            success = factory.load_machines(log_file_name)

            if success:
                if len(factory.machines) > 0:
                    factory.check_for_critical_machines(CRITICAL_ERROR_THRESHOLD)
                    factory.generate_report()
                    factory.plot_efficiency()
                break

            else:
                continue


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

    # added properties so that the attributes are read-only and ensure proper encapsulation when the factory classes access this information
    @property
    def machine_id(self):
        return self._machine_id
    @property
    def type(self):
        return self._type
    @property
    def hours_run(self):
        return self._hours_run
    @property
    def units_produced(self):
        return self._units_produced
    @property
    def units_rejected(self):
        return self._units_rejected
    @property
    def error_count(self):
        return self._error_count
    @property
    def efficiency(self):
        return self._efficiency

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

    def __init__(self,log_file_name,name):
        self._machines = []
        self.name = name
        self.log_file_name = log_file_name
        self._cutting_machines_number = 0
        self._quality_machines_number = 0
        self._assembly_machines_number = 0
        self._load_warnings = []

    @property
    def machines(self):
        return self._machines


    def add_machine(self,_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed):
        if _type == "cutting":
            self._cutting_machines_number+=1
            self._machines.append(CuttingMachine(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed))
        elif _type == "assembly":
            self._assembly_machines_number += 1
            self._machines.append(AssemblyMachine(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed))
        elif _type == "quality":
            self._quality_machines_number += 1
            self._machines.append(QualityChecker(_machine_id , _type , _hours_run , _units_produced , _units_rejected , _error_count , seed))

    def load_machines(self, filename):

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')

                    if len(parts) != 7:
                        self._load_warnings.append(f"Warning: line {line_num} has wrong number of fields - skipped.")
                        continue

                    m_id = parts[0].strip()
                    m_type = parts[1].strip().lower()

                    if m_type not in ["cutting", "assembly", "quality"]:
                        self._load_warnings.append(f"Warning: unknown type '{m_type}' on line {line_num} - skipped.")
                        continue

                    try:
                        hours_run = float(parts[2].strip())
                        units_produced = int(parts[3].strip())
                        units_rejected = int(parts[4].strip())
                        error_count = int(parts[5].strip())
                        seed = int(parts[6].strip())

                        if units_rejected > units_produced:
                            self._load_warnings.append(f"Warning: units_rejected exceeds units_produced on line {line_num} - skipped.")
                            continue

                    except ValueError:
                        self._load_warnings.append(f"Warning: invalid values on line {line_num} - skipped.")
                        continue

                    self.add_machine(m_id, m_type, hours_run, units_produced, units_rejected, error_count, seed)

            if len(self._machines) == 0:
                print("Warning: no valid machines loaded.")

            print(f"\n{self.name} loaded successfully.")
            print(
                f"Machines loaded: {len(self._machines)} ({self._cutting_machines_number} cutting, {self._assembly_machines_number} assembly, {self._quality_machines_number} quality)")
            return True

        except FileNotFoundError:
            print(f"Error: Cannot find '{filename}'. Please check the spelling and try again.")
            return False



    def check_for_critical_machines(self,threshold):
        for machine in self._machines:
            if machine.error_count >= threshold:
                print(f"Warning: {machine.machine_id} has {machine.error_count} errors - CRITICAL STATUS")

    def generate_report(self):

        report_filename = "factory_report.txt"

        cutting = [m for m in self._machines if m.type == "cutting"]
        assembly = [m for m in self._machines if m.type == "assembly"]
        quality = [m for m in self._machines if m.type == "quality"]

        efficiencies = np.array([round(m.efficiency, 2) for m in self._machines])
        avg_eff = np.mean(efficiencies)
        best_mach = self._machines[np.argmax(efficiencies)]
        worst_mach = self._machines[np.argmin(efficiencies)]

        total_produced = np.sum([m.units_produced for m in self._machines])
        total_rejected = np.sum([m.units_rejected for m in self._machines])
        overall_rejection = (total_rejected / total_produced) * 100 if total_produced > 0 else 0

        critical_machines = [m for m in self._machines if m.error_count >= CRITICAL_ERROR_THRESHOLD]
        maintenance_machines = [m for m in self._machines if m.hours_run >= MAINTENANCE_HOURS]

        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write(f"  FACTORY REPORT - {self.name}\n")
                f.write("=" * 60 + "\n" + "\n")

                if self._load_warnings:
                    f.write("--- LOAD WARNINGS ---\n")
                    for warning in self._load_warnings:
                        f.write(warning + "\n")
                    f.write("=" * 60 + "\n\n")

                categories = [("--- Cutting Machines ---", cutting), ("--- Assembly Machines ---", assembly),
                              ("--- Quality Checkers ---", quality)]

                for cat_name, machines in categories:
                    if len(machines) > 0:
                        f.write(f"{cat_name}\n")
                        for m in machines:
                            status = ""
                            if m.error_count >= CRITICAL_ERROR_THRESHOLD:
                                status += "  !! CRITICAL"

                            line = f"{m.machine_id:<8}| Hours: {m.hours_run:<5}| Produced: {m.units_produced:<6}| Rejected: {m.units_rejected:<5}| Errors: {m.error_count:<3}| Eff: {m.efficiency:.2f}%{status}\n"
                            f.write(line)
                        f.write("\n")

                f.write("=" * 60 + "\n")
                f.write(" SUMMARY STATISTICS  (numpy)\n")
                f.write("=" * 60 + "\n")
                f.write(f"Average efficiency  : {avg_eff:.2f}%\n")
                f.write(f"Highest efficiency  : {best_mach.machine_id} ({best_mach.efficiency:.2f}%)\n")
                f.write(f"Lowest efficiency   : {worst_mach.machine_id} ({worst_mach.efficiency:.2f}%)\n")
                f.write(f"Total units produced: {total_produced}\n")
                f.write(f"Total units rejected: {total_rejected}\n")
                f.write(f"Overall rejection % : {overall_rejection:.2f}%\n")
                f.write(f"Critical machines   : {len(critical_machines)}")
                if critical_machines:
                    f.write("  →  " +  ", ".join([m.machine_id for m in critical_machines]))
                f.write(f"\nMaintenance due     : {len(maintenance_machines)} machines\n\n")

                f.write("=" * 60 + "\n")
                f.write(" RANKING - best to worst efficiency\n")
                f.write("=" * 60 + "\n")

                ranked_machines = sorted(self._machines, key=lambda x: x._efficiency, reverse=True)
                for i, m in enumerate(ranked_machines, 1):
                    critical_flag = "  !!" if m.error_count >= CRITICAL_ERROR_THRESHOLD else ""
                    f.write(f"{i}. {m.machine_id:<8} [{m.type}]  {m.efficiency:.2f}%{critical_flag}\n")

                f.write("=" * 60 + "\n")

            print("Report saved to: factory_report.txt")
        except Exception as e:
            print(f"Error saving report: {e}")

    def plot_efficiency(self):
        ids = [m.machine_id for m in self._machines]
        scores = [m.efficiency for m in self._machines]

        colors = ['green' if score >= MIN_EFFICIENCY else 'red' for score in scores]

        plt.figure(figsize=(10, 6))
        plt.bar(ids, scores, color=colors,edgecolor='black')

        plt.axhline(y=MIN_EFFICIENCY, color='red', linestyle='--', label=f'Min threshold ({MIN_EFFICIENCY}%)')

        plt.title(f"Machine Efficiency - {self.name}")
        plt.xlabel("Machine ID")
        plt.ylabel("Efficiency Score (%)")
        plt.legend()

        plt.savefig('efficiency_chart.png')
        plt.close()
        print("Efficiency chart saved to: efficiency_chart.png")
main()