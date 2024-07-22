import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
import webbrowser

# Set the default template for Plotly
pio.templates.default = "plotly_white"

# Read the CSV file
file_path = 'predicted_vs_actual_1.csv'  # Replace with the correct path to your CSV file
df = pd.read_csv(file_path)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Filter predicted values to include only those after mid-2011
mid_2011 = pd.to_datetime('2011-07-01')
df['Filtered_Predicted'] = df.apply(
    lambda row: row['Predicted_20%'] if row['Date'] >= mid_2011 else None, axis=1
)

# Drop rows where 'Filtered_Predicted' is NaN
filtered_data = df.dropna(subset=['Filtered_Predicted'])

# Create the interactive plot
fig = make_subplots(specs=[[{"secondary_y": False}]])

# Add trace for Actual values
fig.add_trace(
    go.Scatter(x=df['Date'], y=df['Actual'], name="Actual Sales", line=dict(color='blue')),
)

# Add trace for Predicted values after mid-2011
fig.add_trace(
    go.Scatter(x=filtered_data['Date'], y=filtered_data['Filtered_Predicted'], name="Predicted Sales",
               line=dict(color='red'), mode='lines+markers'),
)

# Set x-axis title
fig.update_xaxes(title_text="Date")

# Set y-axis title
fig.update_yaxes(title_text="Weekly Sales")

# Add range slider and selector
fig.update_layout(
    title="Actual vs Predicted Weekly Sales (2010-2012)",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Add date range selector
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.1,
            y=1.2,
            buttons=list([
                dict(label="All",
                     method="relayout",
                     args=[{"xaxis.range": [df['Date'].min(), df['Date'].max()]}]),
                dict(label="Last Year",
                     method="relayout",
                     args=[{"xaxis.range": [df['Date'].max() - pd.Timedelta(days=365), df['Date'].max()]}]),
                dict(label="Last 6 Months",
                     method="relayout",
                     args=[{"xaxis.range": [df['Date'].max() - pd.Timedelta(days=180), df['Date'].max()]}]),
                dict(label="Last Month",
                     method="relayout",
                     args=[{"xaxis.range": [df['Date'].max() - pd.Timedelta(days=30), df['Date'].max()]}]),
            ]),
        )
    ]
)

# Add hover data
fig.update_traces(
    hoverinfo="x+y",
    hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>"
)

# Save the plot as an HTML file and open it in the browser
html_file_path = "actual_vs_predicted_sales.html"
fig.write_html(html_file_path)
webbrowser.open(html_file_path)