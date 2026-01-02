import pandas as pd
from datetime import datetime
import os

class EdTechDataCollector:
    """
    Collects and processes EdTech organization data
    """
    
    def __init__(self, data_path='data/edtech_organizations_raw.csv'):
        """
        Initialize the data collector
        
        Args:
            data_path: Path to the raw CSV file
        """
        self.data_path = data_path
        self.df = None
        self.cleaned_df = None
        
    def load_data(self):
        """Load raw data from CSV"""
        print("Loading data...")
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(self.df)} organizations")
            print(f"✅ Columns: {list(self.df.columns)}")
            return self.df
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.data_path}")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def clean_data(self):
        """Clean and standardize the data"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
            
        print("\nCleaning data...")
        self.cleaned_df = self.df.copy()
        
        # Remove duplicates
        initial_count = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.drop_duplicates(subset=['Organization'])
        duplicates_removed = initial_count - len(self.cleaned_df)
        if duplicates_removed > 0:
            print(f"✅ Removed {duplicates_removed} duplicate organizations")
        else:
            print("✅ No duplicates found")
        
        # Standardize country names
        country_mapping = {
            'UK': 'United Kingdom',
            'USA': 'United States',
            'US': 'United States'
        }
        self.cleaned_df['Country'] = self.cleaned_df['Country'].replace(country_mapping)
        
        # Convert numeric columns
        numeric_columns = ['Founded year', 'Total funding (€)', 'Employee count', 
                          'Latitude', 'Longitude']
        
        for col in numeric_columns:
            if col in self.cleaned_df.columns:
                self.cleaned_df[col] = pd.to_numeric(self.cleaned_df[col], errors='coerce')
        
        # Handle missing values
        missing_before = self.cleaned_df.isnull().sum().sum()
        
        # Fill missing numeric values with median
        for col in numeric_columns:
            if col in self.cleaned_df.columns:
                median_val = self.cleaned_df[col].median()
                self.cleaned_df[col].fillna(median_val, inplace=True)
        
        # Fill missing string values
        string_columns = ['Category', 'Funding stage', 'City']
        for col in string_columns:
            if col in self.cleaned_df.columns:
                self.cleaned_df[col].fillna('Unknown', inplace=True)
        
        missing_after = self.cleaned_df.isnull().sum().sum()
        print(f"✅ Handled {missing_before - missing_after} missing values")
        
        print(f"✅ Clean dataset: {len(self.cleaned_df)} organizations")
        return self.cleaned_df
    
    def enrich_data(self):
        """Add calculated fields to the data"""
        if self.cleaned_df is None:
            print("❌ No cleaned data. Run clean_data() first.")
            return None
            
        print("\nEnriching data...")
        
        # Calculate company age
        current_year = datetime.now().year
        self.cleaned_df['Company_Age'] = current_year - self.cleaned_df['Founded year']
        print("✅ Added Company_Age")
        
        # Categorize funding amounts
        def categorize_funding(amount):
            if pd.isna(amount):
                return 'Unknown'
            elif amount < 1000000:
                return 'Under €1M'
            elif amount < 5000000:
                return '€1M - €5M'
            elif amount < 10000000:
                return '€5M - €10M'
            elif amount < 50000000:
                return '€10M - €50M'
            else:
                return 'Over €50M'
        
        self.cleaned_df['Funding_Category'] = self.cleaned_df['Total funding (€)'].apply(categorize_funding)
        print("✅ Added Funding_Category")
        
        # Add region classification
        def classify_region(country):
            northern_europe = ['United Kingdom', 'Ireland', 'Norway', 'Sweden', 
                             'Denmark', 'Finland', 'Iceland', 'Estonia', 'Latvia', 'Lithuania']
            western_europe = ['Germany', 'France', 'Belgium', 'Netherlands', 
                            'Luxembourg', 'Switzerland', 'Austria']
            southern_europe = ['Spain', 'Italy', 'Portugal', 'Greece']
            eastern_europe = ['Poland', 'Czech Republic', 'Hungary', 'Romania', 
                            'Bulgaria', 'Slovakia']
            
            if country in northern_europe:
                return 'Northern Europe'
            elif country in western_europe:
                return 'Western Europe'
            elif country in southern_europe:
                return 'Southern Europe'
            elif country in eastern_europe:
                return 'Eastern Europe'
            else:
                return 'Other'
        
        self.cleaned_df['Region'] = self.cleaned_df['Country'].apply(classify_region)
        print("✅ Added Region classification")
        
        print(f"✅ Enriched dataset ready: {len(self.cleaned_df)} organizations")
        return self.cleaned_df
    
    def save_data(self, output_path='data/edtech_organizations_clean.csv'):
        """Save cleaned and enriched data"""
        if self.cleaned_df is None:
            print("❌ No data to save. Run clean_data() and enrich_data() first.")
            return False
            
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to CSV
            self.cleaned_df.to_csv(output_path, index=False)
            print(f"\n✅ Data saved to: {output_path}")
            print(f"✅ Saved {len(self.cleaned_df)} organizations with {len(self.cleaned_df.columns)} columns")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def generate_summary(self):
        """Generate and display summary statistics"""
        if self.cleaned_df is None:
            print("❌ No data available. Run the pipeline first.")
            return None
            
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        
        print(f"\n📊 Total Organizations: {len(self.cleaned_df)}")
        print(f"🌍 Countries Represented: {self.cleaned_df['Country'].nunique()}")
        print(f"📚 Categories: {self.cleaned_df['Category'].nunique()}")
        print(f"💰 Funding Stages: {self.cleaned_df['Funding stage'].nunique()}")
        
        print("\n🌍 Top 5 Countries:")
        print(self.cleaned_df['Country'].value_counts().head())
        
        print("\n📚 Top 5 Categories:")
        print(self.cleaned_df['Category'].value_counts().head())
        
        print("\n💰 Funding Stage Distribution:")
        print(self.cleaned_df['Funding stage'].value_counts())
        
        # Calculate funding statistics
        total_funding = self.cleaned_df['Total funding (€)'].sum()
        avg_funding = self.cleaned_df['Total funding (€)'].mean()
        
        print(f"\n💶 Total Funding: €{total_funding:,.0f}")
        print(f"💶 Average Funding: €{avg_funding:,.0f}")
        
        # Calculate employee statistics
        total_employees = self.cleaned_df['Employee count'].sum()
        avg_employees = self.cleaned_df['Employee count'].mean()
        
        print(f"\n👥 Total Employees: {total_employees:,.0f}")
        print(f"👥 Average Employees: {avg_employees:.0f}")
        
        # Regional distribution
        print("\n🗺️ Regional Distribution:")
        print(self.cleaned_df['Region'].value_counts())
        
        # Company age statistics
        avg_age = self.cleaned_df['Company_Age'].mean()
        print(f"\n📅 Average Company Age: {avg_age:.1f} years")
        
        print("\n" + "="*60)
        
        # Save summary to file
        summary_path = 'outputs/data_summary.txt'
        os.makedirs('outputs', exist_ok=True)
        
        with open(summary_path, 'w') as f:
            f.write("EDTECH ECOSYSTEM DATA SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total Organizations: {len(self.cleaned_df)}\n")
            f.write(f"Countries: {self.cleaned_df['Country'].nunique()}\n")
            f.write(f"Categories: {self.cleaned_df['Category'].nunique()}\n")
            f.write(f"Total Funding: €{total_funding:,.0f}\n")
            f.write(f"Total Employees: {total_employees:,.0f}\n")
        
        print(f"✅ Summary saved to: {summary_path}")
        
        return self.cleaned_df.describe()


# Main execution
if __name__ == "__main__":
    print("="*60)
    print("EDTECH DATA COLLECTION & PROCESSING")
    print("="*60)
    
    # Initialize collector
    collector = EdTechDataCollector()
    
    # Run the pipeline
    collector.load_data()
    collector.clean_data()
    collector.enrich_data()
    collector.save_data()
    collector.generate_summary()
    
    print("\n✅ Data collection complete!")
    print("="*60)