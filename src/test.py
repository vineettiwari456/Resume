# -*-coding:utf-8 -*-
import sys
import time
import datetime
import json

from base64 import b64decode
import mysql.connector
import os

def eagle_connection():
    # conf_eagle = {"user": "db", "password": "bazookadb", "host": "10.216.204.79", "database": "eagle"}
    conf_eagle = {"user": "vineet", "password": "vineet@123@", "host": "10.216.247.111", "database": "eagle"}
    connection_eagle = mysql.connector.connect(user=conf_eagle['user'], password=conf_eagle['password'],
                                               host=conf_eagle['host'],
                                               database=conf_eagle['database'])
    cursor_eagle = connection_eagle.cursor(dictionary=True)
    return connection_eagle, cursor_eagle

def get_key_value_format_mapping(total_data):
    # print(total_data)
    result = {}
    for da in total_data:
        da_list = list(da.values())
        result[str(da_list[1]).lower().strip()] = da_list[0]
    return result

def master_fetch_data_from_eagle_database():
    connection_master, cursor_master = eagle_connection()
    # query_master_job_location = 'select jll.name,jl.uuid from job_locations as jl inner join job_location_langs as jll on jl.id= jll.job_location_id;'
    # cursor_master.execute(query_master_job_location)
    # countries_locuuid_raw = cursor_master.fetchall()
    # job_locationuuid_name_master = get_key_value_format_mapping(countries_locuuid_raw)
    # query_master_searc_cmp = 'select scl.name,sc.uuid from search_companies as sc inner join search_company_langs as scl on sc.id= scl.search_company_id;'
    # cursor_master.execute(query_master_searc_cmp)
    # compsearch = cursor_master.fetchall()
    # search_cmpuuid_name_master = get_key_value_format_mapping(compsearch)
    # 
    # query_master_designatioon = 'select dll.name,dl.uuid from designations as dl inner join designation_langs as dll on dl.id= dll.designation_id;'
    # cursor_master.execute(query_master_designatioon)
    # designation_raw = cursor_master.fetchall()
    # designation_data_master = get_key_value_format_mapping(designation_raw)
    # 
    # query_master_skill = 'select skl.name,sk.uuid from skills as sk inner join skill_langs as skl on sk.id= skl.skill_id;'
    # cursor_master.execute(query_master_skill)
    # skill_raw = cursor_master.fetchall()
    # skill_data_master = get_key_value_format_mapping(skill_raw)
    # query_master_highest_qualifications = 'select hql.name,hq.uuid from highest_qualifications as hq inner join highest_qualification_langs as hql on hq.id= hql.highest_qualification_id;'
    # cursor_master.execute(query_master_highest_qualifications)
    # highest_qualifications_raw = cursor_master.fetchall()
    # highest_qualifications_master = get_key_value_format_mapping(highest_qualifications_raw)
    # query_master_qualification_specializations = 'select qsl.name,qs.uuid from qualification_specializations as qs inner join qualification_specialization_langs as qsl on qs.id= qsl.qualification_specialization_id;'
    # cursor_master.execute(query_master_qualification_specializations)
    # qualification_specializations_raw = cursor_master.fetchall()
    # qualification_specializations_master = get_key_value_format_mapping(qualification_specializations_raw)
    query_master_job_location = 'select jll.name,jl.uuid from colleges as jl inner join college_langs as jll on jl.id= jll.college_id;'
    cursor_master.execute(query_master_job_location)
    countries_locuuid_raw = cursor_master.fetchall()
    # print(countries_locuuid_raw)
    job_locationuuid_name_master = get_key_value_format_mapping(countries_locuuid_raw)
    query_master_degree = 'select jll.name,jl.uuid from highest_qualifications as jl inner join highest_qualification_langs as jll on jl.id= jll.highest_qualification_id;'
    cursor_master.execute(query_master_degree)
    degreeuuid_raw = cursor_master.fetchall()
    # print(countries_locuuid_raw)
    degree_name_master = get_key_value_format_mapping(degreeuuid_raw)
    connection_master.close()
    return job_locationuuid_name_master,degree_name_master
    # return job_locationuuid_name_master, search_cmpuuid_name_master,  designation_data_master, skill_data_master, highest_qualifications_master, qualification_specializations_master

# job_locationuuid_name_master, search_cmpuuid_name_master,  designation_data_master, skill_data_master, highest_qualifications_master, qualification_specializations_master = master_fetch_data_from_eagle_database()
# college_data, degree_data = master_fetch_data_from_eagle_database()
# print(college_data)
# f=open("uuid/colleges_uuid",'w')
# f.write(str(college_data))
# f.close()
# fd=open("uuid/highest_qualification_uuid",'w')
# fd.write(str(degree_data))
# fd.close()
# print(job_locationuuid_name_master)
#
# f=open("uuid/location_uuid",'w')
# f.write(str(job_locationuuid_name_master))
# f.close()
#
# f1=open("uuid/company_uuid",'w')
# f1.write(str(search_cmpuuid_name_master))
# f1.close()
# f2=open("uuid/designation_uuid",'w')
# f2.write(str(designation_data_master))
# f2.close()
# f3=open("uuid/skills_uuid",'w')
# f3.write(str(skill_data_master))
# f3.close()
# f4=open("uuid/qualifications_uuid",'w')
# f4.write(str(highest_qualifications_master))
# f4.close()


