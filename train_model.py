import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.inspection import permutation_importance

if __name__ == "__main__":
    df = pd.read_csv('./data/processed_data.csv')
    X = df.drop(["strength","password","words"], axis=True)
    y = df['strength']
    X_train,X_test,y_train,y_test = train_test_split(X,y , test_size = 0.2, random_state=42)

    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    classifier = LogisticRegression(random_state=42)
    param_grid = {
        'C': [i/10 for i in range(20)],      
        'penalty': ['l1', 'l2', 'elasticnet'], 
        'solver': ['saga', 'lbfgs'],
        'class_weight':['balanced'],    
        'multi_class': ['ovr']
    }
    grid_search = GridSearchCV(
        estimator=classifier,        
        param_grid=param_grid,  
        scoring='f1_macro',     
        cv=3,                   
        verbose=1,              
        n_jobs=-1            
    )
    grid_search.fit(X_train, y_train)
    print("Best parameters:", grid_search.best_params_)
    print("Best score:", grid_search.best_score_)
    optimal = grid_search.best_params_

    model = LogisticRegression(
        penalty= optimal.get('penalty') , 
        C=optimal.get('C'), 
        solver=optimal.get('solver'),
        class_weight=optimal.get('class_weight'),
        multi_class=optimal.get('multi_class')
    )
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred, average='macro')
    print(f1)

    result = permutation_importance(model, X_test, y_test, scoring='f1_macro', random_state=42)

    # 5. In kết quả
    for i in result.importances_mean.argsort()[::-1]:
        print(f"Feature {i}: {result.importances_mean[i]:.3f} ± {result.importances_std[i]:.3f}")

    # plt.subplots(figsize = (15,5))

    # plt.subplot(1,2,1)
    # sns.boxplot(data = X_train)
    # plt.title("X_train before scaling")
    # plt.show()

    # plt.subplot(1,2,2)
    # sns.boxplot(data = X_train_scaled)
    # plt.title('X_train after scaling')
    # plt.show()