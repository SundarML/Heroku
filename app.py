import streamlit as st
import pandas as pd
from ortools.algorithms import pywrapknapsack_solver
import random
import ortools

header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()

@st.cache
def get_data(filename):
    df_raw = pd.read_csv(filename)    
    return df_raw
category_items = []

with header:
    st.title("Bundle Offer Creation App New....")
    # st.write(ver)

with dataset:
    st.header('This is supermarket dataset') #Header

    # df_raw = get_data('D:/Heroku/stock_shun.csv') # reading data
    df_raw = get_data('stock_shun.csv') # reading data
    df = df_raw[['Product', 'Qty', 'Unit', 'Category', 'MRP', 'Profit_Margin']] # choosing required column
    # df.head()

    st.write(df.sample(10)) # writing some sample dataset

    cat = df['Category'].unique().tolist()

    def main(cap, profit_Margin, cost_Product, Products):
        # Create the solver.
        solver = pywrapknapsack_solver.KnapsackSolver(
            pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
        
        values = profit_Margin
        weights = [cost_Product]
        products = Products
        
        capacity = [cap] #total cost, cart value
        try:
            solver.Init(values, weights, capacity)
        except:
            values_int = [int(round(i)) for i in values]
            solver.Init(values_int, weights, capacity)

        computed_value = solver.Solve()

        packed_items = []
        packed_weights = []
        product = []
        total_weight = 0
    #     print('Total value =', computed_value)
        for i in range(len(values)):
            if solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(weights[0][i])
                total_weight += weights[0][i]
                product.append(Products[i])
                
    #             print('Total Weight =', total_weight)
    #             print('Packed Items =', packed_items)
    #             print('packed_weights=', packed_weights)
    #             print('Products=', product)
        return packed_items, packed_weights, product


    def main_method(cap, df, opti_column, Cost_per_unit, Products, cat_items, main):
        """cap - maximum amount or cart value
        df - data frame of products, profit, cost
        opti_column - profit margin per product
        cat_items - category of products go into bundle"""

        df = df[df['Category'].isin(cat_items)]
        profit_Margin = df[opti_column].values.tolist()
        cost_Product = df[Cost_per_unit].values.tolist()
        Products = df[Products].values.tolist()
        
        if __name__ == '__main__':
            PI, PW, products_selected = main(cap,profit_Margin, cost_Product, Products)
        return PI, PW, products_selected

with features:
    st.title("selct the criteria for bundle offer...")
    sel_cat, sel_cost = st.beta_columns(2)
    total_value = sel_cost.text_input('Enter the purchase value :')
    # category_items = []
    selected_cat = st.multiselect('select category', cat)
    # category_items.append(selected_cat)
    st.write('The categories selected are', selected_cat, type(selected_cat))
    try:
        total_value = int(total_value)
    except :
        total_value = 100
    cat_items =  selected_cat #['grocery', 'snacks']
    opti_column = 'Profit_Margin'
    Cost_per_unit = 'MRP'
    Products = 'Product'
    
    PI, PW, products_selected = main_method(total_value, df, opti_column , Cost_per_unit, Products, cat_items, main)
    st.write(PI, PW, products_selected)

# cat_items = ['grocery', 'snacks', ]
# opti_column = 'Profit_Margin'
# Cost_per_unit = 'MRP'
# Products = 'Product'
# PI, PW, products_selected = main_method(100, df,opti_column , Cost_per_unit, Products, cat_items, main)
