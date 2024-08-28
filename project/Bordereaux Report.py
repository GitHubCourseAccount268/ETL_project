#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[6]:


Bordereaux_Report = pd.read_excel('Bordereaux example.xlsx', header=5)


# In[7]:


Bordereaux_Report.head()


# In[8]:


Bordereaux_Report.shape


# In[9]:


Master_Bordereaux = Bordereaux_Report.copy()


# In[12]:


Master_Bordereaux.shape


# In[11]:


columns_to_keep = [
'Group Name',
'Treaty Year',
'Spec Deductible',
'Contract Months',
'Total Lives YTD',
'YTD Total Gross Premium',
'Total Expense %',
'Total MGU Fee',
'Total Carrier Fee',
'Total Taxes',
'Total YTD Expenses',
'YTD Total Net Premium',
'YTD Gross Retained Premium',
'Retained MGU fee',
'Retained Carrier Fee',
'Retained Taxes',
'YTD Net Retained Premium ',
'YTD Gross Captive Premim',
'Captive MGU Fee',
'Captive Carrier Fee',
'Captive Retained Taxes',
'YTD Captive Net Premium',
'Total Incurred Claims',
'Total IBNR',
'Total Case Reserves',
'Total Paid Claims',
'Retained Incurred Claims',
'Retained IBNR',
'Retained Case Reserves',
'Retained Paid Claims',
'Ceded Incurred Claims',
'Ceded IBNR',
'Ceded Case Reserves',
'Policy Number',
]


# In[13]:


Master_Bordereaux = Master_Bordereaux[columns_to_keep]


# In[14]:


Master_Bordereaux.shape


# In[15]:


columns_to_rename = {
'Group Name': 'Group Name',
'Treaty Year': 'Contract Year',
'Spec Deductible': 'Spec Level',
'Contract Months': 'Contract Months',
'Total Lives YTD': 'Total Lives',
'YTD Total Gross Premium': 'YTD Total Gross Premium',
'Total Expense %': 'Total Expense %',
'Total MGU Fee': 'Total MGU Fee',
'Total Carrier Fee': 'Total Carrier Fee',
'Total Taxes': 'Total Taxes',
'Total YTD Expenses': 'Total YTD Expenses',
'YTD Total Net Premium': 'YTD Total Net Premium',
'YTD Gross Retained Premium': 'YTD Gross Retained Premium',
'Retained MGU fee': 'Retained MGU fee',
'Retained Carrier Fee': 'Retained Carrier Fee',
'Retained Taxes': 'Retained Taxes',
'YTD Net Retained Premium ': 'YTD Net Retained Premium ',
'YTD Gross Captive Premim': 'YTD Gross Captive Premim',
'Captive MGU Fee': 'Captive MGU Fee',
'Captive Carrier Fee': 'Captive Carrier Fee',
'Captive Retained Taxes': 'Captive Retained Taxes',
'YTD Captive Net Premium': 'YTD Captive Net Premium',
'Total Incurred Claims': 'Total Incurred Claims',
'Total IBNR': 'Total IBNR',
'Total Case Reserves': 'Total Case Reserves',
'Total Paid Claims': 'Total Paid Claims',
'Retained Incurred Claims': 'Retained Incurred Claims',
'Retained IBNR': 'Retained IBNR',
'Retained Case Reserves': 'Retained Case Reserves',
'Retained Paid Claims': 'Retained Paid Claims',
'Ceded Incurred Claims': 'Ceded Incurred Claims',
'Ceded IBNR': 'Ceded IBNR',
'Ceded Case Reserves': 'Ceded Case Reserves',
'Policy Number': 'Policy Number',
}


# In[16]:


Master_Bordereaux.rename(columns=columns_to_rename, inplace=True)


# In[17]:


Master_Bordereaux.head()


# In[18]:


Master_Bordereaux["Contract Start"] = ""
Master_Bordereaux["Contract End"] = ""


# In[19]:


Master_Bordereaux["Ceding Commission (Fronting & Policy Administration)"] = Master_Bordereaux["Total MGU Fee"] + Master_Bordereaux["Total Carrier Fee"]


# In[20]:


Master_Bordereaux.head()


# In[21]:


Master_Bordereaux.to_csv("Master_Bordereaux.csv")


# In[ ]:




