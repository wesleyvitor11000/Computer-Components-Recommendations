import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heat_maps(df):
    plt.figure(figsize=(18, 12))

    # Heatmap para score_beta e threshold_iterations
    plt.subplot(2, 2, 1)
    heatmap_data = df.pivot_table(index="threshold_factor", columns="max_components_to_swap", values="result", aggfunc="max")
    sns.heatmap(heatmap_data, annot=True, cmap=sns.light_palette("seagreen", as_cmap=True))
    plt.title("Threshold factor x components_to_swap")

    # Heatmap para score_beta e threshold_factor
    plt.subplot(2, 2, 2)
    heatmap_data = df.pivot_table(index="score_beta", columns="random_parents", values="result", aggfunc="max")
    sns.heatmap(heatmap_data, annot=True, cmap=sns.light_palette("seagreen", as_cmap=True))
    plt.title("Score Beta x random parents")

    # Heatmap para score_beta e max_components_to_swap
    plt.subplot(2, 2, 3)
    heatmap_data = df.pivot_table(index="score_beta", columns="threshold_factor", values="result", aggfunc="max")
    sns.heatmap(heatmap_data, annot=True, cmap=sns.light_palette("seagreen", as_cmap=True))
    plt.title("Score Beta x threshold factor")

    # Heatmap para threshold_iterations e threshold_factor
    plt.subplot(2, 2, 4)
    heatmap_data = df.pivot_table(index="threshold_factor", columns="threshold_iterations", values="result", aggfunc="max")
    sns.heatmap(heatmap_data, annot=True, cmap=sns.light_palette("seagreen", as_cmap=True))
    plt.title("Threshold Iterations and Threshold Factor")

    plt.tight_layout()
    plt.savefig("heatmap.png")
    plt.show()


# df = pd.read_csv("generations_test_1.csv")[:1000]
# plt.plot(df["generation"], df["time"], label="execução 1")

# df = pd.read_csv("generations_test_2.csv")[:1000]
# plt.plot(df["generation"], df["time"], label="execução 2")

# df = pd.read_csv("generations_test_3.csv")[:1000]
# plt.plot(df["generation"], df["time"], label="execução 3")

# plt.xlabel("geração")
# plt.ylabel("tempo")
# # plt.xticks(df["individuals_per_graph"][::2])
# plt.title(f'geração x tempo (segundos)')
# plt.legend()
# plt.savefig("gerações x tempo.png")
# plt.show()

df = pd.read_csv("generated_solutions_f.csv", index_col=0)
df2 = pd.read_csv("generated_solutions.csv", index_col=0)

result = pd.concat([df, df2])
result.to_csv("generated_solutions_f2.csv")