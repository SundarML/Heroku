import streamlit as st
import pandas as pd
from ortools.algorithms import pywrapknapsack_solver
import random
#https://www.youtube.com/watch?v=CSv2TBA9_2E
#https://www.youtube.com/watch?v=B0MUXtmSpiA       - deployment

header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()

@st.cache
def get_data(filename):
    df_raw = pd.read_csv(filename)    
    return df_raw

with header:
    st.title("Bundle Offer Creation App....")


with dataset:
    st.header('This is supermarket dataset')

    def itm_sel(cat, num):
        return random.choice(cat)
    # df_raw = pd.read_csv('D:/project_knap/Vendor_Data.csv')
    df_raw = get_data('Vendor_Data.csv')
    # df_raw = get_data('Vendor_Data.csv')
    df = df_raw[['Products', 'Cost_per_unit', 'Average_Profit_per_unit']]
    # assigning product category randomly 
    cat = ['groc', 'cosmt', 'stanr', 'food', 'bvrg']
    df['category'] = [itm_sel(cat, i) for i in range(0, len(df))]

    # df.head()
    st.write(df.sample(10))
    
    def main(cap, profit_Margin, cost_Product, Products):
    # Create the solver.
        solver = pywrapknapsack_solver.KnapsackSolver(
            pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
        
        values = profit_Margin
        weights = [cost_Product]
        products = Products
        
        capacity = [cap] #total cost
        solver.Init(values, weights, capacity)
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
    def main_method(cap, df,  cat_items, main):
        """cap - maximum amount
        df - data frame of products, profit, cost
        output- 
        PI - index of the list of items
        PW - cost of the items selected - weight- sum of weight is equal to cap ie. max amount
        products selected - product identified by index ie,. PI"""
        df = df[df['category'].isin(cat_items)]
        profit_Margin = list(df.Average_Profit_per_unit.values)
        cost_Product = list(df.Cost_per_unit.values)
        Products = list(df.Products.values)
        
        if __name__ == '__main__':
            PI, PW, products_selected = main(cap,profit_Margin, cost_Product, Products)
        return PI, PW, products_selected

with features:
    st.title("selct the criteria for bundle offer...")
    sel_cat, sel_cost = st.beta_columns(2)
    total_value = sel_cost.text_input('Enter the purchase value :')
    try:
        total_value = int(total_value)
    except :
        total_value = 100.0
    cat_items = ['food', 'cosmt', 'stanr']
    PI, PW, products_selected = main_method(total_value, df, cat_items, main)
    st.write(PI, PW, products_selected)

