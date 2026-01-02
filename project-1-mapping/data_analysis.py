import pandas as pd
import numpy as np
from datetime import datetime
import os

class EdTechAnalyzer:
    """
    Analyzes EdTech ecosystem data and generates insights
    """
    
    def __init__(self, data_path='data/edtech_organizations_clean.csv'):
        """
        Initialize the analyzer
        
        Args:
            data_path: Path to the cleaned CSV file
        """
        self.data_path = data_path
        self.df = None
        self.insights = []
        
    def load_data(self):
        """Load cleaned data"""
        print("Loading data for analysis...")
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(self.df)} organizations")
            return self.df
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.data_path}")
            print("💡 Tip: Make sure to run data_collector.py first!")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def analyze_by_country(self):
        """Analyze organizations by country"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n" + "="*60)
        print("COUNTRY ANALYSIS")
        print("="*60)
        
        # Count by country
        country_counts = self.df['Country'].value_counts()
        
        print(f"\n📍 Total Countries: {self.df['Country'].nunique()}")
        print(f"\n🏆 Top 10 Countries:")
        print(country_counts.head(10))
        
        # Calculate percentages
        country_pct = (country_counts / len(self.df) * 100).round(1)
        
        # Funding by country
        funding_by_country = self.df.groupby('Country')['Total funding (€)'].agg([
            ('Total', 'sum'),
            ('Average', 'mean'),
            ('Count', 'count')
        ]).sort_values('Total', ascending=False)
        
        print(f"\n💰 Top 5 Countries by Total Funding:")
        print(funding_by_country.head())
        
        # Employee count by country
        employees_by_country = self.df.groupby('Country')['Employee count'].agg([
            ('Total', 'sum'),
            ('Average', 'mean')
        ]).sort_values('Total', ascending=False)
        
        print(f"\n👥 Top 5 Countries by Total Employees:")
        print(employees_by_country.head())
        
        # Generate insights
        top_country = country_counts.index[0]
        top_country_pct = country_pct.iloc[0]
        self.insights.append(f"Geographic concentration: {top_country} leads with {top_country_pct}% of organizations")
        
        top_funding_country = funding_by_country.index[0]
        top_funding = funding_by_country.loc[top_funding_country, 'Total']
        self.insights.append(f"Funding leader: {top_funding_country} with €{top_funding:,.0f} total funding")
        
        return {
            'counts': country_counts,
            'funding': funding_by_country,
            'employees': employees_by_country
        }
    
    def analyze_by_category(self):
        """Analyze organizations by category"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n" + "="*60)
        print("CATEGORY ANALYSIS")
        print("="*60)
        
        # Count by category
        category_counts = self.df['Category'].value_counts()
        
        print(f"\n📚 Total Categories: {self.df['Category'].nunique()}")
        print(f"\n🏆 Top 10 Categories:")
        print(category_counts.head(10))
        
        # Funding by category
        funding_by_category = self.df.groupby('Category')['Total funding (€)'].agg([
            ('Total', 'sum'),
            ('Average', 'mean'),
            ('Count', 'count')
        ]).sort_values('Total', ascending=False)
        
        print(f"\n💰 Top 5 Categories by Total Funding:")
        print(funding_by_category.head())
        
        # Average company age by category
        age_by_category = self.df.groupby('Category')['Company_Age'].mean().sort_values(ascending=False)
        
        print(f"\n📅 Top 5 Most Established Categories (by avg age):")
        print(age_by_category.head())
        
        # Generate insights
        top_category = category_counts.index[0]
        top_category_count = category_counts.iloc[0]
        self.insights.append(f"Most common category: {top_category} with {top_category_count} organizations")
        
        most_funded_category = funding_by_category.index[0]
        most_funded_amount = funding_by_category.loc[most_funded_category, 'Total']
        self.insights.append(f"Best funded category: {most_funded_category} with €{most_funded_amount:,.0f}")
        
        return {
            'counts': category_counts,
            'funding': funding_by_category,
            'age': age_by_category
        }
    
    def analyze_funding_stages(self):
        """Analyze organizations by funding stage"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n" + "="*60)
        print("FUNDING STAGE ANALYSIS")
        print("="*60)
        
        # Count by funding stage
        stage_counts = self.df['Funding stage'].value_counts()
        
        print(f"\n💰 Organizations by Funding Stage:")
        print(stage_counts)
        
        # Average funding by stage
        avg_funding_by_stage = self.df.groupby('Funding stage')['Total funding (€)'].mean().sort_values(ascending=False)
        
        print(f"\n💶 Average Funding by Stage:")
        for stage, amount in avg_funding_by_stage.items():
            print(f"  {stage}: €{amount:,.0f}")
        
        # Total funding by stage
        total_funding_by_stage = self.df.groupby('Funding stage')['Total funding (€)'].sum().sort_values(ascending=False)
        
        print(f"\n💵 Total Funding by Stage:")
        for stage, amount in total_funding_by_stage.head().items():
            print(f"  {stage}: €{amount:,.0f}")
        
        # Employee count by stage
        employees_by_stage = self.df.groupby('Funding stage')['Employee count'].mean().sort_values(ascending=False)
        
        print(f"\n👥 Average Employees by Stage:")
        for stage, count in employees_by_stage.items():
            print(f"  {stage}: {count:.0f} employees")
        
        # Generate insights
        most_common_stage = stage_counts.index[0]
        stage_percentage = (stage_counts.iloc[0] / len(self.df) * 100)
        self.insights.append(f"Maturity level: {stage_percentage:.1f}% of companies are in {most_common_stage}")
        
        total_funding = self.df['Total funding (€)'].sum()
        self.insights.append(f"Total ecosystem funding: €{total_funding:,.0f}")
        
        return {
            'counts': stage_counts,
            'avg_funding': avg_funding_by_stage,
            'total_funding': total_funding_by_stage,
            'employees': employees_by_stage
        }
    
    def analyze_by_region(self):
        """Analyze organizations by European region"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n" + "="*60)
        print("REGIONAL ANALYSIS")
        print("="*60)
        
        # Count by region
        region_counts = self.df['Region'].value_counts()
        
        print(f"\n🗺️ Organizations by Region:")
        print(region_counts)
        
        # Funding by region
        funding_by_region = self.df.groupby('Region')['Total funding (€)'].agg([
            ('Total', 'sum'),
            ('Average', 'mean'),
            ('Count', 'count')
        ]).sort_values('Total', ascending=False)
        
        print(f"\n💰 Funding by Region:")
        print(funding_by_region)
        
        # Category diversity by region
        categories_per_region = self.df.groupby('Region')['Category'].nunique().sort_values(ascending=False)
        
        print(f"\n📚 Category Diversity by Region:")
        print(categories_per_region)
        
        # Generate insights
        top_region = region_counts.index[0]
        top_region_count = region_counts.iloc[0]
        self.insights.append(f"Regional hub: {top_region} has {top_region_count} organizations")
        
        return {
            'counts': region_counts,
            'funding': funding_by_region,
            'diversity': categories_per_region
        }
    
    def generate_key_insights(self):
        """Generate automated key insights from the data"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n" + "="*60)
        print("KEY INSIGHTS")
        print("="*60)
        
        insights = []
        
        # Market size insight
        total_orgs = len(self.df)
        total_funding = self.df['Total funding (€)'].sum()
        total_employees = self.df['Employee count'].sum()
        
        insights.append({
            'category': 'Market Size',
            'insight': f'The European EdTech ecosystem tracked includes {total_orgs} organizations across {self.df["Country"].nunique()} countries, with €{total_funding:,.0f} in total funding and {total_employees:,.0f} employees.'
        })
        
        # Geographic concentration
        top_3_countries = self.df['Country'].value_counts().head(3)
        top_3_pct = (top_3_countries.sum() / total_orgs * 100)
        
        insights.append({
            'category': 'Geographic Concentration',
            'insight': f'Top 3 countries ({", ".join(top_3_countries.index)}) represent {top_3_pct:.1f}% of all organizations, indicating significant geographic concentration.'
        })
        
        # Category trends
        top_category = self.df['Category'].value_counts().index[0]
        top_category_count = self.df['Category'].value_counts().iloc[0]
        
        insights.append({
            'category': 'Category Leadership',
            'insight': f'{top_category} is the most represented category with {top_category_count} organizations, showing strong market demand in this sector.'
        })
        
        # Funding maturity
        series_b_plus = self.df[self.df['Funding stage'].isin(['Series B', 'Series C', 'Series D', 'Late Stage', 'Public'])].shape[0]
        mature_pct = (series_b_plus / total_orgs * 100)
        
        insights.append({
            'category': 'Market Maturity',
            'insight': f'{mature_pct:.1f}% of organizations have reached Series B or beyond, indicating a maturing ecosystem with proven business models.'
        })
        
        # Average funding
        avg_funding = self.df['Total funding (€)'].mean()
        median_funding = self.df['Total funding (€)'].median()
        
        insights.append({
            'category': 'Funding Patterns',
            'insight': f'Average funding per organization is €{avg_funding:,.0f}, while median is €{median_funding:,.0f}, showing significant variance in funding amounts.'
        })
        
        # Company age
        avg_age = self.df['Company_Age'].mean()
        
        insights.append({
            'category': 'Ecosystem Age',
            'insight': f'The average company age is {avg_age:.1f} years, suggesting a relatively young but growing ecosystem.'
        })
        
        # Print insights
        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight['category']}")
            print(f"   {insight['insight']}")
        
        self.insights.extend([f"{i['category']}: {i['insight']}" for i in insights])
        
        return insights
    
    def save_insights(self, output_path='outputs/key_insights.txt'):
        """Save all insights to a text file"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("EDTECH ECOSYSTEM ANALYSIS - KEY INSIGHTS\n")
                f.write("="*60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Data source: {self.data_path}\n")
                f.write(f"Organizations analyzed: {len(self.df)}\n")
                f.write("="*60 + "\n\n")
                
                for i, insight in enumerate(self.insights, 1):
                    f.write(f"{i}. {insight}\n")
                
                f.write("\n" + "="*60 + "\n")
                f.write("END OF REPORT\n")
            
            print(f"\n✅ Insights saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving insights: {e}")
            return False
    
    def run_full_analysis(self):
        """Run all analysis methods"""
        print("="*60)
        print("RUNNING FULL EDTECH ECOSYSTEM ANALYSIS")
        print("="*60)
        
        # Load data
        if self.load_data() is None:
            return False
        
        # Run all analyses
        self.analyze_by_country()
        self.analyze_by_category()
        self.analyze_funding_stages()
        self.analyze_by_region()
        self.generate_key_insights()
        
        # Save insights
        self.save_insights()
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE!")
        print("="*60)
        
        return True


# Main execution
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = EdTechAnalyzer()
    
    # Run full analysis
    analyzer.run_full_analysis()
    
    print("\n📊 Check the 'outputs' folder for detailed insights!")