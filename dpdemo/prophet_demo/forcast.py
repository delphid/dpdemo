from matplotlib import pyplot as plt
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly


df = pd.read_csv('./example_wp_log_peyton_manning.csv')
print(df.head())

m = Prophet()
m.fit(df)
import requests
requests.request
future = m.make_future_dataframe(periods=365)
print(future.tail())

forecast = m.predict(future)
print(forecast.tail())

fig = m.plot_components(forecast)

plt.show()
