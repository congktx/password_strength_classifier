import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv('./data/processed_data.csv')

    # sns.relplot(x=df.lowers, y=df.length, hue=df.strength, palette='viridis', alpha=0.5)
    # plt.show()

    # sns.relplot(x=df.uppers, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.relplot(x=df.specials, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.relplot(x=df.entropy, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.relplot(x=df.continous, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.heatmap(df.corr() , annot = True, cmap='coolwarm')
    # plt.show()