import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.title('Iris')
df = pd.read_csv("iris.csv")

st.subheader('Scatter plot')
species = st.multiselect('Show iris per species?', df['species'].unique())
new_df = df[(df['species'].isin(species))]

st.subheader('Histogram')
feature = st.selectbox('Which feature?', df.columns[0:4])
new_df2 = df[(df['species'].isin(species))][feature]
fig2 = px.histogram(new_df, x=feature, color="species", marginal="rug")
st.plotly_chart(fig2)

st.subheader('Machine Learning - Decision Tree')
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
features= df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
labels = df['species'].values
X_train,X_test, y_train, y_test = train_test_split(features, labels, train_size=0.7, random_state=1)
dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
acc = dtc.score(X_test, y_test)
st.write('Accuracy: ', acc)
pred_dtc = dtc.predict(X_test)
cm_dtc=confusion_matrix(y_test,pred_dtc)
st.write('Confusion matrix: ', cm_dtc)

