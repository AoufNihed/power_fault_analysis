import pandas as pd

class FaultAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
    
    def classify_faults(self, row):
        V_A, V_B, V_C = row['V_A (kV)'], row['V_B (kV)'], row['V_C (kV)']
        I_A, I_B, I_C = row['I_A (A)'], row['I_B (A)'], row['I_C (A)']
        
        # Define fault conditions
        if V_A < 0.2 * V_B and V_A < 0.2 * V_C:
            return "Monophase"
        elif V_A < 0.2 * V_B and V_B < 0.2 * V_C:
            return "Biphase Simple"
        elif V_A < 0.2 * V_B and V_B < 0.2 * V_C and (I_A > 1.5 * I_B or I_B > 1.5 * I_C):
            return "Biphase Terre"
        elif V_A < 0.2 * V_B and V_B < 0.2 * V_C and V_C < 0.2 * V_A:
            return "Triphase"
        elif I_A < 0.1 and I_B < 0.1 and I_C < 0.1:
            return "Open Circuit"
        else:
            return "Normal"

class System:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        print("\n✅ Data loaded. First rows:")
        print(self.data.head())
        
        self.fault_analyzer = FaultAnalyzer(self.data)
    
    def run(self):
        print("\n✅ Classifying faults...")
        
        # Apply fault classification
        self.data['Fault_Type'] = self.data.apply(self.fault_analyzer.classify_faults, axis=1)
        
        print("\n✅ Classification complete. First rows with Fault_Type:")
        print(self.data[['V_A (kV)', 'V_B (kV)', 'V_C (kV)', 'Fault_Type']].head())
        
        # Save the processed data
        self.data.to_csv("processed_data.csv", index=False)
        print("\n✅ Processed data saved to processed_data.csv")

if __name__ == "__main__":
    system = System("grte_data.csv")  # Ensure the file exists and has expected columns
    system.run()
