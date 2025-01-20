import pandas as pd

final_results = []

for test_num in range(1, 6):
    max_values = []

    for run_num in range(1, 4):
        file_path = f"test_{test_num}/run_{run_num}/logs.csv"
        
        try:
            df = pd.read_csv(file_path)
            df["mean_episode_return"] = df["mean_episode_return"] * 100
            max_row = df.loc[df["mean_episode_return"].idxmax()]
            max_values.append(max_row[["mean_episode_return", "mean_episode_step"]])
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except KeyError as e:
            print(f"Missing column in {file_path}: {e}")

    if max_values:
        max_df = pd.DataFrame(max_values)
        final_results.append({
            "test": test_num,
            "mean(mean_episode_return)": max_df["mean_episode_return"].mean(),
            "var(mean_episode_return)": max_df["mean_episode_return"].std(),
            "mean(mean_episode_step)": max_df["mean_episode_step"].mean(),
            "var(mean_episode_step)": max_df["mean_episode_step"].std(),
        })

final_results_df = pd.DataFrame(final_results)

print(final_results_df)

# final_results_df.to_csv("final_test_results.csv", index=False)
