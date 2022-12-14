import pandas as pd
import altair as alt
import streamlit as st

def show_graphs():
    #####################################
    # top 10 states with most customers #
    st.subheader('**States with most customers**')

    customer_df = pd.read_csv('data/olist_customers_dataset.csv')

    top_10_customer_state = (
        pd.DataFrame(
            customer_df.customer_state.value_counts().sort_values(ascending=False).reset_index().values,
                                          columns=["customer_state", "total"]).head(10))

    c = alt.Chart(
        top_10_customer_state,
        width=1000
    ).mark_bar().encode(
        x=alt.X('customer_state', sort='-y'),
        y=alt.Y('total')
    
    ).configure_axis(
    labelFontSize=16,
    titleFontSize=16
    ).transform_window(
        rank='rank(total)',
        sort=[alt.SortField('total', order='descending')]
    ).transform_filter(
        (alt.datum.rank < 10)
    )

    st.altair_chart(c, use_container_width=False)

    ###################################
    # top 10 states with most sellers #
    st.subheader('**States with most sellers**')

    seller_df = pd.read_csv('data/olist_sellers_dataset.csv')

    top_10_seller_state = (
        pd.DataFrame(
            seller_df.seller_state.value_counts().sort_values(ascending=False).reset_index().values,
                                          columns=["seller_state", "total"]).head(10))

    c = alt.Chart(
        top_10_seller_state,
        width=1000
    ).mark_bar().encode(
        x=alt.X('seller_state', sort='-y'),
        y=alt.Y('total')
        #color=alt.Color('IMDB_Rating:Q')
    
    ).configure_axis(
    labelFontSize=16,
    titleFontSize=16
    ).transform_window(
        rank='rank(total)',
        sort=[alt.SortField('total', order='descending')]
    ).transform_filter(
        (alt.datum.rank < 10)
    )

    st.altair_chart(c, use_container_width=False)

    #######################
    # Mean sales per year #
    st.subheader('**Mean sales per year**')

    order_items_df = pd.read_csv('data/olist_order_items_dataset.csv')
    
    order_items_df['shipping_limit_date'] = pd.to_datetime(order_items_df['shipping_limit_date'], infer_datetime_format=True)
    order_items_df['shipping_limit_date'] = order_items_df.shipping_limit_date.dt.year

    order_items_df = order_items_df.groupby('shipping_limit_date').price.mean()

    dict = {
        'year': ['2016', '2017', '2018', '2020'],
         'mean_price': order_items_df.values
        }

    mean_price_year = pd.DataFrame(dict)

    c = alt.Chart(
        mean_price_year,
        width=1000
    ).mark_line().encode(
        x=alt.X('year'),
        y=alt.Y('mean_price')
        #color=alt.Color('IMDB_Rating:Q')
    ).configure_axis(
    labelFontSize=16,
    titleFontSize=16
    )

    st.altair_chart(c, use_container_width=False)

    #st.line_chart(data=mean_price_year, x='year', y='mean_price')




   
