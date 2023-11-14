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


st.title('Operational Expenditures Calculator')

#Slider for number of users
num_users = st.slider("Number of Users", 1, 20000, 1)

#Existing Checkboxes
database_paid = st.checkbox("Database Paid ($190/month)")
jira_paid = st.checkbox("Jira Paid ($110/month)")
dwolla_upgrade = st.checkbox("Upgrade Dwolla to Paid ($200/month)")

#Additional dynamic checkboxes
additional_costs = {}

#Free until x users
free_until = st.checkbox("Free until X Users then Cost")
if free_until:
    x_users = st.number_input("Enter X Users", min_value=1)
    free_until_cost = st.number_input("Enter Cost after X Users", min_value=0)
    additional_costs["Free until X Users"] = free_until_cost if num_users > x_users else 0 
#Always Free
always_free = st.checkbox("Always Free")
if always_free:
    additional_costs["Always Free"] = 0

#Paid
paid_service = st.checkbox("Paid: Cost $400")
if paid_service:
    additional_costs["Paid Service"] = 400

#Combine all costs
total_costs = {
    "Database": 190 if database_paid else 0,
    "Instances": 110 if num_users > 100 else 0,
    "Hosting": 107,
    "BitBucket": 18,
    "Jira": 110 if jira_paid else 0,
    "Dwolla": 200 if dwolla_upgrade else 0,
    "Envestnet": 0 if num_users <= 100 else 500
}
total_costs.update(additional_costs)

#Calculate cost per user
cost_per_user = sum(total_costs.values()) / num_users if num_users > 0 else 0

#Table to display enabled costs
st.table(total_costs.items())

#Display the calculated cost per user
st.write(f"Cost per paid user: ${cost_per_user:.2f}")