import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import seaborn as sns
import os
from scipy.ndimage import gaussian_filter1d

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

def plot_faults(df):
    """Plot the distribution of fault types."""
    plt.figure(figsize=(12, 6))
    df["Fault_Type"].value_counts().plot(kind="bar", color="royalblue")
    plt.xlabel("Fault Type")
    plt.ylabel("Count")
    plt.title("Fault Type Distribution")
    plt.savefig("reports/fault_distribution.png")
    plt.close()

def plot_voltage_current(df):
    """Plot voltage and current trends over time with smoothing (lissage)."""
    df = df.sort_values(by="Timestamp")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    plt.figure(figsize=(12, 6))
    for phase in ["A", "B", "C"]:
        smoothed_voltage = gaussian_filter1d(df[f"V_{phase} (kV)"], sigma=2)
        plt.plot(df["Timestamp"], smoothed_voltage, label=f"Smoothed Voltage {phase}")
    plt.xlabel("Time")
    plt.ylabel("Voltage (kV)")
    plt.title("Voltage Trends Over Time (Smoothed)")
    plt.legend()
    plt.savefig("reports/smoothed_voltage_trends.png")
    plt.close()

    plt.figure(figsize=(12, 6))
    for phase in ["A", "B", "C"]:
        smoothed_current = gaussian_filter1d(df[f"I_{phase} (A)"], sigma=2)
        plt.plot(df["Timestamp"], smoothed_current, label=f"Smoothed Current {phase}")
    plt.xlabel("Time")
    plt.ylabel("Current (A)")
    plt.title("Current Trends Over Time (Smoothed)")
    plt.legend()
    plt.savefig("reports/smoothed_current_trends.png")
    plt.close()

def plot_correlation_matrix(df):
    """Plot a correlation heatmap for numerical features."""
    numeric_df = df.select_dtypes(include=["number"])  # Only select numeric columns
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.savefig("reports/correlation_matrix.png")
    plt.close()
    
def generate_fault_report(df):
    """Generate a PDF report with all fault-related visualizations."""
    df = df.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])  # Ensure proper time indexing

    # Generate plots
    plot_faults(df)
    plot_voltage_current(df)
    plot_correlation_matrix(df)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Fault Analysis Report", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(190, 10, "This report presents an analysis of fault types detected in the system.")

    # Insert the plots
    pdf.ln(5)
    pdf.image("reports/fault_distribution.png", x=15, w=180)
    pdf.ln(10)
    pdf.image("reports/smoothed_voltage_trends.png", x=15, w=180)
    pdf.ln(10)
    pdf.image("reports/smoothed_current_trends.png", x=15, w=180)
    pdf.ln(10)
    pdf.image("reports/correlation_matrix.png", x=15, w=180)
    pdf.ln(10)

    # Save the report
    pdf.output("reports/fault_report.pdf")
    print("✅ Fault report saved as 'reports/fault_report.pdf'.")
