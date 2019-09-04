hostname = '10.216.204.79'
username = 'rmann'
password = 'rmann@123'
database = 'reporting'

hostname1 = '10.216.240.61'
username1 = 'rmann'
password1 = 'rmann@123'
database1 = 'monsterpie'

queries=[" SELECT count(distinct search_id) FROM monsterpie.rec_search_trends where entity_type='title' and terms is not null and date(created_at) between '2019-06-27' and '2019-07-26' ",
" SELECT count(distinct search_id) FROM monsterpie.rec_search_trends where entity_type='skills' and terms is not null and date(created_at) between '2019-06-27' and '2019-07-26' ",
" select count(distinct search_id) from monsterpie.rec_search_trends where location is not null and  date(created_at) between '2019-06-27' and '2019-07-26' ",
" select count(distinct search_id) from monsterpie.rec_search_trends where qualification is not null and  date(created_at) between '2019-06-27' and '2019-07-26' ",
" select count(distinct search_id) from monsterpie.rec_search_trends where (minexp is not null or maxexp is not null) and  date(created_at) between '2019-06-27' and '2019-07-26' ",
" select count(distinct search_id) from monsterpie.rec_search_trends where  date(created_at) between '2019-06-27' and '2019-07-26' " ]
# Simple routine to run a query on a database and print the results:
def doQuery( conn ,a,b,c) :


    cur = conn.cursor()
    cur.execute( "SELECT parameter,percentage_weightage,relative_weightage FROM parameter_searches_weightage" )
    for row in cur.fetchall():
        a.append(row[0]),b.append(row[1]),c.append(row[2])
def doquerylist( conn , queries,result):
    cur=conn.cursor()
    for x in queries:
        cur.execute(" %s " % x)
        result.append(cur.fetchall())


def doquery1( conn ):
    cur=conn.cursor()
    cur.execute("SELECT count(distinct search_id) FROM monsterpie.rec_search_trends where entity_type='title' and terms is not null and date(created_at) between '2019-06-27' and '2019-07-26' ")
    print(cur.fetchall())
    cur.execute(" SELECT count(distinct search_id) FROM monsterpie.rec_search_trends where entity_type='skills' and terms is not null and date(created_at) between '2019-06-27' and '2019-07-26' ")
    print(cur.fetchall())
    cur.execute(" select count(distinct search_id) from monsterpie.rec_search_trends where location is not null and  date(created_at) between '2019-06-27' and '2019-07-26' ")
    print(cur.fetchall())
    cur.execute(" select count(distinct search_id) from monsterpie.rec_search_trends where qualification is not null and  date(created_at) between '2019-06-27' and '2019-07-26' ")
    print(cur.fetchall())
    cur.execute(" select count(distinct search_id) from monsterpie.rec_search_trends where (minexp is not null or maxexp is not null) and  date(created_at) between '2019-06-27' and '2019-07-26' ")
    print(cur.fetchall())
    cur.execute(" select count(distinct search_id) from monsterpie.rec_search_trends where  date(created_at) between '2019-06-27' and '2019-07-26' ")
    print(cur.fetchall())


import pymysql

myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
myConnection1 = pymysql.connect( host=hostname1, user=username1, passwd=password1, db=database1 )
par=[]
pw=[]
rw=[]
#des,ski,loc,qua,exp,tot=[]
doQuery( myConnection ,par,pw,rw)
#doquery1(myConnection1)

result=[]
doquerylist(myConnection1, queries,result)

result = [i[0][0] for i in result]
pw = [float(i) for i in pw]
print(result)
print ("=====pw:",pw)
# [((461958,),), ((953656,),), ((836688,),), ((85050,),), ((820890,),), ((1091129,),)]
#doquery1(myConnection1,des,ski,loc,qua,exp,tot)
#print(des,ski,loc,qua,exp,tot)

#calculating percentage weightage  and comparing
j=0
counted_percentage_weightage=[]
for i in [0,4,2,3,1]:
 counted_percentage_weightage.append(round(result[i]/result[5],2))
 if counted_percentage_weightage[j]== pw[j]:
     print(str(par[j]) + str(pw[j]) + str(counted_percentage_weightage[j]) +"PASS")
 else:
     print(str(par[j]) + str(pw[j]) + str(counted_percentage_weightage[j]) +"FAIL")
 j +=1



myConnection.close()
myConnection1.close()

# print ("Using mysql.connector…")
# import mysql.connector
# myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database )
# doQuery( myConnection )
# myConnection.close()
