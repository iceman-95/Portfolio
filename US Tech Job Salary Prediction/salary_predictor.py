import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, ExtraTreesRegressor, ExtraTreesClassifier
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
from sklearn.svm import SVR, SVC
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

class SalaryPredictor:
    def __init__(self, data_path='ds_salaries.csv'):
        self.data_path = data_path
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_train_class = None
        self.y_test_class = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.regression_models = {}
        self.classification_models = {}
        self.regression_results = {}
        self.classification_results = {}
        self.best_regression_model = None
        self.best_classification_model = None
        self.salary_thresholds = {}
        
    def load_and_explore_data(self):
        """Load and explore the dataset"""
        print("Loading dataset...")
        self.data = pd.read_csv(self.data_path)
        
        print(f"Dataset shape: {self.data.shape}")
        print(f"Columns: {list(self.data.columns)}")
        print(f"Unique countries: {self.data['employee_residence'].nunique()}")
        print(f"Unique job titles: {self.data['job_title'].nunique()}")
        
        # Show salary statistics
        print(f"\nSalary statistics (USD):")
        print(f"Mean: ${self.data['salary_in_usd'].mean():,.0f}")
        print(f"Median: ${self.data['salary_in_usd'].median():,.0f}")
        print(f"Min: ${self.data['salary_in_usd'].min():,.0f}")
        print(f"Max: ${self.data['salary_in_usd'].max():,.0f}")
        
        return self.data
    
    def create_salary_classification(self):
        """Create salary classification (Low/Medium/High)"""
        print("\nCreating salary classification...")
        
        # Use fixed thresholds for classification
        low_threshold = 100000
        high_threshold = 160000
        
        def classify_salary(salary):
            if salary < low_threshold:
                return 'Low'
            elif salary <= high_threshold:
                return 'Medium'
            else:
                return 'High'
        
        self.data['salary_class'] = self.data['salary_in_usd'].apply(classify_salary)
        
        # Store thresholds for later use
        self.salary_thresholds = {
            'Low': low_threshold,
            'Medium': high_threshold,
            'High': self.data['salary_in_usd'].max()
        }
        
        # Show classification distribution
        class_dist = self.data['salary_class'].value_counts()
        print(f"\nSalary Classification Distribution:")
        print(f"Low (<${low_threshold:,}): {class_dist.get('Low', 0)} ({class_dist.get('Low', 0)/len(self.data)*100:.1f}%)")
        print(f"Medium (${low_threshold:,}-${high_threshold:,}): {class_dist.get('Medium', 0)} ({class_dist.get('Medium', 0)/len(self.data)*100:.1f}%)")
        print(f"High (>${high_threshold:,}): {class_dist.get('High', 0)} ({class_dist.get('High', 0)/len(self.data)*100:.1f}%)")
        
        return self.data
    
    def create_overview_plot(self):
        """Generates and saves the salary overview plot."""
        plt.style.use('seaborn-v0_8')
        colors = {'Low': 'red', 'Medium': 'orange', 'High': 'green'}
        fig, axes = plt.subplots(2, 2, figsize=(15, 11))
        fig.suptitle('Salary Analysis: Overview', fontsize=18, y=0.98)
        
        # Plot 1a: Salary distribution
        ax = axes[0, 0]
        for salary_class in ['Low', 'Medium', 'High']:
            subset = self.data[self.data['salary_class'] == salary_class]
            if not subset.empty:
                ax.hist(subset['salary_in_usd'], bins=30, alpha=0.7, label=salary_class, color=colors[salary_class])
        ax.set_title('Salary Distribution by Classification')
        ax.set_xlabel('Salary (USD)')
        ax.set_ylabel('Frequency')
        ax.legend()

        # Plot 1b: Work year trend
        ax = axes[0, 1]
        year_salary = self.data.groupby('work_year')['salary_in_usd'].mean()
        ax.plot(year_salary.index, year_salary.values, marker='o', linewidth=2, markersize=8)
        ax.set_title('Average Salary Trend Over Years')
        ax.set_xlabel('Work Year')
        ax.set_ylabel('Average Salary (USD)')
        ax.set_xticks(year_salary.index)

        # Plot 1c: Experience level vs salary
        ax = axes[1, 0]
        exp_salary = self.data.groupby('experience_level')['salary_in_usd'].mean().sort_values(ascending=False)
        bars = ax.bar(exp_salary.index, exp_salary.values, color='lightcoral')
        ax.set_title('Average Salary by Experience Level')
        ax.set_xlabel('Experience Level')
        ax.set_ylabel('Average Salary (USD)')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'${height:,.0f}', ha='center', va='bottom', fontsize=7)

        # Plot 1d: Company size vs salary
        ax = axes[1, 1]
        size_salary = self.data.groupby('company_size')['salary_in_usd'].mean()
        bars = ax.bar(size_salary.index, size_salary.values, color='gold')
        ax.set_title('Average Salary by Company Size')
        ax.set_xlabel('Company Size')
        ax.set_ylabel('Average Salary (USD)')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'${height:,.0f}', ha='center', va='bottom', fontsize=7)
        
        fig.tight_layout(pad=3.0, rect=[0, 0, 1, 0.96])
        plt.savefig('salary_overview_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)
        print("✅ Saved 'salary_overview_analysis.png'")

    def create_top_categories_plot(self):
        """Generates and saves the top categories plot."""
        plt.style.use('seaborn-v0_8')
        colors = {'Low': 'red', 'Medium': 'orange', 'High': 'green'}
        fig, axes = plt.subplots(2, 2, figsize=(16, 11))
        fig.suptitle('Salary Analysis: Top Categories', fontsize=18, y=0.98)

        # Plot 2a: Top countries by average salary
        ax = axes[0, 0]
        country_salary = self.data.groupby('employee_residence')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
        ax.bar(range(len(country_salary)), country_salary.values, color='skyblue', alpha=0.7)
        ax.set_title('Top 10 Countries by Average Salary')
        ax.set_xlabel('Country')
        ax.set_ylabel('Average Salary (USD)')
        ax.set_xticks(range(len(country_salary)))
        ax.set_xticklabels(country_salary.index, rotation=45, ha='right')

        # Plot 2b: Top job titles
        ax = axes[0, 1]
        job_salary = self.data.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False).head(10)
        ax.barh(job_salary.index, job_salary.values, color='lightgreen')
        ax.set_title('Top 10 Highest Paying Job Titles')
        ax.set_xlabel('Average Salary (USD)')
        ax.invert_yaxis()

        # Plot 2c: Remote ratio vs salary
        ax = axes[1, 0]
        remote_salary = self.data.groupby('remote_ratio')['salary_in_usd'].mean()
        ax.bar(remote_salary.index.astype(str), remote_salary.values, color='lightblue')
        ax.set_title('Average Salary by Remote Ratio')
        ax.set_xlabel('Remote Ratio (%)')
        ax.set_ylabel('Average Salary (USD)')

        # Plot 2d: Salary classification distribution
        ax = axes[1, 1]
        class_counts = self.data['salary_class'].value_counts()
        if not class_counts.empty:
            ax.pie(class_counts.values, labels=class_counts.index, autopct='%1.1f%%', 
                    colors=[colors.get(c, '#cccccc') for c in class_counts.index])
        ax.set_title('Salary Classification Distribution')

        fig.tight_layout(pad=3.0, rect=[0, 0, 1, 0.96])
        plt.savefig('top_categories_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)
        print("✅ Saved 'top_categories_analysis.png'")

    def create_classification_dive_plot(self):
        """Generates and saves the classification deep dive plot."""
        plt.style.use('seaborn-v0_8')
        colors = {'Low': 'red', 'Medium': 'orange', 'High': 'green'}
        fig, axes = plt.subplots(2, 2, figsize=(17, 13))
        fig.suptitle('Salary Analysis: Classification Deep Dive', fontsize=18, y=0.98)

        # Plot 3a: Experience level vs classification
        ax = axes[0, 0]
        exp_class = pd.crosstab(self.data['experience_level'], self.data['salary_class'])
        if not exp_class.empty:
            exp_class.plot(kind='bar', ax=ax, color=[colors.get(c, '#cccccc') for c in exp_class.columns], rot=0)
        ax.set_title('Experience Level vs Salary Classification')
        ax.set_xlabel('Experience Level')
        ax.set_ylabel('Count')
        ax.legend(title='Salary Class')

        # Plot 3b: Company size vs classification
        ax = axes[0, 1]
        size_class = pd.crosstab(self.data['company_size'], self.data['salary_class'])
        if not size_class.empty:
            size_class.plot(kind='bar', ax=ax, color=[colors.get(c, '#cccccc') for c in size_class.columns], rot=0)
        ax.set_title('Company Size vs Salary Classification')
        ax.set_xlabel('Company Size')
        ax.set_ylabel('Count')
        ax.legend(title='Salary Class')

        # Plot 3c: Top job titles vs classification
        ax = axes[1, 0]
        top_jobs = self.data['job_title'].value_counts().head(10).index
        job_class_data = self.data[self.data['job_title'].isin(top_jobs)]
        job_class = pd.crosstab(job_class_data['job_title'], job_class_data['salary_class'])
        if not job_class.empty:
            job_class.plot(kind='bar', ax=ax, color=[colors.get(c, '#cccccc') for c in job_class.columns])
        ax.set_title('Top 10 Job Titles vs Classification')
        ax.set_xlabel('Job Title')
        ax.set_ylabel('Count')
        ax.legend(title='Salary Class')
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

        # Plot 3d: Remote ratio vs classification
        ax = axes[1, 1]
        remote_class = pd.crosstab(self.data['remote_ratio'], self.data['salary_class'])
        if not remote_class.empty:
            remote_class.plot(kind='bar', ax=ax, color=[colors.get(c, '#cccccc') for c in remote_class.columns], rot=0)
        ax.set_title('Remote Ratio vs Salary Classification')
        ax.set_xlabel('Remote Ratio (%)')
        ax.set_ylabel('Count')
        ax.legend(title='Salary Class')

        fig.tight_layout(pad=3.0, rect=[0, 0, 1, 0.96])
        plt.savefig('classification_deep_dive.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)
        print("✅ Saved 'classification_deep_dive.png'")
        
    def create_comprehensive_visualizations(self):
        """Create all comprehensive visualizations."""
        print("\nCreating all visualizations...")
        self.create_overview_plot()
        self.create_top_categories_plot()
        self.create_classification_dive_plot()

    def preprocess_data(self):
        """Preprocess the data for machine learning"""
        print("\nPreprocessing data...")
        
        df = self.data.copy()
        
        # Feature engineering
        exp_mapping = {'EN': 1, 'MI': 2, 'SE': 3, 'EX': 4}
        emp_mapping = {'PT': 1, 'FT': 2, 'CT': 3, 'FL': 4}
        size_mapping = {'S': 1, 'M': 2, 'L': 3}
        
        df['experience_level_encoded'] = df['experience_level'].map(exp_mapping)
        df['employment_type_encoded'] = df['employment_type'].map(emp_mapping)
        df['company_size_encoded'] = df['company_size'].map(size_mapping)
        
        # Encode categorical variables
        categorical_cols = ['job_title', 'employee_residence', 'company_location']
        for col in categorical_cols:
            le = LabelEncoder()
            df[f'{col}_encoded'] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        
        # Select features
        feature_cols = [
            'work_year', 'experience_level_encoded', 'employment_type_encoded',
            'job_title_encoded', 'employee_residence_encoded', 'remote_ratio',
            'company_location_encoded', 'company_size_encoded'
        ]
        
        X = df[feature_cols]
        y_regression = df['salary_in_usd']
        y_classification = df['salary_class']
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y_regression, test_size=0.2, random_state=42
        )
        
        # Split classification data with same indices
        _, _, self.y_train_class, self.y_test_class = train_test_split(
            X, y_classification, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"Training set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")
        
        return X, y_regression, y_classification
    
    def define_models(self):
        """Define all machine learning models"""
        print("\nDefining machine learning models...")
        
        # Regression models for exact salary prediction
        self.regression_models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=0.1),
            'Elastic Net': ElasticNet(alpha=0.1, l1_ratio=0.5),
            'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=10),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'K-Neighbors': KNeighborsRegressor(n_neighbors=5),
            'SVR (RBF)': SVR(kernel='rbf', C=100, gamma='scale'),
            'SVR (Linear)': SVR(kernel='linear', C=100)
        }
        
        # Classification models for salary classification (Low/Medium/High)
        self.classification_models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Decision Tree Classifier': DecisionTreeClassifier(random_state=42, max_depth=10),
            'Random Forest Classifier': RandomForestClassifier(n_estimators=100, random_state=42),
            'Extra Trees Classifier': ExtraTreesClassifier(n_estimators=100, random_state=42),
            'K-Neighbors Classifier': KNeighborsClassifier(n_neighbors=5),
            'SVC (RBF)': SVC(kernel='rbf', C=100, gamma='scale', probability=True),
            'SVC (Linear)': SVC(kernel='linear', C=100, probability=True)
        }
        
        print(f"Regression models: {len(self.regression_models)}")
        print(f"Classification models: {len(self.classification_models)}")
    
    def train_all_models(self):
        """Train all regression and classification models"""
        print("\n" + "="*60)
        print("TRAINING ALL MACHINE LEARNING MODELS")
        print("="*60)
        
        # Train regression models
        print("\n📊 TRAINING REGRESSION MODELS (Exact Salary Prediction)")
        print("-" * 50)
        
        self.regression_results = {}
        for name, model in self.regression_models.items():
            print(f"Training {name}...")
            
            # Use scaled data for SVR and KNN, regular data for others
            if 'SVR' in name or 'K-Neighbors' in name:
                model.fit(self.X_train_scaled, self.y_train)
                y_pred = model.predict(self.X_test_scaled)
            else:
                model.fit(self.X_train, self.y_train)
                y_pred = model.predict(self.X_test)
            
            # Calculate metrics
            mae = mean_absolute_error(self.y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
            r2 = r2_score(self.y_test, y_pred)
            
            self.regression_results[name] = {
                'MAE': mae,
                'RMSE': rmse,
                'R2': r2,
                'model': model,
                'predictions': y_pred
            }
            
            print(f"  MAE: ${mae:,.0f}, RMSE: ${rmse:,.0f}, R²: {r2:.3f}")
        
        # Train classification models
        print("\n🏷️  TRAINING CLASSIFICATION MODELS (Low/Medium/High)")
        print("-" * 50)
        
        self.classification_results = {}
        for name, model in self.classification_models.items():
            print(f"Training {name}...")
            
            # Use scaled data for SVC and KNN, regular data for others
            if 'SVC' in name or 'K-Neighbors' in name:
                model.fit(self.X_train_scaled, self.y_train_class)
                y_pred = model.predict(self.X_test_scaled)
                y_pred_proba = model.predict_proba(self.X_test_scaled) if hasattr(model, 'predict_proba') else None
            else:
                model.fit(self.X_train, self.y_train_class)
                y_pred = model.predict(self.X_test)
                y_pred_proba = model.predict_proba(self.X_test) if hasattr(model, 'predict_proba') else None
            
            # Calculate metrics
            accuracy = (y_pred == self.y_test_class).mean()
            
            self.classification_results[name] = {
                'Accuracy': accuracy,
                'model': model,
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            print(f"  Accuracy: {accuracy:.3f}")
        
        # Find best models
        best_regression_name = max(self.regression_results.keys(), key=lambda x: self.regression_results[x]['R2'])
        best_classification_name = max(self.classification_results.keys(), key=lambda x: self.classification_results[x]['Accuracy'])
        
        self.best_regression_model = self.regression_results[best_regression_name]['model']
        self.best_classification_model = self.classification_results[best_classification_name]['model']
        
        print(f"\n🏆 BEST MODELS:")
        print(f"   Regression (Exact Salary): {best_regression_name} (R²: {self.regression_results[best_regression_name]['R2']:.3f})")
        print(f"   Classification (Low/Med/High): {best_classification_name} (Accuracy: {self.classification_results[best_classification_name]['Accuracy']:.3f})")
        
        return self.regression_results, self.classification_results
    
    def create_model_comparison_plot(self):
        """Create model comparison visualization"""
        print("\nCreating model comparison plot...")
        
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(18, 16))
        fig.suptitle('Model Performance Comparison', fontsize=20, y=0.98)

        # Sort models for better visualization
        reg_results_df = pd.DataFrame(self.regression_results).T.sort_values('R2', ascending=True)
        class_results_df = pd.DataFrame(self.classification_results).T.sort_values('Accuracy', ascending=True)

        # Plot 1: Regression models R² comparison
        ax = axes[0, 0]
        bars = ax.barh(reg_results_df.index, reg_results_df['R2'], color='skyblue', alpha=0.8)
        ax.set_title('Regression Models - R² Scores', fontsize=14)
        ax.set_xlabel('R² Score', fontsize=12)
        ax.set_ylabel('Models', fontsize=12)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(True, axis='x', linestyle='--', alpha=0.6)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.005, bar.get_y() + bar.get_height()/2, f'{width:.3f}', 
                    ha='left', va='center', fontsize=9)

        # Plot 2: Regression models RMSE comparison
        ax = axes[0, 1]
        reg_results_df_rmse = pd.DataFrame(self.regression_results).T.sort_values('RMSE', ascending=False)
        bars = ax.barh(reg_results_df_rmse.index, reg_results_df_rmse['RMSE'], color='lightgreen', alpha=0.8)
        ax.set_title('Regression Models - RMSE', fontsize=14)
        ax.set_xlabel('RMSE (USD)', fontsize=12)
        ax.set_ylabel('') # No label to avoid clutter
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(True, axis='x', linestyle='--', alpha=0.6)

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 500, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
                    ha='left', va='center', fontsize=9)

        # Plot 3: Classification models accuracy comparison
        ax = axes[1, 0]
        bars = ax.barh(class_results_df.index, class_results_df['Accuracy'], color='lightcoral', alpha=0.8)
        ax.set_title('Classification Models - Accuracy', fontsize=14)
        ax.set_xlabel('Accuracy', fontsize=12)
        ax.set_ylabel('Models', fontsize=12)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(True, axis='x', linestyle='--', alpha=0.6)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.005, bar.get_y() + bar.get_height()/2, f'{width:.3f}', 
                    ha='left', va='center', fontsize=9)
        
        # Plot 4: Best regression model predictions vs actual
        ax = axes[1, 1]
        best_reg_name = reg_results_df.index[-1]
        best_reg_pred = self.regression_results[best_reg_name]['predictions']
        
        ax.scatter(self.y_test, best_reg_pred, alpha=0.5, color='royalblue')
        ax.plot([self.y_test.min(), self.y_test.max()], [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        ax.set_title(f'Best Model: {best_reg_name}\nPredictions vs Actual', fontsize=14)
        ax.set_xlabel('Actual Salary (USD)', fontsize=12)
        ax.set_ylabel('Predicted Salary (USD)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        
        fig.tight_layout(pad=3.0, rect=[0, 0, 1, 0.96])
        plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)

    def predict_salary_and_classification(self, **kwargs):
        """Predict salary and classification for a single data point."""
        
        # Create a DataFrame from the input
        input_data = pd.DataFrame([kwargs])
        
        # Feature engineering
        exp_mapping = {'EN': 1, 'MI': 2, 'SE': 3, 'EX': 4}
        emp_mapping = {'PT': 1, 'FT': 2, 'CT': 3, 'FL': 4}
        size_mapping = {'S': 1, 'M': 2, 'L': 3}
        
        input_data['experience_level_encoded'] = input_data['experience_level'].map(exp_mapping)
        input_data['employment_type_encoded'] = input_data['employment_type'].map(emp_mapping)
        input_data['company_size_encoded'] = input_data['company_size'].map(size_mapping)
        
        # Encode categorical variables using stored label encoders
        for col in self.label_encoders:
            le = self.label_encoders[col]
            # Handle unseen labels by assigning a default value (e.g., -1 or a new code)
            input_data[f'{col}_encoded'] = input_data[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

        # Ensure all feature columns are present
        feature_cols = [
            'work_year', 'experience_level_encoded', 'employment_type_encoded',
            'job_title_encoded', 'employee_residence_encoded', 'remote_ratio',
            'company_location_encoded', 'company_size_encoded'
        ]
        
        final_input = input_data[feature_cols]

        # Use scaled data for appropriate models
        if 'SVR' in self.best_regression_model.__class__.__name__ or 'KNeighbors' in self.best_regression_model.__class__.__name__:
             final_input_scaled = self.scaler.transform(final_input)
             predicted_salary = self.best_regression_model.predict(final_input_scaled)[0]
        else:
            predicted_salary = self.best_regression_model.predict(final_input)[0]

        if 'SVC' in self.best_classification_model.__class__.__name__ or 'KNeighbors' in self.best_classification_model.__class__.__name__:
            final_input_scaled = self.scaler.transform(final_input)
            predicted_class = self.best_classification_model.predict(final_input_scaled)[0]
            class_probs = self.best_classification_model.predict_proba(final_input_scaled)[0]
        else:
            predicted_class = self.best_classification_model.predict(final_input)[0]
            class_probs = self.best_classification_model.predict_proba(final_input)[0]
            
        return predicted_salary, predicted_class, class_probs

    def run_example_predictions(self):
        """Run example predictions on a few profiles."""
        print("\n" + "="*50)
        print("EXAMPLE SALARY PREDICTIONS")
        print("="*50)
        
        example_profiles = [
            {
                'work_year': 2023, 'experience_level': 'SE', 'employment_type': 'FT', 
                'job_title': 'Data Scientist', 'employee_residence': 'US', 'remote_ratio': 100, 
                'company_location': 'US', 'company_size': 'M'
            },
            {
                'work_year': 2023, 'experience_level': 'MI', 'employment_type': 'FT', 
                'job_title': 'Machine Learning Engineer', 'employee_residence': 'GB', 'remote_ratio': 50, 
                'company_location': 'GB', 'company_size': 'L'
            },
            {
                'work_year': 2023, 'experience_level': 'EN', 'employment_type': 'FT', 
                'job_title': 'Data Analyst', 'employee_residence': 'CA', 'remote_ratio': 0, 
                'company_location': 'CA', 'company_size': 'S'
            }
        ]
        
        for i, profile in enumerate(example_profiles):
            print(f"\n👤 EXAMPLE PROFILE {i+1}:")
            print(f"   Job: {profile['job_title']} ({profile['experience_level']})")
            print(f"   Location: {profile['employee_residence']} (Company: {profile['company_location']}, Size: {profile['company_size']})")
            
            predicted_salary, predicted_class, class_probs = self.predict_salary_and_classification(**profile)
            
            confidence_range = predicted_salary * 0.15
            
            print(f"\n   📊 PREDICTION:")
            print(f"   💰 Predicted Salary: ${predicted_salary:,.0f}")
            print(f"   📈 Est. Range: ${predicted_salary - confidence_range:,.0f} - ${predicted_salary + confidence_range:,.0f}")
            print(f"   🏷️  Salary Class: {predicted_class}")
            
            classes = self.best_classification_model.classes_
            print(f"   📊 Class Confidence:")
            for class_name, prob in zip(classes, class_probs):
                print(f"      {class_name}: {prob:.1%}")
        print("\n" + "="*50)

    def print_comprehensive_summary(self):
        """Print comprehensive analysis summary"""
        print("\n" + "="*80)
        print("COMPREHENSIVE SALARY ANALYSIS SUMMARY")
        print("="*80)
        
        # Overall statistics
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"Total jobs analyzed: {len(self.data):,}")
        print(f"Average salary: ${self.data['salary_in_usd'].mean():,.0f}")
        print(f"Median salary: ${self.data['salary_in_usd'].median():,.0f}")
        print(f"Salary range: ${self.data['salary_in_usd'].min():,.0f} - ${self.data['salary_in_usd'].max():,.0f}")
        
        # Salary classification thresholds
        print(f"\n🏷️  SALARY CLASSIFICATION THRESHOLDS:")
        print(f"   Low: < $100,000")
        print(f"   Medium: $100,000 - $160,000")
        print(f"   High: > $160,000")
        
        # Classification distribution
        class_dist = self.data['salary_class'].value_counts()
        print(f"\n📊 CLASSIFICATION DISTRIBUTION:")
        print(f"   Low: {class_dist.get('Low', 0)} jobs ({class_dist.get('Low', 0)/len(self.data)*100:.1f}%)")
        print(f"   Medium: {class_dist.get('Medium', 0)} jobs ({class_dist.get('Medium', 0)/len(self.data)*100:.1f}%)")
        print(f"   High: {class_dist.get('High', 0)} jobs ({class_dist.get('High', 0)/len(self.data)*100:.1f}%)")
        
        # Top paying countries
        country_avg = self.data.groupby('employee_residence')['salary_in_usd'].mean().sort_values(ascending=False)
        print(f"\n🌍 TOP 5 HIGHEST PAYING COUNTRIES:")
        for i, (country, salary) in enumerate(country_avg.head(5).items(), 1):
            print(f"{i}. {country}: ${salary:,.0f}")
        
        # Top paying job titles
        job_avg = self.data.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)
        print(f"\n💼 TOP 5 HIGHEST PAYING JOB TITLES:")
        for i, (job, salary) in enumerate(job_avg.head(5).items(), 1):
            print(f"{i}. {job}: ${salary:,.0f}")
        
        # Experience level analysis
        exp_avg = self.data.groupby('experience_level')['salary_in_usd'].mean().sort_values(ascending=False)
        print(f"\n📈 SALARY BY EXPERIENCE LEVEL:")
        exp_names = {'EN': 'Entry Level', 'MI': 'Mid Level', 'SE': 'Senior Level', 'EX': 'Executive Level'}
        for level, salary in exp_avg.items():
            print(f"   {exp_names[level]}: ${salary:,.0f}")
        
        # Company size analysis
        size_avg = self.data.groupby('company_size')['salary_in_usd'].mean().sort_values(ascending=False)
        print(f"\n🏢 SALARY BY COMPANY SIZE:")
        size_names = {'S': 'Small (<50)', 'M': 'Medium (50-250)', 'L': 'Large (>250)'}
        for size, salary in size_avg.items():
            print(f"   {size_names[size]}: ${salary:,.0f}")
        
        # Model performance summary
        if hasattr(self, 'regression_results') and self.regression_results:
            best_reg_name = max(self.regression_results.keys(), key=lambda x: self.regression_results[x]['R2'])
            best_class_name = max(self.classification_results.keys(), key=lambda x: self.classification_results[x]['Accuracy'])
            
            print(f"\n🤖 MODEL PERFORMANCE:")
            print(f"   Best Regression Model: {best_reg_name} (R²: {self.regression_results[best_reg_name]['R2']:.3f})")
            print(f"   Best Classification Model: {best_class_name} (Accuracy: {self.classification_results[best_class_name]['Accuracy']:.3f})")
        
        print("\n" + "="*80)
    
    def interactive_prediction(self):
        """Interactive salary prediction interface"""
        print("\n" + "="*50)
        print("INTERACTIVE SALARY PREDICTION")
        print("="*50)
        
        # Get available options
        job_titles = sorted(self.data['job_title'].unique())
        residences = sorted(self.data['employee_residence'].unique())
        locations = sorted(self.data['company_location'].unique())
        
        print("\nAvailable job titles:")
        for i, title in enumerate(job_titles[:20]):  # Show first 20
            print(f"{i+1:2d}. {title}")
        print("... and more")
        
        print("\nExperience levels: EN (Entry), MI (Mid), SE (Senior), EX (Executive)")
        print("Employment types: PT (Part-time), FT (Full-time), CT (Contract), FL (Freelance)")
        print("Company sizes: S (Small), M (Medium), L (Large)")
        
        while True:
            try:
                print("\n" + "-"*30)
                print("Enter your details (or 'quit' to exit):")
                
                # Get user input
                work_year = int(input("Work year (2020-2023): ") or "2023")
                experience_level = (input("Experience level (EN/MI/SE/EX): ") or "SE").upper()
                employment_type = (input("Employment type (PT/FT/CT/FL): ") or "FT").upper()
                job_title = input("Job title: ") or "Data Scientist"
                employee_residence = (input("Employee residence (country code): ") or "US").upper()
                remote_ratio = int(input("Remote ratio (0-100): ") or "50")
                company_location = (input("Company location (country code): ") or "US").upper()
                company_size = (input("Company size (S/M/L): ") or "M").upper()
                
                # Validate inputs
                if experience_level not in ['EN', 'MI', 'SE', 'EX']:
                    print("Invalid experience level. Using SE.")
                    experience_level = 'SE'
                
                if employment_type not in ['PT', 'FT', 'CT', 'FL']:
                    print("Invalid employment type. Using FT.")
                    employment_type = 'FT'
                
                if company_size not in ['S', 'M', 'L']:
                    print("Invalid company size. Using M.")
                    company_size = 'M'
                
                # Make prediction
                predicted_salary, predicted_class, class_probs = self.predict_salary_and_classification(
                    work_year=work_year,
                    experience_level=experience_level,
                    employment_type=employment_type,
                    job_title=job_title,
                    employee_residence=employee_residence,
                    remote_ratio=remote_ratio,
                    company_location=company_location,
                    company_size=company_size
                )
                
                confidence_range = predicted_salary * 0.15
                
                print(f"\n📊 PREDICTION RESULTS:")
                print(f"💰 Predicted Salary: ${predicted_salary:,.0f}")
                print(f"📈 Estimated Range: ${predicted_salary - confidence_range:,.0f} - ${predicted_salary + confidence_range:,.0f}")
                print(f"🏷️  Salary Classification: {predicted_class}")
                
                # Show classification probabilities
                classes = self.best_classification_model.classes_
                print(f"📊 Classification Confidence:")
                for class_name, prob in zip(classes, class_probs):
                    print(f"   {class_name}: {prob:.1%}")
                
                continue_prediction = input("\nMake another prediction? (y/n): ").lower()
                if continue_prediction != 'y':
                    break
                    
            except ValueError as e:
                print(f"Error: {e}. Please try again.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}. Please try again.")

def main():
    """Main function to run the complete salary prediction system"""
    print("Complete US Tech Job Salary Prediction System")
    print("="*60)
    
    # Initialize predictor
    predictor = SalaryPredictor()
    
    while True:
        print("\n" + "="*60)
        print("🎯 WHAT WOULD YOU LIKE TO DO?")
        print("="*60)
        print("1. 📋 Display Analysis Summary")
        print("2. 📊 Create comprehensive visualizations")
        print("3. 🤖 Train & Compare All 18 Models")
        print("4. 🎯 Show Example Predictions")
        print("5. 💬 Predict Your Salary")
        print("0. ❌ Exit")
        print("="*60)
        
        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == '0':
                print("\n👋 Goodbye!")
                break
                
            elif choice == '1':
                # Load and train models if not already done
                if predictor.X_train is None:
                    print("\n📊 Loading and preprocessing data...")
                    predictor.load_and_explore_data()
                    predictor.create_salary_classification()
                    predictor.preprocess_data()
                    predictor.define_models()
                
                if not predictor.regression_results:
                    print("Training models for summary...")
                    predictor.train_all_models()
                print("\n📋 Generating comprehensive summary...")
                predictor.print_comprehensive_summary()
                
            elif choice == '2':
                # Load data if not already loaded
                if predictor.data is None:
                    print("\n📊 Loading data...")
                    predictor.load_and_explore_data()
                    predictor.create_salary_classification()
                
                while True:
                    print("\n" + "-"*40)
                    print("📊 VISUALIZATION MENU")
                    print("-"*40)
                    print("1. Salary Overview Analysis")
                    print("2. Top Categories Analysis")
                    print("3. Classification Deep Dive")
                    print("0. Back to Main Menu")
                    print("-"*40)
                    
                    viz_choice = input("Enter your choice (0-3): ").strip()

                    if viz_choice == '0':
                        break
                    elif viz_choice == '1':
                        print("\n📊 Creating Salary Overview plot...")
                        predictor.create_overview_plot()
                    elif viz_choice == '2':
                        print("\n📊 Creating Top Categories plot...")
                        predictor.create_top_categories_plot()
                    elif viz_choice == '3':
                        print("\n📊 Creating Classification Deep Dive plot...")
                        predictor.create_classification_dive_plot()
                    else:
                        print("❌ Invalid choice. Please enter a number between 0-3.")
                
            elif choice == '3':
                # Load and preprocess data if not already done
                if predictor.X_train is None:
                    print("\n📊 Loading and preprocessing data...")
                    predictor.load_and_explore_data()
                    predictor.create_salary_classification()
                    predictor.preprocess_data()
                    predictor.define_models()
                
                print("\n🤖 Training all ML models...")
                reg_results, class_results = predictor.train_all_models()
                predictor.create_model_comparison_plot()
                print("✅ Model training completed! Check 'model_comparison.png'")
                
            elif choice == '4':
                # Load and train models if not already done
                if predictor.X_train is None:
                    print("\n📊 Loading and preprocessing data...")
                    predictor.load_and_explore_data()
                    predictor.create_salary_classification()
                    predictor.preprocess_data()
                    predictor.define_models()
                
                if not predictor.best_regression_model:
                    print("Training models...")
                    predictor.train_all_models()
                print("\n🎯 Running example predictions...")
                predictor.run_example_predictions()
                
            elif choice == '5':
                # Load and train models if not already done
                if predictor.X_train is None:
                    print("\n📊 Loading and preprocessing data...")
                    predictor.load_and_explore_data()
                    predictor.create_salary_classification()
                    predictor.preprocess_data()
                    predictor.define_models()
                
                if not predictor.best_regression_model:
                    print("Training models...")
                    predictor.train_all_models()
                print("\n💬 Starting interactive prediction...")
                predictor.interactive_prediction()
                
            else:
                print("❌ Invalid choice. Please enter a number between 0-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main() 