import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

try:
    # Read the CSV file with proper delimiter and quotechar
    df = pd.read_csv('dataset.txt', header=None, delimiter=',', quotechar='"')
    
    # Assign column headers
    columns = [
        "symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors",
        "body-style", "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight",
        "engine-type", "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke", "compression-ratio",
        "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"
    ]
    df.columns = columns

    print('DataFrame shape:', df.shape)
    print(df.head())
    # Show full DataFrame in a separate window using tkinter
    def show_dataframe_window(df):
        root = tk.Tk()
        root.title('Full DataFrame')
        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)
        xscroll = tk.Scrollbar(frame, orient='horizontal')
        xscroll.pack(side='bottom', fill='x')
        text = ScrolledText(frame, width=180, height=40, font=('Courier', 10), wrap='none', xscrollcommand=xscroll.set)
        text.pack(fill='both', expand=True)
        xscroll.config(command=text.xview)
        text.insert('end', df.to_string())
        text.config(state='disabled')
        root.mainloop()
    show_dataframe_window(df)

    # Check for missing values
    print('\nMissing values per column:')
    print(df.isnull().sum())

    # Convert MPG to L/100km
    df['city-mpg'] = pd.to_numeric(df['city-mpg'], errors='coerce')
    df['highway-mpg'] = pd.to_numeric(df['highway-mpg'], errors='coerce')
    df['city-L/100km'] = 235.214583 / df['city-mpg']
    df['highway-L/100km'] = 235.214583 / df['highway-mpg']

    print('\nConverted city-mpg and highway-mpg to L/100km:')
    print(df[['city-mpg', 'city-L/100km', 'highway-mpg', 'highway-L/100km']].head())

    # Convert price column to integer
    df['price'] = pd.to_numeric(df['price'], errors='coerce').astype('Int64')
    print('\nPrice column after conversion to integer:')
    print(df['price'].head())

    # Normalize numerical columns
    from sklearn.preprocessing import MinMaxScaler
    numeric_cols = [
        "symboling", "normalized-losses", "wheel-base", "length", "width", "height", "curb-weight",
        "engine-size", "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
        "city-mpg", "highway-mpg", "city-L/100km", "highway-L/100km", "price"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print('\nHead of normalized numerical columns:')
    print(df_normalized[numeric_cols].head())

    # Categorize cars based on price with custom bins
    price_bins = [float('-inf'), 15000, 20000, float('inf')]
    price_labels = ['Low', 'Medium', 'High']
    df['price_category'] = pd.cut(df['price'], bins=price_bins, labels=price_labels, include_lowest=True)
    
    # Print detailed price category distribution
    print('\nDetailed Price Category Distribution:')
    price_distribution = df['price_category'].value_counts()
    print('\nCount of cars in each price category:')
    print(price_distribution)
    print('\nPercentage distribution:')
    print((price_distribution / len(df) * 100).round(2))
    
    # Visualization: Bar plot with percentage labels
    plt.figure(figsize=(10, 7), dpi=120)
    ax = sns.countplot(x='price_category', data=df, order=['Low', 'Medium', 'High'])
    plt.title('Distribution of Cars by Price Category')
    plt.xlabel('Price Category')
    plt.ylabel('Count')
    total = len(df)
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        ax.annotate(percentage, (p.get_x() + p.get_width() / 2., p.get_height() * 0.95),
                    ha='center', va='top', fontsize=12, color='white', fontweight='bold')
    plt.tight_layout()
    plt.savefig('output/price_category_distribution.png')
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')
    except Exception:
        try:
            mng.window.showMaximized()
        except Exception:
            pass
    plt.show()
    plt.close()
    
    print('\nPrice statistics by category:')
    print(df.groupby('price_category', observed=False)['price'].agg(['min', 'max', 'mean', 'count']).round(2))
    
    print('\nPrice categories (custom bins):')
    print(df[['price', 'price_category']].head(20))

    # Add price_category to normalized DataFrame for plotting
    df_normalized['price_category'] = df['price_category']

    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    # 1. Histogram of normalized price
    plt.figure(figsize=(12, 8), dpi=120)
    ax = sns.histplot(df_normalized['price'], kde=True)
    plt.title('Histogram of Normalized Price')
    plt.xlabel('Normalized Price')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('output/histogram_normalized_price.png')
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')
    except Exception:
        try:
            mng.window.showMaximized()
        except Exception:
            pass
    plt.show()
    plt.close()

    # 2. Count plot of price categories
    plt.figure(figsize=(10, 7), dpi=120)
    ax = sns.countplot(x='price_category', data=df)
    plt.title('Count of Cars by Price Category')
    plt.xlabel('Price Category')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('output/count_price_category.png')
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')
    except Exception:
        try:
            mng.window.showMaximized()
        except Exception:
            pass
    plt.show()
    plt.close()

    # 3. Boxplot of normalized price by price category
    plt.figure(figsize=(12, 8), dpi=120)
    ax = sns.boxplot(x='price_category', y='price', data=df_normalized)
    plt.title('Boxplot of Normalized Price by Price Category')
    plt.xlabel('Price Category')
    plt.ylabel('Normalized Price')
    plt.tight_layout()
    plt.savefig('output/boxplot_normalized_price_by_category.png')
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')
    except Exception:
        try:
            mng.window.showMaximized()
        except Exception:
            pass
    plt.show()
    plt.close()

    # Convert categorical columns to numerical using one-hot encoding
    categorical_cols = [
        "make", "fuel-type", "aspiration", "num-of-doors", "body-style", "drive-wheels",
        "engine-location", "engine-type", "num-of-cylinders", "fuel-system", "price_category"
    ]
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    print('\nHead of DataFrame after converting categorical columns to numerical:')
    print(df_encoded.head())

    # Grouping Data by Drive-Wheels and Body-Style
    grouped = df.groupby(['drive-wheels', 'body-style'])['price'].mean().reset_index()
    print('\nMean price grouped by drive-wheels and body-style:')
    print(grouped)

    # Create a Pivot Table
    pivot = df.pivot_table(values='price', index='drive-wheels', columns='body-style', aggfunc='mean')
    print('\nPivot Table (mean price):')
    print(pivot)

    # Convert pivot table to float to handle NAType for heatmap
    pivot = pivot.astype(float)

    # Plot a Heatmap
    plt.figure(figsize=(14, 10), dpi=120)
    ax = sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('Mean Price by Drive-Wheels and Body-Style')
    plt.ylabel('Drive-Wheels')
    plt.xlabel('Body-Style')
    plt.tight_layout()
    plt.savefig('output/heatmap_drivewheels_bodystyle.png')
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')
    except Exception:
        try:
            mng.window.showMaximized()
        except Exception:
            pass
    plt.show()
    plt.close()

except Exception as e:
    print(f"An error occurred: {str(e)}")
    import traceback
    print("\nDetailed error information:")
    print(traceback.format_exc()) 