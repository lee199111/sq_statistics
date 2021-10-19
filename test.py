import streamlit as st
import numpy as np
import pandas as pd
from shangqi_statistics import auth,read_table,get_result_from_hasura,write_csv,run_np
import os
import datetime
import time

a=[1,2,3,4,5,5,6,7,8,1,2,3,4,1,12,3,4]
progress = 0
bar = st.progress(progress)
step = 1/len(a)
for i in range(len(a)):
    time.sleep(0.1)
    progress += step
    bar.progress(progress)




