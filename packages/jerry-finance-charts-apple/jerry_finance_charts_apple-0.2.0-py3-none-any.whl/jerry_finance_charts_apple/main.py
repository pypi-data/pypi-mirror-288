import pandas
import plotly


def run(csv_path):
    pandas.options.mode.copy_on_write = True
    df = pandas.read_csv(csv_path)
    df['Date'] = pandas.to_datetime(df['Date'])

    # 1.1 Report min, max, mean. Note describe() can also be used but contains more info than requested
    print(f"The mean is : {df['AAPL.Close'].mean()}")
    print(f"The min is : {df['AAPL.Close'].min()}")
    print(f"The max is : {df['AAPL.Close'].max()}")

    # 1.2 - make sure time series is in order and report duplicates if they exist
    df.sort_values(by=['Date'])
    dups = df[df.duplicated() == True]
    print(f"Duplicate Data: {dups}")

    # 2.1 Find the average volume of the entire dataset. Remove entries lower than such value. Add in day of week and
    # export to csv
    avg_vol = df['AAPL.Volume'].mean()
    print(f"The average volume is: {avg_vol}")
    df_filtered = df[df['AAPL.Volume'] >= avg_vol]
    df_filtered['Day Of Week'] = df_filtered['Date'].dt.day_name()
    df_filtered.to_csv('finance-charts-apple-filtered.csv', index=False)

    # 3 Aggregate the data sets to a week level
    df_week = df.groupby([pandas.Grouper(key='Date', freq='W')]).agg(
        {'AAPL.Open': 'mean', 'AAPL.High': 'max', 'AAPL.Low': 'min', 'AAPL.Close': 'mean'}).reset_index()
    df_week.to_csv('finance-charts-apple-weekly.csv', index=False)

    # 4 plot it on candlestick chart
    fig = plotly.graph_objs.Figure(data=[plotly.graph_objs.Candlestick(x=df_week['Date'],
                                                                       open=df_week['AAPL.Open'],
                                                                       high=df_week['AAPL.High'],
                                                                       low=df_week['AAPL.Low'],
                                                                       close=df_week['AAPL.Close'])])
    fig.show()

if __name__ == '__main__':
    run('../../test/finance-charts-apple.csv')