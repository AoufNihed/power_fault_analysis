import pandas as pd
import numpy as np
from analyzers.fault_analyzer import FaultAnalyzer
from analyzers.predictive_model import PredictiveModel

class FaultAnalysisSystem:
    def __init__(self, data_path):
        """Initialize system with data and required components."""
        self.data_path = data_path
        self.data = pd.read_csv(data_path)

        # Initialize fault analyzer with data
        self.fault_analyzer = FaultAnalyzer(self.data)

        # Initialize predictive model (without pre-loading data)
        self.model = PredictiveModel()  # ✅ FIXED

    def run(self):
        """Run the fault analysis system."""
        print("🔄 Running Fault Analysis...")

        # Step 1: Classify existing faults
        print("🔍 Classifying faults...")
        self.data['Fault_Type'] = self.data.apply(self.fault_analyzer.classify_faults, axis=1)

        # Save classified data
        self.data.to_csv("data/fault_classified.csv", index=False)
        print("✅ Fault classification completed and saved.")

        # Step 2: Train the model
        print("🤖 Training predictive model...")
        if self.data['Fault_Type'].nunique() > 1:
            self.model.train_model(self.data)  # ✅ Pass data correctly

            # Step 3: Generate simulated future data
            print("🔮 Generating simulated future data...")
            date_range = pd.date_range(start="2025-08-01 00:00:00", periods=144, freq='10T')
            next_week_range = pd.date_range(start="2025-08-08 00:00:00", periods=144, freq='10T')
            simulated_data = pd.DataFrame({
                'V_A (kV)': np.random.uniform(220, 240, 144),
                'V_B (kV)': np.random.uniform(220, 240, 144),
                'V_C (kV)': np.random.uniform(220, 240, 144),
                'I_A (A)': np.random.uniform(10, 20, 144),
                'I_B (A)': np.random.uniform(10, 20, 144),
                'I_C (A)': np.random.uniform(10, 20, 144)
            }, index=date_range)
            next_week_data = simulated_data.copy()
            next_week_data.index = next_week_range

            # Step 4: Predict future faults
            print("🔮 Predicting future faults...")
            predicted_next_day = self.model.predict_faults(simulated_data)
            predicted_next_week = self.model.predict_faults(next_week_data)

            if predicted_next_day is not None and predicted_next_week is not None:
                simulated_data['Fault_Type'] = predicted_next_day
                next_week_data['Fault_Type'] = predicted_next_week

                simulated_data.to_csv("data/fault_predictions_08_01.csv")
                next_week_data.to_csv("data/fault_predictions_next_week.csv")
                print("✅ Predictions saved for 08/01 and next week!")
            else:
                print("⚠️ Model failed to generate predictions.")
        else:
            print("⚠️ Not enough fault types to train the model. Skipping training...")

        print("✅ Fault analysis completed and saved.")

if __name__ == "__main__":
    system = FaultAnalysisSystem("data/grte_data.csv")
    system.run()