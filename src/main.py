from system import FaultAnalysisSystem
from visualization import generate_fault_report  # Import the new function

if __name__ == "__main__":
    # Initialize and run the system
    system = FaultAnalysisSystem(data_path="data/grte_data.csv")
    system.run()

    # Generate fault report after analysis
    generate_fault_report(system.data)
