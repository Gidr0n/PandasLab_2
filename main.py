
import pandas as pd
#1
headers = ["date", "ticker", "open", "high","low", "close", "volume"]
df = pd.read_csv("sp500hst.txt", sep=',',names=headers,  header=None)
print(df)
#2
df.iloc[:, 3:7].mean()
#3
pd.to_datetime(df['date'],format="%Y%m%d").dt.month.head()
#4
df.groupby('ticker')['open'].mean()
#5
headers = ["ticker","company", "percent"]
sp = pd.read_csv("sp_data2.csv", sep=";",names=headers)
pd.merge(df, sp, how='inner', left_on='ticker', right_on='ticker')
# Лабораторная работа №2
#1.1
recipes = pd.read_csv("recipes_sample.csv", sep=",", parse_dates=['submitted'])
reviews = pd.read_csv("reviews_sample.csv", sep=",", parse_dates=["date"])
print(reviews)
#1.2
print(f"recipes: {recipes.shape[0]} {len(recipes.columns)}", recipes.dtypes)
print(f"reviews: {reviews.shape[0]} {len(reviews.columns)}", reviews.dtypes)
#1.3
total = recipes.shape[0]
without_none = recipes.dropna().shape[0]
none_count = total - without_none
print(round(none_count*100/total,2))

total = reviews.shape[0]
without_none = reviews.dropna().shape[0]
none_count = total - without_none
print(round(none_count*100/total,2))

print(recipes.isnull().sum())
#1.4
for column in ("minutes","n_ingredients","n_steps"):
    print(f"{column} {round(recipes[column].mean(),2)}")

for column in ["rating"]:
    print(f"{column} {round(reviews[column].mean(),2)}")
#1.5
result = recipes["name"].sample(10)
print(type(result))
print(result)
#1.6
reviews.rename(columns={'Unnamed: 0': 'index'}, inplace=True)
reviews = reviews.set_index('index')
print(reviews)
#1.7
condition = (recipes['minutes'] <= 20) & (recipes['n_ingredients'] <= 5)
print(recipes.loc[condition])
# Работа с датами в pandas
#2.1
print(recipes.dtypes)
#2.2
before2010 = recipes['submitted'].dt.year <= 2010
print(recipes.loc[defore2010])
#3.1
recipes["description_length"] = recipes["description"].str.len()
print(recipes)
#3.2
recipes["name"] = recipes["name"].str.title()
print(recipes)
#3.3
recipes["name_word_count"] = recipes["name"].str.split().apply(len)
print(recipes)
# Группировки таблиц `pd.DataFrame`
#4.1
temp = recipes.groupby("contributor_id")["id"].count()
print(temp)
#4.2
temp = reviews.groupby("recipe_id")["rating"].mean()
reviews.loc[reviews["recipe_id"] == 55]
#4.3
temp = recipes.groupby(recipes["submitted"].dt.year)["name"].count()
print(temp)
# Объединение таблиц `pd.DataFrame`
#5.1
concat = pd.merge(recipes[["id","name"]], reviews[["user_id","rating","recipe_id"]], how='inner',left_on="id", right_on='recipe_id')
concat = concat.drop(labels="recipe_id",axis=1)
concat.index.name='index'
print(concat)
print(reviews.loc[int(reviews[reviews['review'].isna()].index[0])])
print(concat.loc[int(reviews[reviews['review'].isna()].index[0])])
#5.2
concated_df = recipes.merge(reviews, how='left', left_on="id", right_on="recipe_id").sort_values(by="user_id")
print(concated_df[concated_df['review'].isna() & concated_df['rating'].isna()]["id"])
temp_concated = recipes.merge(reviews['review'].groupby(reviews['recipe_id']).count(), how='left', left_on="id", right_on="recipe_id")[['id', 'name', 'review']]
temp_concated = temp_concated.rename(columns={'id': 'recipe_id', 'review': 'review_count'})
temp_concated = temp_concated.fillna(0)
print(temp_concated)
#5.3
print(reviews['rating'].groupby(pd.DatetimeIndex(reviews['date']).year).mean().sort_values())
# Сохранение таблиц `pd.DataFrame`
#6.1
recipes.sort_values(by=['name_word_count'])
recipes.to_csv("task_6.csv")
print(recipes)
#6.2
with pd.ExcelWriter(r"6.2.xlsx") as writer:
    concat.to_excel(writer, sheet_name="Рецепты с оценками")
    temp_concated.to_excel(writer, sheet_name="Количество отзывов по рецептам")