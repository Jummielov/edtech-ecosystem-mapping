import os
import sys
import time
from datetime import datetime
import logging

# Add project-1-mapping to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'project-1-mapping'))

from data_collector import EdTechDataCollector
from data_analysis import EdTechAnalyzer
from visualizations import EdTechVisualizer

class AutomatedPipeline:
    """
    Automated pipeline for EdTech data analysis
    Runs data collection, analysis, and visualization with logging
    """
    
    def __init__(self):
        """Initialize the automated pipeline"""
        self.start_time = None
        self.end_time = None
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the pipeline"""
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        log_filename = f'logs/pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("="*60)
        self.logger.info("AUTOMATED EDTECH PIPELINE STARTED")
        self.logger.info("="*60)
    
    def run_data_collection(self):
        """Run data collection and processing"""
        self.logger.info("\n📊 STEP 1: Data Collection & Processing")
        self.logger.info("-" * 60)
        
        try:
            collector = EdTechDataCollector()
            
            self.logger.info("Loading raw data...")
            collector.load_data()
            
            self.logger.info("Cleaning data...")
            collector.clean_data()
            
            self.logger.info("Enriching data...")
            collector.enrich_data()
            
            self.logger.info("Saving processed data...")
            collector.save_data()
            
            self.logger.info("Generating summary...")
            collector.generate_summary()
            
            self.logger.info("✅ Data collection complete!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Data collection failed: {str(e)}")
            return False
    
    def run_analysis(self):
        """Run data analysis"""
        self.logger.info("\n📈 STEP 2: Data Analysis")
        self.logger.info("-" * 60)
        
        try:
            analyzer = EdTechAnalyzer()
            
            self.logger.info("Loading cleaned data...")
            analyzer.load_data()
            
            self.logger.info("Analyzing by country...")
            analyzer.analyze_by_country()
            
            self.logger.info("Analyzing by category...")
            analyzer.analyze_by_category()
            
            self.logger.info("Analyzing funding stages...")
            analyzer.analyze_funding_stages()
            
            self.logger.info("Analyzing by region...")
            analyzer.analyze_by_region()
            
            self.logger.info("Generating insights...")
            analyzer.generate_key_insights()
            
            self.logger.info("Saving insights...")
            analyzer.save_insights()
            
            self.logger.info("✅ Analysis complete!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Analysis failed: {str(e)}")
            return False
    
    def run_visualizations(self):
        """Run visualization generation"""
        self.logger.info("\n🎨 STEP 3: Visualization Generation")
        self.logger.info("-" * 60)
        
        try:
            visualizer = EdTechVisualizer()
            
            self.logger.info("Loading data...")
            visualizer.load_data()
            
            self.logger.info("Creating interactive map...")
            visualizer.create_interactive_map()
            
            self.logger.info("Creating funding chart...")
            visualizer.create_funding_chart()
            
            self.logger.info("Creating category chart...")
            visualizer.create_category_chart()
            
            self.logger.info("Creating funding stage chart...")
            visualizer.create_funding_stage_chart()
            
            self.logger.info("Creating dashboard...")
            visualizer.create_dashboard()
            
            self.logger.info("✅ Visualizations complete!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Visualization generation failed: {str(e)}")
            return False
    
    def calculate_time_savings(self):
        """Calculate time saved through automation"""
        execution_time = (self.end_time - self.start_time) / 60  # in minutes
        
        # Manual process estimates
        manual_time = {
            'data_collection': 120,  # 2 hours
            'data_cleaning': 60,     # 1 hour
            'analysis': 90,          # 1.5 hours
            'visualization': 180,    # 3 hours
            'total': 450            # 7.5 hours
        }
        
        time_saved = manual_time['total'] - execution_time
        efficiency_gain = (time_saved / manual_time['total']) * 100
        
        return {
            'manual_time': manual_time['total'],
            'automated_time': execution_time,
            'time_saved': time_saved,
            'efficiency_gain': efficiency_gain
        }
    
    def run(self):
        """Run the complete automated pipeline"""
        self.start_time = time.time()
        
        # Run all steps
        steps = [
            ('Data Collection', self.run_data_collection),
            ('Analysis', self.run_analysis),
            ('Visualizations', self.run_visualizations)
        ]
        
        success_count = 0
        for step_name, step_function in steps:
            if step_function():
                success_count += 1
            else:
                self.logger.error(f"Pipeline stopped due to {step_name} failure")
                break
        
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time
        
        # Generate final report
        self.logger.info("\n" + "="*60)
        self.logger.info("PIPELINE EXECUTION SUMMARY")
        self.logger.info("="*60)
        
        self.logger.info(f"\n✅ Steps completed: {success_count}/{len(steps)}")
        self.logger.info(f"⏱️  Total execution time: {execution_time:.2f} seconds ({execution_time/60:.2f} minutes)")
        
        # Calculate time savings
        if success_count == len(steps):
            savings = self.calculate_time_savings()
            
            self.logger.info("\n💰 TIME SAVINGS ANALYSIS")
            self.logger.info("-" * 60)
            self.logger.info(f"Manual process time:     {savings['manual_time']:.0f} minutes ({savings['manual_time']/60:.1f} hours)")
            self.logger.info(f"Automated process time:  {savings['automated_time']:.2f} minutes")
            self.logger.info(f"Time saved:              {savings['time_saved']:.2f} minutes ({savings['time_saved']/60:.1f} hours)")
            self.logger.info(f"Efficiency gain:         {savings['efficiency_gain']:.1f}%")
            
            self.logger.info("\n💡 BUSINESS IMPACT")
            self.logger.info("-" * 60)
            weekly_runs = 1
            monthly_savings = (savings['time_saved'] / 60) * weekly_runs * 4
            self.logger.info(f"Weekly time saved (1 run):   {savings['time_saved']/60:.1f} hours")
            self.logger.info(f"Monthly time saved:          {monthly_savings:.1f} hours")
            self.logger.info(f"Allows analyst to focus on:  Strategic insights, not manual processing")
        
        self.logger.info("\n" + "="*60)
        self.logger.info("PIPELINE COMPLETE!")
        self.logger.info("="*60)
        
        # Save summary to file
        self.save_summary(success_count, len(steps), execution_time)
        
        return success_count == len(steps)
    
    def save_summary(self, success_count, total_steps, execution_time):
        """Save execution summary to file"""
        summary_path = 'outputs/automation_summary.txt'
        
        with open(summary_path, 'w') as f:
            f.write("AUTOMATED PIPELINE EXECUTION SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Steps completed: {success_count}/{total_steps}\n")
            f.write(f"Execution time: {execution_time:.2f} seconds\n\n")
            
            if success_count == total_steps:
                savings = self.calculate_time_savings()
                f.write("TIME SAVINGS:\n")
                f.write("-"*60 + "\n")
                f.write(f"Manual process: {savings['manual_time']} minutes\n")
                f.write(f"Automated process: {savings['automated_time']:.2f} minutes\n")
                f.write(f"Time saved: {savings['time_saved']:.2f} minutes\n")
                f.write(f"Efficiency gain: {savings['efficiency_gain']:.1f}%\n")
        
        self.logger.info(f"\n📄 Summary saved to: {summary_path}")


# Main execution
if __name__ == "__main__":
    print("\n🤖 Starting Automated EdTech Analysis Pipeline...")
    print("="*60)
    
    pipeline = AutomatedPipeline()
    success = pipeline.run()
    
    if success:
        print("\n✅ All pipeline steps completed successfully!")
        print("📊 Check the outputs/ folder for results")
        print("📝 Check the logs/ folder for detailed logs")
    else:
        print("\n❌ Pipeline encountered errors")
        print("📝 Check the logs/ folder for details")
    
    sys.exit(0 if success else 1)