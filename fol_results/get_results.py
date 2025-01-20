import re
import numpy as np

# Funzione per estrarre i dati dal file
def parse_test_data(file_path):
    with open("results_prolog.txt", 'r') as file:
        content = file.read()
    
    # Dividi i dati per test
    tests = re.split(r"----- Test \d+ -----", content)[1:]  # Ignora il primo elemento vuoto
    
    results = []
    for test in tests:
        # Estrai i risultati delle 3 run
        runs = re.findall(
            r"After 100 episodes, mean return is ([\d.]+)\s+"
            r"and the total number of winning episodes is (\d+)\s+"
            r"the mean number of step per episode is ([\d.]+)\s+"
            r"the mean number of step per winning epidose is ([\d.]+)",
            test
        )
        
        # Converti i risultati in float
        runs_data = [list(map(float, run)) for run in runs]
        results.append(runs_data)
    
    return results

# Funzione per calcolare media e deviazione standard
def calculate_stats(data):
    stats = []
    for test in data:
        test_stats = {
            "mean_return": (np.mean([run[0] for run in test]), np.std([run[0] for run in test])),
            "winning_episodes": (np.mean([run[1] for run in test]), np.std([run[1] for run in test])),
            "mean_steps_per_episode": (np.mean([run[2] for run in test]), np.std([run[2] for run in test])),
            "mean_steps_per_winning_episode": (np.mean([run[3] for run in test]), np.std([run[3] for run in test])),
        }
        stats.append(test_stats)
    return stats

# Leggi i dati dal file
file_path = "test_data.txt"  # Modifica con il percorso corretto del file
test_data = parse_test_data(file_path)

# Calcola le statistiche
statistics = calculate_stats(test_data)

# Stampa i risultati
for i, stats in enumerate(statistics, 1):
    print(f"Test {i}:")
    for key, (mean, std) in stats.items():
        print(f"  {key}: Mean = {mean:.4f}, Std = {std:.4f}")
