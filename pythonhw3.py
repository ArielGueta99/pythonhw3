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
            factory.read_log_file()
            factory.check_for_Critical_machines(CRITICAL_ERROR_THRESHOLD)
            factory.generate_report()
            factory.plot_efficiency()

            if factory is None:
                continue
            else:
                break

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
    def __init__(self,log_file_name,name):
        self._machines = []
        self.name = name
        self.log_file_name = log_file_name
        self._cutting_machines_number = 0
        self._quality_machines_number = 0
        self._assembly_machines_number = 0

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

    def read_log_file(self):
        machines = []
        try:
            with open(self.log_file_name) as f:

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
                    self.add_machine(_machine_id=m_id, _type=m_type,_hours_run=hours_run, _units_produced=units_produced,
                                     _units_rejected=units_rejected, _error_count=error_count, seed=seed)
                print(f"\n{self.name} loaded successfully.")
                print(f"Machines loaded: {len(self._machines)} ({self._cutting_machines_number} cutting, "
                      f"{self._assembly_machines_number} assembly, {self._quality_machines_number} quality)")

        except FileNotFoundError:
            print(f"Error: Cannot find '{self.log_file_name}'. Please check the spelling and try again.")
            return None
    def check_for_Critical_machines(self,threshold):
        for machine in self._machines:
            if machine._error_count >= threshold:
                print(f"Warning: {machine._machine_id} has {machine._error_count} errors - CRITICAL STATUS")

    def generate_report(self):

        # Section C: Export to text file
        report_filename = "factory_report.txt"

        # Helper lists for categories
        cutting = [m for m in self._machines if m._type == "cutting"]
        assembly = [m for m in self._machines if m._type == "assembly"]
        quality = [m for m in self._machines if m._type == "quality"]

        # Statistics using NumPy
        efficiencies = np.array([m._efficiency for m in self._machines])
        avg_eff = np.mean(efficiencies)
        best_mach = self._machines[np.argmax(efficiencies)]
        worst_mach = self._machines[np.argmin(efficiencies)]

        total_produced = np.sum([m._units_produced for m in self._machines])
        total_rejected = np.sum([m._units_rejected for m in self._machines])
        overall_rejection = (total_rejected / total_produced) * 100 if total_produced > 0 else 0

        critical_machines = [m for m in self._machines if m._error_count >= CRITICAL_ERROR_THRESHOLD]
        maintenance_machines = [m for m in self._machines if m._hours_run >= MAINTENANCE_HOURS]

        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write(f"  FACTORY REPORT - {self.name}\n")
                f.write("=" * 60 + "\n" + "\n")

                # Print Categories
                categories = [("--- Cutting Machines ---", cutting), ("--- Assembly Machines ---", assembly),
                              ("--- Quality Checkers ---", quality)]

                for cat_name, machines in categories:
                    f.write(f"{cat_name}\n")
                    for m in machines:
                        status = ""
                        if m._error_count >= CRITICAL_ERROR_THRESHOLD:
                            status += "  !! CRITICAL"

                        # Exact formatting string as requested in the assignment tip
                        line = f"{m._machine_id:<8}| Hours: {m._hours_run:<5}| Produced: {m._units_produced:<5} | Rejected: {m._units_rejected:<4} | Errors: {m._error_count:<3}| Eff: {m._efficiency:.2f}%{status}\n"
                        f.write(line)
                    f.write("\n")

                # Summary Statistics
                f.write("=" * 60 + "\n")
                f.write(" SUMMARY STATISTICS  (numpy)\n")
                f.write("=" * 60 + "\n")
                f.write(f"Average efficiency  : {avg_eff:.2f}%\n")
                f.write(f"Highest efficiency  : {best_mach._machine_id} ({best_mach._efficiency:.2f}%)\n")
                f.write(f"Lowest efficiency   : {worst_mach._machine_id} ({worst_mach._efficiency:.2f}%)\n")
                f.write(f"Total units produced: {total_produced}\n")
                f.write(f"Total units rejected: {total_rejected}\n")
                f.write(f"Overall rejection % : {overall_rejection:.2f}%\n")
                f.write(f"Critical machines   : {len(critical_machines)}")
                if critical_machines:
                    f.write("  →  " +  ", ".join([m._machine_id for m in critical_machines]) + "\n")
                f.write(f"Maintenance due     : {len(maintenance_machines)} machines\n\n")

                # Rankings
                f.write("=" * 60 + "\n")
                f.write(" RANKING - best to worst efficiency\n")
                f.write("=" * 60 + "\n")

                # Sort machines by efficiency (descending)
                ranked_machines = sorted(self._machines, key=lambda x: x._efficiency, reverse=True)
                for i, m in enumerate(ranked_machines, 1):
                    critical_flag = "  !!" if m._error_count >= CRITICAL_ERROR_THRESHOLD else ""
                    f.write(f"{i}. {m._machine_id:<8} [{m._type}]  {m._efficiency:.2f}%{critical_flag}\n")

                f.write("=" * 60 + "\n")

            print("Report saved to: factory_report.txt")
        except Exception as e:
            print(f"Error saving report: {e}")

    def plot_efficiency(self):
        ids = [m._machine_id for m in self._machines]
        scores = [m._efficiency for m in self._machines]

        colors = ['green' if score >= MIN_EFFICIENCY else 'red' for score in scores]

        plt.figure(figsize=(10, 6))
        plt.bar(ids, scores, color=colors)

        plt.axhline(y=MIN_EFFICIENCY, color='red', linestyle='--', label=f'Min threshold ({MIN_EFFICIENCY}%)')

        plt.title(f"Machine Efficiency - {self.name}")
        plt.xlabel("Machine ID")
        plt.ylabel("Efficiency Score (%)")
        plt.legend()

        plt.savefig('efficiency_chart.png')
        plt.close()
        print("Efficiency chart saved to: efficiency_chart.png")
main()