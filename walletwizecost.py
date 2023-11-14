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

#Slider for number of users
num_users = st.slider("Number of Users", 1, 20000, 1)

#Session state to store cost options
if 'cost_options' not in st.session_state:
    st.session_state.cost_options = {}

#Function to add new cost option
def add_cost_option():
    option_type = st.session_state.option_type
    if option_type == 'Free until X users':
        x_users = st.number_input("Enter X Users", min_value=1, key='x_users')
        cost = st.number_input("Enter Cost after X Users", min_value=0, key='cost')
        condition = f"num_users > {x_users}"
    elif option_type == 'Always Free':
        cost = 0
        condition = "True"
    elif option_type == 'Paid':
        cost = st.number_input("Enter Cost", min_value=0, key='paid_cost')
        condition = "True"

    st.session_state.cost_options[f"{option_type} - {st.session_state.new_option}"] = (condition, cost)

#Add new cost option
with st.expander("Add New Cost Option"):
    st.session_state.new_option = st.text_input("Option Name")
    st.session_state.option_type = st.selectbox("Select Option Type", ["Free until X users", "Always Free", "Paid"])
    st.button("Add Option", on_click=add_cost_option)

#Display cost options and calculate cost
for name, (condition, cost) in st.session_state.cost_options.items():
    st.checkbox(name, value=eval(condition), disabled=True)

cost_per_user = calculate_cost(num_users, st.session_state.cost_options)
st.write(f"Cost per user: ${cost_per_user:.2f}")