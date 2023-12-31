
import csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns

df = pd.read_csv('classification_1_14_09.csv')
print(df)
df = df[~(df['sex'].isnull() | df['age'].isnull() | df['profession'].isnull() | df['income'].isnull())]
df = df.reset_index(drop=True)
print(df)

plt.boxplot(df['age'])
plt.title('Диаграмма Box-and-Whisker возраста')
plt.show()

sns.countplot(data=df, x='sex')
plt.xlabel('Пол')
plt.ylabel('Частота')
plt.title('Гистограмма частот вариантов')
plt.xticks(rotation=45)
plt.show()

sns.countplot(data=df, x='profession')
plt.xlabel('Профессия')
plt.ylabel('Частота')
plt.title('Гистограмма частот вариантов')
plt.xticks(rotation=45)
plt.show()

sns.countplot(data=df, x='income')
plt.xlabel('Доход')
plt.ylabel('Частота')
plt.title('Гистограмма частот вариантов')
plt.xticks(rotation=45)
plt.show()

mean_age = df['age'].mean()
print(f'Средний возраст: {mean_age}')

age_range = df['age'].max() - df['age'].min()
print(f'Размах возраста: {age_range}')

unique_ages = df['age'].nunique()
print(f'Число уникальных возрастов: {unique_ages}')

from sklearn.preprocessing import OneHotEncoder

df_oh = df

encoder_sex = OneHotEncoder(drop='first')
X = df_oh['sex'].values.reshape(-1, 1)
encoded_data = encoder_sex.fit_transform(X).toarray()
encoded_df = pd.DataFrame(encoded_data, columns=encoder_sex.get_feature_names_out(['sex']))
df_oh = pd.concat([df_oh, encoded_df], axis=1)


encoder_profession = OneHotEncoder(drop='first', sparse=False)
encoded_data = encoder_profession.fit_transform(df_oh[['profession']])
encoded_df = pd.DataFrame(encoded_data, columns=encoder_profession.get_feature_names_out(['profession']))
df_oh = pd.concat([df_oh, encoded_df], axis=1)


encoder_income = OneHotEncoder(drop='first')
X = df_oh['income'].values.reshape(-1, 1)
encoded_data = encoder_income.fit_transform(X).toarray()
encoded_df = pd.DataFrame(encoded_data, columns=encoder_income.get_feature_names_out(['income']))
df_oh = pd.concat([df_oh, encoded_df], axis=1)

if 'sex_male' in df_oh.columns:
    df_oh = df_oh.drop(columns=['sex'])
if 'profession_unemployed' in df_oh.columns:
    df_oh = df_oh.drop(columns=['profession'])
if 'income_low' in df_oh.columns:
    df_oh = df_oh.drop(columns=['income'])

print(df_oh)

X = df_oh[['age', 'sex_male', 'profession_unemployed', 'profession_worker']]
Y = df_oh[['income_low']]

correlation_matrix = X.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Корреляционная матрица признаков')
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test = train_test_split(X, test_size=0.3)
Y_train, Y_test = train_test_split(Y, test_size=0.3)

model = LogisticRegression()
model.fit(X_train, Y_train)

Y_predicted = model.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score

Y_train_preticted = model.predict(X_train)
confusion_matrix_train = confusion_matrix(Y_train, Y_train_preticted)
confusion_matrix_test = confusion_matrix(Y_test, Y_predicted)

print(confusion_matrix_train)
print(confusion_matrix_test)

accuracy_train = accuracy_score(Y_train, Y_train_preticted)
accuracy_test = accuracy_score(Y_test, Y_predicted)

print(accuracy_train)
print(accuracy_test)

from sklearn.metrics import f1_score, classification_report

f1_train = f1_score(Y_train, Y_train_preticted)
f1_test = f1_score(Y_test, Y_predicted)

f1_micro_train = f1_score(Y_train, Y_train_preticted, average='micro')
f1_micro_test = f1_score(Y_test, Y_predicted, average='micro')

print("F1-мера для каждого класса на обучающей выборке:", f1_train)
print("F1-мера для каждого класса на тестовой выборке:", f1_test)
print("Микро-усредненная F1-мера на обучающей выборке:", f1_micro_train)
print("Микро-усредненная F1-мера на тестовой выборке:", f1_micro_test)
