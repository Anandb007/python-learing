# 📘 Day 35: Train, Validation & Test Sets

## 🎯 Learning Objectives
By the end of today, you will understand:
- Why we NEVER train and evaluate on the same data
- The purpose of Training, Validation, and Test sets
- How to properly split your data
- Common split ratios for different scenarios
- Why this matters in MLOps and LLMOps

---

## 📚 Section 1: Why Do We Split Data?

### 🚨 The Problem: Models Can Cheat!

When building an ML model, we **NEVER** train and evaluate on the same data.

**Why?** Because the model may **cheat** by memorizing!

```
┌─────────────────────────────────────────────────────────────────┐
│                  WHY WE SPLIT DATA                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ❌ WRONG APPROACH:                                             │
│   ─────────────────                                             │
│                                                                 │
│   ┌─────────────────┐      ┌─────────────────┐                 │
│   │   ALL DATA      │      │    MODEL        │                 │
│   │   (100%)        │ ──→  │    TRAINS       │                 │
│   │                 │      │    on ALL       │                 │
│   └─────────────────┘      └────────┬────────┘                 │
│                                     │                           │
│                                     ▼                           │
│                            ┌─────────────────┐                 │
│                            │   EVALUATE      │                 │
│                            │   on SAME data  │                 │
│                            └─────────────────┘                 │
│                                     │                           │
│                                     ▼                           │
│                            "Accuracy: 99%!" 🎉                  │
│                                                                 │
│   BUT WAIT... Model just MEMORIZED the answers!                 │
│   On NEW data → "Accuracy: 45%" 😱                              │
│                                                                 │
│   ───────────────────────────────────────────────────────────   │
│                                                                 │
│   ✅ CORRECT APPROACH:                                           │
│   ───────────────────                                           │
│   Split data into SEPARATE sets with DIFFERENT purposes         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 The Solution: Split Into 3 Parts

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE THREE DATA SPLITS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TOTAL DATASET                                                 │
│   ═══════════════════════════════════════════════════════════   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │  ┌─────────────────┬──────────────┬──────────────┐      │  │
│   │  │   TRAINING      │  VALIDATION  │    TEST      │      │  │
│   │  │     SET         │     SET      │    SET       │      │  │
│   │  │   (60-80%)      │   (10-20%)   │  (10-20%)    │      │  │
│   │  │                 │              │              │      │  │
│   │  │  📚 LEARN       │  🔧 TUNE     │  📝 FINAL    │      │  │
│   │  │                 │              │    EXAM      │      │  │
│   │  └─────────────────┴──────────────┴──────────────┘      │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   Each set has a DIFFERENT purpose!                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 2: Training Set

### 📚 What is the Training Set?

The **Training Set** is the largest portion of data used to **teach** the model patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│                      TRAINING SET                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SIZE: Largest portion (60-80% of total data)                  │
│                                                                 │
│   PURPOSE:                                                      │
│   ─────────                                                     │
│   • Teach the model patterns                                    │
│   • Model sees BOTH input (X) and labels (Y)                    │
│   • Model adjusts its weights to minimize errors                │
│   • Can iterate over this data multiple times (epochs)          │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   Training Data                    Model                  │  │
│   │   ┌──────────────┐               ┌──────────────┐        │  │
│   │   │ Features (X) │               │              │        │  │
│   │   │ CPU: 85%     │  ──────────→  │   LEARNS     │        │  │
│   │   │ Memory: 90%  │               │   PATTERNS   │        │  │
│   │   │ Errors: 50   │               │              │        │  │
│   │   ├──────────────┤               │  Adjusts     │        │  │
│   │   │ Label (Y)    │  ──────────→  │  weights     │        │  │
│   │   │ "Will Fail"  │               │              │        │  │
│   │   └──────────────┘               └──────────────┘        │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🎓 Real-Life Analogy: Textbook Study

```
┌─────────────────────────────────────────────────────────────────┐
│              TRAINING SET = TEXTBOOK STUDY                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   STUDENT ANALOGY:                                              │
│   ─────────────────                                             │
│                                                                 │
│   ┌─────────────┐                                               │
│   │    📚      │                                                │
│   │  TEXTBOOK   │  ← Training Set                               │
│   │             │                                                │
│   │  Problems   │  • Student reads & studies                    │
│   │     +       │  • Sees questions AND answers                 │
│   │  Answers    │  • Learns concepts & methods                  │
│   │             │  • Can review multiple times                  │
│   └─────────────┘                                               │
│                                                                 │
│   EXAMPLE:                                                      │
│   ─────────                                                     │
│   Chapter 1: "2 + 3 = ?" → Answer: 5                           │
│   Chapter 2: "5 × 4 = ?" → Answer: 20                          │
│   Chapter 3: "10 ÷ 2 = ?" → Answer: 5                          │
│                                                                 │
│   Student LEARNS: How addition, multiplication, division work   │
│                                                                 │
│   ✅ This is TRAINING — learning from examples with answers     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 3: Validation Set

### 🔧 What is the Validation Set?

The **Validation Set** is used to **tune** the model and **prevent overfitting**.

```
┌─────────────────────────────────────────────────────────────────┐
│                      VALIDATION SET                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SIZE: Smaller portion (10-20% of total data)                  │
│                                                                 │
│   PURPOSE:                                                      │
│   ─────────                                                     │
│   • Tune model hyperparameters                                  │
│   • Select best model version                                   │
│   • Detect overfitting early                                    │
│   • NOT used for final evaluation                               │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   TRAINING LOOP:                                         │  │
│   │                                                          │  │
│   │   ┌───────────┐     ┌───────────┐     ┌───────────┐     │  │
│   │   │ Train on  │     │ Check on  │     │  Adjust   │     │  │
│   │   │ Training  │ ──→ │Validation │ ──→ │  Model    │     │  │
│   │   │   Set     │     │   Set     │     │  Settings │     │  │
│   │   └───────────┘     └───────────┘     └─────┬─────┘     │  │
│   │         ↑                                    │           │  │
│   │         └────────────────────────────────────┘           │  │
│   │                      (Repeat)                            │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   WHAT WE TUNE:                                                 │
│   ─────────────                                                 │
│   • Learning rate                                               │
│   • Number of layers                                            │
│   • Number of trees (Random Forest)                             │
│   • Regularization strength                                     │
│   • Any hyperparameter!                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📝 Real-Life Analogy: Practice Exams

```
┌─────────────────────────────────────────────────────────────────┐
│             VALIDATION SET = PRACTICE EXAMS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   STUDENT ANALOGY:                                              │
│   ─────────────────                                             │
│                                                                 │
│   ┌─────────────┐                                               │
│   │    📝      │                                                │
│   │  PRACTICE   │  ← Validation Set                             │
│   │   EXAM      │                                                │
│   │             │  • Test your understanding                    │
│   │  Similar to │  • Not the real exam                          │
│   │  real exam  │  • See what you need to improve               │
│   │             │  • Adjust study strategy                      │
│   └─────────────┘                                               │
│                                                                 │
│   EXAMPLE:                                                      │
│   ─────────                                                     │
│   Practice Exam Score: 65%                                      │
│                                                                 │
│   Student thinks:                                               │
│   "I need to study Chapter 3 more"                              │
│   "I should practice more multiplication"                       │
│                                                                 │
│   → ADJUSTS study approach (like tuning hyperparameters)        │
│                                                                 │
│   Practice Exam Again: 82%                                      │
│   "Better! But still need work on division"                     │
│                                                                 │
│   ✅ This is VALIDATION — checking progress & adjusting         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🔍 Detecting Overfitting with Validation Set

```
┌─────────────────────────────────────────────────────────────────┐
│          VALIDATION SET DETECTS OVERFITTING                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SCENARIO: Training over multiple epochs                       │
│                                                                 │
│   Epoch │ Training Acc │ Validation Acc │ Status                │
│   ──────┼──────────────┼────────────────┼───────────────────    │
│     1   │     60%      │      58%       │ 🟢 Learning           │
│     5   │     75%      │      73%       │ 🟢 Improving          │
│    10   │     85%      │      82%       │ 🟢 Good progress      │
│    15   │     92%      │      84%       │ 🟡 Gap growing...     │
│    20   │     97%      │      83%       │ 🔴 OVERFITTING!       │
│    25   │     99%      │      80%       │ 🔴 Getting worse!     │
│                                                                 │
│   VISUALIZATION:                                                │
│   ───────────────                                               │
│                                                                 │
│   Accuracy                                                      │
│     │                          Training ────                    │
│   99│                        ╱────────────                      │
│     │                      ╱                                    │
│   85│              ╱──────╱                                     │
│     │            ╱    ╲───────────── Validation                 │
│   70│          ╱                                                │
│     │        ╱                                                  │
│   55│──────╱                                                    │
│     └────────────────────────────────────────                   │
│       1    5    10   15   20   25    Epochs                     │
│                      ↑                                          │
│                  STOP HERE! (Early Stopping)                    │
│                                                                 │
│   When validation accuracy STOPS improving → STOP TRAINING      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 4: Test Set

### 📝 What is the Test Set?

The **Test Set** is used **ONLY at the end** to measure true performance on completely unseen data.

```
┌─────────────────────────────────────────────────────────────────┐
│                        TEST SET                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SIZE: Final portion (10-20% of total data)                    │
│                                                                 │
│   PURPOSE:                                                      │
│   ─────────                                                     │
│   • Measure TRUE performance on UNSEEN data                     │
│   • Used ONLY ONCE at the very end                              │
│   • Model has NEVER seen this data during training/tuning       │
│   • Gives honest estimate of real-world performance             │
│                                                                 │
│   CRITICAL RULES:                                               │
│   ───────────────                                               │
│   ❌ NEVER use test set to make model decisions                 │
│   ❌ NEVER tune hyperparameters based on test results           │
│   ❌ NEVER look at test set until you're completely done        │
│   ✅ Use ONLY for final evaluation                              │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   WORKFLOW:                                              │  │
│   │                                                          │  │
│   │   Training ──→ Validation ──→ Final Model ──→ TEST      │  │
│   │   (learn)      (tune)         (selected)      (evaluate)│  │
│   │                                                 ↑        │  │
│   │                                         Used ONCE only! │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🎓 Real-Life Analogy: Final Exam

```
┌─────────────────────────────────────────────────────────────────┐
│                TEST SET = FINAL EXAM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   STUDENT ANALOGY:                                              │
│   ─────────────────                                             │
│                                                                 │
│   ┌─────────────┐                                               │
│   │    📋      │                                                │
│   │   FINAL    │  ← Test Set                                    │
│   │   EXAM     │                                                │
│   │             │  • Completely new questions                   │
│   │  Never seen │  • No second chances                          │
│   │  before!    │  • True measure of knowledge                  │
│   │             │  • Happens only ONCE                          │
│   └─────────────┘                                               │
│                                                                 │
│   IMPORTANT:                                                    │
│   ───────────                                                   │
│   • You can't ask to "redo" the final exam                      │
│   • You can't "adjust your study" after seeing it               │
│   • It's the FINAL, honest measure of what you learned          │
│                                                                 │
│   ✅ This is TESTING — final evaluation, no do-overs            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 5: Why Can't We Use Only Training + Test?

### ❌ The Problem with Only 2 Splits

```
┌─────────────────────────────────────────────────────────────────┐
│           PROBLEM: ONLY TRAINING + TEST SETS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   WRONG APPROACH:                                               │
│   ───────────────                                               │
│                                                                 │
│   ┌─────────────────────────┬─────────────────────────┐        │
│   │     TRAINING (80%)      │       TEST (20%)        │        │
│   └─────────────────────────┴─────────────────────────┘        │
│                                                                 │
│   WORKFLOW:                                                     │
│   1. Train model on training data                               │
│   2. Check accuracy on test data                                │
│   3. Test accuracy = 75% → "Not good enough"                    │
│   4. Adjust model (change hyperparameters)                      │
│   5. Check test again → 78%                                     │
│   6. Adjust again...                                            │
│   7. Check test → 82%                                           │
│   8. Keep adjusting based on test results...                    │
│                                                                 │
│   THE PROBLEM:                                                  │
│   ─────────────                                                 │
│   By adjusting based on test results, you're INDIRECTLY         │
│   training on the test set!                                     │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   Test set is no longer "unseen" ❌                       │  │
│   │   Test performance becomes FAKE ❌                        │  │
│   │   You're optimizing FOR the test set ❌                   │  │
│   │   Real-world performance will be WORSE ❌                 │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   It's like practicing with the actual final exam questions!    │
│   Your "score" doesn't reflect true knowledge.                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ✅ The Solution: 3-Way Split

```
┌─────────────────────────────────────────────────────────────────┐
│            SOLUTION: THREE-WAY SPLIT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CORRECT APPROACH:                                             │
│   ─────────────────                                             │
│                                                                 │
│   ┌───────────────────┬─────────────┬─────────────┐            │
│   │  TRAINING (70%)   │ VALID (15%) │ TEST (15%)  │            │
│   └───────────────────┴─────────────┴─────────────┘            │
│                                                                 │
│   WORKFLOW:                                                     │
│   1. Train model on training data                               │
│   2. Check accuracy on VALIDATION data                          │
│   3. Validation = 75% → "Need to improve"                       │
│   4. Adjust model based on validation                           │
│   5. Check validation → 82%                                     │
│   6. Keep tuning using validation...                            │
│   7. When satisfied, FINALLY check TEST                         │
│   8. Test = 80% → TRUE performance!                             │
│                                                                 │
│   WHY THIS WORKS:                                               │
│   ───────────────                                               │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   Test set remains truly UNSEEN ✅                        │  │
│   │   Validation absorbs the "tuning leakage" ✅              │  │
│   │   Test result is HONEST ✅                                │  │
│   │   Real-world performance will be similar ✅               │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 6: Real-Time Example — Loan Approval System

### 🏦 Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│           LOAN APPROVAL ML SYSTEM - DATA SPLITS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TOTAL DATA: 100,000 past loan applications                    │
│                                                                 │
│   ┌───────────────────────────────────────────────────────────┐│
│   │                                                            ││
│   │  ┌───────────────┬─────────────┬─────────────┐            ││
│   │  │   TRAINING    │ VALIDATION  │    TEST     │            ││
│   │  │   70,000      │   15,000    │   15,000    │            ││
│   │  │   (70%)       │   (15%)     │   (15%)     │            ││
│   │  └───────────────┴─────────────┴─────────────┘            ││
│   │                                                            ││
│   └───────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Stage-by-Stage Usage

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRAINING DATA                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   STAGE: Model Training                                         │
│   DATA: 70,000 past loan records with outcomes                  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  Income  │ Credit │ Employment │ Age │ → │  Outcome    │  │
│   ├──────────┼────────┼────────────┼─────┼───┼─────────────┤  │
│   │ $50,000  │  720   │  5 years   │ 35  │ → │  Approved   │  │
│   │ $30,000  │  580   │  1 year    │ 23  │ → │  Rejected   │  │
│   │ $75,000  │  680   │  8 years   │ 42  │ → │  Approved   │  │
│   │ ...      │  ...   │  ...       │ ... │ → │  ...        │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   MODEL LEARNS:                                                 │
│   • Higher income + good credit = likely approved               │
│   • Low credit score = likely rejected                          │
│   • Employment stability matters                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION DATA                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   STAGE: Model Tuning                                           │
│   DATA: 15,000 different loan records                           │
│                                                                 │
│   QUESTIONS WE ANSWER:                                          │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │  • What threshold for credit score works best?           │  │
│   │    Try 650 → 72% accuracy                                │  │
│   │    Try 620 → 75% accuracy ← Better!                      │  │
│   │    Try 700 → 70% accuracy                                │  │
│   │                                                          │  │
│   │  • Should we use Random Forest or XGBoost?               │  │
│   │    Random Forest → 75% accuracy                          │  │
│   │    XGBoost → 78% accuracy ← Better!                      │  │
│   │                                                          │  │
│   │  • How many trees?                                       │  │
│   │    50 trees → 76% accuracy                               │  │
│   │    100 trees → 78% accuracy ← Best!                      │  │
│   │    200 trees → 78% accuracy (no improvement)             │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   FINAL TUNED MODEL: XGBoost, 100 trees, credit threshold 620  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      TEST DATA                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   STAGE: Final Evaluation (ONE TIME ONLY!)                      │
│   DATA: 15,000 completely unseen loan records                   │
│                                                                 │
│   RESULT:                                                       │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   Test Accuracy: 77%                                     │  │
│   │   Test Precision: 82%                                    │  │
│   │   Test Recall: 74%                                       │  │
│   │                                                          │  │
│   │   ✅ This is the TRUE performance expectation             │  │
│   │   ✅ This is what we'll see in production                 │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   DECISION: Model is ready for deployment!                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ✅ What This Ensures

| Benefit | How It's Achieved |
|---------|-------------------|
| **Fairness** | Model doesn't "cheat" by seeing test data |
| **Accuracy** | Test accuracy reflects real-world performance |
| **Generalization** | Model works on truly new applicants |
| **Trust** | Business can trust the reported metrics |

---

## 📚 Section 7: Typical Split Ratios

### 📊 Split Ratios Based on Dataset Size

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPLIT RATIO GUIDE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   SMALL DATASET (< 10,000 samples)                              │
│   ─────────────────────────────────                             │
│   ┌───────────────────┬─────────────┬─────────────┐            │
│   │  TRAINING (70%)   │ VALID (15%) │ TEST (15%)  │            │
│   └───────────────────┴─────────────┴─────────────┘            │
│                                                                 │
│   Why: Need enough validation data to tune properly             │
│                                                                 │
│   ─────────────────────────────────────────────────────────     │
│                                                                 │
│   MEDIUM DATASET (10,000 - 100,000 samples)                     │
│   ──────────────────────────────────────────                    │
│   ┌─────────────────────┬───────────┬───────────┐              │
│   │   TRAINING (80%)    │VALID (10%)│ TEST (10%)│              │
│   └─────────────────────┴───────────┴───────────┘              │
│                                                                 │
│   Why: More training data helps, validation still meaningful    │
│                                                                 │
│   ─────────────────────────────────────────────────────────     │
│                                                                 │
│   LARGE DATASET (> 100,000 samples)                             │
│   ─────────────────────────────────                             │
│   ┌───────────────────────┬─────────┬─────────┐                │
│   │    TRAINING (90%)     │VAL (5%) │TEST (5%)│                │
│   └───────────────────────┴─────────┴─────────┘                │
│                                                                 │
│   Or even: Training + Test only (validation during training)    │
│                                                                 │
│   Why: 5% of 1 million = 50,000 samples (plenty for testing!)  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📋 Quick Reference Table

| Dataset Size | Train | Validation | Test |
|--------------|-------|------------|------|
| Small (< 10K) | 70% | 15% | 15% |
| Medium (10K-100K) | 80% | 10% | 10% |
| Large (> 100K) | 90% | 5% | 5% |
| Very Large (> 1M) | 98% | 1% | 1% |

---

## 📚 Section 8: Why This Matters in MLOps

### 🔄 MLOps Pipeline Integration

```
┌─────────────────────────────────────────────────────────────────┐
│              DATA SPLITS IN MLOps PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PRODUCTION ML PIPELINE:                                       │
│   ───────────────────────                                       │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   📦 Raw Data                                            │  │
│   │       │                                                  │  │
│   │       ▼                                                  │  │
│   │   ┌─────────────┐                                       │  │
│   │   │ Data Split  │ ← Automated split in pipeline         │  │
│   │   └──────┬──────┘                                       │  │
│   │          │                                               │  │
│   │   ┌──────┴──────┬──────────────┐                        │  │
│   │   ▼             ▼              ▼                         │  │
│   │ Training     Validation      Test                        │  │
│   │   │             │              │                         │  │
│   │   ▼             ▼              ▼                         │  │
│   │ ┌──────┐    ┌──────┐     ┌──────┐                       │  │
│   │ │Train │    │Select│     │Final │                       │  │
│   │ │Model │───→│Best  │────→│Eval  │                       │  │
│   │ │Step  │    │Model │     │Step  │                       │  │
│   │ └──────┘    └──────┘     └──────┘                       │  │
│   │                              │                           │  │
│   │                              ▼                           │  │
│   │                     ┌──────────────┐                    │  │
│   │                     │   Deploy?    │                    │  │
│   │                     │ (if metrics  │                    │  │
│   │                     │   pass)      │                    │  │
│   │                     └──────────────┘                    │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   BECOMES PART OF:                                              │
│   ✅ CI/CD for ML                                               │
│   ✅ Model versioning                                           │
│   ✅ Automated model selection                                  │
│   ✅ Model retraining workflows                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 Continuous Monitoring

```
┌─────────────────────────────────────────────────────────────────┐
│              DATA SPLITS + PRODUCTION MONITORING                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   After Deployment:                                             │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   TRAINING DATA ──→ Model trained                        │  │
│   │   VALIDATION DATA ──→ Model tuned                        │  │
│   │   TEST DATA ──→ Model evaluated (77% accuracy)           │  │
│   │                                                          │  │
│   │   PRODUCTION DATA ──→ NEW! Real users                    │  │
│   │                                                          │  │
│   │   Monitor: Is production accuracy similar to test?       │  │
│   │                                                          │  │
│   │   Test Accuracy: 77%                                     │  │
│   │   Prod Accuracy (Week 1): 76% ✅ Good                    │  │
│   │   Prod Accuracy (Week 4): 74% 🟡 Slight drop             │  │
│   │   Prod Accuracy (Week 8): 68% 🔴 Retrain needed!         │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   If production significantly differs from test:                │
│   → Data drift detected                                         │
│   → Model retraining triggered                                  │
│   → New data becomes new training set                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Section 9: Why This Matters in LLMOps

### 🤖 LLM Training & Evaluation

```
┌─────────────────────────────────────────────────────────────────┐
│                DATA SPLITS IN LLMOps                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   FOR FINE-TUNING LLMs:                                         │
│   ─────────────────────                                         │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │   TRAINING PROMPTS                                       │  │
│   │   • Used to fine-tune the model                          │  │
│   │   • Model learns domain-specific patterns                │  │
│   │                                                          │  │
│   │   VALIDATION PROMPTS                                     │  │
│   │   • Tune hyperparameters (learning rate, epochs)         │  │
│   │   • Select best checkpoint                               │  │
│   │   • Detect overfitting to training prompts               │  │
│   │                                                          │  │
│   │   TEST PROMPTS                                           │  │
│   │   • Measure true generalization                          │  │
│   │   • Evaluate quality metrics (BLEU, perplexity)          │  │
│   │   • Check for hallucinations                             │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   CRITICAL FOR:                                                 │
│   ─────────────                                                 │
│   ✅ Preventing hallucination (model doesn't memorize)          │
│   ✅ Ensuring prompt generalization                             │
│   ✅ Detecting overfitting to training text patterns            │
│   ✅ Measuring real-world response quality                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 LLM Evaluation Example

```
┌─────────────────────────────────────────────────────────────────┐
│            LLM FINE-TUNING: CUSTOMER SERVICE BOT                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   TRAINING PROMPTS (1,000):                                     │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  Q: "What is your return policy?"                        │  │
│   │  A: "You can return items within 30 days..."             │  │
│   │                                                          │  │
│   │  Q: "How do I track my order?"                           │  │
│   │  A: "Visit our tracking page at..."                      │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   VALIDATION PROMPTS (200):                                     │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  Q: "Can I get a refund?"                                │  │
│   │  Check: Does model understand it's about returns?        │  │
│   │                                                          │  │
│   │  Q: "Where's my package?"                                │  │
│   │  Check: Does model understand it's about tracking?       │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   TEST PROMPTS (200) - COMPLETELY NEW:                          │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  Q: "I want my money back for the broken item"           │  │
│   │  Expected: Provide return + refund information           │  │
│   │                                                          │  │
│   │  Q: "When will my stuff arrive?"                         │  │
│   │  Expected: Provide tracking information                  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   If test quality drops → Model overfitted to training phrasing │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Day 35 Summary

| Concept | Purpose |
|---------|---------|
| **Training Set** | Teach the model patterns (60-80%) |
| **Validation Set** | Tune hyperparameters, prevent overfitting (10-20%) |
| **Test Set** | Final evaluation on unseen data (10-20%) |
| **Why 3 Splits?** | Prevent indirect training on test data |
| **MLOps Relevance** | CI/CD, model selection, monitoring |
| **LLMOps Relevance** | Prevent hallucination, ensure generalization |

### 🎓 Student Analogy Summary

| ML Concept | Student Analogy |
|------------|-----------------|
| Training Set | Textbook study (problems + answers) |
| Validation Set | Practice exams (check progress, adjust) |
| Test Set | Final exam (one-time, honest evaluation) |

---

## ✅ Day 35 Checklist

- [ ] Understand why we can't train and evaluate on same data
- [ ] Know the purpose of Training Set
- [ ] Know the purpose of Validation Set
- [ ] Know the purpose of Test Set
- [ ] Understand why 2 splits is not enough
- [ ] Know typical split ratios for different dataset sizes
- [ ] Understand how this applies to MLOps pipelines
- [ ] Understand how this applies to LLMOps

---

## 🔜 Next: Day 36

In Day 36, we'll learn about **Linear Regression**:
- The simplest regression algorithm
- How it finds the best fit line
- Mathematical intuition (without complex math)
- Real-world applications

---

> 💡 **Key Takeaway:** Always split your data into Training (learn), Validation (tune), and Test (evaluate) sets. NEVER make model decisions based on test results — that defeats the purpose! The test set should only be used ONCE at the very end for honest evaluation.

**Great job completing Day 35! 🎉**

---

**Ready for Day 36?** Let me know when you want to continue!

