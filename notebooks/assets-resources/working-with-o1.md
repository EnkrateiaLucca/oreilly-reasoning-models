def hybrid_workflow(complex_problem):
    """
    Demonstrates a hybrid approach using both reasoning and GPT models:
    1. Reasoning model (o-series) for planning
    2. GPT model for execution
    
    Parameters:
    - complex_problem: str (Description of the problem to solve)
    Returns:
    
    - solution: dict containing the plan and execution results
    """
    # Step 1: Use reasoning model to create a detailed plan
    planning_prompt = f"""
    Given the following complex problem, create a detailed plan to solve it.
    Break down the solution into specific, executable steps.
    
    Problem: {complex_problem}
    
    Your plan should:
    1. Identify key challenges and considerations
    2. Break down the solution into 3-5 concrete steps
    3. For each step, specify what type of model would be best suited (reasoning or GPT)
    4. Provide clear success criteria for each step
    """
    
    # Simulate reasoning model output
    # In a real implementation, you would call: plan = call_reasoning_model(planning_prompt)
    plan = """
    SOLUTION PLAN FOR DATA ANALYSIS CHALLENGE
    
    Key Challenges:
    - Large, unstructured dataset with potential inconsistencies
    - Need to identify subtle patterns across multiple variables
    - Time-sensitive analysis requiring both accuracy and reasonable speed
    
    Step 1: Data Cleaning and Preparation
    - Best Model: GPT (faster processing for well-defined task)
    - Actions: Normalize data formats, handle missing values, identify outliers
    - Success Criteria: Clean dataset with consistent formatting and documented handling of anomalies
    
    Step 2: In-depth Pattern Analysis
    - Best Model: Reasoning (complex relationship identification)
    - Actions: Identify correlations between variables, detect unusual patterns, generate hypotheses
    - Success Criteria: Comprehensive list of statistically significant patterns with confidence levels
    
    Step 3: Predictive Model Development
    - Best Model: GPT (code generation for standard ML algorithms)
    - Actions: Implement predictive models based on patterns identified in Step 2
    - Success Criteria: Working code for at least 2 different predictive models with evaluation metrics
    
    Step 4: Result Interpretation and Recommendations
    - Best Model: Reasoning (complex decision making with multiple factors)
    - Actions: Interpret results, assess business implications, develop actionable recommendations
    - Success Criteria: Clear, prioritized set of recommendations with expected business impacts
    """
    
    # Step 2: Execute each step of the plan using the appropriate model type
    # For this example, we'll simulate the execution of just one step
    
    execution_step = "Step 1: Data Cleaning and Preparation"
    execution_prompt = f"""
    Execute the following step from our data analysis plan:
    
    {execution_step}
    
    For this step, please write Python code that:
    1. Loads a CSV file
    2. Identifies and handles missing values
    3. Normalizes numeric columns
    4. Identifies and handles outliers
    5. Outputs a cleaned dataset
    
    The code should be well-commented and follow best practices.
    """
    
    # Simulate GPT model output
    # In a real implementation, you would call: execution_result = call_gpt_model(execution_prompt)
    execution_result = """
    ```python
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    
    def clean_dataset(file_path, output_path=None):
        '''
        Clean and prepare a dataset for analysis
        
        Parameters:
        - file_path: Path to the input CSV file
        - output_path: Optional path to save cleaned CSV file
        
        Returns:
        - cleaned_df: The cleaned pandas DataFrame
        '''
        # Load the dataset
        print(f"Loading dataset from {file_path}...")
        df = pd.read_csv(file_path)
        
        # Get initial dataset info
        print(f"Initial dataset shape: {df.shape}")
        print(f"Missing values per column:\\n{df.isnull().sum()}")
        
        # Handle missing values
        print("Handling missing values...")
        # For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                median_value = df[col].median()
                df[col] = df[col].fillna(median_value)
                print(f"  - Filled {col} missing values with median: {median_value}")
        
        # For categorical columns, fill with mode
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode()[0]
                df[col] = df[col].fillna(mode_value)
                print(f"  - Filled {col} missing values with mode: {mode_value}")
        
        # Normalize numeric columns
        print("Normalizing numeric columns...")
        scaler = StandardScaler()
        df_numeric = df[numeric_cols].copy()
        df_normalized = pd.DataFrame(
            scaler.fit_transform(df_numeric),
            columns=numeric_cols,
            index=df.index
        )
        
        # Handle outliers using IQR method
        print("Identifying and handling outliers...")
        for col in numeric_cols:
            Q1 = df_normalized[col].quantile(0.25)
            Q3 = df_normalized[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df_normalized[(df_normalized[col] < lower_bound) | 
                                     (df_normalized[col] > upper_bound)]
            
            if not outliers.empty:
                print(f"  - Found {len(outliers)} outliers in {col}")
                
                # Cap outliers at the boundaries instead of removing
                df_normalized.loc[df_normalized[col] < lower_bound, col] = lower_bound
                df_normalized.loc[df_normalized[col] > upper_bound, col] = upper_bound
                print(f"  - Capped outliers in {col} at IQR boundaries")
        
        # Replace original numeric columns with normalized values
        for col in numeric_cols:
            df[col] = df_normalized[col]
        
        # Save cleaned dataset if output path is provided
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"Saved cleaned dataset to {output_path}")
        
        print(f"Final dataset shape: {df.shape}")
        return df
    
    # Example usage
    if __name__ == "__main__":
        cleaned_df = clean_dataset("input_data.csv", "cleaned_data.csv")
        
        # Create a quick summary of the cleaned data
        print("\\nSummary statistics of cleaned data:")
        print(cleaned_df.describe())
        
        # Plot histograms of numeric columns to verify normalization
        cleaned_df.hist(figsize=(12, 10))
        plt.tight_layout()
        plt.savefig("data_distribution.png")
        plt.close()
        print("Created histograms of cleaned numeric data in 'data_distribution.png'")
    ```
    
    This code:
    6. Loads the CSV file
    7. Identifies and handles missing values (using median for numeric, mode for categorical)
    8. Normalizes numeric columns using StandardScaler
    9. Identifies outliers using the IQR method and caps them at the boundaries
    10. Outputs a cleaned dataset and creates visualizations to verify the cleaning process
    
    The code follows best practices with clear documentation, error handling, and informative logging.
    """
    
    # Return the combined solution
    return {
        "problem": complex_problem,
        "plan": plan,
        "executed_step": execution_step,
        "execution_result": execution_result
    }

# Test the hybrid workflow
problem_statement = """
You have been provided with a large dataset containing 5 years of customer transaction data 
from a retail company. The dataset includes purchase history, customer demographics, 
product categories, and various time-based features. Your task is to analyze this data to 
identify spending patterns, predict future purchasing behavior, and develop actionable 
recommendations for improving customer retention and increasing average order value.
"""

solution = hybrid_workflow(problem_statement)

print("\n===== HYBRID WORKFLOW DEMONSTRATION =====")
print("\nPROBLEM:")
print(problem_statement)
print("\nPLAN CREATED BY REASONING MODEL:")
print(solution["plan"])
print("\nEXECUTED STEP (USING GPT MODEL):")
print(solution["executed_step"])
print(solution["execution_result"])