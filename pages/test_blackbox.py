import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui
import numpy as np

# Connect to SQLite database

# Function to insert data into the database


def display_investor_preferences():
    st.title("Investor Preferences")

    # Gather investor preferences
    investment_amount = st.slider("Investment Amount ($)", min_value=1, max_value=100000, value=100, step=100)
    time_horizon = st.selectbox("Investment Time Horizon", ["Short-term", "Medium-term", "Long-term"])
    risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
    investment_objectives = st.multiselect("Investment Objectives", ["Wealth Preservation", "Income Generation", "Capital Appreciation"])
    preferred_asset_classes = st.multiselect("Preferred Asset Classes", ["Stocks", "Bonds", "Real Estate", "Commodities", "Alternative Investments"])
    liquidity_needs = st.selectbox("Liquidity Needs", ["High", "Medium", "Low"])
    tax_considerations = st.checkbox("Tax Considerations")
    diversification_preferences = st.multiselect("Diversification Preferences", ["Geographic", "Sector", "Asset Class"])
    ethical_social_preferences = st.multiselect("Ethical/Social Preferences", ["Socially Responsible Investing", "Sustainable Investments"])
    past_investment_experience = st.text_area("Past Investment Experience")

    # Display investor preferences
    st.subheader("Investor Preferences Summary")
    st.write(f"- Investment Amount: ${investment_amount}")
    st.write(f"- Investment Time Horizon: {time_horizon}")
    st.write(f"- Risk Tolerance: {risk_tolerance}")
    st.write(f"- Investment Objectives: {', '.join(investment_objectives)}")
    st.write(f"- Preferred Asset Classes: {', '.join(preferred_asset_classes)}")
    st.write(f"- Liquidity Needs: {liquidity_needs}")
    st.write(f"- Tax Considerations: {'Yes' if tax_considerations else 'No'}")
    st.write(f"- Diversification Preferences: {', '.join(diversification_preferences)}")
    st.write(f"- Ethical/Social Preferences: {', '.join(ethical_social_preferences)}")
    st.write(f"- Past Investment Experience: {past_investment_experience}")


def main():
    st.title("Preferences Form • Black Box")
    ui.badges(badge_list=[("experimental", "secondary")], class_name="flex gap-2", key="viz_badges2")

    # Input fields
    investment_amount = st.number_input("Enter Investment Amount:", min_value=1)
    time_frame = st.number_input("Enter Time Frame (in years):", min_value=1, step=1)
    risk_tolerance = st.radio("Risk Appetite:", options=["Low", "Medium", "High"], horizontal=True, key="risk_appetite", captions=["Play it safe through the maze", "Play like adventure", "Play like a pro"])
    investment_goals = st.text_area("Investment Goals:")
    preferences = st.text_area("Any Specific Preferences:")

    # Define the range of values for the exponential slider
    min_exp_value = 1
    max_exp_value = 5
    min_actual_value = 0.1
    max_actual_value = 1000

    # Convert exponential value to actual value
    def exp_to_actual(value):
        return 10**value
        return min_actual_value * (max_actual_value / min_actual_value) ** ((value - min_exp_value) / (max_exp_value - min_exp_value))

    # Convert actual value to exponential value
    def actual_to_exp(value):
        return min_exp_value + (max_exp_value - min_exp_value) * (np.log(value) - np.log(min_actual_value)) / (np.log(max_actual_value) - np.log(min_actual_value))

    # Exponential slider
    exp_value = st.slider("Exponential Slider", min_value=min_exp_value, max_value=max_exp_value, value=min_exp_value)

    # Convert exponential value to actual value
    actual_value = exp_to_actual(exp_value)

    st.write(f"Actual Value: {actual_value}")
    


    # Define the labels and corresponding amounts
    labels = ["Test", "Coffee", "Dinner", "Engage", "Venture", "Maximum"]
    amounts = [1.11, 10, 100, 1e3, 1e4, 1e5]

    # Create a select slider with labels and corresponding amounts
    selected_label = st.select_slider("Select Amount", options=labels)

    # Get the corresponding amount based on the selected label
    selected_amount = amounts[labels.index(selected_label)]

    st.write(f"Selected Amount: {selected_amount}")
    # Submit button
    if st.button("Submit"):
        st.write(investment_amount, time_frame, risk_tolerance, investment_goals, preferences)
        st.success("Data Submitted Successfully!")



    st.divider()
    st.title("Investment Opportunity Overview")
    with st.expander("Investment Opportunity Introduction", expanded=False):
        st.markdown("## Introduction")
        st.write("Explore a unique investment opportunity designed to redefine your approach to returns. "
                "Our investment protocol allows you to set both an 'expected' and a 'dream' return rate, "
                "offering a personalized and attainable financial goal.")

        st.markdown("## Key Features")
        st.subheader("Expected Return Rate")
        st.write("- **Definition:** Baseline return on investment over a fixed time span.")
        st.write("- **Purpose:** Conservative estimate of return without active involvement.")
        st.write("- **Your Role:** State your desired expected return rate.")

        st.subheader("Dream Return Rate")
        st.write("- **Definition:** Ambitious return rate aligned with personal wishes.")
        st.write("- **Purpose:** Express your ideal financial outcome.")
        st.write("- **Your Role:** Share your dream return rate.")

        st.subheader("Intermediate Value")
        st.write("- **Proposal:** Bridge between expected and dream return rates.")
        st.write("- **Strategy:** Carefully planned investments for balance.")
        st.write("- **Risk Management:** Approach includes risk management.")

        st.markdown("## Process")
        st.write("1. **Set Rates:** Clearly define expected and dream return rates.")
        st.write("2. **Receive Proposal:** Analysis for an attainable intermediate value.")
        st.write("3. **Investments:** Benefit from a curated investment plan.")
        st.write("4. **Review:** Regular reviews for adapting to changes.")

        st.markdown("## Why Us")
        st.write("- **Innovation:** Tailored and flexible investment experience.")
        st.write("- **Transparency:** Clear understanding of the investment process.")
        st.write("- **Expertise:** Backed by a team of financial experts.")

        st.markdown("## Next Steps")
        st.write("Seize this investment opportunity tailored to your financial aspirations. "
                "Set your expected and dream return rates today to embark on a journey towards financial success.")
        st.write("Contact us for more details and personalized assistance.")
        st.title("Investment Opportunity Overview")

    with st.expander("Investment Opportunity Overview", expanded=False):
        st.markdown("## Introduction")
        st.write("Explore a unique investment opportunity designed to redefine your approach to returns. "
                "Our investment protocol allows you to set both an 'expected' and a 'dream' return rate, "
                "offering a personalized and attainable financial goal.")

        st.markdown("## Key Features")
        st.subheader("Expected Return Rate")
        st.write("- **Definition:** Baseline return on investment over a fixed time span.")
        st.write("- **Purpose:** Conservative estimate of return without active involvement.")
        st.write("- **Your Role:** State your desired expected return rate.")

        st.subheader("Dream Return Rate")
        st.write("- **Definition:** Ambitious return rate aligned with personal wishes.")
        st.write("- **Purpose:** Express your ideal financial outcome.")
        st.write("- **Your Role:** Share your dream return rate.")

        st.subheader("Intermediate Value")
        st.write("- **Proposal:** Bridge between expected and dream return rates.")
        st.write("- **Strategy:** Carefully planned investments for balance.")
        st.write("- **Risk Management:** Approach includes risk management.")

        st.markdown("## Process")
        st.write("1. **Set Rates:** Clearly define expected and dream return rates.")
        st.write("2. **Receive Proposal:** Analysis for an attainable intermediate value.")
        st.write("3. **Investments:** Benefit from a curated investment plan.")
        st.write("4. **Review:** Regular reviews for adapting to changes.")

        st.markdown("## Why Us")
        st.write("- **Innovation:** Tailored and flexible investment experience.")
        st.write("- **Transparency:** Clear understanding of the investment process.")
        st.write("- **Expertise:** Backed by a team of financial experts.")

        st.markdown("## Next Steps")
        st.write("Seize this investment opportunity tailored to your financial aspirations. "
                "Set your expected and dream return rates today to embark on a journey towards financial success.")
        st.write("Contact us for more details and personalized assistance.")

    option = st.radio("Select how you want to express return rates:", ("Percentage", "Leverage Factor", "Mixed mode"), horizontal=True)

    col1, col2 = st.columns(2)
    
    if option == "Percentage":
        col1.markdown("## Expected Return Rate (Percentage)")
        expected_return_rate = col1.number_input("Enter your expected return rate (%):", min_value=0.0, step=1.)
        col2.markdown("## Dream Return Rate (Percentage)")
        dream_return_rate = col2.number_input("Enter your dream return rate (%):", min_value=0.0, step=1.)
    elif option == "Leverage Factor":
        col1.markdown("## Expected Return Rate (Leverage Factor)")
        expected_return_rate = col1.number_input("Enter your expected leverage factor:", min_value=0, step=1)
        col2.markdown("## Dream Return Rate (Leverage Factor)")
        dream_return_rate = col2.number_input("Enter your dream leverage factor:", min_value=1, step=1)
    else:
        col1.markdown("## Expected Return Rate (Percentage)")
        expected_return_rate = col1.number_input("Enter your expected return rate (%):", min_value=0.0, step=1.)
        col2.markdown("## Dream Return Rate (Leverage Factor)")
        dream_return_rate = col2.number_input("Enter your dream leverage factor:", min_value=1, step=1)
        
    st.markdown("## Summary")
    if option == "Percentage":
        st.write("Your expected return rate:", expected_return_rate, "%")
        st.write("Your dream return rate:", dream_return_rate, "%")
    elif option == "Leverage Factor":
        st.write("Your expected leverage factor:", expected_return_rate)
        st.write("Your dream leverage factor:", dream_return_rate)
    else:
        st.markdown("## Expected Return Rate (Percentage)")
        st.write("Your expected return rate:", expected_return_rate, "%")
        st.write("Your dream leverage factor:", dream_return_rate)



    # st.markdown("## Expected Return Rate")
    # expected_return_rate = st.number_input("Enter your expected return rate:", min_value=0.0)

    # st.markdown("## Dream Return Rate")
    # dream_return_rate = st.number_input("Enter your dream return rate:", min_value=0.0)

    # st.markdown("## Summary")
    # st.write("Your expected return rate:", expected_return_rate)
    # st.write("Your dream return rate:", dream_return_rate)

if __name__ == "__main__":
    main()
    
    display_investor_preferences()


