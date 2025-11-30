# 📚 Week 1: ML Foundations Practice

## 🎯 Overview

This folder contains hands-on practice exercises for Week 1 (Days 31-37) of the MLOps & LLMOps Learning Course.

## 📁 Folder Structure

```
Week-1-ML-Foundations-Practice/
├── README.md                              ← You are here
├── Day-31-Practice-Intro-to-ML.py         ← ML Basics & Terminology
├── Day-32-Practice-Supervised-Learning.py ← First ML Model
├── Day-33-34-Practice-Bias-Variance.py    ← Bias & Variance
├── Day-35-36-Practice-Evaluation.py       ← Train-Test & Metrics
├── Day-37-Practice-Regularization.py      ← Regularization
└── Week-1-Complete-Practice.py            ← Complete Project
```

## 🚀 How to Use

### Step 1: Setup
Make sure you have the required libraries installed:

```bash
pip install numpy pandas matplotlib scikit-learn
```

### Step 2: Run Practice Files
Work through the files in order:

| Day | File | Concepts |
|-----|------|----------|
| 31 | `Day-31-Practice-Intro-to-ML.py` | ML basics, terminology, data exploration |
| 32 | `Day-32-Practice-Supervised-Learning.py` | Supervised learning, first model |
| 33-34 | `Day-33-34-Practice-Bias-Variance.py` | Bias, variance, overfitting |
| 35-36 | `Day-35-36-Practice-Evaluation.py` | Train-test split, metrics |
| 37 | `Day-37-Practice-Regularization.py` | Ridge, Lasso regularization |

### Step 3: Complete Project
After completing individual days, run the complete project:

```bash
python Week-1-Complete-Practice.py
```

## 📋 Learning Checklist

### Day 31: Introduction to ML
- [ ] Understand what ML is
- [ ] Know the difference between features (X) and labels (y)
- [ ] Create a dataset with pandas
- [ ] Explore data with df.describe()
- [ ] Create visualizations with matplotlib

### Day 32: Supervised Learning
- [ ] Understand supervised learning concept
- [ ] Know Classification vs Regression
- [ ] Build first Linear Regression model
- [ ] Make predictions with model.predict()
- [ ] Understand the ML workflow

### Day 33-34: Bias & Variance
- [ ] Understand what Bias is (underfitting)
- [ ] Understand what Variance is (overfitting)
- [ ] Visualize the difference
- [ ] Diagnose from train vs test scores
- [ ] Know how to fix each problem

### Day 35-36: Evaluation
- [ ] Perform train-test split
- [ ] Understand MAE, MSE, RMSE
- [ ] Understand R² Score
- [ ] Interpret model performance
- [ ] Visualize predictions

### Day 37: Regularization
- [ ] Understand why regularization is needed
- [ ] Know difference between L1 (Lasso) and L2 (Ridge)
- [ ] Apply regularization in code
- [ ] Tune alpha parameter
- [ ] Analyze feature importance

## 💡 Tips

1. **Run each file completely** - Don't skip sections
2. **Read the output** - The files explain what's happening
3. **Try the exercises** - Each file has practice exercises
4. **Check the visualizations** - PNG files are saved for review
5. **Modify the code** - Experiment with different parameters

## 📊 Expected Output Files

After running the practice files, you'll generate:
- `day31_visualization.png`
- `day32_scatter.png`
- `day32_prediction.png`
- `day33_34_bias_variance.png`
- `day33_34_dartboard.png`
- `day35_36_evaluation.png`
- `day37_alpha_effect.png`
- `day37_weights.png`
- `week1_eda.png`
- `week1_bias_variance.png`
- `week1_feature_importance.png`
- `week1_final_results.png`

## 🎯 Key Concepts Summary

| Concept | Key Points |
|---------|------------|
| **Features (X)** | Input variables used for prediction |
| **Labels (y)** | Output we want to predict |
| **Train-Test Split** | 80% train, 20% test (typical) |
| **Bias** | Model too simple → underfits |
| **Variance** | Model too complex → overfits |
| **MAE** | Average absolute error (lower = better) |
| **R²** | Variance explained (higher = better, max 1.0) |
| **Ridge (L2)** | Shrinks weights |
| **Lasso (L1)** | Removes features |

## 🎉 Completion

After completing all exercises:
1. You should understand fundamental ML concepts
2. You can build and evaluate regression models
3. You know how to prevent overfitting
4. You're ready for Week 2: ML Algorithms!

---

**Happy Learning! 🚀**




