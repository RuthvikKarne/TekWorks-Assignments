# Pandas Transaction Data Analysis

This project provides a comprehensive analysis of transaction data using pandas. The analysis covers various business insights including sales trends, customer behavior, product performance, and geographical analysis.

## Dataset Overview

The dataset contains transaction records with the following columns:
- `t_date`: Transaction date
- `cust_id`: Customer ID
- `t_amt`: Transaction amount
- `services`: Service category
- `products_used`: Product category
- `city`: City
- `state`: State
- `t_details`: Transaction details (payment method)

## Files Required

- `transactions.csv`: The main dataset containing 50,002 transaction records
- `Transaction_Data_Analysis_Notebook (1).ipynb`: Jupyter notebook with complete analysis

## Key Insights

### Business Performance
- **Total Revenue**: $5,110,820
- **Peak Month**: March (Month 3)
- **Peak Quarter**: Q3
- **Highest Transaction**: $200.00

### Customer Behavior
- **Total Customers**: 9,926
- **Repeat Customer Rate**: 96.56%
- **Average Transactions per Customer**: 5
- **Most customers purchase from multiple service categories**

### Top Performers
- **Best Service Category**: Outdoor Recreation ($846,678.64)
- **Best Product**: Yoga & Pilates ($47,804.94)
- **Best State**: California ($702,346.23)
- **Best City**: Pasadena (highest transaction count)

### Payment Methods
- **Credit Transactions**: 43,151 out of 50,002 total
- **Credit transactions average**: $114.09
- **Cash transactions average**: $27.40
