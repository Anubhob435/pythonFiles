# Seaborn: Statistical Data Visualization in Python

## Introduction
Seaborn is a Python data visualization library based on matplotlib that provides a high-level interface for drawing attractive and informative statistical graphics. It's specifically designed to work well with pandas DataFrames and offers built-in themes for styling matplotlib graphics.

## Installation
```python
# Using pip
pip install seaborn

# Using conda
conda install seaborn
```

## Key Features
- **Built on Matplotlib**: Extends matplotlib's functionality with a more intuitive interface
- **Integration with pandas**: Works seamlessly with pandas DataFrames
- **Statistical estimation**: Automatic statistical estimation and plotting
- **Beautiful default aesthetics**: Attractive themes and color palettes
- **Complex visualizations with minimal code**: Simplifies the creation of complex visualizations

## Importing Seaborn
```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
```

## Main Plot Types

### 1. Relational Plots
#### Scatter plots (scatterplot, relplot)
```python
# Basic scatter plot
tips = sns.load_dataset("tips")
sns.scatterplot(x="total_bill", y="tip", data=tips)
plt.show()

# With additional dimensions using hue, size, and style
sns.relplot(
    x="total_bill", y="tip", 
    hue="smoker", size="size", 
    style="time", data=tips
)
plt.show()
```

#### Line plots (lineplot)
```python
# Basic line plot
fmri = sns.load_dataset("fmri")
sns.lineplot(x="timepoint", y="signal", data=fmri)
plt.show()
```

### 2. Categorical Plots
#### Bar plots (barplot)
```python
# Bar plot showing mean values
sns.barplot(x="day", y="total_bill", data=tips)
plt.show()
```

#### Box plots (boxplot)
```python
# Box plot
sns.boxplot(x="day", y="total_bill", data=tips)
plt.show()
```

#### Violin plots (violinplot)
```python
# Violin plot combines box plot with kernel density estimation
sns.violinplot(x="day", y="total_bill", data=tips)
plt.show()
```

#### Count plots (countplot)
```python
# Count plot - show counts of observations in each categorical bin
sns.countplot(x="day", data=tips)
plt.show()
```

### 3. Distribution Plots
#### Histogram (histplot)
```python
# Histogram
sns.histplot(tips["total_bill"], kde=True)
plt.show()
```

#### Kernel Density Estimation (kdeplot)
```python
# KDE plot
sns.kdeplot(data=tips["total_bill"], shade=True)
plt.show()
```

### 4. Matrix Plots
#### Heatmaps (heatmap)
```python
# Generate a correlation matrix
corr = tips.corr()
# Plot heatmap
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()
```

#### Cluster maps (clustermap)
```python
# Clustered heatmap
sns.clustermap(corr, annot=True, cmap="coolwarm")
plt.show()
```

### 5. Regression Plots
#### Simple regression (regplot)
```python
# Simple regression plot
sns.regplot(x="total_bill", y="tip", data=tips)
plt.show()
```

#### Advanced regression (lmplot)
```python
# Advanced regression with facets
sns.lmplot(x="total_bill", y="tip", hue="smoker", col="time", data=tips)
plt.show()
```

### 6. Multi-plot Grids
#### Pair plots (pairplot)
```python
# Create pairwise relationships
iris = sns.load_dataset("iris")
sns.pairplot(iris, hue="species")
plt.show()
```

#### Joint plots (jointplot)
```python
# Joint distribution plot
sns.jointplot(x="total_bill", y="tip", data=tips, kind="reg")
plt.show()
```

## Customizing Seaborn Plots

### Setting Themes
```python
# Available themes: darkgrid, whitegrid, dark, white, ticks
sns.set_theme(style="whitegrid")
sns.set_theme(style="darkgrid")
sns.set_theme(style="ticks")
```

### Using Color Palettes
```python
# Predefined palettes: deep, muted, pastel, bright, dark, colorblind
sns.set_palette("pastel")

# Using specific colors
sns.set_palette(["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"])
```

### Figure Aesthetics
```python
# Control figure aesthetics
sns.set_context("paper")  # Options: paper, notebook, talk, poster
sns.set_context("talk", font_scale=1.4)
```

## Working with Seaborn and pandas
```python
# Creating a complex visualization from a pandas DataFrame
titanic = sns.load_dataset("titanic")

# Grid of plots
g = sns.FacetGrid(titanic, col="survived", row="class", height=2.5, aspect=1.5)
g.map_dataframe(sns.histplot, x="age")
g.set_axis_labels("Age", "Count")
g.set_titles(col_template="{col_name} = {col_var}", row_template="{row_name} = {row_var}")
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Age Distribution by Survival Status and Class")
plt.show()
```

## Advanced Example: Combining Multiple Plot Types
```python
# Create a figure with different plot types
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Box plot
sns.boxplot(x="day", y="total_bill", data=tips, ax=axes[0, 0])
axes[0, 0].set_title("Box Plot")

# Plot 2: Violin plot
sns.violinplot(x="day", y="total_bill", data=tips, ax=axes[0, 1])
axes[0, 1].set_title("Violin Plot")

# Plot 3: Bar plot
sns.barplot(x="day", y="total_bill", data=tips, ax=axes[1, 0])
axes[1, 0].set_title("Bar Plot")

# Plot 4: Swarm plot
sns.swarmplot(x="day", y="total_bill", data=tips, ax=axes[1, 1])
axes[1, 1].set_title("Swarm Plot")

plt.tight_layout()
plt.show()
```

## Tips for Effective Visualization with Seaborn
1. **Choose the right plot type** based on your data and what you want to communicate
2. **Use color consciously** - color should enhance understanding, not distract
3. **Don't overload your plots** with too many variables or dimensions
4. **Label everything clearly** - axes, titles, legends
5. **Consider your audience** when designing visualizations

## Resources for Learning More
- [Seaborn Official Documentation](https://seaborn.pydata.org/)
- [Seaborn Tutorial Gallery](https://seaborn.pydata.org/examples/index.html)
- [Seaborn API Reference](https://seaborn.pydata.org/api.html)

## Conclusion
Seaborn makes it easy to create beautiful and informative statistical visualizations in Python. Its tight integration with pandas and matplotlib provides a powerful toolkit for exploring and presenting data. Whether you're doing exploratory data analysis, creating visualizations for presentations, or generating publication-quality figures, Seaborn is an essential library in a data scientist's toolbox.
