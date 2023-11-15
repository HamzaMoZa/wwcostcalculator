import streamlit as st
def calculate_cost(num_users, cost_options):
    total_cost = sum(cost for condition, cost in cost_options.values() if eval(condition))
    return total_cost / num_users if num_users > 0 else 0
st.title('Operational Expenditures Calculator')
# Initialize session state for dynamic costs if not already set
if 'dynamic_costs' not in st.session_state:
    st.session_state['dynamic_costs'] = {}
# Slider for number of users
num_users = st.slider("Number of Users", 1, 20000, 1)
# Checkbox states
database_paid = st.checkbox("Database Paid ($190/month)")
jira_paid = st.checkbox("Jira Paid ($110/month)")
dwolla_upgrade = st.checkbox("Upgrade Dwolla to Paid ($200/month)")
# Existing fixed costs
fixed_costs = {
    "Database Paid": ("True", 190 if database_paid else 0),
    "Jira Paid": ("True", 110 if jira_paid else 0),
    "Dwolla Upgrade": ("True", 200 if dwolla_upgrade else 0),
    "Instances": (f"num_users > 100", 110 if num_users > 100 else 0),
    "Hosting": ("True", 107),
    "BitBucket": ("True", 18),
    "Envestnet": (f"num_users > 100", 500 if num_users > 100 else 0)
}
# Combine fixed and dynamic costs
total_costs = {**fixed_costs, **st.session_state.dynamic_costs}
# UI for adding new dynamic cost option
with st.expander("Add New Cost Option"):
    option_name = st.text_input("Option Name")
    option_type = st.selectbox("Select Option Type", ["Free until X users", "Always Free", "Paid"])
    cost = 0
    condition = "True"
    if option_type == 'Free until X users':
        x_users = st.number_input("Enter X Users", min_value=1)
        cost = st.number_input("Enter Cost after X Users", min_value=0)
        condition = f"num_users > {x_users}"
    elif option_type == 'Paid':
        cost = st.number_input("Enter Cost", min_value=0)
    if st.button("Add Option"):
        st.session_state.dynamic_costs[f"{option_type} - {option_name}"] = (condition, cost)
        total_costs.update({f"{option_type} - {option_name}": (condition, cost)})
# Calculate cost per user
cost_per_user = calculate_cost(num_users, total_costs)
st.write(f"Cost per user: ${cost_per_user:.2f}")
# Display costs
st.table({name: cost for name, (_, cost) in total_costs.items()})