"""
Data Validation and Preprocessing Script
Validates and cleans web traffic data before analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys

class DataValidator:
    """Validates and preprocesses web traffic data"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.issues = []
        
    def load_data(self):
        """Load CSV file"""
        try:
            self.df = pd.read_csv(self.filepath)
            print(f"✓ Successfully loaded {len(self.df):,} records")
            return True
        except FileNotFoundError:
            print(f"✗ Error: File '{self.filepath}' not found")
            return False
        except Exception as e:
            print(f"✗ Error loading file: {str(e)}")
            return False
    
    def validate_columns(self):
        """Check if all required columns exist"""
        required_columns = [
            'date', 'page', 'device', 'country', 
            'sessions', 'users', 'bounce_rate', 
            'conversions', 'avg_session_duration'
        ]
        
        missing_columns = set(required_columns) - set(self.df.columns)
        
        if missing_columns:
            print(f"✗ Missing columns: {missing_columns}")
            self.issues.append(f"Missing columns: {missing_columns}")
            return False
        
        print("✓ All required columns present")
        return True
    
    def validate_dates(self):
        """Validate date format and values"""
        try:
            # Try parsing dates
            self.df['date'] = pd.to_datetime(self.df['date'], format='%d-%m-%Y %H:%M')
            
            # Check for future dates
            future_dates = self.df[self.df['date'] > datetime.now()]
            if len(future_dates) > 0:
                print(f"⚠ Warning: {len(future_dates)} records have future dates")
                self.issues.append(f"{len(future_dates)} future dates found")
            
            print(f"✓ Date range: {self.df['date'].min()} to {self.df['date'].max()}")
            return True
            
        except Exception as e:
            print(f"✗ Date parsing error: {str(e)}")
            print("  Expected format: DD-MM-YYYY HH:MM")
            self.issues.append(f"Date parsing error: {str(e)}")
            return False
    
    def validate_numeric_columns(self):
        """Validate numeric columns"""
        numeric_cols = ['sessions', 'users', 'conversions', 
                       'bounce_rate', 'avg_session_duration']
        
        all_valid = True
        
        for col in numeric_cols:
            # Check if numeric
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                print(f"✗ Column '{col}' is not numeric")
                self.issues.append(f"'{col}' is not numeric")
                all_valid = False
                continue
            
            # Check for negative values (except bounce_rate which can be 0-1)
            if col != 'bounce_rate':
                negative_count = (self.df[col] < 0).sum()
                if negative_count > 0:
                    print(f"⚠ Warning: {negative_count} negative values in '{col}'")
                    self.issues.append(f"{negative_count} negative values in '{col}'")
            
            # Check bounce_rate range
            if col == 'bounce_rate':
                invalid_bounce = ((self.df[col] < 0) | (self.df[col] > 1)).sum()
                if invalid_bounce > 0:
                    print(f"⚠ Warning: {invalid_bounce} invalid bounce_rate values (should be 0-1)")
                    self.issues.append(f"{invalid_bounce} invalid bounce_rate values")
            
            # Check for missing values
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                print(f"⚠ Warning: {missing_count} missing values in '{col}'")
                self.issues.append(f"{missing_count} missing values in '{col}'")
        
        if all_valid and not self.issues:
            print("✓ All numeric validations passed")
        
        return all_valid
    
    def validate_categorical_columns(self):
        """Validate categorical columns"""
        print("\n📊 Categorical Column Summary:")
        
        for col in ['page', 'device', 'country']:
            unique_count = self.df[col].nunique()
            top_values = self.df[col].value_counts().head(5)
            
            print(f"\n  {col}:")
            print(f"    - Unique values: {unique_count}")
            print(f"    - Top 5:")
            for val, count in top_values.items():
                print(f"      {val}: {count:,} ({count/len(self.df)*100:.1f}%)")
        
        return True
    
    def check_data_quality(self):
        """Check overall data quality metrics"""
        print("\n📈 Data Quality Metrics:")
        
        total_records = len(self.df)
        
        # Check for duplicates
        duplicates = self.df.duplicated().sum()
        print(f"  - Duplicate rows: {duplicates:,} ({duplicates/total_records*100:.2f}%)")
        
        # Check sessions vs users logic
        invalid_sessions = (self.df['sessions'] < self.df['users']).sum()
        if invalid_sessions > 0:
            print(f"  ⚠ Warning: {invalid_sessions} records where sessions < users")
            self.issues.append(f"{invalid_sessions} records with sessions < users")
        
        # Check conversions vs sessions logic
        invalid_conversions = (self.df['conversions'] > self.df['sessions']).sum()
        if invalid_conversions > 0:
            print(f"  ⚠ Warning: {invalid_conversions} records where conversions > sessions")
            self.issues.append(f"{invalid_conversions} records with conversions > sessions")
        
        # Check for zero sessions
        zero_sessions = (self.df['sessions'] == 0).sum()
        if zero_sessions > 0:
            print(f"  ⚠ Warning: {zero_sessions} records with zero sessions")
            self.issues.append(f"{zero_sessions} records with zero sessions")
        
        return True
    
    def generate_summary_stats(self):
        """Generate summary statistics"""
        print("\n📊 Summary Statistics:")
        
        stats = {
            'Total Records': len(self.df),
            'Date Range': f"{self.df['date'].min()} to {self.df['date'].max()}",
            'Total Sessions': self.df['sessions'].sum(),
            'Total Users': self.df['users'].sum(),
            'Total Conversions': self.df['conversions'].sum(),
            'Avg Bounce Rate': f"{self.df['bounce_rate'].mean()*100:.2f}%",
            'Avg Session Duration': f"{self.df['avg_session_duration'].mean():.0f}s",
            'Overall Conversion Rate': f"{(self.df['conversions'].sum()/self.df['sessions'].sum()*100):.2f}%"
        }
        
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        
        return stats
    
    def clean_data(self, output_file='cleaned_data.csv'):
        """Clean and export cleaned data"""
        print("\n🧹 Cleaning Data...")
        
        original_count = len(self.df)
        
        # Remove duplicates
        self.df = self.df.drop_duplicates()
        print(f"  - Removed {original_count - len(self.df)} duplicate records")
        
        # Remove records with zero sessions
        self.df = self.df[self.df['sessions'] > 0]
        print(f"  - Removed records with zero sessions")
        
        # Cap bounce rate at 0-1
        self.df['bounce_rate'] = self.df['bounce_rate'].clip(0, 1)
        
        # Ensure conversions don't exceed sessions
        self.df['conversions'] = self.df[['conversions', 'sessions']].min(axis=1)
        
        # Fill missing values if any
        numeric_columns = ['sessions', 'users', 'conversions', 
                          'bounce_rate', 'avg_session_duration']
        for col in numeric_columns:
            if self.df[col].isna().sum() > 0:
                self.df[col].fillna(0, inplace=True)
        
        # Export cleaned data
        self.df.to_csv(output_file, index=False)
        print(f"\n✓ Cleaned data exported to '{output_file}'")
        print(f"  Final record count: {len(self.df):,}")
        
        return self.df
    
    def run_full_validation(self):
        """Run complete validation pipeline"""
        print("=" * 60)
        print("🔍 DATA VALIDATION REPORT")
        print("=" * 60)
        
        if not self.load_data():
            return False
        
        steps = [
            ("Column Validation", self.validate_columns),
            ("Date Validation", self.validate_dates),
            ("Numeric Validation", self.validate_numeric_columns),
            ("Categorical Validation", self.validate_categorical_columns),
            ("Quality Checks", self.check_data_quality),
            ("Summary Statistics", self.generate_summary_stats)
        ]
        
        all_passed = True
        
        for step_name, step_func in steps:
            print(f"\n{'='*60}")
            print(f"  {step_name}")
            print(f"{'='*60}")
            result = step_func()
            if not result:
                all_passed = False
        
        print("\n" + "=" * 60)
        if all_passed and not self.issues:
            print("✓ VALIDATION PASSED: Data is ready for analysis!")
        elif self.issues:
            print(f"⚠ VALIDATION COMPLETED WITH {len(self.issues)} ISSUES:")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        else:
            print("✗ VALIDATION FAILED: Please fix errors before proceeding")
        print("=" * 60)
        
        # Ask if user wants to clean data
        if self.issues:
            response = input("\n🤔 Would you like to clean the data automatically? (y/n): ")
            if response.lower() == 'y':
                self.clean_data()
        
        return all_passed


def main():
    """Main execution"""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'web_traffic_data.csv'
    
    validator = DataValidator(filepath)
    validator.run_full_validation()


if __name__ == "__main__":
    main()