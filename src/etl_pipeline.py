import pandas as pd
import sqlite3
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TwigaETL:
    def __init__(self):
        """Initialize ETL pipeline with absolute paths"""
        self.base_dir = os.getcwd()
        self.input_file = os.path.join(self.base_dir, 'data', 'vendor_orders.csv')
        
        # Create db directory if it doesn't exist
        self.db_dir = os.path.join(self.base_dir, 'db')
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
            
        self.db_name = os.path.join(self.db_dir, 'twiga_orders.db')
        self.data = None
        
        print(f"Base directory: {self.base_dir}")
        print(f"Input file: {self.input_file}")
        print(f"Database file: {self.db_name}")
        print(f"Database directory exists: {os.path.exists(self.db_dir)}")
        print(f"Database directory writable: {os.access(self.db_dir, os.W_OK)}")

    def extract(self):
        """Extract data from CSV file"""
        try:
            if not os.path.exists(self.input_file):
                raise FileNotFoundError(f"CSV file not found at: {self.input_file}")
            
            self.data = pd.read_csv(self.input_file)
            print(f"Successfully read {len(self.data)} records from CSV")
            return True
        except Exception as e:
            print(f"Error reading CSV: {str(e)}")
            return False

    def transform(self):
        """Transform the data"""
        try:
            # Convert date format
            self.data['order_date'] = pd.to_datetime(self.data['order_date'])
            
            # Calculate total amount
            self.data['total_amount'] = self.data['quantity'] * self.data['price']
            
            # Clean up location data
            self.data['delivery_location'] = self.data['delivery_location'].str.strip().str.upper()
            
            # Clean up payment method
            self.data['payment_method'] = self.data['payment_method'].str.strip().str.upper()
            
            print("Data transformation completed")
            return True
        except Exception as e:
            print(f"Error during transformation: {str(e)}")
            return False

    def load(self):
        """Load data into SQLite database"""
        try:
            print(f"Attempting to create database at: {self.db_name}")
            
            # Try to create a connection
            conn = sqlite3.connect(self.db_name)
            print("Successfully connected to database")
            
            # Load the data
            self.data.to_sql('vendor_orders', conn, if_exists='replace', index=False)
            print("Data loaded to table")
            
            # Create indexes
            conn.execute('CREATE INDEX IF NOT EXISTS idx_vendor_id ON vendor_orders(vendor_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON vendor_orders(order_date)')
            print("Indexes created")
            
            conn.commit()
            conn.close()
            print("Database connection closed")
            
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {str(e)}")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Database path: {self.db_name}")
            print(f"Database directory exists: {os.path.exists(self.db_dir)}")
            print(f"Database directory writable: {os.access(self.db_dir, os.W_OK)}")
            return False
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return False

    def run_pipeline(self):
        """Run the complete ETL pipeline"""
        print("\n=== Starting ETL Pipeline ===\n")
        
        if not self.extract():
            print("Extract phase failed")
            return False
            
        if not self.transform():
            print("Transform phase failed")
            return False
            
        if not self.load():
            print("Load phase failed")
            return False
            
        print("\n=== ETL Pipeline completed successfully ===\n")
        return True

if __name__ == "__main__":
    # Create ETL instance
    etl = TwigaETL()
    
    # Run the pipeline
    success = etl.run_pipeline()
    
    if not success:
        print("\nPipeline failed. Please check the errors above.")
    else:
        print("\nPipeline completed successfully. Database created at:", etl.db_name)