#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


Claims_Report = pd.read_excel('Claims Exampt.xlsx', header=5)


# In[4]:


Claims_Report.shape


# In[5]:


Master_Claims = Claims_Report.copy()


# In[7]:


Master_Claims.shape


# In[8]:


Master_Claims.head(2)


# In[13]:


Master_Claims.columns


# In[14]:


columns_to_keep = [
'Employer Name',
'Claimant Name',
'Incurred From',
'Incurred To',
'Paid From',
'Paid To',
'Administrator Paid',
'Allowable Charges',
'Specific Deductible Applied',
'Aggregating Specific Deductible Applied',
'Carrier Paid',
'Carrier Outstanding',
'Carrier Reserve',
'Payment Register Total',
'Paid \n(Over)/Short Validation',
'Carrier \nClaim Number',
'Captive Reimbursed',
'Captive Reserve',
'Close Period',
'Incurred Date',
'Payment Request Date',
'Paid Date',
'Claimant Name',
'Carrier Payment',
'Claim Type',
'Carrier Claim Number',
'Claimant Name',
'Paid Claims',
'Allowable Charges',
'Specific Deductible Applied',
'Aggregating Specific Deductible Applied',
'Reimbursed or Reimbursable',
'SIR (Self-Insured Retention)',

]


# In[15]:


Master_Claims = Master_Claims[columns_to_keep]


# In[16]:


Master_Claims.shape


# In[17]:


Master_Claims.head(2)


# In[18]:


columns_to_rename = {
'Employer Name': 'Group Name',
'Claimant Name': 'Claimant Name',
'Incurred From': 'Incurred From',
'Incurred To': 'Incurred To',
'Paid From': 'Paid From',
'Paid To': 'Paid To',
'Administrator Paid': 'Administrator Paid',
'Allowable Charges': 'Allowable Charges',
'Specific Deductible Applied': 'Specific Deductible Applied',
'Aggregating Specific Deductible Applied': 'Aggregating Specific Deductible Applied',
'Carrier Paid': 'Carrier Paid',
'Carrier Outstanding': 'Carrier Outstanding',
'Carrier Reserve': 'Carrier Reserve',
'Payment Register Total': 'Payment Register Total',
'Paid \n(Over)/Short Validation': 'Paid (Over)/Short Validation',
'Carrier \nClaim Number': 'Carrier Claim Number',
'Captive Reimbursed': 'Captive Reimbursed',
'Captive Reserve': 'Captive Reserve',
'Close Period': 'Close Period',
'Incurred Date': 'Incurred Date',
'Payment Request Date': 'Payment Request Date',
'Paid Date': 'Paid Date',
'Claimant Name': 'Claimant Name',
'Carrier Payment': 'Carrier Payment',
'Claim Type': 'Claim Type',
'Carrier Claim Number': 'Carrier Claim Number',
'Claimant Name': 'Claimant Name',
'Paid Claims': 'Paid Claims',
'Allowable Charges': 'Allowable Charges',
'Specific Deductible Applied': 'Specific Deductible Applied',
'Aggregating Specific Deductible Applied': 'Aggregating Specific Deductible Applied',
'Reimbursed or Reimbursable': 'Reimbursed or Reimbursable',
'SIR (Self-Insured Retention)': 'SIR (Self-Insured Retention)',


}


# In[19]:


Master_Claims.rename(columns=columns_to_rename, inplace=True)


# In[20]:


Master_Claims.head()


# In[21]:


Master_Claims.shape


# In[25]:


Master_Claims.to_csv("Master_Claims.csv")


# In[ ]:





# In[ ]:




