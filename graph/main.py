import plotly.express as px
import pandas as pd
import json


#print(json.dumps(j2))
df = pd.read_json('flt_data.jsonl', lines = True)
print(df)
df = df.sort_values(by='sold_date')
df = df[(df.sold_date > '2023-01-24') & (df.price < 5000)]

gpu_order = sorted(list(set(df['query'])))

pd.options.plotting.backend = "plotly"
fig = df.plot.scatter(x="sold_date", y="price", color="query", category_orders={'query': gpu_order}, template='plotly_dark')
fig.write_html('flt_index.html')

