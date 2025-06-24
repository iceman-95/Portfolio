# Car Price Analysis

This project performs a comprehensive analysis of car prices and their relationships with various features using Python. The analysis includes data visualization, statistical analysis, and feature engineering to understand the factors that influence car prices.

## Features

- Data preprocessing and cleaning
- Conversion of MPG to L/100km for better understanding
- Price categorization (Low, Medium, High)
- Feature normalization
- Categorical data encoding
- Interactive data visualization
- Statistical analysis
- Price distribution analysis
- Correlation analysis between different features

## Visualizations

The project generates several visualizations saved in the `output` directory:
- Price category distribution
- Histogram of normalized prices
- Boxplot of prices by category
- Heatmap of mean prices by drive-wheels and body-style

## Requirements

- Python 3.x
- pandas
- matplotlib
- seaborn
- scikit-learn
- tkinter

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```
4. Install required packages:
   ```bash
   pip install pandas matplotlib seaborn scikit-learn
   ```

## Usage

1. Ensure your dataset is in the correct format (CSV file named 'dataset.txt')
2. Run the analysis script:
   ```bash
   python car_price_analysis.py
   ```

## Data Structure

The dataset includes the following features:
- symboling
- normalized-losses
- make
- fuel-type
- aspiration
- num-of-doors
- body-style
- drive-wheels
- engine-location
- wheel-base
- length
- width
- height
- curb-weight
- engine-type
- num-of-cylinders
- engine-size
- fuel-system
- bore
- stroke
- compression-ratio
- horsepower
- peak-rpm
- city-mpg
- highway-mpg
- price

## Output

The analysis generates:
1. Interactive visualizations displayed during runtime
2. Saved plots in the `output` directory
3. Statistical summaries and analysis results in the console

## License

This project is open source and available under the MIT License. 