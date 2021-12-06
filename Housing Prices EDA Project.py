#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data analysis

# In[5]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

pd.pandas.set_option('display.max_columns',None)


# In[7]:


dataset=pd.read_csv(r'D:\DATA\Housing Prices\train.csv')


# In[8]:


print(dataset.shape)


# In[5]:


dataset.head


# In[9]:


features_with_na=[features for features in dataset.columns if dataset[features].isnull().sum()>1]

for feature in features_with_na:
    print(feature, np.round(dataset[feature].isnull().mean(), 4),'% missing values')









# ### relation betweeen missing values
# 

# In[ ]:





# In[10]:



for feature in features_with_na:
    data= dataset.copy()
    data[feature]=np.where(data[feature].isnull(), 1, 0)

    data.groupby(feature)['SalePrice'].median().plot.bar()
    plt.title(feature)
    plt.show()


# In[19]:


print("number of variables are {}" .format(len(dataset.Id)))


# ## TO find Numerical variables

# In[22]:


numerical_features=[feature for feature in dataset.columns if dataset[feature].dtypes != 'O']
print('Number of numerical variables: ', len(numerical_values))


# In[23]:


dataset[numerical_features].head()


# In[14]:



year_feature=[feature for feature in numerical_features if 'Yr' in feature or 'Year' in feature]


# In[25]:


year_feature


# In[15]:


dataset.groupby('YrSold')['SalePrice'].median().plot()
plt.xlabel('Year Sold')
plt.ylabel('Median House Price')
plt.title('House price vs year sold')


# In[20]:


for feature in year_feature:
    if feature != 'YrSold': 
        data=dataset.copy()
        data[feature]=data['YrSold']-data[feature]
    
        plt.scatter(data[feature],data['SalePrice'])
        plt.xlabel(feature)
        plt.ylabel('SalePrice')
        plt.show()


# ### to find discrete variable

# In[24]:


discrete_feature=[feature for feature in numerical_features if len(dataset[feature].unique())<25 and feature not in year_feature+['Id']]
print('Discrete variable count is {}'.format(len(discrete_feature)))


# In[26]:


discrete_feature


# ### To find relation between discrete features

# In[31]:


for feature in discrete_feature:
    data=dataset.copy()
    data.groupby(feature)['SalePrice'].median().plot.bar()
    plt.xlabel(feature)
    plt.ylabel('SalePrice')
    plt.title(feature)
    plt.show()


# ### Continous variable

# In[38]:


continous_feature=[feature for feature in numerical_features if feature not in discrete_feature + year_feature+['Id']]
print('continous feature are {}'.format(len(continous_feature)))


# ### analyze continous variable 

# In[41]:


for feature in continous_feature:
    data=dataset.copy()
    data[feature].hist(bins=25)
    plt.xlabel(feature)
    plt.ylabel("Count")
    plt.title(feature)
    plt.show()


# ### using logrithmic transformation to make standard normal distributio

# In[45]:


for feature in continous_feature:
    data=dataset.copy()
    if 0 in data [feature].unique():
        pass
    else:
        data[feature]=np.log(data[feature])
        data["SalePrice"]=np.log(data['SalePrice'])
        plt.scatter(data[feature],data["SalePrice"])
        plt.xlabel(feature)
        plt.ylabel("SalePrice")
        plt.title(feature)
        plt.show()


# ## Outliers 

# ### we us boxplot to see outliers ( only for continous variables doesnt work for categorical variables)
# 

# In[47]:


for feature in continous_feature:
    data=dataset.copy()
    if 0 in data [feature].unique():
        pass
    else:
        data[feature]=np.log(data[feature])
        data.boxplot(column=feature)
        plt.ylabel(feature)
        plt.title(feature)
        plt.show()
        


# ## Categorical variables

# In[54]:


categorical_features=[feature for feature in dataset.columns if data[feature].dtypes=="O"]
print("The number of categorical features are {}".format(len(categorical_features)))


# In[55]:


dataset[categorical_features].head()


# In[57]:


for feature in categorical_features:
    print("The features is {} and the no of unique categories are {}".format(feature,len(dataset[feature].unique())   ))


# ### relationship between categorical features

# In[59]:


for features in categorical_features:
    data=dataset.copy()
    data.groupby(feature)["SalePrice"].median().plot.bar()
    plt.xlabel(feature)
    plt.ylabel("SalePrice")
    plt.title(feature)
    plt.show()


# ## Feature engineering
# 
# #### we will be performing the below steps
# 
# #### 1.find missing values
# #### 2. Temporal variables (date and time variable)
# #### 3. Categorical variables : remove rare labels
# #### 4. standarise the values of the variables to the same range(Feature Scaling)

# In[64]:


### to find null values in categorical features


feature_nan=[feature for feature in dataset.columns if dataset[feature].isnull().sum()>1 and dataset[feature].dtypes=="O"]

for feature in feature_nan:
    print("{} : {}% missing values".format(feature,np.round(dataset[feature].isnull().mean(),4)))


# In[65]:


## Replacing nan values

def replace_cat_feature(dataset,feature_nan):
    data=dataset.copy()
    data[feature_nan]=data[feature_nan].fillna('Missing')
    return data
dataset=replace_cat_feature(dataset,feature_nan)

dataset[feature_nan].isnull().sum()


# In[68]:


## to  find the nan  values in numerical variables



numerical_with_nan=[feature for feature in dataset.columns if dataset[feature].isnull().sum()>1 and dataset[feature].dtypes!="O"]

for feature in numerical_with_nan:
    print("{} : {}% are the numerical null values ".format(feature,dataset[feature].isnull().mean(),4))


# In[72]:


### replacing the numerical missing values

for feature in numerical_with_nan:
    
    ### to remove outliers we are using the median
    
    median_value=dataset[feature].median()
    
    ### creating the new feature to capture nan values and inserting the median value to the nan value
    
    dataset[feature+'_nan']=np.where(dataset[feature].isnull,1,0)
    dataset[feature].fillna(median_value,inplace=True)
    
dataset[numerical_with_nan].isnull().sum()
    
    


# In[73]:


dataset.head()


# In[78]:


### to handle temoporal variables ( Date and time variables)

for feature in ["YearBuilt","YearRemodAdd","GarageYrBlt"]:
    dataset[feature]=dataset['YrSold']-dataset[feature]

dataset[["YearBuilt","YearRemodAdd","GarageYrBlt"]].head()


# ### Numerical variables
# since the numerical variables are skewed we will perform log normal distribution.

# In[79]:


dataset.head()


# In[80]:


num_features=['LotFrontage','LotArea','1stFlrSF','GrLivArea','SalePrice']
for feature in num_features:
    dataset[feature]=np.log(dataset[feature])
    
dataset.head()  


# In[87]:


for feature in num_features:
    data=dataset.copy()
    data[feature].hist(bins=25)
    plt.xlabel(feature)
    plt.ylabel("Count")
    plt.title(feature)
    plt.show()
    
### Now we can see that the data follows Normal Distribution/Gaussian Distribution.


# ### Handling the rare categorical feature
# we will remove categorical variables that are present less than 1% of the observations

# In[81]:


categorical_features=[feature for feature in dataset.columns if dataset[feature].dtypes=="O"]
categorical_features


# In[82]:


for feature in categorical_features:
    temp=dataset.groupby(feature)["SalePrice"].count()/len(dataset)
    temp_df=temp[temp>0.01].index
    dataset[feature]=np.where(dataset[feature].isin(temp_df),dataset[feature],"Rare_Var")


# In[85]:


dataset.head()


# 

# In[ ]:





# In[ ]:




