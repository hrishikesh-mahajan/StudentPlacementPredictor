# %%
import pandas as pd

# %%
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score

# %%
data = pd.read_csv("cocubes_2024.csv")

# %%
data.head()

# %%
data.drop(["Name", "Branch"], axis=1, inplace=True)

# %%
data.head()

# %%
imputer = SimpleImputer(strategy="mean")
data_imputed = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

# %%
data_imputed.head()

# %%
X_df = data_imputed.drop("LPA", axis=1)
y = data_imputed["LPA"]

# %%
scaler = StandardScaler()
X_scaled_data = scaler.fit_transform(X_df)

# %%
weights = [0.1, 0.1, 0.3, 0.2, 0.15, 0.15]
X_scaled_data_weighted = X_scaled_data.copy()

# %%
for i in range(X_scaled_data.shape[1] - 1):
    X_scaled_data_weighted[:, i] *= weights[i]

# %%
X = X_scaled_data_weighted

# %%
# Training model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# %%
y_pred = lr_model.predict(X_test)

# %%
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# %%
print("Mean Squared Error:", mse)
print("R-squared:", r2)

# %%
print("Coefficients:", lr_model.coef_)
print("Intercept:", lr_model.intercept_)

# %%
feature_coefficients = lr_model.coef_

feature_impact = {
    feature: coefficient
    for feature, coefficient in zip(X_df.columns, feature_coefficients)
}

print("Impact of Features on LPA:")
for feature, impact in feature_impact.items():
    print(f"{feature}: {impact}")

# %%
import joblib

# %%
print()

print("Exporting the model and scaler to files")

# Save the trained model
model_path = "cocubes_model.pkl"
joblib.dump(lr_model, model_path)
print(f"Saved {model_path}")

# Save the scaler
scaler_path = "cocubes_scaler.pkl"
joblib.dump(scaler, scaler_path)
print(f"Saved {scaler_path}")

# %%
import sklearn
import matplotlib

print()

print("Library Verions:")
print("sklearn: \t", sklearn.__version__)
print("pandas: \t", pd.__version__)
print("joblib: \t", joblib.__version__)
print("matplotlib: \t", matplotlib.__version__)
