import arrow
import asyncio
import numpy as np
import pandas as pd
import requests
import streamlit as st
import time


st.title('aaa')

async def timer(container, refresh):
    while True:
        container.write(arrow.now())
        r = await asyncio.sleep(refresh)


async def title(container, name, wait):
    await asyncio.sleep(wait)
    container.title(name)


async def forever():
    while True:
        r = await asyncio.sleep(10)


async def main():
    container1 = st.empty()
    container2 = st.empty()
    asyncio.create_task(timer(container1, 1))
    asyncio.create_task(timer(container2, 5))
    r = await asyncio.sleep(6)


asyncio.run(main())
