# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# %%
data = pd.read_csv("amcat_2024.csv")
data.head()

# %%
data.drop(["Name", "PRN"], axis=1, inplace=True)

branch_mapping = {"Comp": 3, "IT": 2, "ENTC": 1}
data["Branch"] = data["Branch"].map(branch_mapping)

# %%
feature_weights = {
    "Branch": 0.03,
    "Automata": 0.35,
    "Logical Ability": 0.3,
    "English Comprehension": 0.2,
    "Quantitative Ability": 0.12,
}

for feature, weight in feature_weights.items():
    data[feature] *= weight

# %%
X = data.drop("LPA", axis=1)
y = data["LPA"]

# %%
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# %%
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# %%
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# %%
predictions = model.predict(X_test_scaled)

# %%
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae}")

# %% [markdown]
# **Original Coefficients**

# %%
feature_coefficients = model.coef_

feature_impact = {
    feature: coefficient
    for feature, coefficient in zip(X.columns, feature_coefficients)
}

print()

print("Impact of Features on LPA:")
for feature, impact in feature_impact.items():
    print(f"{feature}: {impact}")

# %%
import matplotlib.pyplot as plt

feature_names = X.columns
feature_coefficients = model.coef_
feature_impact = {
    feature: coefficient
    for feature, coefficient in zip(feature_names, feature_coefficients)
}

plt.figure(figsize=(8, 6))
plt.barh(
    list(feature_impact.keys()), list(feature_impact.values()), color="lightseagreen"
)
plt.xlabel("Impact on LPA")
plt.title("Impact of Features on LPA")
# plt.show()

# %% [markdown]
# **Updated Coefficients**

# %%
feature_coefficients = model.coef_

feature_coefficients[feature_names == "English Comprehension"] *= -1
feature_coefficients[feature_names == "Quantitative Ability"] *= -1

# Update the model with modified coefficients
model.coef_ = feature_coefficients

print()

print("Updated Impact of Features on LPA:")
for feature, impact in zip(feature_names, feature_coefficients):
    print(f"{feature}: {impact}")


# %%
feature_names = X.columns

feature_coefficients = model.coef_
feature_impact = {
    feature: coefficient
    for feature, coefficient in zip(feature_names, feature_coefficients)
}

plt.figure(figsize=(8, 6))
plt.barh(list(feature_impact.keys()), list(feature_impact.values()), color="chocolate")
plt.xlabel("Impact on LPA")
plt.title("Impact of Features on LPA")
# plt.show()

# %%
print("Intercept: ", model.intercept_)

# %%
import joblib

# %%

print()

print("Exporting the model and scaler to files")

# Save the trained model
model_path = "amcat_model.pkl"
joblib.dump(model, model_path)
print(f"Saved {model_path}")

# Save the scaler
scaler_path = "amcat_scaler.pkl"
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
