import mysql.connector
import pandas as pd
import json
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import requests

st.set_page_config(layout = "wide")
st.title(":violet[Phonepe Pulse Data Visualization and Exploration]")

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "")
print(mydb)
mycursor = mydb.cursor(buffered = True)

#mycursor.execute('create database phonepe_pulse')
mycursor.execute('use phonepe_pulse')
#Dataframe Creation from the SQL database

#Agg_trans table
mycursor.execute("select * from Agg_trans")
mydb.commit()
table1 = mycursor.fetchall()

Agg_trans_df = pd.DataFrame(table1, columns = ("States", "Year", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#Agg_user table
mycursor.execute("select * from Agg_user")
mydb.commit()
table2 = mycursor.fetchall()

Agg_user_df = pd.DataFrame(table2, columns = ("States", "Year", "Quarter", "Brands", "Transaction_count", "Percentage"))



#Map_trans table
mycursor.execute("select * from Map_trans")
mydb.commit()
table3 = mycursor.fetchall()

Map_trans_df = pd.DataFrame(table3, columns = ("States", "Year", "Quarter", "District", "Transaction_count", "Transaction_amount"))



#Map_user table
mycursor.execute("select * from Map_user")
mydb.commit()
table4 = mycursor.fetchall()

Map_user_df = pd.DataFrame(table4, columns = ("States", "Year", "Quarter", "District", "Registered_user", "App_opens"))



#Top_trans table
mycursor.execute("select * from Top_trans")
mydb.commit()
table5 = mycursor.fetchall()

Top_trans_df = pd.DataFrame(table5, columns = ("States", "Year", "Quarter", "Pincode", "Transaction_count", "Transaction_amount"))



#Top_user table
mycursor.execute("select * from Top_user")
mydb.commit()
table6 = mycursor.fetchall()

Top_user_df = pd.DataFrame(table6, columns = ("States", "Year", "Quarter", "Pincode", "Registered_users"))

#------------------------------------------------------------------------------

#Transaction year based

def Transaction_amount_count_Y(df,year):
    A_trans = df[df['Year'] == year]
    A_trans.reset_index(drop = True, inplace = True)
    
    ATDF = A_trans.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    ATDF.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(ATDF, x = "States", y = "Transaction_amount", title = f"{year} Transaction Amount", color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(ATDF, x = "States", y = "Transaction_count", title = f"{year} Transaction Count", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 650, width = 600)
        st.plotly_chart(fig_count)
    
    col1, col2 = st.columns(2)
    with col1:
        #Getting the lat and long of the India map    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states = []
        for feature in data1["features"]:
            states.append(feature["properties"]["ST_NM"])
        states.sort()
    
        fig_india_1 = px.choropleth(ATDF, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Rainbow",
                                    range_color = (ATDF["Transaction_amount"].min(), ATDF["Transaction_amount"].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                    height = 600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2 = px.choropleth(ATDF, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Rainbow",
                                    range_color = (ATDF["Transaction_count"].min(), ATDF["Transaction_count"].max()),
                                    hover_name = "States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                    height = 600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
        
    return A_trans


#Transaction Quarter based

def Transaction_amount_count_Y_Q(df,quarter):
    A_trans = df[df['Quarter'] == quarter]
    A_trans.reset_index(drop = True, inplace = True)
    
    ATDF = A_trans.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    ATDF.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(ATDF, x = "States", y = "Transaction_amount", title = f"{A_trans['Year'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Aggrnyl, height = 650, width = 600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(ATDF, x = "States", y = "Transaction_count", title = f"{A_trans['Year'].min()} Year {quarter} QUARTER TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r, height = 650, width = 600)
        st.plotly_chart(fig_count)
    
    col1, col2 = st.columns(2)
    with col1:
        #Getting the lat and long of the India map    
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states = []
        for feature in data1["features"]:
            states.append(feature["properties"]["ST_NM"])
        states.sort()
    
        fig_india_1 = px.choropleth(ATDF, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Rainbow",
                                    range_color = (ATDF["Transaction_amount"].min(), ATDF["Transaction_amount"].max()),
                                    hover_name = "States", title = f"{A_trans['Year'].min()} Year {quarter} QUARTER TRANSACTION AMOUNT", fitbounds = "locations",
                                    height = 600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2 = px.choropleth(ATDF, geojson = data1, locations = "States", featureidkey = "properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Rainbow",
                                    range_color = (ATDF["Transaction_count"].min(), ATDF["Transaction_count"].max()),
                                    hover_name = "States", title = f"{A_trans['Year'].min()} Year {quarter} QUARTER TRANSACTION COUNT", fitbounds = "locations",
                                    height = 600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    
    return A_trans

#Transaction type based

def Aggre_Tran_Transaction_type(df, state):

    A_trans = df[df["States"] == state]
    A_trans.reset_index(drop = True, inplace = True)

    ATDF = A_trans.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    ATDF.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame = ATDF, names = "Transaction_type", values = "Transaction_amount",
                            width = 600, title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame = ATDF, names = "Transaction_type", values = "Transaction_count",
                            width = 600, title = f"{state.upper()} TRANSACTION COUNT", hole = 0.5)
        st.plotly_chart(fig_pie_2)


#Agg User Analysis 1

def Aggre_user_plot_1(df, year):
    A_user = df[df["Year"] == year]
    A_user.reset_index(drop= True, inplace= True)

    AUDF = pd.DataFrame(A_user.groupby("Brands")["Transaction_count"].sum())
    AUDF.reset_index(inplace = True)

    fig_bar_1 = px.bar(AUDF, x = "Brands", y = "Transaction_count", title = f"{year} BRANDS AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence = px.colors.sequential.Agsunset, hover_name = "Brands")
    st.plotly_chart(fig_bar_1)

    return A_user


#Aggre_user_Analysis_2

def Aggre_user_plot_2(df, quarter):
    A_user = df[df["Quarter"] == quarter]
    A_user.reset_index(drop = True, inplace = True)

    AUDF = pd.DataFrame(A_user.groupby("Brands")["Transaction_count"].sum())
    AUDF.reset_index(inplace = True)

    fig_bar_1 = px.bar(AUDF, x = "Brands", y = "Transaction_count", title =  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width = 1000, color_discrete_sequence = px.colors.sequential.Magenta_r, hover_name ="Brands")
    st.plotly_chart(fig_bar_1)

    return A_user


#Aggre_user_analysis_3

def Aggre_user_plot_3(df, state):
    A_user = df[df["States"] == state]
    A_user.reset_index(drop = True, inplace = True)

    fig_line_1 = px.line(A_user, x = "Brands", y = "Transaction_count", hover_data = "Percentage",
                        title = f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width = 1000, markers = True)
    st.plotly_chart(fig_line_1)


#Map_trans_district

def Map_trans_District(df, state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg = tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x = "District", y = "Transaction_amount", height = 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence = px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(tacyg, x = "District", y = "Transaction_amount", height = 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence = px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


# map_user_plot_1
def map_user_plot_1(df, year):
    muy = df[df["Year"] == year]
    muy.reset_index(drop = True, inplace = True)

    muyg = muy.groupby("States")[["Registered_user", "App_opens"]].sum()
    muyg.reset_index(inplace = True)

    fig_line_1 = px.line(muyg, x = "States", y = ["Registered_user", "App_opens"],
                        title = f"{year} REGISTERED USER, APPOPENS",width = 1000, height = 800, markers = True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace = True)

    muyqg = muyq.groupby("States")[["Registered_user", "App_opens"]].sum()
    muyqg.reset_index(inplace = True)

    fig_line_1 = px.line(muyqg, x = "States", y = ["Registered_user", "App_opens"],
                        title = f"{df['Year'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width = 1000, height = 800, markers = True,
                        color_discrete_sequence = px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True, inplace = True)

    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x = "District", y = "Registered_user", 
                                title = f"{states.upper()} REGISTERED USER", height = 800, color_discrete_sequence = px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x = "District", y = "App_opens", 
                                title = f"{states.upper()} APPOPENS", height = 800, color_discrete_sequence = px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)



# top_transaction_plot_1

def Top_trans_plot_1(df, state):
    T_trans = df[df["States"] == state]
    T_trans.reset_index(drop = True, inplace = True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_trans_bar_1 = px.bar(T_trans, x = "Quarter", y = "Transaction_amount", hover_data = "Pincode",
                                title = "TRANSACTION AMOUNT", height = 650, width = 600, color_discrete_sequence = px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_trans_bar_1)

    with col2:
        fig_top_trans_bar_2 = px.bar(T_trans, x = "Quarter", y = "Transaction_count", hover_data = "Pincode",
                                title = "TRANSACTION COUNT", height = 650, width = 600, color_discrete_sequence = px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_trans_bar_2)


def top_user_plot_1(df, year):
    T_user = df[df["Year"] == year]
    T_user.reset_index(drop = True, inplace = True)

    tuyg= pd.DataFrame(T_user.groupby(["States", "Quarter"])["Registered_users"].sum())
    tuyg.reset_index(inplace = True)

    fig_top_plot_1 = px.bar(tuyg, x = "States", y = "Registered_users", color = "Quarter", width = 1000, height = 800,
                        color_discrete_sequence = px.colors.sequential.Burgyl, hover_name = "States",
                        title = f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return T_user


# top_user_plot_2
def top_user_plot_2(df, state):
    T_user = df[df["States"] == state]
    T_user.reset_index(drop = True, inplace = True)

    fig_top_pot_2 = px.bar(T_user, x = "Quarter", y = "Registered_users", title = "REGISTEREDUSERS, PINCODES, QUARTER",
                        width = 1000, height = 800, color = "Registered_users", hover_data = "Pincode",
                        color_continuous_scale = px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)



#---------------------------------------------------------------------------------------------------------------------------------------------

#Streamlit Part

with st.sidebar:
    select = option_menu("Main Menu",["Home", "Data Explore", "Top charts"],
                         icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                         menu_icon= "menu-button-wide",
                         default_index=0,
                         styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                                 "nav-link-selected": {"background-color": "#6F36AD"}})
phonepe_logo = "C:/Users/WELCOME/Downloads/phonepe_logo.png"
if select == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.image(phonepe_logo, output_format = "PNG")
        
    with col2:
        st.markdown("# :violet[PhonePe: Your All-in-One Digital Payments Platform]")
        st.markdown("##### Welcome to PhonePe, India's leading digital payments platform! Here, you can manage your finances with ease and convenience, all from your smartphone.")

        st.markdown("###### :violet[Why Choose PhonePe?]")
        
        st.markdown("* Simple and Secure: Our user-friendly interface makes it easy for anyone to send and receive money, pay bills, and recharge your phone. We prioritize security with industry-leading encryption and fraud protection measures.")
        st.markdown("* All Your Needs Covered: From mobile recharges and bill payments to online shopping and investments, PhonePe offers a wide range of services to simplify your daily life.")
        st.markdown("* Instant Transfers: Send and receive money instantly to any bank account in India, 24/7, with just a few taps.")
        st.markdown("* Quick and Easy Bill Payments: Pay your electricity, water, gas, and other utility bills conveniently and securely within the app.")
        st.markdown("* Great Deals and Rewards: Enjoy exclusive discounts and cashback offers on various transactions with our partner merchants.")
        
        st.markdown("###### :violet[Getting Started with PhonePe:]")
        
        st.markdown("* Download the App: Available for free on the App Store and Google Play.")
        st.markdown("* Sign Up: A quick and easy registration process using your mobile number.")
        st.markdown("* Link Your Bank Account: Securely link your bank account(s) for seamless transactions.")
        st.markdown("* Start Exploring: Discover the vast array of services PhonePe offers and experience the convenience of digital payments!")
        
        st.markdown("###### :violet[Beyond Payments:]")
        
        st.markdown("_PhonePe goes beyond just transactions. We offer additional features to empower your financial well-being:_")
        st.markdown("* Invest in Mutual Funds: Start your investment journey with easy-to-use mutual fund options directly within the app.")
        st.markdown("* Buy Digital Gold: Invest in gold securely and conveniently through PhonePe.")
        st.markdown("* Manage Insurance: Access insurance products and manage your existing policies with ease.")
        
        st.markdown("###### :violet[Join Millions of Indians Using PhonePe:]")
        
        st.markdown("Experience the power of digital payments and simplify your life with PhonePe. Download the app today and step into a world of convenience, security, and financial freedom!")
        


elif select == "Data Explore":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    with tab1:
        trans_method = st.radio("Select the method",["Transaction Analysis", "User Analysis"], key = "trans_method_radio")
        
        #Agg Transaction analysis tab
        if trans_method == "Transaction Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year", Agg_trans_df["Year"].min(), Agg_trans_df["Year"].max(), Agg_trans_df["Year"].min())
            Aggre_trans_tac_Y = Transaction_amount_count_Y(Agg_trans_df,years)
            
            with col2:
                st.info("""This interactive visualization provides a comprehensive view of transaction activity
                        across states from 2018 to 2023. The chart clearly depicts both the total transaction amount
                        and the number of transactions for each state, presented on a quarterly basis. Additionally,
                        a geographically mapped view is included to highlight areas with higher and lower transaction volumes,
                        allowing for easy identification of trends and potential regional variations.""", icon = "ℹ️")
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the state", Aggre_trans_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_trans_tac_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter", Aggre_trans_tac_Y["Quarter"].min(), Aggre_trans_tac_Y["Quarter"].max(), Aggre_trans_tac_Y["Quarter"].min())
            Aggre_trans_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_trans_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the state to visualize the aggregate transaction data Quarter wise", Aggre_trans_tac_Y_Q["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_trans_tac_Y_Q, states)
            
            
        #Agg User analysis Tab    
        elif trans_method == "User Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year", Agg_user_df["Year"].min(), Agg_user_df["Year"].max(), Agg_user_df["Year"].min())
            Aggre_user_Y = Aggre_user_plot_1(Agg_user_df, years)
            
            with col2:
                st.info("""This interactive visualization provides a comprehensive view of transaction activity
                        across states from 2018 to 2023 based on the mobile brands. The chart clearly depicts both the total transaction count
                        and the mobile brands with the percentage for each state, presented on a quarterly basis.""", icon = "ℹ️")
                        
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the state", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
            
    
    
    
    with tab2:
        map_method = st.radio("Select the method",["Transaction Analysis", "User Analysis"], key = "map_method_radio")
        if map_method == "Transaction Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year_MT", Map_trans_df["Year"].min(), Map_trans_df["Year"].max(), Map_trans_df["Year"].min())
            Map_trans_tac_Y = Transaction_amount_count_Y(Map_trans_df,years)
            
            with col2:
                st.info("""This interactive visualization provides a comprehensive view of transaction activity
                        across states from 2018 to 2023. The chart clearly depicts both the total transaction amount
                        and the number of transactions for each state and district, presented on a quarterly basis. Additionally,
                        a geographically mapped view is included to highlight areas with higher and lower transaction volumes,
                        allowing for easy identification of trends and potential regional variations.""", icon = "ℹ️")
                        
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_MT",Map_trans_tac_Y["States"].unique())

            Map_trans_District(Map_trans_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_MT",Map_trans_tac_Y["Quarter"].min(), Map_trans_tac_Y["Quarter"].max(),Map_trans_tac_Y["Quarter"].min())
            Map_trans_tac_Y_Q = Transaction_amount_count_Y_Q(Map_trans_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State to visualize the map tansaction data Quarter wise", Map_trans_tac_Y_Q["States"].unique())

            Map_trans_District(Map_trans_tac_Y_Q, states)
            
            
        elif map_method == "User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_mu",Map_user_df["Year"].min(), Map_user_df["Year"].max(),Map_user_df["Year"].min())
            Map_user_Y= map_user_plot_1(Map_user_df, years)
            
            with col2:
                st.info("""This interactive visualization provides a comprehensive view of registered users and usage of the app
                        across states from 2018 to 2023. The chart clearly depicts both the registered users and opening of the app
                        for each state, presented on a quarterly basis.""", icon = "ℹ️")
                        
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",Map_user_Y["Quarter"].min(), Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q= map_user_plot_2(Map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", Map_user_Y_Q["States"].unique())

            map_user_plot_3(Map_user_Y_Q, states)
    
    
    
    with tab3:
        top_method = st.radio("Select the method",["Transaction Analysis", "User Analysis"], key = "top_method_radio")
        if top_method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_TT",Top_trans_df["Year"].min(), Top_trans_df["Year"].max(),Top_trans_df["Year"].min())
            top_tran_tac_Y= Transaction_amount_count_Y(Top_trans_df, years)

            with col2:
                st.info("""This interactive visualization provides a comprehensive view of transaction activity
                        across states from 2018 to 2023. The chart clearly depicts both the total transaction amount
                        and the number of transactions for each state and district, presented on a quarterly basis. Additionally,
                        a geographically mapped view is included to highlight areas with higher and lower transaction volumes,
                        allowing for easy identification of trends and potential regional variations.""", icon = "ℹ️")
                        
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_TT", top_tran_tac_Y["States"].unique())
            Top_trans_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter_TT",top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)

        elif top_method == "User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_TU",Top_user_df["Year"].min(), Top_user_df["Year"].max(),Top_user_df["Year"].min())
            top_user_Y= top_user_plot_1(Top_user_df, years)
            
            with col2:
                st.info("""This interactive visualization provides a comprehensive view of top registered users
                        across states from 2018 to 2023 based on the pincode. The chart clearly depicts the number
                        of registered users for each pincodepresented on a quarterly basis.""", icon = "ℹ️")

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_TU", top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y, states)
        
 
#------------------------------------------------------------------------------
        
       
elif select == "Top charts":
    st.markdown("Top Charts")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district , sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        col3,col4 = st.columns(2)    
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        col1,col2 = st.columns(2)
        
        with col1:
            st.markdown("### :violet[Brands]")
            mycursor.execute(f"select brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="Brand",
                         orientation='h',
                         color='Avg_Percentage',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        
            
        col3,col4 = st.columns(2)
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)