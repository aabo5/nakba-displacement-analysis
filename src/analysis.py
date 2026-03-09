"""
Statistical Analysis of Palestinian Displacement Data (1947–2024)

This script performs descriptive statistics, confidence interval estimation,
sample size calculation, hypothesis testing, and data visualization on
historical displacement data from the Nakba and subsequent events.

Author: Abdelfatah M.A Alhoot
Course: Statistics Project (2321051372)
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Nakba_Displacement_Historical.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


def load_data() -> pd.DataFrame:
    """Load the displacement dataset from CSV."""
    return pd.read_csv(DATA_PATH)


def descriptive_statistics(df: pd.DataFrame) -> dict:
    """Calculate and print descriptive statistics."""
    col = df["Estimated_Displaced"]
    result = {
        "mean": col.mean(),
        "median": col.median(),
        "variance": col.var(),
        "std_dev": col.std(),
        "std_error": col.std() / (len(df) ** 0.5),
    }

    print("\n[Descriptive Statistics]")
    print(f"   Mean             : {result['mean']:>12,.2f}")
    print(f"   Median           : {result['median']:>12,.2f}")
    print(f"   Variance         : {result['variance']:>12,.2f}")
    print(f"   Standard Deviation: {result['std_dev']:>12,.2f}")
    print(f"   Standard Error   : {result['std_error']:>12,.2f}")

    return result


def confidence_intervals(df: pd.DataFrame, stats_dict: dict) -> None:
    """Compute and print 95% confidence intervals for mean and variance."""
    n = len(df)
    mean = stats_dict["mean"]
    variance = stats_dict["variance"]
    se = stats_dict["std_error"]

    ci_mean = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)
    ci_var = (
        (n - 1) * variance / stats.chi2.ppf(0.975, n - 1),
        (n - 1) * variance / stats.chi2.ppf(0.025, n - 1),
    )

    print("\n[95% Confidence Intervals]")
    print(f"   Mean     : ({ci_mean[0]:>12,.2f}, {ci_mean[1]:>12,.2f})")
    print(f"   Variance : ({ci_var[0]:>12,.2f}, {ci_var[1]:>12,.2f})")


def sample_size_estimation(std_dev: float) -> None:
    """Estimate the required sample size (margin = 10% of std dev, alpha = 0.10)."""
    Z = 1.645 e
    E = 0.1 * std_dev
    required_n = (Z * std_dev / E) ** 2

    print(f"\n[Sample Size Estimation]")
    print(f"   Required n (90% confidence): {int(required_n) + 1}")


def hypothesis_test(df: pd.DataFrame) -> None:
    """Perform a one-sample t-test against H0: mu = 250,000."""
    t_stat, p_val = stats.ttest_1samp(df["Estimated_Displaced"], 250_000)

    print("\n[Hypothesis Test]")
    print(f"   H0 : Mean displacement = 250,000")
    print(f"   H1 : Mean displacement != 250,000")
    print(f"   T-statistic : {t_stat:.4f}")
    print(f"   P-value     : {p_val:.4f}")

    if p_val < 0.05:
        print("   => Reject H0 -- mean is significantly different from 250,000")
    else:
        print("   => Fail to reject H0")


def visualize(df: pd.DataFrame) -> None:
    """Generate a histogram and boxplot of displacement data."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram
    sns.histplot(
        df["Estimated_Displaced"], kde=True, color="#2e8b57", bins=10, ax=axes[0]
    )
    axes[0].set_title("Distribution of Displacement Estimates", fontsize=12)
    axes[0].set_xlabel("Estimated Displaced")
    axes[0].set_ylabel("Frequency")

# Boxplot
    sns.boxplot(x=df["Estimated_Displaced"], color="#f4a261", ax=axes[1])
    axes[1].set_title("Boxplot — Outlier Detection", fontsize=12)
    axes[1].set_xlabel("Estimated Displaced")

    plt.tight_layout()
    output_path = OUTPUT_DIR / "Displacement_Plots.png"
    plt.savefig(output_path, dpi=150)
    print(f"\n[Plot saved to: {output_path}]")
    plt.show()


def main() -> None:
    """Run the full analysis pipeline."""
    print("=" * 65)
    print("  Nakba in Numbers:")
    print("  A Statistical Analysis of Palestinian Displacement (1947-2024)")
    print("=" * 65)

    df = load_data()
    result = descriptive_statistics(df)
    confidence_intervals(df, result)
    sample_size_estimation(result["std_dev"])
    hypothesis_test(df)
    visualize(df)

    print("  Analysis complete.")


if __name__ == "__main__":
    main()
