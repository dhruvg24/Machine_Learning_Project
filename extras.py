import pandas as pd

# Load the CSV
df = pd.read_csv("artifacts/test.csv")

# Rename columns
df.rename(columns={
    'race/ethnicity': 'race_ethnicity',
    'parental level of education': 'parental_level_of_education',
    'test preparation course': 'test_preparation_course',
    'reading score': 'reading_score',
    'writing score': 'writing_score',
    'math score':'math_score'
}, inplace=True)

# Save the modified CSV
df.to_csv("artifacts/test.csv", index=False)