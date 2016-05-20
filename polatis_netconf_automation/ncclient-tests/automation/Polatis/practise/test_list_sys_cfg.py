

list1 = ['tera', 'tera2']

name2 = ['tera', 'tera2']

list_tera = []

lst2 = 'list_'+name2[0]
lst2 = list(lst2)
lst2[:] = []
for i in list1:
   
    lst2.append(i)


print lst2 
