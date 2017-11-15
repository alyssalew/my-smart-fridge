
# coding: utf-8

# In[1]:


from tinydb import TinyDB, Query
db = TinyDB('db.json')


# In[2]:


db.insert({'type': 'apple', 'count': 7})
db.insert({'type': 'peach', 'count': 3})
db.insert({'type': 'banana', 'count': 5})


# In[3]:


Fruit = Query()
db.search (Fruit.type == 'apple')


# In[4]:


db.update ({'count': 8}, Fruit.type == 'apple')


# In[5]:


db.all()


# In[6]:


db.insert_multiple ([{'type':'guava', 'count': 3}, {'type': 'mango', 'count': 6}, {'type':'pear', 'count': 10}])


# In[7]:


db.all()


# In[ ]:


#db.purge()

