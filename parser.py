
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
                    hours = float(parts[2].strip())
                    produced = int(parts[3].strip())
                    rejected = int(parts[4].strip())
                    errors = int(parts[5].strip())
                    seed = int(parts[6].strip())

                except ValueError:
                    continue

            print(f"{factory_name} loaded successfully.")
            print(machines)
            return machines

    except FileNotFoundError:
        print(f"Error: Cannot find '{log_file_name}'. Please check the spelling and try again.")
        return None

main()

