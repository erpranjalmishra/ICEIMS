import pandas as pd
import os

# Create sample registration fees table
data = {
    'Category': ['Student', 'Academician', 'Industry Professional', 'Virtual Attendee'],
    'Early Bird (Before Jan 31)': ['$100', '$200', '$300', '$50'],
    'Regular (Feb 1 - Mar 15)': ['$150', '$250', '$350', '$75'],
    'Late (After Mar 15)': ['$200', '$300', '$400', '$100']
}

df = pd.DataFrame(data)

# Create media directory if it doesn't exist
os.makedirs('media/guidelines/tables', exist_ok=True)

# Save to Excel
excel_path = 'media/guidelines/tables/registration_fees_sample.xlsx'
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f"✅ Sample Excel file created: {excel_path}")
print(f"📊 File size: {os.path.getsize(excel_path)} bytes")
print("\n📋 Table Preview:")
print(df.to_string(index=False))

# Also create a CSV version
csv_path = 'media/guidelines/tables/important_dates_sample.csv'
dates_data = {
    'Event': ['Paper Submission Opens', 'Submission Deadline', 'Notification Date', 'Camera Ready Deadline', 'Conference Dates'],
    'Date': ['Nov 1, 2025', 'Jan 31, 2026', 'Mar 15, 2026', 'Apr 15, 2026', 'May 20-22, 2026'],
    'Status': ['Completed', 'Open', 'Upcoming', 'Upcoming', 'Upcoming']
}
dates_df = pd.DataFrame(dates_data)
dates_df.to_csv(csv_path, index=False)

print(f"\n✅ Sample CSV file created: {csv_path}")
print(f"📊 File size: {os.path.getsize(csv_path)} bytes")
print("\n📋 Table Preview:")
print(dates_df.to_string(index=False))
