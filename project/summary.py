#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np


# In[13]:


summary_given = pd.read_csv('Summary Example.csv', header=1)


# In[14]:


summary_given.head()


# In[15]:


master_summary = summary_given.copy()


# In[16]:


master_summary.head()


# In[18]:


columns_to_rename = {
'Employer Name': 'Group Name',
'Gross Premium': 'YTD Total Gross Premium',
'Ceding Commission (Premium & Excise Taxes)': 'Total Taxes',
'Captive Premium': 'YTD Gross Captive Premim',
'Net Captive Premium (Claims Fund)': 'YTD Captive Net Premium',
'Captive Claim Reserves': 'Total Case Reserves',
'State': 'State',
'Policy Number': 'Policy Number',
'Administrator': 'Administrator',
'Ceding Commission (Fronting & Policy Administration)': 'Ceding Commission (Fronting & Policy Administration)',
'Ceding Commission (Program Management)': 'Ceding Commission (Program Management)',
'Ceding Commission (Captive Expenses)': 'Ceding Commission (Captive Expenses)',
'Ceding Commission (Broker or Producer Commission)': 'Ceding Commission (Broker or Producer Commission)',
'Total Ceding Commission (Captive Expenses)': 'Total Ceding Commission (Captive Expenses)',
'Average of Captive  Percent of  Gross Premium': 'Average of Captive  Percent of  Gross Premium',
'Captive Reimbursed (Paid) Claims*': 'Captive Reimbursed (Paid) Claims*',
'Funds Withheld': 'Funds Withheld',
'Required Collateral': 'Required Collateral',
'Collateral Received': 'Collateral Received',
'Collateral BalanceOver/(Short)': 'Collateral BalanceOver/(Short)'

}


# In[19]:


master_summary.rename(columns=columns_to_rename, inplace=True)


# In[21]:


master_summary["Contract Start"] = ""
master_summary["Contract End"] = ""


# In[22]:


master_summary.head()


# In[23]:


master_summary.to_csv("master_summary.csv")


# In[ ]:




