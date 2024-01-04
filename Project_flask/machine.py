import string
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Load the csv file
df = pd.read_csv("Language Detection.csv")

print(df.head())

df.info()

df["Language"].value_counts()

#Data Pre-Processing

for char in string.punctuation:
    print(char,end=" ")
translate_table = dict((ord(char),None) for char in string.punctuation)

language= df['Language'].value_counts().reset_index()
language


