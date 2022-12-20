#!/usr/bin/env python
# coding: utf-8

# # Research on the reliability of borrowers

# This research try to resolve a question: does the civil status and the number of children affect when returning a credit? To answer this question to answer this question we have customer data from a bank.
# 
# The results of the study will be taken into account when building a credit scoring model, a special system that evaluates the ability of a potential borrower to repay a loan to a bank.

# In[1]:


# importing the library

import pandas as pd


# In[2]:


# reading the file

data = pd.read_csv(r'C:\Users\pinos\Downloads\data.csv')


# # Data Overview

# In[3]:


# first look to the data

display(data.head())


# In[4]:


# taking a look at the data types

data.info()


# # Data preprocessing

# In[5]:


# counting the missing data

data.isna().mean()


# There are missing values in two columns. One of them is days_employed. I will process the omissions in this column in the next step. Another column with missing values is total_income that stores income data. The amount of income is most affected by the type of employment, so I need to fill in the gaps in this column with the median value for each type from the income_type column. For example, for a person with the employee employment type, the pass in the total_income column should be filled with the median income among all records with the same type

# In[6]:


data['total_income'] = data[
    
    'total_income'

].fillna(data.groupby([
    
    'income_type'])['total_income'].transform('median'))


# In[7]:


data['total_income']


# # Abnormal values processing

# There may be anomalies in the data — values that do not reflect reality and appeared by some mistake. Such an anomalie will be the negative number of days of work experience in the days_employed column. For real data, this is normal. I process the values in this column and replace all negative values with positive ones using the abs() method.

# In[8]:


data['days_employed'] = data['days_employed'].abs()


# In[9]:


data['days_employed']


# For each type of employment, I am going to output the median value of the days_employed length of service in days.

# In[10]:


data.groupby('income_type')['days_employed'].median()


# Two types (unemployed and pensioners) will have abnormally large values. It is difficult to correct such values, so I leave them as they are. Moreover, I will not need this column for my research.

# I output a list of unique values of the children column.

# In[11]:


data['children'].unique()


# There are two abnormal values in the children column. I am going to delete the rows in which this abnormal values occur from the dataframe.

# In[12]:


data = data.drop(data[(data['children']==-1) | (data['children']==20)].index)


# In[13]:


data['children'].unique()


# I am going to fill in the gaps in the days_employed column with median values for each income_type employment type.

# In[14]:


data['days_employed'] = data[
    
    'days_employed'

].fillna(data.groupby([
    
    'income_type'])[
    
    'days_employed'].transform('median'))


# In[15]:


data['days_employed']


# I make sure that all the gaps are filled in, and check, and print the number of missing values for each column again using two methods.

# In[16]:


data.isna().mean()


# I replace the real data type in the total_income column with an integer using the astype() method.

# In[17]:


data['total_income']=data['total_income'].astype('int')


# In[18]:


data.info()


# I handle implicit duplicates in the education column. In this column there are the same values, but written in different ways: using uppercase and lowercase letters.  I want them to be lowercase, and I check the other columns.

# In[19]:


data['education'] = data['education'].str.lower()


# In[20]:


data['education']


# I display the number of duplicate rows in the data, and If such lines are present, I would like to delete them. 

# In[21]:


data.duplicated().sum()


# In[22]:


data.drop_duplicates()


# # Categorization of data

# Based on the ranges specified below, I will create a total_income_category column with categories in the dataframe:
# 
# ·0–30000 — 'E'
# 
# ·30001–50000 — 'D'
# 
# ·50001–200000 — 'C'
# 
# ·200001–1000000 — 'B'
# 
# ·1000001 and more — 'A'
# 
# For example, a borrower with an income of 25,000 needs to be assigned a category 'E', and a client receiving 235,000 needs to be assigned a category 'B'. I use my own function named categorize_income() and the apply() method.

# In[23]:


income = data['total_income']

def categorize_income(total_income):
    
    if total_income <= 30000:
        
        return 'E'
    
    elif total_income <= 50000:
        
        return 'D'
    
    elif total_income <= 200000:
        
        return 'C'
    
    elif total_income <= 1000000:
        
        return 'B'
    
    else:
        
        return 'A'


# In[24]:


data['total_income_category'] = income.apply(categorize_income)


# I display a list of the unique purposes of taking a loan from the purpose column.

# In[25]:


data['purpose'].unique()


# I create another function that, based on the data from the purpose column, will form a new purpose_category column, which will include the following categories:
# 
# · 'car operations', 'real estate transactions', 'conducting a wedding', 'getting an education'
# 
# I use my own function named categorize_purpose() and the apply() method.

# In[26]:


category = data['purpose']

def categorize_purpose(category):
    
    if 'авто' in category:
        
        return 'car operations'
    
    elif 'жиль' in category or 'недвиж' in category :
        
        return 'real estate transactions' 
    
    elif 'свадь' in category:
        
        return 'conducting a wedding'
    
    elif 'образ' in category:
        
        return 'getting an education'
    
    else:
        
        return 'no category' 


# In[27]:


data['purpose_category'] = category.apply(categorize_purpose)


# # First hypothesis

# Is there a relationship between the number of children and the repayment of the loan on time?

# In[28]:


# We have created a pivot table for clarity of analysis

children_debt = data.pivot_table(
    
    index=['children'], 
    columns='debt', 
    values='total_income', 
    aggfunc='count', 
    fill_value=0
    
) 


# In[29]:


children_debt


# In[30]:


# Conversion calculations

children_debt['% no_debt'] = children_debt[0] / (children_debt[0] + children_debt[1]) * 100


# In[31]:


children_debt.round(decimals=0)


# Conclusion: the data show that there is no relationship between debt and the number of children, but 10% of those who have debt have four children, which is 1% -2% higher than the rest of the categories.
# 
# Within the framework of the available data, it is impossible to conclude that families with children relative to families without them have any delays in loan repayments. The shares are too close, the sample will change a little and the values ​​may change in the other direction. That is, we can conclude that there is no arbitrarily significant difference between the groups.
# 
# But if we assume that any difference between groups is a reason for the "separation" of classes, then I would conclude that borrowers without children are more responsible than clients who have children. Apparently, the presence of a child imposes an additional financial burden (obligations) on the client, and clients either take their credit obligations less responsibly or are not able to pay their obligations on time.
# 
# Please note that for some groups of borrowers we do not have enough data. It is said that the sample is not balanced, the classes in the sample have different sizes.

# # Second hypothesis

# Is there a relationship between marital status and loan repayment on time?

# In[32]:


# We have created a pivot table for clarity of analysis

status_debt = data.pivot_table(
    
    index=['family_status'], 
    
    columns='debt', 
    
    values='total_income', 
    
    aggfunc='count', fill_value=0
    
)


# In[33]:


status_debt


# In[34]:


# Conversion calculations

status_debt['% no_debt'] = status_debt[0] / (status_debt[0] + status_debt[1]) * 100


# In[35]:


status_debt.round(decimals=0)


# Conclusion: data show that there is no relationship between debt and marital status, although 10% of those who have debt are not married, which is 1-3% higher than the rest of the categories.
# 
# The credit department should be wary of clients who are not or have not been married. According to the data, such clients are less responsible. It turns out that legalized relationships lead to a more responsible attitude to their obligations. Well, it seems to coincide with common sense - family people more scrupulously take care of their family peace and are responsible for it.

# # Third hypothesis

# Is there a relationship between income level and loan repayment on time?

# In[36]:


# We repeat the same operation again

income_debt = data.pivot_table(
    
    index=['total_income_category'], 
    
    columns='debt', 
    
    values='total_income', 
    
    aggfunc='count', 
    
    fill_value=0
    
)


# In[37]:


income_debt


# In[38]:


income_debt['% no_debt'] = income_debt[0] / (income_debt[0] + income_debt[1]) * 100


# In[39]:


income_debt.round(decimals=0)


# Conclusion: the data show that there is no relationship between the level of income and the repayment of the loan on time. The group with the minimum share of debtors - "D" (conversion 94%), the group with the maximum share of debtors - "E" (conversion 91%).
# 
# Based on common sense, it is logical to assume that most often the debtors are people with low incomes, for whom financial problems do not allow them to make payments on time. But looking at our results, the sample of borrowers, both with the lowest income and with the highest income, is extremely insufficient to form unambiguous conclusions. One might think that the E-category is the lowest paid, cannot properly manage money and "gets" into loans, but then it is not clear why the A-category also has a fairly high percentage of debt. In general, the conclusion for groups A and E is not obvious, there is not enough data.
# 
# If, however, we take only groups B, C and D for analysis, then according to the data obtained, we do not observe the relationship "those who receive more salary repay the loan better." In general, this is logical, since material wealth is not the only variable that affects quality of credit history.
# 
# However, 2174 gaps in the data of the "total_income" column cast doubt on our result. A pivot table (or grouping) with data on the relationship between income and loan repayment on time might have looked different if it were not for the missing data.

# # Fourth hypothesis

# In[40]:


purpose_debt = data.pivot_table(
    
    index=['purpose_category'], 
    
    columns='debt', 
    
    values='total_income', 
    
    aggfunc='count', 
    
    fill_value=0
    
)


# In[41]:


purpose_debt


# In[42]:


purpose_debt['% no_debt'] = purpose_debt[0] / (purpose_debt[0] + purpose_debt[1]) * 100


# In[43]:


purpose_debt.round(decimals=0)


# Conclusion: The data show that: the purpose of the loan does not affect the repayment of the loan on time. The group with the minimum share of debtors - real estate transactions (93% conversion), the group with the maximum share of debtors - car transactions (91% conversion).

# # General conclusion

# As part of the developed study, the task was to oppose the following working hypotheses:
# 
# 1. There is a relationship between the number of children and the timely repayment of the loan.
# 
# 2. There is a relationship between marital status and loan repayment.
# 
# 3. There is a relationship between income and loan repayment.
# 
# 4. There is a relationship between the purpose of the loan and its return.
# 
# In none of the above cases can we say that there is a relationship between the variables.
# 
# Let's summarize the results they show for each category analyzed with numbers.
# 
# 1. Number of children and loan repayment:
# 
# · In the group of the childless, the share of those whose debts are repaid on time is 92%.
# 
# · Category with one and two children the percentage reaches 91 percent, indicating that they are more late in payment.
# 
# · Among those who have 3 or more children, this figure is 92 and 90 percent, respectively. However, here we must pay attention to the fact that we do not have enough data to draw more reliable conclusions.
# 
# Overall, more research is needed to reach firmer conclusions.
# 
# 2. Marital status and loan repayment:
# 
# · The percentage of single people with debts is 10%, which is 1-3% more than in other groups. In this sense, we can say that this group of people is more likely to become debtors.
# 
# · The group of divorced and widowed people, on the contrary, pays the debts on time most of all - 93%. It is followed by the married categories with 91 and 92 percent who are less likely to be in debt.
# 
# 3. Income level and loan repayment:
# 
# · The percentage of debtors in categories B (50,001 to 200,000) and C (200,001 to 1,000,000) is 7 and 8 percent, respectively, which is low when other analyzed variables are taken into account. People with average income generally pay their debts on time.
# 
# A more accurate analysis of the relationship of these variables will require more data for categories A (from 1,000,001), D (from 30,001 to 50,000) and E (up to 30,000).
# 
# 4. Purpose of the loan and repayment of the loan:
# 
# · Those who use credit for real estate purposes account for 7% of debtors.
# 
# · Those who use the loan to hold a wedding, they account for 8% of debtors.
# 
# · Those who use credit to buy a car account for 9% of debtors, as well as those who use it for education.
# 
# There is a difference of 2% of debtors between points 1 and 3, which means that the group of those who apply for a loan to buy a car and receive a diploma is more risky for the company providing the loan.
# 
# As a conclusion, points two and four are what the loan company can use the most. In other cases, more data needs to be collected to make better recommendations.
