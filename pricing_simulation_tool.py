import streamlit as st
import pandas as pd

def calculate_inflation_impact():
    st.title("Inflation Impact Calculator - FA")

    # Input Parameters
    current_cost_usd = st.number_input("Enter the current cost per stem in USD", value=0.079, format="%.5f")

    st.subheader("Enter the inflation rates")
    inflation_rates = {
        "KES": st.number_input("Inflation rate for KES (%)", value=4.0),
        "USD": st.number_input("Inflation rate for USD (%)", value=3.0),
        "EUR": st.number_input("Inflation rate for EUR (%)", value=2.0)
    }

    st.subheader("Enter the cost distribution (must sum to 100)")
    cost_distribution = {
        "KES": st.number_input("Proportion of costs in KES (e.g., 0.55 for 55%)", value=0.55),
        "USD": st.number_input("Proportion of costs in USD (e.g., 0.30 for 30%)", value=0.30),
        "EUR": st.number_input("Proportion of costs in EUR (e.g., 0.15 for 15%)", value=0.15)
    }

    # Step 1: Calculate weighted inflation impact percentage
    weighted_inflation_impact = sum(
        cost_distribution[currency] * (inflation_rates[currency] / 100)
        for currency in inflation_rates
    )

    # Step 2: Calculate total inflation impact in USD
    total_inflation_impact_usd = current_cost_usd * weighted_inflation_impact

    # Step 3: Calculate updated cost per stem
    updated_cost_usd = current_cost_usd + total_inflation_impact_usd

    # Add input for flower volume
    flower_volume = st.number_input("Flower Volume (Comparable Period)", value=1000, step=1, format="%d")

    # Calculate total impact
    total_impact_usd = total_inflation_impact_usd * flower_volume

    # Prepare results table
    results = pd.DataFrame({
        "Currency": ["KES", "USD", "EUR"],
        "Cost Distribution": [
            cost_distribution["KES"],
            cost_distribution["USD"],
            cost_distribution["EUR"]
        ],
        "Inflation Rate (%)": [
            inflation_rates["KES"],
            inflation_rates["USD"],
            inflation_rates["EUR"]
        ],
        "Weighted Inflation Contribution": [
            f"{cost_distribution['KES'] * (inflation_rates['KES'] / 100):.5f}",
            f"{cost_distribution['USD'] * (inflation_rates['USD'] / 100):.5f}",
            f"{cost_distribution['EUR'] * (inflation_rates['EUR'] / 100):.5f}"
        ]
    })

    # Add total and updated cost
    summary = pd.DataFrame({
        "Metric": [
            "Current Cost per Stem (USD)", 
            "Weighted Inflation Impact (%)", 
            "Total Inflation Impact (USD)", 
            "Updated Cost per Stem (USD)",
            "Flower Volume (Comparable Period)"
        ],
        "Value in USD": [
            f"{current_cost_usd:.5f}", 
            f"{weighted_inflation_impact * 100:.5f}",  # Convert to percentage
            total_inflation_impact_usd, 
            updated_cost_usd,
            f"{flower_volume:,}"
        ]
    })

    st.subheader("Inflation Impact by Currency")
    st.dataframe(results)

    st.subheader("Summary")
    st.dataframe(summary)

    # Display total impact in bold red with comma-separated thousands
    st.markdown(f"<h3 style='color: red;'>Total Impact in USD: {total_impact_usd:,.2f}</h3>", unsafe_allow_html=True)

# Streamlit will execute this function to display the app
if __name__ == "__main__":
    calculate_inflation_impact()
