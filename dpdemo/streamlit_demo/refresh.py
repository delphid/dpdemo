import arrow
import asyncio
import numpy as np
import pandas as pd
import requests
import streamlit as st
import time


container = st.empty()
st.title('aaa')
while True:
    container.write(arrow.now())
    time.sleep(1)