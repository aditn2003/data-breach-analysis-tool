import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class DataBreachProcessor:
    """Data processor for data breach datasets"""
    
    def __init__(self):
        self.breach_types = [
            'Hacking', 'Phishing', 'Malware', 'Insider', 
            'Physical', 'Social Engineering', 'Other'
        ]
    
    def load_sample_data(self):
        """Load or create sample data breach records"""
        sample_data = [
            {
                'organization': 'TechCorp',
                'breachType': 'Hacking',
                'date': '2023-01-15',
                'recordsCompromised': 2500000,
                'description': 'SQL injection attack',
                'year': 2023
            },
            {
                'organization': 'BankSecure',
                'breachType': 'Phishing',
                'date': '2023-03-22',
                'recordsCompromised': 150000,
                'description': 'Employee fell for phishing email',
                'year': 2023
            },
            {
                'organization': 'HealthData',
                'breachType': 'Malware',
                'date': '2023-06-10',
                'recordsCompromised': 500000,
                'description': 'Ransomware attack',
                'year': 2023
            },
            {
                'organization': 'EduNet',
                'breachType': 'Insider',
                'date': '2023-08-05',
                'recordsCompromised': 75000,
                'description': 'Disgruntled employee data theft',
                'year': 2023
            },
            {
                'organization': 'RetailChain',
                'breachType': 'Physical',
                'date': '2023-11-12',
                'recordsCompromised': 30000,
                'description': 'Stolen backup drives',
                'year': 2023
            },
            {
                'organization': 'TechCorp',
                'breachType': 'Hacking',
                'date': '2022-05-20',
                'recordsCompromised': 1800000,
                'description': 'API vulnerability exploited',
                'year': 2022
            },
            {
                'organization': 'BankSecure',
                'breachType': 'Malware',
                'date': '2022-09-15',
                'recordsCompromised': 320000,
                'description': 'Keylogger infection',
                'year': 2022
            },
            {
                'organization': 'HealthData',
                'breachType': 'Phishing',
                'date': '2022-12-03',
                'recordsCompromised': 89000,
                'description': 'CEO fraud attack',
                'year': 2022
            },
            {
                'organization': 'EduNet',
                'breachType': 'Hacking',
                'date': '2022-02-28',
                'recordsCompromised': 450000,
                'description': 'Database breach',
                'year': 2022
            },
            {
                'organization': 'RetailChain',
                'breachType': 'Insider',
                'date': '2022-07-14',
                'recordsCompromised': 125000,
                'description': 'Employee data sale',
                'year': 2022
            }
        ]
        
        return sample_data
    
    def clean_data(self, data):
        """Clean and validate data breach records"""
        cleaned_data = []
        
        for record in data:
            if not all(key in record for key in ['organization', 'breachType', 'recordsCompromised']):
                continue
            
            org = str(record['organization']).strip()
            if not org:
                continue
            
            breach_type = str(record['breachType']).strip()
            if breach_type not in self.breach_types:
                breach_type = 'Other'
            
            try:
                records = int(record['recordsCompromised'])
                if records <= 0:
                    continue
            except (ValueError, TypeError):
                continue
            
            date_str = record.get('date', '')
            try:
                if date_str:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    year = date_obj.year
                else:
                    year = datetime.now().year
            except ValueError:
                year = datetime.now().year
            
            cleaned_record = {
                'organization': org,
                'breachType': breach_type,
                'recordsCompromised': records,
                'date': date_str if date_str else f"{year}-01-01",
                'year': year,
                'description': record.get('description', ''),
                'createdAt': datetime.now().isoformat()
            }
            
            cleaned_data.append(cleaned_record)
        
        return cleaned_data
    
    def generate_statistics(self, data):
        """Generate statistics from data breach records"""
        if not data:
            return {}
        
        df = pd.DataFrame(data)
        
        stats = {
            'total_breaches': len(data),
            'total_records': df['recordsCompromised'].sum(),
            'avg_records': df['recordsCompromised'].mean(),
            'max_records': df['recordsCompromised'].max(),
            'min_records': df['recordsCompromised'].min(),
            'breach_types': df['breachType'].value_counts().to_dict(),
            'organizations': df['organization'].value_counts().to_dict(),
            'yearly_trends': df.groupby('year').agg({
                'recordsCompromised': ['count', 'sum', 'mean']
            }).to_dict()
        }
        
        return stats
    
    def export_to_json(self, data, filename):
        """Export data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def export_to_csv(self, data, filename):
        """Export data to CSV file"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

if __name__ == '__main__':
    processor = DataBreachProcessor()
    
    sample_data = processor.load_sample_data()
    
    cleaned_data = processor.clean_data(sample_data)
    
    stats = processor.generate_statistics(cleaned_data)
    
    processor.export_to_json(cleaned_data, 'data/breaches.json')
    processor.export_to_csv(cleaned_data, 'data/breaches.csv')
    processor.export_to_json(stats, 'data/statistics.json')
    
    print(f"Processed {len(cleaned_data)} data breach records")
    print(f"Total records compromised: {stats['total_records']:,}")
    print(f"Average records per breach: {stats['avg_records']:,.0f}") 