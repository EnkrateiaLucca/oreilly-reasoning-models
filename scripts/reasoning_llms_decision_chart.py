# I'll create a Python script that calculates normalized scores for LLM models based on your specified ranges. The script will handle data input, calculate normalized values and weighted scores, and visualize the results.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tabulate import tabulate

# Define normalization ranges
INTELLIGENCE_MAX = 100  # intelligence index
SPEED_MAX = 500        # tokens per second
COST_MAX = 100         # $ per 1M tokens

def normalize_score(value, max_value, higher_is_better=True):
    """Normalize a value to 0-1 range."""
    bounded_value = max(0, min(value, max_value))
    
    if higher_is_better:
        return bounded_value / max_value
    else:
        # For metrics where lower is better (like cost)
        return 1 - (bounded_value / max_value)

def calculate_scores(models_data, weights):
    """Calculate normalized scores for LLM models."""
    # Create a copy to avoid modifying the original
    results = models_data.copy()
    
    # Normalize each factor
    results['intelligence_norm'] = results['intelligence'].apply(
        lambda x: normalize_score(x, INTELLIGENCE_MAX)
    )
    
    results['speed_norm'] = results['speed'].apply(
        lambda x: normalize_score(x, SPEED_MAX)
    )
    
    results['cost_norm'] = results['cost'].apply(
        lambda x: normalize_score(x, COST_MAX, higher_is_better=False)
    )
    
    # Calculate weighted scores for each factor
    results['intelligence_score'] = weights['intelligence'] * results['intelligence_norm']
    results['speed_score'] = weights['speed'] * results['speed_norm'] 
    results['cost_score'] = weights['cost'] * results['cost_norm']
    
    # Calculate total weighted score
    results['total_score'] = (
        results['intelligence_score'] +
        results['speed_score'] +
        results['cost_score']
    )
    
    # Sort by total score
    return results.sort_values('total_score', ascending=False)

def visualize_results(results, weights, save_path):
    """Create visualizations for model comparison."""
    sns.set(style="whitegrid")
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(18, 15))
    
    # Plot 1: Bar chart of total scores
    ax1 = axes[0, 0]
    bars = sns.barplot(x='model', y='total_score', data=results, ax=ax1)
    ax1.set_title('Total Score by Model', fontsize=14)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars.patches:
        ax1.annotate(f"{bar.get_height():.3f}",
                   (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha='center', va='bottom',
                   size=10, xytext=(0, 5),
                   textcoords='offset points')
    
    # Plot 2: Stacked bar chart showing contribution of each factor
    ax2 = axes[0, 1]
    stacked_data = results[['model', 'intelligence_score', 'speed_score', 'cost_score']]
    stacked_data = stacked_data.set_index('model')
    stacked_data.plot(kind='bar', stacked=True, ax=ax2, 
                    color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax2.set_title('Score Contribution by Factor', fontsize=14)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
    ax2.legend(['Intelligence', 'Speed', 'Cost'])
    
    # Plot 3: Normalized values heatmap
    ax3 = axes[1, 0]
    heatmap_data = results[['model', 'intelligence_norm', 'speed_norm', 'cost_norm']]
    heatmap_data = heatmap_data.set_index('model')
    heatmap_data = heatmap_data.rename(columns={
        'intelligence_norm': 'Intelligence',
        'speed_norm': 'Speed',
        'cost_norm': 'Cost Efficiency'
    })
    sns.heatmap(heatmap_data, annot=True, cmap='viridis', ax=ax3)
    ax3.set_title('Normalized Factors (0-1 scale)', fontsize=14)
    
    # Plot 4: Scatter plot of intelligence vs speed with cost as size
    ax4 = axes[1, 1]
    scatter = ax4.scatter(
        results['intelligence'], 
        results['speed'],
        s=400 * (1 - results['cost']/COST_MAX),  # Size inversely related to cost
        alpha=0.6
    )
    
    ax4.set_xlabel('Intelligence Score (0-100)')
    ax4.set_ylabel('Speed (tokens/s)')
    ax4.set_title('Intelligence vs Speed (larger bubbles = more cost-efficient)', fontsize=14)
    
    # Add model names as annotations
    for idx, row in results.iterrows():
        ax4.annotate(
            row['model'],
            (row['intelligence'], row['speed']),
            xytext=(5, 5),
            textcoords='offset points'
        )
    
    # Add a title for the entire figure
    plt.suptitle(f'LLM Model Comparison\nWeights: Intelligence={weights["intelligence"]:.2f}, '
                f'Speed={weights["speed"]:.2f}, Cost={weights["cost"]:.2f}', 
                fontsize=16)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(save_path)
    return fig

def main():
    print("\n=== LLM Model Comparison Tool ===\n")
    
    # Set output folder
    output_folder = '/Users/greatmaster/Desktop/projects/oreilly-live-trainings/oreilly-reasoning-models/notebooks'
    os.makedirs(output_folder, exist_ok=True)
    
    # Option to use example data or input custom data
    use_example = input("Use example data? (y/n): ").strip().lower() == 'y'
    
    if use_example:
        # Example data for popular LLMs
        data = {
            'model': ['Nova Micro', 'Gemini 2.0 Flash', 'Command R', 'Llama 3.1 70B', 
                      'Claude 3 Opus', 'GPT-4o', 'Mistral Large', 'Claude 3 Sonnet'],
            'intelligence': [82, 78, 75, 70, 92, 90, 72, 88],
            'speed': [316, 254, 181, 179, 111, 125, 162, 119],
            'cost': [12, 8, 10, 15, 25, 20, 7, 15]
        }
        
        # Default weights
        weights = {
            'intelligence': 0.4,
            'speed': 0.4,
            'cost': 0.2
        }
        
        # Option to customize weights
        if input("\nUse default weights (Intelligence=0.4, Speed=0.4, Cost=0.2)? (y/n): ").strip().lower() == 'n':
            print("\nEnter weights (they'll be normalized to sum to 1.0):")
            w_intelligence = float(input("Intelligence weight: "))
            w_speed = float(input("Speed weight: "))
            w_cost = float(input("Cost weight: "))
            
            # Normalize to sum to 1
            total = w_intelligence + w_speed + w_cost
            weights = {
                'intelligence': w_intelligence / total,
                'speed': w_speed / total,
                'cost': w_cost / total
            }
    else:
        # Get user input for models
        models = []
        num_models = int(input("Enter number of models to compare: "))
        
        for i in range(num_models):
            print(f"\nModel {i+1} details:")
            model_name = input("Model name: ")
            intelligence = float(input(f"Intelligence score (0-{INTELLIGENCE_MAX}): "))
            speed = float(input(f"Speed (tokens/s, 0-{SPEED_MAX}): "))
            cost = float(input(f"Cost ($/1M tokens, 0-{COST_MAX}): "))
            
            models.append({
                'model': model_name,
                'intelligence': intelligence,
                'speed': speed,
                'cost': cost
            })
        
        data = {
            'model': [m['model'] for m in models],
            'intelligence': [m['intelligence'] for m in models],
            'speed': [m['speed'] for m in models],
            'cost': [m['cost'] for m in models]
        }
        
        # Get weights
        print("\nEnter weights for each factor (they'll be normalized to sum to 1.0):")
        w_intelligence = float(input("Intelligence weight: "))
        w_speed = float(input("Speed weight: "))
        w_cost = float(input("Cost weight: "))
        
        # Normalize to sum to 1
        total = w_intelligence + w_speed + w_cost
        weights = {
            'intelligence': w_intelligence / total,
            'speed': w_speed / total,
            'cost': w_cost / total
        }
    
    # Create DataFrame and calculate scores
    df = pd.DataFrame(data)
    results = calculate_scores(df, weights)
    
    # Display results
    print("\nModel Comparison Results:")
    print(tabulate(
        results[['model', 'intelligence', 'speed', 'cost', 
                'intelligence_norm', 'speed_norm', 'cost_norm', 
                'intelligence_score', 'speed_score', 'cost_score', 'total_score']],
        headers='keys',
        tablefmt='grid',
        floatfmt='.3f'
    ))
    
    # Create visualizations
    fig_path = os.path.join(output_folder, 'llm_model_comparison.png')
    visualize_results(results, weights, fig_path)
    
    # Save to CSV
    csv_path = os.path.join(output_folder, 'llm_model_comparison.csv')
    results.to_csv(csv_path, index=False)
    
    # Save as Python script for future use/modification
    py_path = os.path.join(output_folder, 'llm_model_comparison.py')
    
    with open(py_path, 'w') as f:
        f.write("""
# LLM Model Comparison Script
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Normalization ranges
INTELLIGENCE_MAX = 100  # intelligence index
SPEED_MAX = 500        # tokens per second
COST_MAX = 100         # $ per 1M tokens

# Define normalization and scoring functions
""")
        # Add the rest of the script content...
        f.write(f"""
# Weights used in this analysis
weights = {weights}

# Model data used in this analysis
model_data = {results[['model', 'intelligence', 'speed', 'cost']].to_dict('records')}

# Load the results directly
results_df = pd.read_csv('{csv_path}')
print("Top models by total score:")
print(results_df[['model', 'total_score']].head())
""")
    
    print(f"\nResults saved to {output_folder}:")
    print(f"- CSV data: {csv_path}")
    print(f"- Visualization: {fig_path}")
    print(f"- Python script: {py_path}")
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()

# This script:

# 1. Takes input data for LLM models (either example or custom)
# 2. Normalizes each factor using your specified ranges (0-100 for intelligence, 0-500 for speed, 0-100 for cost)
# 3. Applies weights to calculate scores
# 4. Generates visualizations including:
#    - Bar chart of total scores
#    - Stacked bar chart showing contribution of each factor
#    - Heatmap of normalized values
#    - Scatter plot of intelligence vs speed (with bubble size representing cost efficiency)
# 5. Saves results in multiple formats (CSV, visualization, Python script)

# You can run this script and either use the example data or input your own model information.