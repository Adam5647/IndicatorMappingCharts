import streamlit as st
import nutritionCharts
import healthCharts
import agricultureCharts

def main():
    st.title("Main Dashboard")

    choice = st.sidebar.selectbox(
        "Select a Dashboard",
        ["Nutrition", "Health", "Agriculture"]
    )

    if choice == "Nutrition":
        nutritionCharts.show_nutrition_dashboard()
    elif choice == "Health":
        healthCharts.show_health_dashboard()
    else:  # Agriculture
        agricultureCharts.show_agriculture_dashboard()

if __name__ == "__main__":
    main()
