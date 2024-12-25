import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    features = pd.read_csv('./data/processed_data.csv')
    features = features.drop('password', axis=True)
    features = features[((9 <= features['length']) & (features['length'] <= 12))]

    categorical_features = [
        'length',
        'lowers',
        'uppers',
        'digits',
        'specials',
        'words',
    ]
    target_col = 'strength' 

    # Thiết lập kích thước lưới subplot
    num_features = len(categorical_features)
    fig, axes = plt.subplots(
        nrows=(num_features + 3) // 4,  # Số hàng
        ncols=4,                        # Số cột
        figsize=(12, 4 * ((num_features + 1) // 4)),  # Kích thước tổng thể
    )

    axes = axes.flatten()  # Chuyển axes thành 1D để dễ truy cập

    for i, feature in enumerate(categorical_features):
        # Bảng tần suất chéo với phần trăm
        crosstab = pd.crosstab(
            features[feature],
            features[target_col],
            normalize='index'  # Chuẩn hóa theo hàng
        ) * 100

        # Vẽ biểu đồ stacked bar
        crosstab.plot(
            kind='bar',
            stacked=True,
            ax=axes[i],  # Subplot tương ứng
            color=['pink', 'blue', 'red', 'green', 'brown']  # Màu tùy chỉnh
        )

        # Tùy chỉnh tiêu đề và nhãn
        axes[i].set_title(f'{feature} vs {target_col}', fontsize=10)
        axes[i].set_xlabel(f'{feature}')
        axes[i].set_ylabel('Percentage')
        axes[i].legend(title='Label', loc='upper left')
    # Ẩn các subplot thừa (nếu có)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

    # sns.relplot(x=df.lowers, y=df.length, hue=df.strength, palette='coolwarm', alpha=0.5)
    # plt.show()

    # sns.relplot(x=df.uppers, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.relplot(x=df.specials, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.relplot(x=df.entropy, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.relplot(x=df.continous, y=df.length, hue=df.strength, palette='coolwarm')
    # plt.show()

    # sns.heatmap(features.corr() , annot = True, cmap='coolwarm')
    # plt.show()