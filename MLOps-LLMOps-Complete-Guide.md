# 🚀 Complete MLOps & LLMOps Learning Guide
## Phase 2 & Phase 3 (Days 31-90) | Beginner → Advanced

> **Target Audience:** DevOps/Cloud Engineers transitioning to ML/LLM  
> **Time Commitment:** 4 hours/day  
> **Total Duration:** 60 days (Phase 2 + Phase 3)

---

# 📘 PHASE 2: Machine Learning (Beginner → Advanced)
## Days 31-60 | ~120 Hours Total

This phase takes you from zero ML knowledge to confidently building ML projects.

---

## 🗓️ WEEK 1 (Days 31-37) — ML Foundations

### 🎯 Week Goals
- Understand ML types and workflow
- Master data preprocessing
- Learn feature engineering
- Understand model evaluation

---

### Day 31 — Introduction to Machine Learning

#### 📚 Topics to Learn
| Topic | Description |
|-------|-------------|
| What is ML? | Machines learning patterns from data |
| Types of ML | Supervised, Unsupervised, Reinforcement |
| Dataset Concepts | Labels, Features, Samples |
| ML Workflow | Data → Preprocess → Train → Evaluate → Deploy |

#### 🛠️ Hands-on Exercise
```
✏️ Identify 5 ML use-cases in:
   - Banking (fraud detection, credit scoring)
   - E-commerce (recommendations, pricing)
   - Healthcare (diagnosis, drug discovery)
```

#### 📦 Deliverable
- Document: "ML Types & Real-World Applications" (1 page)

---

### Day 32 — Understanding Data

#### 📚 Topics to Learn
| Data Type | Examples |
|-----------|----------|
| Tabular | CSV, Excel, SQL tables |
| Text | Documents, tweets, reviews |
| Image | Photos, medical scans |
| Time-series | Stock prices, sensor data |

#### 🛠️ Hands-on Exercise
```python
import pandas as pd

# Load and explore dataset
df = pd.read_csv('your_dataset.csv')

# Basic exploration
print(df.info())          # Data types, non-null counts
print(df.describe())      # Statistical summary
print(df.isnull().sum())  # Missing values
print(df.duplicated().sum())  # Duplicates
```

#### 📦 Deliverable
- Jupyter notebook with EDA of any public dataset

---

### Day 33 — Data Cleaning

#### 📚 Topics to Learn

**1. Handling Missing Values**
```python
# Methods
df.fillna(df.mean())           # Fill with mean
df.fillna(df.median())         # Fill with median
df.dropna()                    # Drop rows
from sklearn.impute import KNNImputer  # KNN imputation
```

**2. Encoding Categorical Variables**
```python
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Label Encoding (ordinal)
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# One-Hot Encoding (nominal)
df_encoded = pd.get_dummies(df, columns=['category'])
```

**3. Feature Scaling**
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standardization (mean=0, std=1)
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[['feature1', 'feature2']])

# Normalization (0-1 range)
minmax = MinMaxScaler()
df_normalized = minmax.fit_transform(df[['feature1', 'feature2']])
```

#### 📦 Deliverable
- Clean a housing dataset (handle missing values, encode, scale)

---

### Day 34 — Feature Engineering

#### 📚 Topics to Learn

| Technique | Description |
|-----------|-------------|
| Feature Selection | Remove irrelevant/redundant features |
| Polynomial Features | Create interaction terms (x₁ × x₂) |
| Binning | Convert continuous to categorical |
| Feature Importance | Identify most predictive features |

#### 🛠️ Hands-on Exercise
```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Correlation matrix
correlation = df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.show()

# Feature importance (after training a model)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
importance = pd.Series(model.feature_importances_, index=X.columns)
importance.sort_values(ascending=False).plot(kind='bar')
```

#### 📦 Deliverable
- Feature engineering notebook with correlation analysis

---

### Day 35 — Train-Test Split & Cross-Validation

#### 📚 Topics to Learn

| Concept | Description |
|---------|-------------|
| Overfitting | Model memorizes training data |
| Underfitting | Model too simple to capture patterns |
| Bias-Variance Tradeoff | Balance between simplicity and complexity |
| Data Leakage | Training data "leaks" into test set |

#### 🛠️ Hands-on Exercise
```python
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

# Simple split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# K-Fold Cross Validation
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
scores = cross_val_score(model, X, y, cv=5)
print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")

# Stratified K-Fold (for imbalanced data)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

#### 📦 Deliverable
- Implement 5-fold cross-validation on any classification dataset

---

### Day 36 — Evaluation Metrics

#### 📚 Classification Metrics

| Metric | Formula | When to Use |
|--------|---------|-------------|
| Accuracy | (TP+TN)/(Total) | Balanced classes |
| Precision | TP/(TP+FP) | Minimize false positives |
| Recall | TP/(TP+FN) | Minimize false negatives |
| F1-Score | 2×(P×R)/(P+R) | Balance precision/recall |
| ROC-AUC | Area under ROC curve | Overall ranking ability |

#### 📚 Regression Metrics

| Metric | Description |
|--------|-------------|
| MAE | Mean Absolute Error |
| MSE | Mean Squared Error |
| RMSE | Root Mean Squared Error |
| R² | Coefficient of determination |

#### 🛠️ Hands-on Exercise
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)

# Classification
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall: {recall_score(y_test, y_pred):.3f}")
print(f"F1: {f1_score(y_test, y_pred):.3f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d')
```

#### 📦 Deliverable
- Evaluation report for a logistic regression model

---

### Day 37 — Build Your First ML Model

#### 🛠️ Complete Pipeline
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Load data
df = pd.read_csv('data.csv')

# 2. Prepare features and target
X = df.drop('target', axis=1)
y = df['target']

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 4. Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# 6. Predict & Evaluate
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

#### 📦 Deliverable
- End-to-end ML pipeline notebook

---

## 🗓️ WEEK 2 (Days 38-44) — Supervised Learning Algorithms

### 🎯 Week Goals
- Master core ML algorithms
- Understand when to use each algorithm
- Build practical projects

---

### Day 38 — Linear Regression

#### 📚 Key Concepts
- **Line of best fit:** y = mx + b
- **Gradient Descent:** Optimization algorithm
- **Regularization:** L1 (Lasso), L2 (Ridge)

#### 🛠️ Hands-on
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso

# Basic Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Coefficients: {model.coef_}")
print(f"Intercept: {model.intercept_}")

# Ridge Regression (L2)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Lasso Regression (L1)
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
```

#### 📦 Project: House Price Prediction

---

### Day 39 — Logistic Regression

#### 📚 Key Concepts
- **Sigmoid function:** Converts output to probability (0-1)
- **Decision boundary:** Threshold for classification
- **Odds ratio:** Interpretation of coefficients

#### 🛠️ Hands-on
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Probability predictions
probabilities = model.predict_proba(X_test)
```

#### 📦 Project: Customer Churn Prediction

---

### Day 40 — Decision Trees

#### 📚 Key Concepts
| Concept | Description |
|---------|-------------|
| Gini Impurity | Measure of node purity |
| Entropy | Information gain measure |
| Pruning | Prevent overfitting |
| Max Depth | Control tree complexity |

#### 🛠️ Hands-on
```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

model = DecisionTreeClassifier(max_depth=5, min_samples_split=10)
model.fit(X_train, y_train)

# Visualize tree
plt.figure(figsize=(20, 10))
plot_tree(model, feature_names=X.columns, filled=True)
plt.show()
```

#### 📦 Project: Fraud Detection

---

### Day 41 — Random Forest

#### 📚 Key Concepts
- **Bagging:** Bootstrap Aggregating
- **Feature Importance:** Which features matter most
- **Out-of-Bag Score:** Built-in validation

#### 🛠️ Hands-on
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    oob_score=True
)
model.fit(X_train, y_train)

print(f"OOB Score: {model.oob_score_:.3f}")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
```

#### 📦 Project: Loan Approval Prediction

---

### Day 42 — Gradient Boosting

#### 📚 Key Concepts
| Algorithm | Strength |
|-----------|----------|
| XGBoost | Speed, regularization |
| LightGBM | Large datasets, categorical features |
| CatBoost | Handles categorical natively |

#### 🛠️ Hands-on
```python
# XGBoost
from xgboost import XGBClassifier
xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
xgb.fit(X_train, y_train)

# LightGBM
from lightgbm import LGBMClassifier
lgbm = LGBMClassifier(n_estimators=100, learning_rate=0.1)
lgbm.fit(X_train, y_train)

# CatBoost
from catboost import CatBoostClassifier
cat = CatBoostClassifier(iterations=100, learning_rate=0.1, verbose=0)
cat.fit(X_train, y_train)
```

#### 📦 Project: Kaggle Titanic Challenge

---

### Day 43 — Support Vector Machines (SVM)

#### 📚 Key Concepts
- **Hyperplane:** Decision boundary
- **Margin:** Distance from hyperplane to nearest points
- **Kernels:** Linear, RBF, Polynomial

#### 🛠️ Hands-on
```python
from sklearn.svm import SVC

# Linear kernel
svm_linear = SVC(kernel='linear')
svm_linear.fit(X_train, y_train)

# RBF kernel (non-linear)
svm_rbf = SVC(kernel='rbf', C=1.0, gamma='scale')
svm_rbf.fit(X_train, y_train)
```

---

### Day 44 — k-Nearest Neighbors (kNN)

#### 📚 Key Concepts
- **Distance Metrics:** Euclidean, Manhattan, Cosine
- **k Value:** Number of neighbors
- **Curse of Dimensionality:** Performance degrades in high dimensions

#### 🛠️ Hands-on
```python
from sklearn.neighbors import KNeighborsClassifier

# Find optimal k
from sklearn.model_selection import cross_val_score
k_range = range(1, 31)
k_scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5)
    k_scores.append(scores.mean())

# Plot k vs accuracy
plt.plot(k_range, k_scores)
plt.xlabel('k')
plt.ylabel('Cross-Validation Accuracy')
```

#### 📦 Project: Movie Recommendation System (Content-Based)

---

## 🗓️ WEEK 3 (Days 45-51) — Unsupervised Learning

### 🎯 Week Goals
- Master clustering algorithms
- Learn dimensionality reduction
- Understand association rules

---

### Day 45 — Clustering Basics

#### 📚 When to Use Clustering
- Customer segmentation
- Anomaly detection
- Document grouping
- Image compression

---

### Day 46 — K-Means Clustering

#### 📚 Key Concepts
- **Centroids:** Cluster centers
- **Elbow Method:** Find optimal k
- **Silhouette Score:** Measure cluster quality

#### 🛠️ Hands-on
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Find optimal k using elbow method
inertias = []
K_range = range(2, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

plt.plot(K_range, inertias, 'bx-')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.title('Elbow Method')

# Final model
kmeans = KMeans(n_clusters=4, random_state=42)
labels = kmeans.fit_predict(X)
print(f"Silhouette Score: {silhouette_score(X, labels):.3f}")
```

#### 📦 Project: Customer Segmentation

---

### Day 47 — Hierarchical Clustering

#### 🛠️ Hands-on
```python
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

# Create dendrogram
linkage_matrix = linkage(X, method='ward')
plt.figure(figsize=(12, 6))
dendrogram(linkage_matrix)
plt.title('Hierarchical Clustering Dendrogram')

# Agglomerative clustering
agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = agg.fit_predict(X)
```

---

### Day 48 — DBSCAN

#### 📚 Key Concepts
- **Density-based:** Finds clusters of arbitrary shape
- **eps:** Maximum distance between points
- **min_samples:** Minimum points to form cluster
- **Handles outliers:** Labels noise as -1

#### 🛠️ Hands-on
```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)

# Number of clusters (excluding noise)
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)
print(f"Clusters: {n_clusters}, Noise points: {n_noise}")
```

---

### Day 49 — PCA (Principal Component Analysis)

#### 📚 Key Concepts
- **Dimensionality Reduction:** Reduce features while preserving variance
- **Explained Variance:** How much information each component holds
- **Eigenvectors:** Directions of maximum variance

#### 🛠️ Hands-on
```python
from sklearn.decomposition import PCA

# Reduce to 2 components for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {sum(pca.explained_variance_ratio_):.3f}")

# Find optimal components (95% variance)
pca_full = PCA(n_components=0.95)
X_reduced = pca_full.fit_transform(X)
print(f"Components needed for 95% variance: {pca_full.n_components_}")
```

---

### Day 50 — t-SNE & UMAP

#### 🛠️ Hands-on
```python
# t-SNE
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X)

# UMAP (install: pip install umap-learn)
import umap
reducer = umap.UMAP(n_components=2, random_state=42)
X_umap = reducer.fit_transform(X)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='viridis')
axes[0].set_title('t-SNE')
axes[1].scatter(X_umap[:, 0], X_umap[:, 1], c=labels, cmap='viridis')
axes[1].set_title('UMAP')
```

---

### Day 51 — Association Rules (Market Basket Analysis)

#### 📚 Key Concepts
| Metric | Description |
|--------|-------------|
| Support | Frequency of itemset |
| Confidence | P(B\|A) - If A, then B |
| Lift | Strength of association |

#### 🛠️ Hands-on
```python
# pip install mlxtend
from mlxtend.frequent_patterns import apriori, association_rules

# Create transaction matrix (one-hot encoded)
frequent_items = apriori(basket_df, min_support=0.01, use_colnames=True)

# Generate rules
rules = association_rules(frequent_items, metric="lift", min_threshold=1.0)
rules = rules.sort_values('lift', ascending=False)
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
```

#### 📦 Project: Retail Market Basket Analysis

---

## 🗓️ WEEK 4 (Days 52-58) — Deep Learning Basics

### 🎯 Week Goals
- Understand neural networks
- Learn PyTorch fundamentals
- Build CNN and RNN models

---

### Day 52 — Introduction to Deep Learning

#### 📚 Key Concepts
| Concept | Description |
|---------|-------------|
| ML vs DL | DL = many layers, automatic feature extraction |
| Tensors | Multi-dimensional arrays |
| GPU vs CPU | GPUs excel at parallel matrix operations |

#### 🛠️ Setup
```python
# Install PyTorch
# pip install torch torchvision

import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Tensor basics
x = torch.tensor([[1, 2], [3, 4]])
print(x.shape)  # torch.Size([2, 2])
```

---

### Day 53 — Neural Network Fundamentals

#### 📚 Key Concepts
- **Perceptron:** Single neuron
- **Activation Functions:** ReLU, Sigmoid, Tanh, Softmax
- **Loss Functions:** MSE, Cross-Entropy

#### 🛠️ Simple NN from Scratch
```python
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Simple 2-layer network
class SimpleNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
    
    def forward(self, X):
        self.z1 = np.dot(X, self.W1)
        self.a1 = sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2)
        self.a2 = sigmoid(self.z2)
        return self.a2
```

---

### Day 54 — Backpropagation & Optimizers

#### 📚 Key Concepts
| Optimizer | Description |
|-----------|-------------|
| SGD | Basic gradient descent |
| Momentum | Accelerates SGD |
| Adam | Adaptive learning rate (most popular) |
| RMSprop | Adaptive, good for RNNs |

#### 🛠️ PyTorch Optimizers
```python
import torch.optim as optim

model = MyModel()
optimizer = optim.Adam(model.parameters(), lr=0.001)
# optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Training step
optimizer.zero_grad()  # Clear gradients
loss.backward()        # Compute gradients
optimizer.step()       # Update weights
```

---

### Day 55 — Build a Neural Network in PyTorch

#### 🛠️ Complete Example
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

# Create model
model = NeuralNetwork(input_size=10, hidden_size=64, num_classes=2)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(100):
    for batch_X, batch_y in dataloader:
        # Forward pass
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

---

### Day 56 — Convolutional Neural Networks (CNN)

#### 📚 Key Concepts
| Component | Description |
|-----------|-------------|
| Convolution | Filter slides over image, extracts features |
| Pooling | Reduces spatial dimensions |
| Feature Maps | Output of convolution layers |
| Flatten | Convert 2D to 1D for dense layers |

#### 🛠️ MNIST CNN
```python
import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.25)
    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 28x28 -> 14x14
        x = self.pool(F.relu(self.conv2(x)))  # 14x14 -> 7x7
        x = x.view(-1, 64 * 7 * 7)            # Flatten
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
```

#### 📦 Project: MNIST Digit Classification

---

### Day 57 — Transfer Learning

#### 📚 Pre-trained Models
- **VGG:** Simple, easy to understand
- **ResNet:** Skip connections, very deep
- **EfficientNet:** Best accuracy/efficiency tradeoff

#### 🛠️ Hands-on
```python
import torchvision.models as models
import torch.nn as nn

# Load pretrained ResNet
model = models.resnet18(pretrained=True)

# Freeze all layers
for param in model.parameters():
    param.requires_grad = False

# Replace final layer for your task
num_classes = 5
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Only train the final layer
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
```

#### 📦 Project: Custom Image Classification

---

### Day 58 — Recurrent Neural Networks (RNN/LSTM)

#### 📚 Key Concepts
| Type | Use Case |
|------|----------|
| RNN | Simple sequences |
| LSTM | Long sequences (solves vanishing gradient) |
| GRU | Simpler LSTM alternative |

#### 🛠️ LSTM Example
```python
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])  # Last time step
        return out
```

---

## 🗓️ Days 59-60 — ML Capstone Projects

### 📦 Project 1: Credit Card Fraud Detection (Classification)

**Requirements:**
- Handle imbalanced data (SMOTE, class weights)
- Feature engineering
- Model comparison (Logistic Regression, Random Forest, XGBoost)
- Evaluation with Precision, Recall, F1, ROC-AUC
- Save model with pickle

### 📦 Project 2: House Price Prediction (Regression)

**Requirements:**
- Comprehensive EDA
- Feature engineering (polynomial features, encoding)
- Model comparison (Linear, Ridge, Lasso, Random Forest)
- Evaluation with MAE, RMSE, R²
- Hyperparameter tuning with GridSearchCV

```python
import pickle

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load model
with open('model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)
```

---

# 📗 PHASE 3: MLOps + LLMOps (Days 61-90)
## Production-Ready ML/LLM Systems | ~120 Hours Total

This phase takes you from ML notebooks to production-grade systems.

---

## 🗓️ WEEK A (Days 61-67) — MLOps Foundations & Model Lifecycle

### 🎯 Week Goals
- Understand MLOps scope and challenges
- Master experiment tracking
- Learn data and model versioning
- Set up feature stores

---

### Day 61 — Introduction to MLOps

#### 📚 Topics

**MLOps Lifecycle:**
```
┌─────────────────────────────────────────────────────────┐
│  Data → Feature Eng → Train → Validate → Deploy → Monitor  │
│    ↑                                              │        │
│    └──────────── Retrain ←───────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

**Production ML Challenges:**
| Challenge | Description |
|-----------|-------------|
| Reproducibility | Same code + data = same model |
| Data Drift | Input distribution changes over time |
| Model Decay | Model performance degrades |
| Technical Debt | ML systems accumulate debt faster |

#### 📦 Deliverable
- Document: "ML Lifecycle & Failure Modes" (1 page)

---

### Day 62 — Experiment Tracking with MLflow

#### 🛠️ Setup & Usage
```bash
# Install
pip install mlflow

# Start UI
mlflow ui --port 5000
```

```python
import mlflow
import mlflow.sklearn

# Start experiment
mlflow.set_experiment("house-price-prediction")

with mlflow.start_run(run_name="random_forest_v1"):
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)
    
    # Log metrics
    y_pred = model.predict(X_test)
    mlflow.log_metric("rmse", np.sqrt(mean_squared_error(y_test, y_pred)))
    mlflow.log_metric("r2", r2_score(y_test, y_pred))
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
```

#### 📦 Deliverable
- MLflow experiment with at least 3 runs

---

### Day 63 — Model Registry & Versioning

#### 🛠️ MLflow Model Registry
```python
import mlflow
from mlflow.tracking import MlflowClient

# Register model
model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, "HousePriceModel")

# Transition stages
client = MlflowClient()
client.transition_model_version_stage(
    name="HousePriceModel",
    version=1,
    stage="Staging"
)

# Promote to production
client.transition_model_version_stage(
    name="HousePriceModel",
    version=1,
    stage="Production"
)

# Load production model
model = mlflow.pyfunc.load_model("models:/HousePriceModel/Production")
```

#### 📦 Deliverable
- Model registered with Staging and Production stages

---

### Day 64 — Data Versioning with DVC

#### 🛠️ Setup & Usage
```bash
# Install
pip install dvc dvc-s3  # or dvc-gdrive, dvc-azure

# Initialize
git init
dvc init

# Add remote storage
dvc remote add -d myremote s3://my-bucket/dvc

# Track data
dvc add data/training_data.csv
git add data/training_data.csv.dvc data/.gitignore
git commit -m "Add training data v1"

# Push data to remote
dvc push

# Pull data
dvc pull
```

#### 📦 Deliverable
- Dataset versioned with DVC, linked to model run

---

### Day 65 — Feature Stores

#### 📚 Key Concepts
| Feature Type | Description |
|--------------|-------------|
| Offline Features | Batch computed, used for training |
| Online Features | Real-time, used for inference |

#### 🛠️ Simple Feature Store (Feast)
```python
# pip install feast

# feature_repo/feature_definition.py
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from datetime import timedelta

# Define entity
customer = Entity(name="customer_id", value_type=ValueType.INT64)

# Define feature source
customer_features_source = FileSource(
    path="data/customer_features.parquet",
    timestamp_field="event_timestamp"
)

# Define feature view
customer_features = FeatureView(
    name="customer_features",
    entities=["customer_id"],
    ttl=timedelta(days=1),
    features=[
        Feature(name="total_purchases", dtype=ValueType.FLOAT),
        Feature(name="avg_purchase_value", dtype=ValueType.FLOAT),
    ],
    online=True,
    source=customer_features_source
)
```

---

### Day 66 — Data Validation with Great Expectations

#### 🛠️ Setup & Usage
```bash
pip install great_expectations
great_expectations init
```

```python
import great_expectations as gx

context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite("training_data_suite")

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="training_data_suite"
)

validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_be_between("age", min_value=18, max_value=120)
validator.expect_column_values_to_be_in_set("status", ["active", "inactive"])

# Run validation
results = validator.validate()
print(results.success)
```

#### 📦 Deliverable
- Great Expectations test suite with sample failure report

---

### Day 67 — Week Integration Project

#### 📦 Deliverable: End-to-End Reproducible Pipeline

```
project/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── train.py
│   └── evaluate.py
├── notebooks/
├── mlruns/                 # MLflow tracking
├── dvc.yaml               # DVC pipeline
├── requirements.txt
└── README.md
```

**DVC Pipeline (dvc.yaml):**
```yaml
stages:
  process:
    cmd: python src/data_processing.py
    deps:
      - data/raw/
      - src/data_processing.py
    outs:
      - data/processed/

  train:
    cmd: python src/train.py
    deps:
      - data/processed/
      - src/train.py
    outs:
      - models/model.pkl
    metrics:
      - metrics.json:
          cache: false
```

---

## 🗓️ WEEK B (Days 68-74) — Pipelines, Orchestration & CI/CD

### 🎯 Week Goals
- Build ML pipelines with Airflow
- Implement CI/CD for ML
- Containerize models
- Deploy to Kubernetes

---

### Day 68 — Pipeline Orchestration with Airflow

#### 🛠️ Simple DAG
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

def extract_data():
    # Extract data from source
    pass

def transform_data():
    # Feature engineering
    pass

def train_model():
    # Train and log to MLflow
    pass

extract = PythonOperator(task_id='extract', python_callable=extract_data, dag=dag)
transform = PythonOperator(task_id='transform', python_callable=transform_data, dag=dag)
train = PythonOperator(task_id='train', python_callable=train_model, dag=dag)

extract >> transform >> train
```

---

### Day 69 — CI for ML (Testing)

#### 🛠️ Test Structure
```python
# tests/test_data.py
import pytest
import pandas as pd

def test_data_schema():
    df = pd.read_csv("data/processed/train.csv")
    expected_columns = ['feature1', 'feature2', 'target']
    assert all(col in df.columns for col in expected_columns)

def test_no_null_values():
    df = pd.read_csv("data/processed/train.csv")
    assert df.isnull().sum().sum() == 0

# tests/test_model.py
def test_model_accuracy_threshold():
    model = load_model("models/model.pkl")
    X_test, y_test = load_test_data()
    accuracy = model.score(X_test, y_test)
    assert accuracy > 0.8, f"Accuracy {accuracy} below threshold 0.8"

def test_model_inference_time():
    import time
    model = load_model("models/model.pkl")
    X_sample = get_sample_input()
    
    start = time.time()
    model.predict(X_sample)
    inference_time = time.time() - start
    
    assert inference_time < 0.1, f"Inference time {inference_time}s exceeds 100ms"
```

---

### Day 70 — CD for ML (Model Promotion)

#### 🛠️ GitHub Actions CI/CD
```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/ -v
      
      - name: Data validation
        run: python scripts/validate_data.py

  train:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Train model
        run: python src/train.py
      
      - name: Evaluate model
        run: python src/evaluate.py
      
      - name: Promote to staging
        if: success()
        run: python scripts/promote_model.py --stage staging

  deploy:
    needs: train
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          python scripts/promote_model.py --stage production
          kubectl apply -f k8s/deployment.yaml
```

---

### Day 71 — Infrastructure as Code (Terraform)

#### 🛠️ ML Infrastructure
```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

# S3 for artifacts
resource "aws_s3_bucket" "ml_artifacts" {
  bucket = "ml-artifacts-bucket"
}

# ECR for model images
resource "aws_ecr_repository" "ml_models" {
  name = "ml-models"
}

# EKS cluster for serving
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "ml-cluster"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    ml_nodes = {
      instance_types = ["m5.large"]
      min_size       = 1
      max_size       = 5
      desired_size   = 2
    }
  }
}
```

---

### Day 72 — Containerizing ML Models

#### 🛠️ Dockerfile for Model Server
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and code
COPY models/model.pkl .
COPY src/serve.py .

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# src/serve.py
from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

# Load model at startup
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
async def predict(features: list[float]):
    X = np.array(features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

```bash
# Build and run
docker build -t ml-model:v1 .
docker run -p 8000:8000 ml-model:v1
```

---

### Day 73 — Kubernetes Deployment

#### 🛠️ K8s Manifests
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: ml-model
        image: ml-model:v1
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### 🛠️ Helm Chart Structure
```
helm-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── hpa.yaml
```

---

### Day 74 — Week Integration Project

#### 📦 Deliverable: Complete CI/CD Pipeline

```
End-to-End Flow:
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│  Code   │ →  │  Test   │ →  │  Train   │ →  │Register │ →  │  Deploy  │
│ Commit  │    │ (pytest)│    │(MLflow)  │    │(staging)│    │  (K8s)   │
└─────────┘    └─────────┘    └──────────┘    └─────────┘    └──────────┘
```

---

## 🗓️ WEEK C (Days 75-81) — Serving, Inference & Scaling

### 🎯 Week Goals
- Master different serving patterns
- Implement high-performance inference
- Set up autoscaling
- Optimize costs

---

### Day 75 — Serving Patterns

#### 📚 Pattern Comparison

| Pattern | Latency | Throughput | Use Case |
|---------|---------|------------|----------|
| Synchronous | Low | Medium | Real-time predictions |
| Asynchronous | High | High | Non-urgent, high volume |
| Batch | Very High | Very High | Scheduled bulk processing |
| Streaming | Medium | High | Continuous data flows |

#### 🛠️ Batch Inference
```python
# batch_inference.py
import pandas as pd
import pickle
from datetime import datetime

def batch_predict(input_path: str, output_path: str):
    # Load model
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Load data
    df = pd.read_csv(input_path)
    
    # Predict
    predictions = model.predict(df)
    
    # Save results
    df['prediction'] = predictions
    df['predicted_at'] = datetime.now()
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    batch_predict("data/to_predict.csv", "data/predictions.csv")
```

---

### Day 76 — Model Serving Frameworks

#### 📚 Framework Comparison

| Framework | Best For |
|-----------|----------|
| FastAPI | Simple REST APIs |
| BentoML | Full lifecycle management |
| TorchServe | PyTorch models |
| Triton | Multi-framework, GPU |
| Ray Serve | Distributed serving |

#### 🛠️ BentoML Example
```python
# pip install bentoml

import bentoml
from bentoml.io import JSON, NumpyNdarray

# Save model to BentoML
bentoml.sklearn.save_model("house_price_model", model)

# Create service
runner = bentoml.sklearn.get("house_price_model:latest").to_runner()
svc = bentoml.Service("house_price_service", runners=[runner])

@svc.api(input=NumpyNdarray(), output=JSON())
async def predict(input_array):
    result = await runner.predict.async_run(input_array)
    return {"prediction": result.tolist()}

# Build and serve
# bentoml build
# bentoml serve service:svc
```

---

### Day 77 — High-Performance Inference

#### 📚 Optimization Techniques

| Technique | Description | Speedup |
|-----------|-------------|---------|
| Batching | Process multiple requests together | 2-5x |
| Quantization | Reduce model precision (FP32→INT8) | 2-4x |
| ONNX | Optimized runtime | 1.5-3x |
| Caching | Cache frequent predictions | 10-100x |

#### 🛠️ ONNX Conversion
```python
# Convert sklearn model to ONNX
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

initial_type = [('float_input', FloatTensorType([None, n_features]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Save
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Inference with ONNX Runtime
import onnxruntime as ort
session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name
result = session.run(None, {input_name: X.astype(np.float32)})
```

---

### Day 78 — Autoscaling

#### 🛠️ Kubernetes HPA
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

---

### Day 79 — Feature Serving & Caching

#### 🛠️ Redis Caching
```python
import redis
import json
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_prediction_cached(features: list) -> dict:
    # Create cache key
    key = hashlib.md5(json.dumps(features).encode()).hexdigest()
    
    # Check cache
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    # Compute prediction
    prediction = model.predict([features])[0]
    result = {"prediction": float(prediction)}
    
    # Cache for 1 hour
    redis_client.setex(key, 3600, json.dumps(result))
    
    return result
```

---

### Day 80 — Cost Optimization & Observability

#### 🛠️ Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Define metrics
PREDICTION_COUNT = Counter('predictions_total', 'Total predictions made')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')

@app.post("/predict")
async def predict(features: list[float]):
    start_time = time.time()
    
    # Make prediction
    prediction = model.predict([features])
    
    # Record metrics
    PREDICTION_COUNT.inc()
    PREDICTION_LATENCY.observe(time.time() - start_time)
    
    return {"prediction": prediction.tolist()}

# Start metrics server
start_http_server(8001)
```

---

### Day 81 — Week Integration Project

#### 📦 Deliverable: Scalable Serving Stack

- Model deployed on K8s
- HPA configured
- Prometheus metrics exported
- Grafana dashboard created

---

## 🗓️ WEEK D (Days 82-85) — Monitoring, Reliability & Governance

### 🎯 Week Goals
- Implement ML monitoring
- Detect data and model drift
- Set up model governance

---

### Day 82 — ML Monitoring & SLIs

#### 📚 Key Metrics to Monitor

| Category | Metrics |
|----------|---------|
| **System** | Latency, throughput, error rate, CPU/memory |
| **Model** | Prediction distribution, confidence scores |
| **Data** | Feature distributions, missing values |
| **Business** | Conversion rate, revenue impact |

#### 🛠️ Define SLIs/SLOs
```yaml
# SLO Definition
slos:
  - name: prediction_latency
    target: 99% of requests < 100ms
    measurement: histogram_quantile(0.99, prediction_latency_seconds)
    
  - name: availability
    target: 99.9% uptime
    measurement: sum(rate(requests_success)) / sum(rate(requests_total))
    
  - name: accuracy
    target: > 85% accuracy on live data
    measurement: monthly evaluation against ground truth
```

---

### Day 83 — Drift Detection

#### 📚 Types of Drift

| Drift Type | Description | Detection Method |
|------------|-------------|------------------|
| Data Drift | Input distribution changes | KS test, PSI |
| Concept Drift | Relationship X→Y changes | Monitor performance |
| Feature Drift | Individual feature shifts | Per-feature monitoring |

#### 🛠️ Evidently AI
```python
# pip install evidently

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

# Create drift report
report = Report(metrics=[
    DataDriftPreset(),
    TargetDriftPreset()
])

report.run(reference_data=train_df, current_data=production_df)
report.save_html("drift_report.html")

# Programmatic drift check
from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfDriftedColumns

suite = TestSuite(tests=[
    TestNumberOfDriftedColumns(lt=3)  # Less than 3 drifted columns
])
suite.run(reference_data=train_df, current_data=production_df)

if not suite.as_dict()['summary']['all_passed']:
    trigger_retraining_alert()
```

---

### Day 84 — Explainability & Fairness

#### 🛠️ SHAP Explanations
```python
# pip install shap

import shap

# Create explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test)

# Single prediction explanation
shap.waterfall_plot(shap.Explanation(
    values=shap_values[0],
    base_values=explainer.expected_value,
    data=X_test.iloc[0]
))
```

---

### Day 85 — Model Governance & Model Cards

#### 🛠️ Model Card Template
```markdown
# Model Card: House Price Prediction

## Model Details
- **Model Type:** Random Forest Regressor
- **Version:** 1.0.0
- **Date:** 2024-01-15
- **Owner:** ML Team

## Intended Use
- **Primary Use:** Estimate house prices for listings
- **Users:** Real estate agents, homeowners
- **Out of Scope:** Commercial properties

## Training Data
- **Source:** Historical sales data (2020-2023)
- **Size:** 50,000 samples
- **Features:** 15 features (location, size, bedrooms, etc.)

## Performance
| Metric | Value |
|--------|-------|
| RMSE | $25,000 |
| R² | 0.87 |
| MAE | $18,000 |

## Limitations
- Limited to residential properties
- May underperform for luxury homes (>$2M)

## Ethical Considerations
- Checked for bias across neighborhoods
- No demographic data used
```

---

## 🗓️ WEEK E (Days 86-90) — LLMOps Core

### 🎯 Week Goals
- Understand LLM fundamentals
- Build RAG systems
- Fine-tune models with PEFT
- Deploy LLMs at scale

---

### Day 86 — LLM Basics & Inference

#### 📚 Key Concepts

| Concept | Description |
|---------|-------------|
| Tokenization | Text → tokens (subwords) |
| Context Window | Max tokens model can process |
| Temperature | Randomness in generation (0-1) |
| Top-p (nucleus) | Cumulative probability threshold |

#### 🛠️ Using Transformers
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Generate text
input_text = "What is machine learning?"
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

---

### Day 87 — RAG (Retrieval-Augmented Generation)

#### 📚 RAG Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                         RAG Pipeline                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Documents│ → │ Chunking │ → │ Embedding│ → │Vector DB │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                       ↓         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Response │ ← │   LLM    │ ← │  Prompt  │ ← │ Retrieve │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 🛠️ Build RAG Pipeline
```python
# pip install langchain chromadb sentence-transformers

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

# 1. Load documents
loader = TextLoader("documents/")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# 4. Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 5. Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 6. Query
result = qa_chain({"query": "What is the return policy?"})
print(result["result"])
```

---

### Day 88 — Fine-tuning with PEFT/LoRA

#### 📚 Fine-tuning Methods

| Method | Memory | Training Time | When to Use |
|--------|--------|---------------|-------------|
| Full Fine-tuning | Very High | Long | Abundant data, resources |
| LoRA | Low | Medium | Limited resources |
| QLoRA | Very Low | Medium | Very limited resources |

#### 🛠️ LoRA Fine-tuning
```python
# pip install peft transformers datasets

from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType
from trl import SFTTrainer

# Load base model
model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(model_name, load_in_8bit=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configure LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,                    # Rank
    lora_alpha=32,          # Scaling factor
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"]  # Which layers to adapt
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # Shows ~0.1% trainable

# Training arguments
training_args = TrainingArguments(
    output_dir="./lora_model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,
    logging_steps=10
)

# Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    args=training_args
)
trainer.train()

# Save adapter
model.save_pretrained("./lora_adapter")
```

---

### Day 89 — LLM Serving & Optimization

#### 📚 Serving Frameworks

| Framework | Best For |
|-----------|----------|
| vLLM | High throughput, PagedAttention |
| TGI | Production-ready, Hugging Face |
| TensorRT-LLM | NVIDIA GPUs, maximum speed |

#### 🛠️ vLLM Serving
```python
# pip install vllm

from vllm import LLM, SamplingParams

# Load model
llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=256
)

# Generate
prompts = ["What is artificial intelligence?"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.outputs[0].text)
```

```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-2-7b-chat-hf \
    --port 8000
```

#### 🛠️ Response Caching
```python
import hashlib
import redis

redis_client = redis.Redis()

def get_llm_response_cached(prompt: str) -> str:
    # Create cache key
    cache_key = f"llm:{hashlib.md5(prompt.encode()).hexdigest()}"
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return cached.decode()
    
    # Generate response
    response = llm.generate(prompt)
    
    # Cache for 24 hours
    redis_client.setex(cache_key, 86400, response)
    
    return response
```

---

### Day 90 — Safety, Evaluation & Final Project

#### 📚 LLM Safety

| Risk | Mitigation |
|------|------------|
| Hallucination | RAG, fact-checking, "I don't know" |
| Prompt Injection | Input validation, guardrails |
| Harmful Content | Content filters, safety training |
| Data Leakage | PII detection, output filtering |

#### 🛠️ Guardrails
```python
# pip install guardrails-ai

from guardrails import Guard
from guardrails.hub import ToxicLanguage, PIIDetection

guard = Guard().use_many(
    ToxicLanguage(threshold=0.8, on_fail="filter"),
    PIIDetection(on_fail="mask")
)

# Validate output
result = guard(
    llm.generate,
    prompt="Generate customer response",
    metadata={"user_id": "123"}
)

if result.validation_passed:
    print(result.validated_output)
else:
    print("Output failed safety checks")
```

---

## 🏆 FINAL CAPSTONE PROJECTS

Choose one of these production-ready projects:

### Project 1: RAG Chatbot for Documents

**Components:**
- Document ingestion pipeline
- Vector database (Chroma/Milvus)
- Embedding model
- LLM (local or API)
- FastAPI backend
- Kubernetes deployment
- Monitoring (latency, token usage)
- CI/CD pipeline

### Project 2: End-to-End MLOps Platform

**Components:**
- Data versioning (DVC)
- Experiment tracking (MLflow)
- Pipeline orchestration (Airflow)
- Model registry & promotion
- Containerized serving (K8s)
- Drift detection (Evidently)
- Automated retraining

### Project 3: Fine-tuned LLM Service

**Components:**
- PEFT/LoRA fine-tuning pipeline
- Model evaluation framework
- Serving with vLLM or TGI
- Response caching
- Cost monitoring
- Safety guardrails

---

## 📋 QUICK REFERENCE CHECKLIST

### Phase 2 Skills ✅
- [ ] Data preprocessing & cleaning
- [ ] Feature engineering
- [ ] Classification algorithms
- [ ] Regression algorithms
- [ ] Clustering algorithms
- [ ] Deep learning basics (CNN, RNN)
- [ ] Model evaluation & selection

### Phase 3 Skills ✅
- [ ] Experiment tracking (MLflow)
- [ ] Data versioning (DVC)
- [ ] Pipeline orchestration (Airflow)
- [ ] CI/CD for ML
- [ ] Containerization (Docker)
- [ ] Kubernetes deployment
- [ ] Model monitoring & drift detection
- [ ] LLM fundamentals
- [ ] RAG systems
- [ ] Fine-tuning (LoRA/PEFT)
- [ ] LLM serving (vLLM/TGI)

---

## 🛠️ ESSENTIAL TOOLS SUMMARY

| Category | Tools |
|----------|-------|
| **Experiment Tracking** | MLflow, Weights & Biases |
| **Data Versioning** | DVC, LakeFS |
| **Pipeline** | Airflow, Kubeflow, Prefect |
| **Serving** | FastAPI, BentoML, KServe |
| **LLM Serving** | vLLM, TGI, TensorRT-LLM |
| **Vector DB** | Chroma, Pinecone, Milvus |
| **Monitoring** | Prometheus, Grafana, Evidently |
| **Infrastructure** | Docker, Kubernetes, Terraform |

---

> 🎯 **Success Tip:** Focus on building projects, not just reading. Each day's deliverable should be committed to your GitHub portfolio!

**Good luck on your MLOps & LLMOps journey! 🚀**

