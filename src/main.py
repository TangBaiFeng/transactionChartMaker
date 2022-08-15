import os
import pandas as pd
import re


bannedWords = ['payment', 'internet transfer', 'pmt', 'epay', 'pymt']


def parseFinances(fileName):
    """
    Take in a directory, find all .csv files, and parse them into a dictionary. Export this dictionary to a new CSV file in out folder
    """
    # Read every csv file in the directory
    finances = {}

    for file in os.listdir(fileName):
        if file.endswith(".csv") or file.endswith(".CSV"):
            # Read the file
            with open(fileName + "/" + file, 'r') as csvinput:
                # Read the file into a dictionary
                df = pd.read_csv(csvinput, header=[0])
                # Add the dictionary to the dictionary of all finances
                print(str(file) + "  " + str(len(df)))
                # print(df.head())

                # Remove rows where the 'Description' column contains the word 'Payment' or 'Transfer' ignoring case
                for word in bannedWords:
                    df = df[~df['Description'].str.contains(
                        word, case=False, na=False, regex=True)]

                print(df)
                # add dataframe to a dictionary
                finances[file] = df

    # Export the dictionary to a CSV file
    for file in finances:
        finances[file].to_csv("../out/EDITED"+file, index=False)


# Create a function that sums the column of a csv file
def sumColumns(fileDir):
    """
    Take in a file name and a column name, and return the sum of the column
    """
    # Read the file
    moneyFlow = {}
    for file in os.listdir(fileDir):
        if file.endswith(".csv") or file.endswith(".CSV"):
            with open(fileDir + "/" + file, 'r') as csvinput:
                # Read the file into a dictionary
                df = pd.read_csv(csvinput, header=[0])
                debitSum = 0
                creditSum = 0
                filtered = df.filter(regex=re.compile(
                    "debit", re.IGNORECASE))
                if filtered.empty:
                    filtered = df.filter(
                        regex=re.compile("amount", re.IGNORECASE))
                    # If the value is positive, add it to the debit sum, otherwise add it to the credit sum
                    for _, row in filtered.iterrows():
                        if row['Amount'] < 0:
                            debitSum += row['Amount'] * -1
                        else:
                            creditSum += row['Amount']
                    debitSum = round(debitSum, 2)
                    creditSum = round(creditSum, 2)
                else:
                    debitSum = re.sub(
                        '[^0-9.]', '', filtered.sum().to_string())
                    filtered = df.filter(regex=re.compile(
                        "credit", re.IGNORECASE))
                    creditSum = re.sub(
                        '[^0-9.]', '', filtered.sum().to_string())
                # Add the sum to the list of money flows
                moneyFlow[str(file)] = [str(file), debitSum,
                                        creditSum, int(float(creditSum)) - int(float(debitSum))]

    print("[Account, Expense, Income, Net]")
    for file in moneyFlow:
        print(moneyFlow[file])


def groupPurchases(fileDir):
    # create new dataframe
    purchases = pd.DataFrame()
    with open('../out/EDITEDchaseCard.CSV', 'r') as csvinput:
        df = pd.read_csv(csvinput, header=[0])
        result1 = df.groupby(['Description'])["Amount"].sum()*-1
        # export to csv
        result1.to_csv('../grouped/groupedChase.csv')

    with open('../out/EDITEDcapitalOne.csv', 'r') as csvinput:
        df = pd.read_csv(csvinput, header=[0])
        result2 = df.groupby(['Description'])["Debit"].sum()
        # export to csv
        result2.to_csv('../grouped/groupedCapital.csv')

    with open('../out/EDITEDmainAccount.csv', 'r') as csvinput:
        df = pd.read_csv(csvinput, header=[0])
        result3 = df.groupby(['Description'])["Debit Amount"].sum()
        # export to csv
        result3.to_csv('../grouped/groupedMain.csv')

    with open('../out/EDITEDalternativeAccounts.csv', 'r') as csvinput:
        df = pd.read_csv(csvinput, header=[0])
        result4 = df.groupby(['Description'])["Debit Amount"].sum()
        # export to csv
        result4.to_csv('../grouped/groupedAlt.csv')

    result2.columns = ['Item', 'Charge']
    result3.columns = ['Item', 'Charge']
    result4.columns = ['Item', 'Charge']
    result1.columns = ['Item', 'Charge']
    purchases = pd.concat([result1, result2, result3, result4], axis=0)
    # Print the sum of the second column
    print(purchases.sum(axis=0))
    # purchases.to_csv('../grouped/groupedAll.csv')


if __name__ == "__main__":
    # parseFinances('../financialImports')
    # print(sumColumns('../out'))
    groupPurchases('../out')
