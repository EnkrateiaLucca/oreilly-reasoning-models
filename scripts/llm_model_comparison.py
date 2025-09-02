
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

# Weights used in this analysis
weights = {'intelligence': 0.4, 'speed': 0.4, 'cost': 0.2}

# Model data used in this analysis
model_data = [{'model': 'Nova Micro', 'intelligence': 82, 'speed': 316, 'cost': 12}, {'model': 'Gemini 2.0 Flash', 'intelligence': 78, 'speed': 254, 'cost': 8}, {'model': 'Command R', 'intelligence': 75, 'speed': 181, 'cost': 10}, {'model': 'GPT-4o', 'intelligence': 90, 'speed': 125, 'cost': 20}, {'model': 'Claude 3 Sonnet', 'intelligence': 88, 'speed': 119, 'cost': 15}, {'model': 'Claude 3 Opus', 'intelligence': 92, 'speed': 111, 'cost': 25}, {'model': 'Mistral Large', 'intelligence': 72, 'speed': 162, 'cost': 7}, {'model': 'Llama 3.1 70B', 'intelligence': 70, 'speed': 179, 'cost': 15}]

# Load the results directly
results_df = pd.read_csv('./llm_model_comparison.csv')
print("Top models by total score:")
print(results_df[['model', 'total_score']].head())
