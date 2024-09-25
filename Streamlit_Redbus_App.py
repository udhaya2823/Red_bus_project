# Importing libraries
import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu


# Streamlit page setup with wide layout
st.set_page_config(page_title="🚌 OnlineBus - Redbus Scraper", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    /* Background and font settings */
    body {
        background-color: #1E1E1E;
        color: white;
    }
    
    /* Title Style */
    h1, h2, h3, h4 {
        font-family: 'Roboto', sans-serif;
        color: #E07C24;
    }
    
    /* Custom Button Styling */
    .stButton button {
        background-color: #E07C24;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
    }
    
    /* Custom Container Boxes */
    .info-card {
        background: linear-gradient(120deg, #304352, #d7d2cc);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin-bottom: 20px;
    }
    
    /* Styling for DataFrames */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    </style>
""", unsafe_allow_html=True)

# Load bus route lists from CSV files
def load_bus_routes():
    bus_routes = {
        "Kerala": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_klrtc.csv")["Route_Name"].tolist(),
        "Adhra Pradesh": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_apsrtc.csv")["Route_Name"].tolist(),
        "Bihar": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_bsrtc.csv")["Route_Name"].tolist(),
        "Jammu and Kashmir": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_jksrtc.csv")["Route_Name"].tolist(),
        "Rajastan": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_rsrtc.csv")["Route_Name"].tolist(),
        "South Bengal": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_sbstc.csv")["Route_Name"].tolist(),
        "Himachal": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_hrtc.csv")["Route_Name"].tolist(),
        "patiala": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_pepsu.csv")["Route_Name"].tolist(),
        "Uttar Pradesh": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_upsrtc.csv")["Route_Name"].tolist(),
        "Kadamba": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_ktcl.csv")["Route_Name"].tolist(),
        "Chandigarh": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_cturtc.csv")["Route_Name"].tolist(),
        "North Bengal": pd.read_csv("E:/UDHAYA/Scrap data/datas/df_nbstc.csv")["Route_Name"].tolist(),
    }
    return bus_routes

bus_routes = load_bus_routes()

# Create a sidebar for the menu
with st.sidebar:
    web = option_menu(
        menu_title="🚌 OnlineBus",
        options=["Home", "States and Routes"],
        icons=["house", "info-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "5px", "background-color": "black"},
            "icon": {"font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "black",
                "padding": "10px",
                "border-radius": "10px",
                "background-color": "rgba(255, 255, 255, 0.6)",
            },
            "nav-link-selected": {"background-color": "red", "color": "white"},
        }
    )

# Home Page Design
if web == "Home":
    st.image("E:/UDHAYA/redBus.png", width=200)
    st.title("Redbus Data Scraping with Selenium & Dynamic Filtering")
    
    # Create a banner
    st.markdown(
        """
        <div class="info-card">
        <h2 style="text-align:center;"> Revolutionizing Transportation Data </h2>
        <p style="font-size:18px;"> This project provides comprehensive solutions for collecting, analyzing, and visualizing bus travel data.
        Utilizing Selenium for automated data extraction from Redbus, the system helps streamline operations and drive data-driven decisions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Skillset Section
    st.subheader("🚀 Key Skills")
    st.markdown(
        """
        - Selenium: Automating web scraping.
        - Pandas: For data manipulation and analysis.
        - MySQL: Efficient database integration.
        - Streamlit: For building interactive applications.
        """
    )

# States and Routes Page Design
if web == "States and Routes":
    st.title("Explore Bus Routes and Filter Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        S = st.selectbox("Lists of States", list(bus_routes.keys()), index=0)
    
    with col2:
        select_type = st.radio("Choose bus type", ("Sleeper", "Semi-Sleeper", "Others"))

    # Fare and Time selection
    select_fare = st.radio("Choose fare range", ("₹50-1000", "₹1000-2000", "₹2000 and above"))
    TIME = st.time_input("Select Departure Time")

    selected_route = st.selectbox("List of Routes", bus_routes[S])

    # Query Function with Try/Except Block
    def type_and_fare(bus_type, fare_range, route_name):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="red_bus_project")
            my_cursor = conn.cursor()

            # Define fare range based on selection
            fare_min, fare_max = (50, 1000) if fare_range == "₹50-1000" else (1000, 2000) if fare_range == "₹1000-2000" else (2000, 100000)

            # Define bus type condition
            bus_type_condition = {
                "Sleeper": "Bus_type LIKE '%Sleeper%'",
                "Semi-Sleeper": "Bus_type LIKE '%A/c Semi Sleeper%'",
                "Others": "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'",
            }[bus_type]

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_Name = "{route_name}"
                AND {bus_type_condition} 
                AND Departing_Time >= '{TIME}'
                ORDER BY Price, Departing_Time DESC
            '''
            
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            
            # Check if there are results
            if not out:
                return pd.DataFrame()  # Return empty DataFrame if no results

            # Dynamically retrieve column names
            columns_names = [desc[0] for desc in my_cursor.description]

            conn.close()

            # Create DataFrame with dynamic column names
            df = pd.DataFrame(out, columns=columns_names)
            return df

        except mysql.connector.Error as e:
            st.error(f"Database error: {str(e)}")
            return pd.DataFrame()  # Return empty DataFrame on error

    # Display filtered results in a table
    df_result = type_and_fare(select_type, select_fare, selected_route)
    
    if not df_result.empty:
        st.dataframe(df_result.style.set_properties(**{'background-color': '#2E2E2E', 'color': 'white'}), height=400)
    else:
        st.warning("No data available for the selected filters!")
