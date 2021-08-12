import asyncio
import arrow
import numpy as np
import pandas as pd
import random
import requests
import streamlit as st
import time


timer_container = st.empty()
banner_container = st.empty()


title = 'makabaka'
if st.checkbox('good night'):
    title = f'good night {title}'
st.title(title)

max = st.slider('rand amount', 5, 50)

chart_container = st.empty()
def make_chart(container):
    chart_data = pd.DataFrame(
        np.random.randn(max, 3),
        columns=['a', 'b', 'c'])
    container.area_chart(chart_data)

if st.button('do some http request'):
    result = requests.request('GET', 'https://baidu.com')
    st.write(result)


sid = st.text_input('put sid here')
shop = {
    'lalala_sid': sid,
    'domain': '女装',
    'sellerNick': '_TC_小白鼠2',
    'spuLinkExpiration': 60,
    'keepingAnswerMode': 'PROMPT_ESC_MODE',
    'domainPack': {'domain': '女装'},
    'lightControl': {'lightResponseTimeLimit': 60, 'lightResponseCountLimit': 1},
    'daSpuAnswerFirst': True,
    'jumpAnswerMode': {},
    'usingEstimateTimeInTrade': True,
    'unContinousDuplicatedMode': {'timeLimitInMinutes': '1', 'countLimit': '1'},
    'assistantOnlineStart': '09:00',
    'assistantOnlineEnd': '18:00',
    'overdueDays': 5
}

if st.button('show shop info'):
    st.title(sid)
    st.json(shop)


async def refresh(container, content, refresh_rate):
    while True:
        container.write(arrow.now())
        r = await asyncio.sleep(refresh_rate)


async def forever():
    while True:
        r = await asyncio.sleep(10)


async def async_task():
    asyncio.create_task(refresh(timer_container, arrow.now(), 1))
    asyncio.create_task(refresh(banner_container, random.choice(['lalala', 'bababa', 'hahaha']), 2))
    r = await forever()

asyncio.run(async_task())