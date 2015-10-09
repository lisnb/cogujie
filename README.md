# cogujie
a little demo to crawl the imgs of the mogujie given item id

##usage:

- set the path *$root* in the config.py, the path of this repository on your local machine is OK
- set loglevel, default is DEBUG, options are :INFO EXCEPTION ERROR etc.
- cd to the *root*, excute ```python console.py youritemid```


**cogujie** will create a directory named *youritemid* under *$root/mogujie.db*, *imgs* directory is used to store the imgs of this item, and an *info* is used to store the properties of this item.
