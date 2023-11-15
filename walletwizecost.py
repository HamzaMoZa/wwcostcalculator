import streamlit as st



def calculate_operational_expenditures(num_users, database_paid, jira_paid, dwolla_upgrade):
    """
    Calculate the cost per user in operational expenditures with updated constraints.

    :param num_users: Number of users.
    :param database_paid: Boolean, True if the database is paid.
    :param jira_paid: Boolean, True if Jira is paid.
    :param dwolla_upgrade: Boolean, True if Dwolla is upgraded to paid version.
    :return: Cost per user.
    """
    # Cost definitions with constraints
    database_cost = 190 if database_paid else 0
    instances_cost = 110 if num_users > 100 else 0
    hosting_cost = 107  # Always paid
    bitbucket_cost = 18  # Always paid
    jira_cost = 110 if jira_paid else 0
    dwolla_cost = 200 if dwolla_upgrade else 0
    envestnet_cost = 0 if num_users <= 100 else 500

    # Total cost
    total_cost = database_cost + instances_cost + hosting_cost + bitbucket_cost + jira_cost + dwolla_cost + envestnet_cost

    # Cost per user
    cost_per_user = total_cost / num_users if num_users > 0 else 0

    return cost_per_user


def calculate_cost(num_users, cost_options):
    total_cost = sum(cost for condition, cost in cost_options.values() if eval(condition))
    return total_cost / num_users if num_users > 0 else 0
st.title('Operational Expenditures Calculator')
# Session state for dynamic cost options
if 'dynamic_costs' not in st.session_state:
    st.session_state.dynamic_costs = {}
# Slider for number of users
num_users = st.slider("Number of Users", 1, 20000, 1)
# Existing costs
fixed_costs = {
    "Database Paid": (f"database_paid", 190 if st.checkbox("Database Paid ($190/month)") else 0),
    "Jira Paid": (f"jira_paid", 110 if st.checkbox("Jira Paid ($110/month)") else 0),
    "Dwolla Upgrade": (f"dwolla_upgrade", 200 if st.checkbox("Upgrade Dwolla to Paid ($200/month)") else 0),
    "Instances": (f"num_users > 100", 110 if num_users > 100 else 0),
    "Hosting": ("True", 107),
    "BitBucket": ("True", 18),
    "Envestnet": (f"num_users > 100", 500 if num_users > 100 else 0)
}
# Update dynamic costs
def add_dynamic_cost(name, condition, cost):
    st.session_state.dynamic_costs[name] = (condition, cost)
# UI for adding new cost option
with st.expander("Add New Cost Option"):
    option_name = st.text_input("Option Name")
    option_type = st.selectbox("Select Option Type", ["Free until X users", "Always Free", "Paid"])
    if option_type == 'Free until X users':
        x_users = st.number_input("Enter X Users", min_value=1)
        cost = st.number_input("Enter Cost after X Users", min_value=0)
        condition = f"num_users > {x_users}"
    elif option_type == 'Always Free':
        cost = 0
        condition = "True"
    elif option_type == 'Paid':
        cost = st.number_input("Enter Cost", min_value=0)
        condition = "True"
    if st.button("Add Option"):
        add_dynamic_cost(f"{option_type} - {option_name}", condition, cost)
# Combine fixed and dynamic costs
total_costs = {**fixed_costs, **st.session_state.dynamic_costs}
# Calculate cost per user
cost_per_user = calculate_cost(num_users, total_costs)
st.write(f"Cost per user: ${cost_per_user:.2f}")
# Display costs
st.table({name: cost for name, (_, cost) in total_costs.items()})