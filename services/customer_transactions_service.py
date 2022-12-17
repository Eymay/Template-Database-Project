from flask import current_app
import sqlite3
from models import CustomerTransactions

def get_customers_transactions():
    query = "SELECT * FROM CustomerTransactions"
    customers_transactions = []

    with sqlite3.connect(current_app.config["dbname"]) as connection:
        cursor = connection.cursor()
        res = cursor.execute(query)
        for row in res:
            customer_transaction = CustomerTransactions(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            customers_transactions.append(customer_transaction)
    return customers_transactions

def get_customers_transactions(id):
    query = "SELECT * FROM CustomerTransactions WHERE(CustomerTransactions.CustomerTransactionID = %s)"

    with sqlite3.connect(current_app.config["dbname"]) as connection:
        cursor = connection.cursor()
        tuple = cursor.fetchone()
        if tuple is not None:
            dictionary = dict(tuple)
            customer_transaction = CustomerTransactions(dictionary['CustomerTransactionID'], dictionary['CustomerID'], dictionary['InvoiceID'], dictionary['TransactionDate'], dictionary['AmountExcludingTax'], dictionary['TaxAmount'], dictionary['TransactionAmount'], dictionary['OutstandingBalance'], dictionary['FinalizationDate'], dictionary['IsFinalize'])
            return customer_transaction
    return None

def add_customers_transactions(Customer_Transaction):
    query = "INSERT INTO CustomerTransactions (CustomerTransactionID, CustomerID, InvoiceID, TransactionDate, AmountExcludingTax, TaxAmount, TransactionAmount, OutstandingBalance, FinalizationDate, IsFinalized)"\
            "VALUES (%(CustomerTransactionID)s, %(CustomerID)s,%(InvoiceID)s,%(TransactionDate)s,%(AmountExcludingTax)s,%(TaxAmount)s,%(TransactionAmount)s,%(OutstandingBalance)s,%(FinalizationDate)s,%(IsFinalized)s)"\
            "RETURNING CustomerTransactionID"
    with sqlite3.connect(current_app.config["dbname"]) as connection:
        cursor = connection.cursor()
        customer_transaction = Customer_Transaction.get()
        cursor.execute(query,customer_transaction)
        customerTransactionID = cursor.fetchone()[0]
        return customerTransactionID
        
def delete_customers_transactions(id):
    query = "DELETE FROM CustomerTransactions WHERE(CustomerTransactionID = %s)"
    try:
        with sqlite3.connect(current_app.config["dbname"]) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (id,))
            return True
    except:
        return False

def update_customers_transactions(id,Customer_Transaction):
    query = "UPDATE CustomerTransactions SET TransactionDate=%s, AmountExcludingTax=%s, taxAmount=%s, transactionAmount=%s, outstandingBalance=%s, finalizationDate=%s, isFinalize=%s WHERE (customerTransactionID = %s)"
    customer_transaction = Customer_Transaction.get()
    try:
        with sqlite3.connect(current_app.config["dbname"]) as connection:
            cursor = connection.cursor()
            cursor.execute(query, (customer_transaction['TransactionDate'], customer_transaction['AmountExcludingTax'], customer_transaction['TaxAmount'], customer_transaction['TransactionAmount'], customer_transaction['OutstandingBalance'], customer_transaction['FinalizationDate'], customer_transaction['IsFinalize'], id))
            return True
    except sqlite3.Error as er:
        # get the extended result code here
        return False 