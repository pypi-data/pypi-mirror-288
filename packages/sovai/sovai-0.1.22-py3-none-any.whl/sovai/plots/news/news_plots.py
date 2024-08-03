import pandas as pd
import plotly.express as px
import ipywidgets as widgets
from ipywidgets import interact
from sovai import data


def create_plot_news_sent_price(ticker, variable, df_price, df_news):
    # Resample df_price to calculate weekly returns for the selected ticker
    df_price_weekly = (
        df_price.query(f"ticker == '{ticker}'")
        .reset_index()
        .set_index("date")
        .resample("W-FRI")["closeadj"]
        .last()
        .pct_change()
    )

    # Resample df_news to align with weekly frequency for the selected ticker
    df_news_weekly = (
        df_news.query(f"ticker == '{ticker}'")
        .reset_index()
        .set_index("date")
        .resample("W-FRI")[["relevance", "sentiment", "polarity", "tone"]]
        .last()
    )

    # Merge df_price_weekly with df_news_weekly
    df_merged = pd.merge(
        df_news_weekly,
        df_price_weekly.rename("returns"),
        left_index=True,
        right_index=True,
        how="left",
    )

    fig = px.line(
        df_merged.reset_index(),
        x="date",
        y=[variable, "returns"],
        labels={"variable": "Variable", "value": "Value", "date": "Date"},
        title=f"{variable.capitalize()} and Weekly Returns for {ticker}",
    )

    # Set the y-axis for the selected variable on the left
    fig.update_traces(yaxis="y1", selector=dict(name=variable))

    # Set the y-axis for returns on the right
    fig.update_traces(yaxis="y2", selector=dict(name="returns"))

    # Configure the y-axes
    fig.update_layout(
        yaxis=dict(
            title=variable.capitalize(),
            titlefont=dict(color="blue"),
            tickfont=dict(color="blue"),
        ),
        yaxis2=dict(
            title="Weekly Returns",
            titlefont=dict(color="red"),
            tickfont=dict(color="red"),
            overlaying="y",
            side="right",
        ),
        legend=dict(
            title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
    )

    return fig


def plot_above_sentiment_returns(df_news=None, tickers=None):
    if df_news is None:
        if tickers is None:
            print("Downloading default tickers, use tickers=[...] to select your own")
            df_news = data(
                "news/daily",
                tickers=["MSFT", "TSLA", "AAPL", "META"],
                start_date="2017-03-30",
            )
        else:
            df_news = data("news/daily", tickers=tickers, start_date="2017-03-30")
    else:
        df_news = df_news.copy()

    unique_tickers = df_news.index.get_level_values("ticker").unique().tolist()
    df_price = data("market/prices", tickers=unique_tickers, start_date="2017-03-30")

    # Get the unique set of tickers from both DataFrames
    tickers = sorted(
        set(df_price.index.get_level_values("ticker")).intersection(
            df_news.index.get_level_values("ticker")
        )
    )

    # Create dropdown widgets
    ticker_dropdown = widgets.Dropdown(
        options=tickers, value=tickers[0], description="Ticker:"
    )

    variable_dropdown = widgets.Dropdown(
        options=["relevance", "sentiment", "polarity", "tone"],
        value="tone",
        description="Variable:",
    )

    # Use the interact function to update the plot based on the dropdown selections
    @interact(ticker=ticker_dropdown, variable=variable_dropdown)
    def update_plot(ticker, variable):
        fig = create_plot_news_sent_price(ticker, variable, df_price, df_news)
        fig.show()


# Call the plot_above_sentiment_returns function
# plot_above_sentiment_returns()
