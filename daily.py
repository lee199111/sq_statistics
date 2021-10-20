from typing import Type
from numpy import r_
import requests
import json
import re
import pandas as pd
from shangqi_statistics import confirm_choice,col_type,read_table,get_result_from_hasura,set_variables,write_csv,auth,run,run_np
import os
import numpy as np
from queries import *


start_time =  "2021-10-8 20:00:00"
end_time =  "2021-10-15 20:00:00"
confirm_msg = "起始时间为：{}       截止时间为:{}\n".format(start_time,end_time)
# confirm_choice(confirm_msg) #confirm
auth_file = "/Users/lizhe/Desktop/shangqi-hasura.json"   # 存放 url、pwd 和 token 的 json
target_table_url = "https://api.notion.com/v1/databases/3d40984aec444edaa74d1d2dbc4402b8/query"
to = "shangqi_{}_{}.xls".format(start_time,end_time)

sheets = {"星尘提交量（不去重）":["客户抽检池",query_of_created_count],
          "星尘提交量（去重）":["客户抽检池",query_of_distinct_created_count],
          "上汽验收合格总量":["客户抽检池",query_of_finished_and_forward_count_all],
          "上汽验收合格量（还在上汽抽检池）":["客户抽检池",query_of_finished_and_forward_and_not_moved_count],
          "上汽验收合格量（已出上汽抽检池）":["客户抽检池",query_of_finished_and_forward_and_moved_count]
          }

try:
  os.remove(to)
except:
  pass


# for k,v in sheets.items():
#     r,r_s = run(auth_file=auth_file,
#                 table_url=target_table_url,
#                 col_name=v[0],
#                 start=start_time, 
#                 end=end_time,
#                 hasura_query=v[1],
#                 hasura_variables=s_e_p_variables)
#     write_csv(file=to,sheet_name=k,data=pd.DataFrame(r),header=None)
#     write_csv(file=to,sheet_name="sum"+k,data=pd.DataFrame(r_s),header=None)


hasura_queries = []
for k,v in sheets.items():
    hasura_queries.append(v[1])
project_name = "SQ-OD融合点云"
r = run_np(auth_file=auth_file,
                table_url=target_table_url,
                col_name=v[0],
                start=start_time, 
                end=end_time,
                hasura_queries=hasura_queries,
                hasura_variables=s_e_p_variables,project_name=project_name)
columns = ["项目名称","项目类型"]+[k for k in sheets.keys()] + ["帧数--"+k for k in sheets.keys()]
print(columns)
write_csv(to,sheet_name="sheet_name",data=pd.DataFrame(r),header=columns)


# r_sum = np.sum(np.array(r),axis=0,initial=2)
# print(r_sum)
