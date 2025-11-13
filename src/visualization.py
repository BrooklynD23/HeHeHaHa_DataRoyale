"""
Visualization Templates

Presentation-ready chart templates for the competition.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List
import warnings

warnings.filterwarnings('ignore')


def setup_presentation_style():
    """
    Configure matplotlib/seaborn for presentation-quality plots.

    Call this at the start of your visualization notebook.
    """
    # Seaborn style
    sns.set_style("whitegrid")
    sns.set_context("talk")  # Larger fonts for presentations

    # Matplotlib settings
    plt.rcParams['figure.figsize'] = (12, 7)
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 14
    plt.rcParams['figure.titlesize'] = 20

    # Use colorblind-friendly palette
    sns.set_palette("colorblind")

    print("✓ Presentation style configured")


def save_figure(filename: str, dpi: int = 300, bbox_inches: str = 'tight'):
    """
    Save current figure to presentation/figures/ directory.

    Args:
        filename: Output filename (e.g., 'card_winrates.png')
        dpi: Resolution (300 for high quality)
        bbox_inches: 'tight' to remove whitespace
    """
    import os
    # Find project root (go up from src/ to project root)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    figures_dir = os.path.join(project_root, 'presentation', 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    output_path = os.path.join(figures_dir, filename)
    plt.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
    print(f"✓ Saved to {output_path}")


def plot_win_rate_comparison(
    data: pd.DataFrame,
    category_col: str,
    win_rate_col: str,
    title: str,
    top_n: int = 15,
    figsize: Tuple[int, int] = (12, 8)
) -> plt.Figure:
    """
    Create horizontal bar chart for win rate comparisons.

    Args:
        data: DataFrame with category and win rate columns
        category_col: Column name for categories (e.g., 'card_name')
        win_rate_col: Column name for win rates (0-1 or 0-100)
        title: Chart title
        top_n: Number of top categories to show

    Returns:
        matplotlib Figure object

    Example:
        >>> fig = plot_win_rate_comparison(
        ...     card_stats,
        ...     'card_name',
        ...     'win_rate',
        ...     'Top 15 Cards by Win Rate'
        ... )
    """
    # Sort and take top N
    plot_data = data.nlargest(top_n, win_rate_col)

    fig, ax = plt.subplots(figsize=figsize)

    # Horizontal bar chart (easier to read labels)
    sns.barplot(
        data=plot_data,
        y=category_col,
        x=win_rate_col,
        ax=ax,
        palette='Blues_r'
    )

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Win Rate (%)', fontsize=16)
    ax.set_ylabel('')

    # Format x-axis as percentage
    if plot_data[win_rate_col].max() <= 1:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.1f}%'))
    else:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}%'))

    # Add value labels
    for i, (idx, row) in enumerate(plot_data.iterrows()):
        value = row[win_rate_col]
        if value <= 1:
            label = f'{value*100:.1f}%'
        else:
            label = f'{value:.1f}%'
        ax.text(value, i, f'  {label}', va='center', fontsize=12)

    plt.tight_layout()
    return fig


def plot_distribution(
    data: pd.Series,
    title: str,
    xlabel: str,
    bins: int = 50,
    kde: bool = True,
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Create histogram with optional KDE overlay.

    Args:
        data: pandas Series to plot
        title: Chart title
        xlabel: X-axis label
        bins: Number of histogram bins
        kde: Whether to overlay kernel density estimate

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)

    sns.histplot(data, bins=bins, kde=kde, ax=ax, color='steelblue')

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel('Count', fontsize=16)

    # Add mean and median lines
    mean_val = data.mean()
    median_val = data.median()

    ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')

    ax.legend()

    plt.tight_layout()
    return fig


def plot_grouped_comparison(
    data: pd.DataFrame,
    group_col: str,
    value_col: str,
    title: str,
    ylabel: str,
    figsize: Tuple[int, int] = (12, 6)
) -> plt.Figure:
    """
    Create grouped bar chart or box plot.

    Args:
        data: DataFrame
        group_col: Column for grouping
        value_col: Column with values to plot
        title: Chart title
        ylabel: Y-axis label

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)

    sns.boxplot(
        data=data,
        x=group_col,
        y=value_col,
        ax=ax,
        palette='Set2'
    )

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(group_col.replace('_', ' ').title(), fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)

    # Rotate x-labels if needed
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    return fig


def plot_correlation_heatmap(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = 'Feature Correlations',
    figsize: Tuple[int, int] = (10, 8),
    annot: bool = True
) -> plt.Figure:
    """
    Create correlation heatmap.

    Args:
        data: DataFrame
        columns: List of columns to include (None = all numeric)
        title: Chart title
        figsize: Figure size
        annot: Whether to annotate cells with values

    Returns:
        matplotlib Figure object
    """
    if columns:
        corr_data = data[columns].corr()
    else:
        corr_data = data.select_dtypes(include=[np.number]).corr()

    fig, ax = plt.subplots(figsize=figsize)

    sns.heatmap(
        corr_data,
        annot=annot,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={'shrink': 0.8},
        ax=ax
    )

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


def plot_time_series(
    data: pd.DataFrame,
    time_col: str,
    value_col: str,
    title: str,
    ylabel: str,
    confidence_interval: bool = True,
    figsize: Tuple[int, int] = (14, 6)
) -> plt.Figure:
    """
    Create time series line plot.

    Args:
        data: DataFrame
        time_col: Column with time/date values
        value_col: Column with values to plot
        title: Chart title
        ylabel: Y-axis label
        confidence_interval: Whether to show confidence bands

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)

    if confidence_interval and len(data) > 30:
        # Calculate rolling mean and std
        window = max(len(data) // 20, 3)
        rolling_mean = data.groupby(time_col)[value_col].mean()
        rolling_std = data.groupby(time_col)[value_col].std()

        ax.plot(rolling_mean.index, rolling_mean.values, linewidth=2, label='Mean')
        ax.fill_between(
            rolling_mean.index,
            rolling_mean - rolling_std,
            rolling_mean + rolling_std,
            alpha=0.3,
            label='±1 Std Dev'
        )
    else:
        data_grouped = data.groupby(time_col)[value_col].mean()
        ax.plot(data_grouped.index, data_grouped.values, linewidth=2)

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Time', fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)

    if confidence_interval:
        ax.legend()

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def plot_scatter_with_regression(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    hue_col: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 7)
) -> plt.Figure:
    """
    Create scatter plot with regression line.

    Args:
        data: DataFrame
        x_col: Column for x-axis
        y_col: Column for y-axis
        title: Chart title
        hue_col: Optional column for color grouping

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)

    sns.regplot(
        data=data,
        x=x_col,
        y=y_col,
        ax=ax,
        scatter_kws={'alpha': 0.5, 's': 50},
        line_kws={'color': 'red', 'linewidth': 2}
    )

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(x_col.replace('_', ' ').title(), fontsize=16)
    ax.set_ylabel(y_col.replace('_', ' ').title(), fontsize=16)

    # Add correlation coefficient
    corr = data[[x_col, y_col]].corr().iloc[0, 1]
    ax.text(
        0.05, 0.95,
        f'Correlation: {corr:.3f}',
        transform=ax.transAxes,
        fontsize=14,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )

    plt.tight_layout()
    return fig


def plot_stacked_bar(
    data: pd.DataFrame,
    category_col: str,
    stack_cols: List[str],
    title: str,
    ylabel: str = 'Count',
    figsize: Tuple[int, int] = (12, 7)
) -> plt.Figure:
    """
    Create stacked bar chart.

    Args:
        data: DataFrame
        category_col: Column for x-axis categories
        stack_cols: List of columns to stack
        title: Chart title
        ylabel: Y-axis label

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=figsize)

    data_pivot = data.groupby(category_col)[stack_cols].sum()

    data_pivot.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        colormap='Set3'
    )

    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(category_col.replace('_', ' ').title(), fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.legend(title='', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def create_insight_annotation(
    ax: plt.Axes,
    text: str,
    xy: Tuple[float, float],
    xytext: Tuple[float, float],
    fontsize: int = 12
):
    """
    Add an annotation arrow to highlight a key insight.

    Args:
        ax: Matplotlib axes object
        text: Annotation text
        xy: Point to annotate (data coordinates)
        xytext: Text position (data coordinates)
        fontsize: Font size for annotation
    """
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        fontsize=fontsize,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', linewidth=2)
    )
