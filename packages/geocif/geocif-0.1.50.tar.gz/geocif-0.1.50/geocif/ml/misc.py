import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from taipy.gui import Gui

# Load the dataset
file_path = r'D:\Users\ritvik\projects\GEOGLAM\Output\ml\analysis\July_05_2024\russian_federation\maize\cumulative_1\2010\X_train_1.csv'  # Update with the correct file path
df = pd.read_csv(file_path)
print(df.head())
# Define a function to create the plot
def plot_auc_ndvi(data):
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.lineplot(data=data, x="Harvest Year", y="AUC_NDVI Oct 7-Mar 25", hue="Region", marker="o", ax=ax)
    ax.set_title("Trends of AUC_NDVI by Region (Oct 7 - Mar 25)")
    ax.set_xlabel("Harvest Year")
    ax.set_ylabel("AUC_NDVI Oct 7 - Mar 25")
    ax.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()
    return fig

# Create the plot and save it
plot_fig = plot_auc_ndvi(df)

# Define the Taipy page with the plot
page = """
# Trends of AUC_NDVI by Region

<|{plot_fig}|chart|>
"""

# Create and run the GUI
gui = Gui(page)
gui.run()
