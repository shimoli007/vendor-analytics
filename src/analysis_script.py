import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys

def main():
    print("Starting analysis script...")
    
    # Use the database from the db directory
    db_path = os.path.join('db', 'twiga_orders.db')
    
    print(f"Looking for database at: {db_path}")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Please make sure you've run the ETL pipeline first.")
        return

    try:
        print("Connecting to database...")
        conn = sqlite3.connect(db_path)
        
        # Test query to verify data
        test_query = "SELECT COUNT(*) FROM vendor_orders"
        count = pd.read_sql_query(test_query, conn).iloc[0, 0]
        print(f"Found {count} records in database")

        # Create reports directory if it doesn't exist
        if not os.path.exists('reports'):
            os.makedirs('reports')
            print("Created reports directory")

        print("\nGenerating visualizations...")
        
        # 1. Location Performance
        print("Creating location sales chart...")
        location_data = pd.read_sql_query("""
            SELECT delivery_location, SUM(total_amount) as total_sales
            FROM vendor_orders
            GROUP BY delivery_location
            ORDER BY total_sales DESC
        """, conn)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=location_data, x='delivery_location', y='total_sales')
        plt.title('Sales by Location')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/location_sales.png')
        plt.close()
        print("Location sales chart saved")

        # 2. Daily Trends
        print("Creating daily trends chart...")
        daily_data = pd.read_sql_query("""
            SELECT order_date, SUM(total_amount) as daily_sales
            FROM vendor_orders
            GROUP BY order_date
            ORDER BY order_date
        """, conn)
        
        plt.figure(figsize=(12, 6))
        plt.plot(daily_data['order_date'], daily_data['daily_sales'])
        plt.title('Daily Sales Trend')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/daily_trends.png')
        plt.close()
        print("Daily trends chart saved")

        # 3. Payment Methods
        print("Creating payment methods chart...")
        payment_data = pd.read_sql_query("""
            SELECT payment_method, SUM(total_amount) as total_sales
            FROM vendor_orders
            GROUP BY payment_method
            ORDER BY total_sales DESC
        """, conn)
        
        plt.figure(figsize=(10, 10))
        plt.pie(payment_data['total_sales'], labels=payment_data['payment_method'],
                autopct='%1.1f%%')
        plt.title('Sales by Payment Method')
        plt.savefig('reports/payment_methods.png')
        plt.close()
        print("Payment methods chart saved")

        # 4. Product Performance
        print("Creating product performance chart...")
        product_data = pd.read_sql_query("""
            SELECT product_name, SUM(total_amount) as total_revenue
            FROM vendor_orders
            GROUP BY product_name
            ORDER BY total_revenue DESC
        """, conn)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(data=product_data, x='product_name', y='total_revenue')
        plt.title('Revenue by Product')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/product_revenue.png')
        plt.close()
        print("Product performance chart saved")

        # Generate summary
        print("\nGenerating summary report...")
        summary_data = {
            'Total Revenue': f"${pd.read_sql_query('SELECT SUM(total_amount) FROM vendor_orders', conn).iloc[0, 0]:,.2f}",
            'Total Orders': pd.read_sql_query('SELECT COUNT(*) FROM vendor_orders', conn).iloc[0, 0],
            'Top Location': location_data.iloc[0]['delivery_location'],
            'Top Product': product_data.iloc[0]['product_name']
        }

        print("\n" + "*" * 50)
        print("TWIGA FOODS BUSINESS SUMMARY")
        print("*" * 50)
        for metric, value in summary_data.items():
            print(f"{metric:<15}: {value}")
        print("*" * 50)

        print("\nAll visualizations have been saved to the 'reports' folder!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {sys.exc_info()}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()