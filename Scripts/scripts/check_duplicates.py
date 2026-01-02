import pandas as pd

# Load the data
df = pd.read_csv('data/edtech_organizations_raw.csv')

print("="*60)
print("📊 DATA QUALITY CHECK")
print("="*60)

# Basic info
print(f"\n✅ Total organizations: {len(df)}")
print(f"✅ Total columns: {len(df.columns)}")

# Check for duplicate organization names
print("\n" + "="*60)
print("🔍 CHECKING FOR DUPLICATES BY ORGANIZATION NAME")
print("="*60)

duplicates_by_name = df[df.duplicated(subset=['Organization'], keep=False)]

if len(duplicates_by_name) > 0:
    print(f"\n⚠️  Found {len(duplicates_by_name)} rows with duplicate organization names")
    print(f"🔧 Unique organizations that appear more than once: {duplicates_by_name['Organization'].nunique()}")
    print("\nDuplicate organizations:")
    print(duplicates_by_name[['Organization', 'Country', 'City']].sort_values('Organization'))
else:
    print("\n✅ No duplicate organization names found!")

# Check for duplicate websites
print("\n" + "="*60)
print("🔍 CHECKING FOR DUPLICATES BY WEBSITE")
print("="*60)

duplicates_by_website = df[df.duplicated(subset=['Website'], keep=False)]

if len(duplicates_by_website) > 0:
    print(f"\n⚠️  Found {len(duplicates_by_website)} rows with duplicate websites")
    print("\nDuplicate websites:")
    print(duplicates_by_website[['Organization', 'Website']].sort_values('Website'))
else:
    print("\n✅ No duplicate websites found!")

# Check for exact duplicate rows
print("\n" + "="*60)
print("🔍 CHECKING FOR EXACT DUPLICATE ROWS")
print("="*60)

exact_duplicates = df[df.duplicated(keep=False)]

if len(exact_duplicates) > 0:
    print(f"\n⚠️  Found {len(exact_duplicates)} exact duplicate rows")
else:
    print("\n✅ No exact duplicate rows found!")

# Show data completeness
print("\n" + "="*60)
print("📋 DATA COMPLETENESS")
print("="*60)

missing = df.isnull().sum()
print("\nMissing values per column:")
for col, count in missing.items():
    if count > 0:
        print(f"  ⚠️  {col}: {count} missing ({count/len(df)*100:.1f}%)")
    else:
        print(f"  ✅ {col}: Complete")

# Country breakdown
print("\n" + "="*60)
print("🌍 ORGANIZATIONS BY COUNTRY")
print("="*60)

country_counts = df['Country'].value_counts()
print(country_counts)

# Category breakdown
print("\n" + "="*60)
print("📚 ORGANIZATIONS BY CATEGORY")
print("="*60)

category_counts = df['Category'].value_counts()
print(category_counts)

# Funding stage breakdown
print("\n" + "="*60)
print("💰 ORGANIZATIONS BY FUNDING STAGE")
print("="*60)

funding_counts = df['Funding stage'].value_counts()
print(funding_counts)

# Summary stats
print("\n" + "="*60)
print("📊 SUMMARY STATISTICS")
print("="*60)

print(f"\n🏢 Organizations: {len(df)}")
print(f"🌍 Countries: {df['Country'].nunique()}")
print(f"📚 Categories: {df['Category'].nunique()}")
print(f"💰 Funding stages: {df['Funding stage'].nunique()}")

# Try to calculate funding stats (handle errors)
try:
    # Convert funding to numeric, forcing errors to NaN
    funding_numeric = pd.to_numeric(df['Total funding(€)'], errors='coerce')
    total_funding = funding_numeric.sum()
    avg_funding = funding_numeric.mean()
    print(f"\n💶 Total funding: €{total_funding:,.0f}")
    print(f"💶 Average funding: €{avg_funding:,.0f}")
    
    # Check if there were conversion issues
    non_numeric_funding = df[pd.to_numeric(df['Total funding(€)'], errors='coerce').isna()]
    if len(non_numeric_funding) > 0:
        print(f"⚠️  Warning: {len(non_numeric_funding)} rows have non-numeric funding values")
except Exception as e:
    print(f"⚠️  Could not calculate funding statistics: {e}")

# Try to calculate employee stats (handle errors)
try:
    # Convert employee count to numeric, forcing errors to NaN
    employees_numeric = pd.to_numeric(df['Employee count'], errors='coerce')
    total_employees = employees_numeric.sum()
    avg_employees = employees_numeric.mean()
    print(f"\n👥 Total employees: {total_employees:,.0f}")
    print(f"👥 Average employees: {avg_employees:.0f}")
    
    # Check if there were conversion issues
    non_numeric_employees = df[pd.to_numeric(df['Employee count'], errors='coerce').isna()]
    if len(non_numeric_employees) > 0:
        print(f"⚠️  Warning: {len(non_numeric_employees)} rows have non-numeric employee counts")
        print("     Examples:")
        for idx, row in non_numeric_employees.head(3).iterrows():
            print(f"     • {row['Organization']}: '{row['Employee count']}'")
except Exception as e:
    print(f"⚠️  Could not calculate employee statistics: {e}")

print("\n" + "="*60)
print("✅ CHECK COMPLETE!")
print("="*60)

# Final verdict
print("\n🎯 FINAL VERDICT:")
if len(duplicates_by_name) == 0 and len(exact_duplicates) == 0:
    print("✅ Your data is CLEAN and READY TO USE!")
    print("✅ No duplicates found!")
    print(f"✅ {len(df)} unique organizations")
    
    # Check for data quality issues
    issues = []
    if missing.sum() > 0:
        issues.append("Some missing values (see above)")
    
    try:
        non_numeric_employees = df[pd.to_numeric(df['Employee count'], errors='coerce').isna()]
        if len(non_numeric_employees) > 0:
            issues.append("Some non-numeric employee counts")
    except:
        pass
    
    try:
        non_numeric_funding = df[pd.to_numeric(df['Total funding(€)'], errors='coerce').isna()]
        if len(non_numeric_funding) > 0:
            issues.append("Some non-numeric funding values")
    except:
        pass
    
    if issues:
        print("\n⚠️  Minor data quality notes:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n💡 These won't prevent your project from working,")
        print("   but you might want to clean them up later.")
else:
    print("⚠️  Please review the duplicates listed above")
    print("⚠️  Clean them up, then run this script again")