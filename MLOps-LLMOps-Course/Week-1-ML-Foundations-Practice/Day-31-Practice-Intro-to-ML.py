# ============================================================
# 📘 DAY 31 PRACTICE: Introduction to Machine Learning
# ============================================================
# 
# 🎯 LEARNING GOALS:
# - Understand what ML is
# - Learn ML terminology (features, labels, samples)
# - Explore a dataset
# - Understand ML types
#
# ⏱️ TIME: 30-45 minutes
# ============================================================

# ============================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================
# First, we need to import the tools we'll use

print("=" * 60)
print("📚 STEP 1: IMPORTING LIBRARIES")
print("=" * 60)

# numpy: For numerical operations (math with arrays)
import numpy as np

# pandas: For data manipulation (working with tables/dataframes)
import pandas as pd

# matplotlib: For creating visualizations (charts, graphs)
import matplotlib.pyplot as plt

print("✅ Libraries imported successfully!")
print("""
What each library does:
- numpy (np): Math operations on arrays
- pandas (pd): Work with data tables (like Excel)
- matplotlib (plt): Create charts and graphs
""")

# ============================================================
# STEP 2: CREATE YOUR FIRST DATASET
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 2: CREATING A DATASET")
print("=" * 60)

# Let's create a simple house price dataset
# In ML, data is organized in rows and columns

# This is a Python dictionary - keys are column names, values are data
house_data = {
    'Area_sqft': [1000, 1500, 1200, 1800, 2000, 2200, 2500, 1600, 1900, 2100],
    'Bedrooms': [2, 3, 2, 3, 4, 4, 5, 3, 3, 4],
    'Age_years': [10, 5, 15, 3, 8, 2, 1, 12, 7, 4],
    'Price_lakhs': [50, 75, 55, 95, 110, 130, 160, 70, 100, 125]
}

# Convert dictionary to a DataFrame (like an Excel table)
df = pd.DataFrame(house_data)

print("\n📋 Here's our dataset:")
print(df)

print(f"""
📌 UNDERSTANDING THE DATASET:
- We have {len(df)} rows (each row = one house = one SAMPLE)
- We have {len(df.columns)} columns (properties of each house)
""")

# ============================================================
# STEP 3: UNDERSTAND ML TERMINOLOGY
# ============================================================
print("\n" + "=" * 60)
print("🔤 STEP 3: ML TERMINOLOGY")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│                   ML TERMINOLOGY                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SAMPLE (Row):                                              │
│  → One example in our data                                  │
│  → Example: One house's information                         │
│                                                             │
│  FEATURE (Input Column):                                    │
│  → What we USE to make predictions                          │
│  → Example: Area, Bedrooms, Age                             │
│                                                             │
│  LABEL (Output Column):                                     │
│  → What we WANT to predict                                  │
│  → Example: Price                                           │
│                                                             │
│  DATASET:                                                   │
│  → Collection of all samples                                │
│  → Example: All 10 houses                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# Let's identify these in our data
print("🔍 In our dataset:")
print(f"   • Number of SAMPLES: {len(df)}")
print(f"   • FEATURES: Area_sqft, Bedrooms, Age_years")
print(f"   • LABEL (what we predict): Price_lakhs")

# Separate features and label
features = df[['Area_sqft', 'Bedrooms', 'Age_years']]  # X
label = df['Price_lakhs']  # y

print("\n📊 FEATURES (X) - What we use to predict:")
print(features)

print("\n🎯 LABEL (y) - What we want to predict:")
print(label.tolist())

# ============================================================
# STEP 4: EXPLORE THE DATA
# ============================================================
print("\n" + "=" * 60)
print("🔍 STEP 4: EXPLORING THE DATA")
print("=" * 60)

# Basic statistics
print("\n📈 Basic Statistics:")
print(df.describe())

print("""
📌 What these statistics mean:
- count: Number of values
- mean: Average value
- std: Standard deviation (how spread out the values are)
- min: Smallest value
- 25%: 25th percentile (25% of values are below this)
- 50%: Median (middle value)
- 75%: 75th percentile
- max: Largest value
""")

# Data types
print("\n📋 Data Types:")
print(df.dtypes)

# Check for missing values
print("\n❓ Missing Values:")
print(df.isnull().sum())
print("✅ No missing values!" if df.isnull().sum().sum() == 0 else "⚠️ Has missing values!")

# ============================================================
# STEP 5: VISUALIZE THE DATA
# ============================================================
print("\n" + "=" * 60)
print("📊 STEP 5: VISUALIZING THE DATA")
print("=" * 60)

# Create a figure with multiple plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Area vs Price (Scatter plot)
axes[0, 0].scatter(df['Area_sqft'], df['Price_lakhs'], color='blue', alpha=0.7)
axes[0, 0].set_xlabel('Area (sqft)')
axes[0, 0].set_ylabel('Price (Lakhs)')
axes[0, 0].set_title('Area vs Price')
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Bedrooms vs Price
axes[0, 1].scatter(df['Bedrooms'], df['Price_lakhs'], color='green', alpha=0.7)
axes[0, 1].set_xlabel('Bedrooms')
axes[0, 1].set_ylabel('Price (Lakhs)')
axes[0, 1].set_title('Bedrooms vs Price')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Price distribution (Histogram)
axes[1, 0].hist(df['Price_lakhs'], bins=5, color='orange', edgecolor='black')
axes[1, 0].set_xlabel('Price (Lakhs)')
axes[1, 0].set_ylabel('Count')
axes[1, 0].set_title('Price Distribution')

# Plot 4: Area distribution (Histogram)
axes[1, 1].hist(df['Area_sqft'], bins=5, color='purple', edgecolor='black')
axes[1, 1].set_xlabel('Area (sqft)')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Area Distribution')

plt.tight_layout()
plt.savefig('day31_visualization.png', dpi=100)
plt.show()

print("✅ Visualization created and saved as 'day31_visualization.png'")

# ============================================================
# STEP 6: UNDERSTAND ML TYPES
# ============================================================
print("\n" + "=" * 60)
print("🎓 STEP 6: TYPES OF MACHINE LEARNING")
print("=" * 60)

print("""
┌─────────────────────────────────────────────────────────────┐
│              THREE TYPES OF MACHINE LEARNING                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ SUPERVISED LEARNING                                     │
│     → We have INPUT data AND correct ANSWERS (labels)       │
│     → Model learns from examples with known outcomes        │
│     → Examples:                                             │
│       • Predicting house prices (we know past prices)       │
│       • Email spam detection (we know which are spam)       │
│                                                             │
│  2️⃣ UNSUPERVISED LEARNING                                   │
│     → We have INPUT data but NO labels                      │
│     → Model finds hidden patterns on its own                │
│     → Examples:                                             │
│       • Customer segmentation (grouping similar customers)  │
│       • Anomaly detection (finding unusual patterns)        │
│                                                             │
│  3️⃣ REINFORCEMENT LEARNING                                  │
│     → Model learns by trial and error                       │
│     → Gets rewards for good actions, penalties for bad      │
│     → Examples:                                             │
│       • Game-playing AI (AlphaGo, Chess)                    │
│       • Self-driving cars                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# ============================================================
# STEP 7: PRACTICE QUIZ
# ============================================================
print("\n" + "=" * 60)
print("📝 STEP 7: PRACTICE QUIZ")
print("=" * 60)

print("""
Answer these questions based on what you learned:

Q1: In our house dataset, what are the FEATURES?
    A) Price
    B) Area, Bedrooms, Age
    C) House number

Q2: What is the LABEL (what we want to predict)?
    A) Area
    B) Bedrooms
    C) Price

Q3: Predicting house prices is which type of ML?
    A) Supervised Learning
    B) Unsupervised Learning
    C) Reinforcement Learning

Q4: How many SAMPLES are in our dataset?
    A) 4
    B) 10
    C) 100

Q5: If we're predicting a NUMBER (like price), it's called:
    A) Classification
    B) Regression
    C) Clustering
""")

print("\n" + "=" * 60)
print("✅ ANSWERS")
print("=" * 60)
print("""
Q1: B) Area, Bedrooms, Age (Features are inputs)
Q2: C) Price (Label is what we predict)
Q3: A) Supervised Learning (we have prices as labels)
Q4: B) 10 (10 rows = 10 houses)
Q5: B) Regression (predicting numbers)
""")

# ============================================================
# STEP 8: HANDS-ON EXERCISE
# ============================================================
print("\n" + "=" * 60)
print("💪 STEP 8: YOUR TURN - HANDS-ON EXERCISE")
print("=" * 60)

print("""
🎯 EXERCISE: Create your own dataset!

1. Create a dataset about CARS with these columns:
   - Engine_CC (engine size)
   - Year (manufacturing year)
   - Mileage_kmpl (fuel efficiency)
   - Price_lakhs (car price)

2. Add at least 8 cars

3. Identify:
   - What are the FEATURES?
   - What is the LABEL?
   - How many SAMPLES?

4. Calculate:
   - Average price
   - Minimum and Maximum engine size

TRY IT YOURSELF! (Uncomment and modify the code below)
""")

# YOUR CODE HERE:
# ---------------
# car_data = {
#     'Engine_CC': [...],
#     'Year': [...],
#     'Mileage_kmpl': [...],
#     'Price_lakhs': [...]
# }
# car_df = pd.DataFrame(car_data)
# print(car_df)
# print(f"Average price: {car_df['Price_lakhs'].mean()}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📋 DAY 31 SUMMARY")
print("=" * 60)

print("""
✅ What you learned today:

1. LIBRARIES:
   - numpy: Math operations
   - pandas: Data manipulation
   - matplotlib: Visualization

2. TERMINOLOGY:
   - Sample: One row of data
   - Feature: Input columns (X)
   - Label: Output column (y)
   - Dataset: Collection of samples

3. DATA EXPLORATION:
   - df.describe(): Statistics
   - df.isnull(): Check missing values
   - Visualization with matplotlib

4. ML TYPES:
   - Supervised: Has labels
   - Unsupervised: No labels
   - Reinforcement: Trial and error

5. PROBLEM TYPES:
   - Regression: Predict numbers
   - Classification: Predict categories

🎉 Great job completing Day 31!
""")


