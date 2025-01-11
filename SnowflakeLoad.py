import requests
from bs4 import BeautifulSoup
import pandas as pd
from snowflake.connector import connect
from datetime import datetime
import logging
from urllib.parse import urljoin, urlparse
from collections import deque

# Import Azure AD authentication libraries
from azure.identity import InteractiveBrowserCredential, DeviceCodeCredential
from snowflake.connector.connection import SnowflakeConnection

class SnowflakeWebCrawler:
    def __init__(self, account, user, warehouse, database, schema):
        """Initialize Snowflake connection parameters for SSO"""
        self.snowflake_config = {
            'account': account,
            'user': user,
            'warehouse': warehouse,
            'database': database,
            'schema': schema,
            'authenticator': 'externalbrowser'  # This enables SSO authentication
        }
        self.visited_urls = set()
        self.setup_logging()
        
    def setup_logging(self):
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def connect_to_snowflake(self):
        """Establish connection to Snowflake using Azure AD SSO"""
        try:
            # Connect using external browser authentication
            conn = connect(**self.snowflake_config)
            self.logger.info("Successfully connected to Snowflake using SSO")
            return conn
        except Exception as e:
            self.logger.error(f"Error connecting to Snowflake: {str(e)}")
            raise

    # ... [rest of the class methods remain the same as in the previous version] ...

# Example usage
if __name__ == "__main__":
    # Snowflake connection details for SSO
    config = {
        'account': 'your_account',
        'user': 'your_email@yourdomain.com',  # Use your AD email
        'warehouse': 'your_warehouse',
        'database': 'your_database',
        'schema': 'your_schema'
    }
    
    # Initialize crawler
    crawler = SnowflakeWebCrawler(**config)
    
    # Start crawling from a specific URL
    start_url = 'https://example.com'
    crawler.crawl_website(start_url, max_depth=5)