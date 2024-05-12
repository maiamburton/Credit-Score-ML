# Harjot Gill 
import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
import joblib
import re

# To run the app with auto reload:
#streamlit run app.py --server.runOnSave true

# Include CSS files
def include_css(filename):
    with open(filename, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Information for the learn more section
def learn_more():
    with st.sidebar:
        st.markdown("<center><h1> What could effect my credit score? </h1></center>", unsafe_allow_html=True)
        st.write("1. Age: The older you are, the more credit history you have. \
                 This means you have more data for the credit bureaus to use to calculate your credit score.")
        st.write("2. Annual Income: A higher income can help you get approved for more credit. \
                 This is because you have more money to pay back potential loans.")
        st.write("3. Monthly Inhand Salary: This is the amount of money you have left after taxes and other deductions. \
                 The more money you have left over, the greater your ability to pay back loans.")
        st.write("4. Number of Bank Accounts: The more bank accounts you have, the more credit history/activity you have generally speaking. \
                 While this is not as important as other factors, it can still have an impact on your credit score.")
        st.write("5. Number of Credit Cards: Multiple credit cards suggests lower credit utilization rates, which can lead to a higher credit score, \
                 so long as you paying them off")
        st.write("6. Interest Rate: A higher interest rate can lead to higher monthly payments, which can lead to a lower credit score.")
        st.write("7. Number of Loans: The more loans you have, the more debt you have, generally speaking. This can lead to a lower credit score.")
        st.write("8. Type of Loan: Certain types of loans can have a negative impact on your credit score.  \
                 For example, payday loans are known to have a negative impact on credit scores, but some loans can help build credit, like auto loans.") 
        st.write("9. Number of Delayed Payments: Late payments can have a very negative impact on your credit score.")
        st.write("10. Number of Credit Inquiries: Multiple credit inquiries can have a negative impact on your credit score as it can suggest financial instability.")
        st.write("11. Outstanding Debt: The more debt you have, the lower your credit score.")
        st.write("12. Credit Utilization Ratio: The higher your credit utilization ratio, the lower your credit score. This is because \
                    it suggests you are using a large portion of your available credit and may be at risk of defaulting.")
        st.write("13. Credit History Age: The longer your credit history, the more data credit bureaus have to calculate your credit score.")
        st.write("14. Total EMI per month: EMI is a fixed payment amount that a borrower needs to pay to a lender at a specified date each month. \
                 The more money you owe, the lower your credit score.")
        st.write("15. Payment Behaviour: Your payment behaviour can have a significant impact on your credit score. The types of purchases you make \
                 can suggest financial instability")
        st.write("16. Monthly Balance: The amount of money you have left over after paying your bills is a good indicator of how much funds you have left over \
                 to pay back a potential loan") 
        
#User input form
def credit_score_input():
    #User Input with button 
    submit_button = None

    with st.form(key='my_form'):
        st.write("Please enter the following information:")
        st.write("Age: ")
        age = st.number_input("Enter your age", min_value=0, max_value=100, value=None)
        
        st.write("\n")
        st.write("Annual Income: ")
        annual_income = st.number_input("Enter your annual income", min_value=0, max_value=10000000, value=None)
        
        st.write("\n")
        st.write("Monthly Inhand Salary: ")
        monthly_inhand_salary = st.number_input("Enter your monthly inhand salary", min_value=0, max_value=1000000, value=None)
        
        st.write("\n")
        st.write("Number of Bank Accounts: ")
        num_BA = st.number_input("Enter the number of bank accounts you have", min_value=0, max_value=15, value=None)

        st.write("\n")
        st.write("Number of Credit Cards: ")
        num_CC = st.number_input("Enter the number of credit cards you have", min_value=0, max_value=15, value=None)
        
        st.write("\n")
        st.write("Interest Rate: ") 
        interest_rate = st.number_input("Enter your average interest rate", min_value=0, max_value=100, value=None)
        
        st.write("\n")
        st.write("Number of Loans: ")
        num_loans = st.number_input("Enter the number of loans you have", min_value=0, max_value=15, value=None)
        
        st.write("\n")
        st.write("Type of Loan: ")
        options = 'Choose an Option', 'Student Loan', 'Equity Loan', 'Payday Loan', 'Personal Loan', 'Consolidation Loan', 'Mortgage Loan', 'Auto Loan', 'Builder Loan'
        loan_types = st.multiselect("Select the type of loans you have, if applicable", options)
        loan_types = ', '.join(loan_types)
        st.write(loan_types)

        st.write("\n")
        st.write("Number of Delayed Payments: ")
        num_delayed_payments = st.number_input("Enter the number of delayed payments", min_value=0, max_value=20, value=None)
        
        st.write("\n")
        st.write("Number of Credit Inquiries: ")
        num_cred_inquires = st.number_input("Enter the number of credit inquiries", min_value=0, max_value=20, value=None)
        
        st.write("\n")
        st.write("Outstanding Debt: ")
        debt = st.number_input("Enter the outstanding debt", min_value=0, max_value=1000000, value=None)
        
        st.write("\n")
        st.write("Credit Utilization Ratio: ")
        cred_util = st.number_input("Enter the credit utilization ratio. For example, for 30% enter 30", min_value=0, max_value=100, value=None)
        
        st.write("\n")
        st.write("Credit History Age: ")
        cred_age = st.number_input("Enter the credit history age in months", min_value=0, value=None)
        
        st.write("\n")
        st.write("Total EMI per month: ")
        emi = st.number_input("Enter the total EMI per month", min_value=0, max_value=100000, value=None)
        
        st.write("\n")
        st.write("Payment Behaviour: ")
        payment_behavior = st.selectbox("Enter the payment behaviour that best fits you", ('High Spending and Large Value Payments', 'High Spending and Medium Value Payments', 
                'High Spending and Small Value Payments', 'Low Spending and Large Value Payments', 'Low Spending and Medium Value Payments', 'Low Spending and Small Value Payments'))
        
        st.write("\n")
        st.write("Monthly Balance: ")
        monthly_balance = st.number_input("Enter the monthly balance", min_value=0, max_value=1000000, value=None)
        
        st.write("\n")
        st.write("\n")
        submit_button = st.form_submit_button(label='Submit')

    #Save user input to session state if submit button is pressed 
    if submit_button: 
        st.session_state.data[0] = {'Age': age, 'Annual_Income': annual_income, 'Monthly_Inhand_Salary': monthly_inhand_salary, 'Num_Bank_Accounts': num_BA, 
                          'Num_Credit_Card': num_CC, 'Interest_Rate': interest_rate, 'Num_of_Loan': num_loans, 'Type_of_Loan': loan_types, 
                          'Num_of_Delayed_Payment': num_delayed_payments, 'Num_Credit_Inquiries': num_cred_inquires, 'Outstanding_Debt': debt, 
                          'Credit_Utilization_Ratio': cred_util, 'Credit_History_Age': cred_age, 'Total_EMI_per_month': emi, 
                          'Payment_Behaviour': payment_behavior, 'Monthly_Balance': monthly_balance}
        

#One Hot Encoding for the user input
def oneHotEncode(dataset):
    #One Hot Encoding for Type of Loan
    dataset['Auto Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if  re.search(r'Auto Loan', x) else 0)
    dataset['Credit-Builder Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Credit-Builder Loan', x) else 0)
    dataset['Personal Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Personal Loan', x) else 0)
    dataset['Payday Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Payday Loan', x) else 0)
    dataset['Student Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Student Loan', x) else 0)
    dataset['Morgage Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Morgage Loan', x) else 0)
    dataset['Home Equity Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Home Equity Loan', x) else 0)
    dataset['Consolidation Loan'] = dataset['Type_of_Loan'].apply(lambda x: 1 if re.search(r'Consolidation Loan', x) else 0)
    dataset = dataset.drop(columns=['Type_of_Loan'])

    #One Hot Encoding for Payment Behaviour
    dataset['High_spent_Large_value_payments'] = dataset['Payment_Behaviour'].apply(lambda x: 1 if  re.search(r'High Spending and Large Value Payments', x) else 0)
    dataset['High_spent_Medium_value_payments'] = dataset['Payment_Behaviour'].apply(lambda x: 1 if re.search(r'High Spending and Medium Value Payments', x) else 0)
    dataset['High_spent_Small_value_payments'] = dataset['Payment_Behaviour'].apply(lambda x: 1 if re.search(r'High Spending and Small Value Payments', x) else 0)
    dataset['Low_spent_Large_value_payments'] = dataset['Payment_Behaviour'].apply(lambda x: 1 if  re.search(r'Low Spending and Large Value Payments', x) else 0)
    dataset['Low_spent_Medium_value_payments'] = dataset['Payment_Behaviour'].apply(lambda x: 1 if re.search(r'Low Spending and Medium Value Payments', x) else 0)
    dataset['Low_spent_Small_value_payments'] = dataset['Payment_Behaviour'].apply(lambda x: 1 if re.search(r'Low Spending and Small Value Payments', x) else 0)  
    dataset = dataset.drop(columns=['Payment_Behaviour'])

    return dataset

def predict(dataset): 
    #Retrieve saved scaler from files     
    scaler = joblib.load("model/scaler.pkl")

    #Scale the user input
    dataset = scaler.transform(dataset)

    #Retrieve saved model from files
    model = joblib.load("model/mlp_model.pkl")
    
    #Make prediction
    prediction = model.predict(dataset)

    return prediction.toarray()

#Display the results of the prediction
def display_results(predictions):
    st.image(".style/credit-score-ranges.png")
    if str(predictions) == '[[1 0 0]]':
        st.header("Estimated Credit Score: 740 - 830")
    elif str(predictions) == '[[1 1 0]]':
        st.header("Estimated Credit Score: 680 - 740")
    elif str(predictions) == '[[0 1 0]]':
        st.header("Estimated Credit Score: 630 - 680")
    elif str(predictions) == '[[0 1 1]]':
        st.header("Estimated Credit Score: 570 - 630")
    elif str(predictions) == '[[0 0 1]]':
        st.header("Estimated Credit Score: 400 - 600")
    else:
        st.header("We are not able to estimate your credit score")
        st.write(str(predictions))

def main():
    #initialize session state to store user input
    if 'data' not in st.session_state:
        st.session_state.data = [{'Age': None, 'Annual_Income': None, 'Monthly_Inhand_Salary': None, 'Num_Bank_Accounts': None, 
                      'Num_Credit_Card': None, 'Interest_Rate': None, 'Num_of_Loan': None, 'Type_of_Loan': None, 
                     'Num_of_Delayed_Payment': None, 'Num_Credit_Inquiries': None, 'Outstanding_Debt': None, 
                     'Credit_Utilization_Ratio': None, 'Credit_History_Age': None, 'Total_EMI_per_month': None, 
                     'Payment_Behaviour': None, 'Monthly_Balance': None}]
    

    # Include header removal CSS files
    include_css('.style/header_remove.css')
    
# ******Main body of the page*****

    # Title of the page 
    title = "Credit Score Form"
    st.markdown(f"<center><h1>{title}</h1></center>", unsafe_allow_html=True)
    st.write("\n")

    st.subheader("Get an estimation on your credit score easily!") 

    # Creating two columns layout
    col1, col2 = st.columns([2.8, 1])  

    # Text along with learn more button 
    with col1:
        st.write("Understanding your credit score is a vital part of your financial well-being")
    with col2:
        if st.button("Learn more"):
            learn_more()

    #User input form 
    credit_score_input()    

    #Updating the dataframe after user input
    dataframe = pd.DataFrame(st.session_state.data)

    #Begin model prediction if user input is valid 
    if not dataframe.isnull().values.any():
        dataframe = oneHotEncode(dataframe)
        predictions = predict(dataframe)
        display_results(predictions)    

if __name__ == "__main__":
    main()
    

