#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import numpy as np

# In[2]:

df = pd.read_csv("glassdoor_jobs.csv")
df

# In[ 3]:
#*** TO DO****

############salary parsing####

#create a colunm called hourly in salary estimate to define per hour and not
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'Per Hour' in x  else 0)

#created a colunm called employer provided in salary est 1-employer provided = 1 else other wise
df['Employer Provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'Employer Provided Salary' in x else 0)

# remove -1 from salary estimate
df = df[df['Salary Estimate'] != '-1']

# remove glassdoor from salary estimate
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

# remove $ and k in salary estimate
minus_kd = salary.apply(lambda x: x.replace('$','').replace('K',''))

#remove per hour and employer provided
min_hr = minus_kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

#create colunm for min salary
df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))

#create colunm for max salary
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))

#create a colunm of av.salary
df['Average salary'] = (df.min_salary + df.max_salary)/2

######company name text only###### return CN if Rat z <0 else..
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3],axis = 1)

#####state field#########
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
#Number of jobs counts
df.job_state.value_counts()
df.columns

#job HeadQuaters = 1 else...
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0,axis=1)

#######age of company##########
df['age'] = df.Founded.apply(lambda x: x if x<1 else 2021-x)

######parsing of job description (python, etc)#####
#Python
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python.value_counts()

#r studio
df['R'] = df['Job Description'].apply(lambda x: 1 if 'R'  or 'studio'in x.lower() else 0)
df.R.value_counts()

#spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

#aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

df.columns

df_out = df.drop(['Unnamed: 0'],axis=1)

df_out.to_csv('salary_data_cleaned.csv',index = False)






































































