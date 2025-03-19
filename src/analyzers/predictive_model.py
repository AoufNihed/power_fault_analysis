import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

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

class PredictiveModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
    
    def train_model(self, df):
        print("📊 Training model with classified fault data...")
        if 'Fault_Type' not in df.columns:
            print("⚠️ No 'Fault_Type' column found. Skipping training.")
            return
        X = df[['V_A (kV)', 'V_B (kV)', 'V_C (kV)', 'I_A (A)', 'I_B (A)', 'I_C (A)']]
        y = self.label_encoder.fit_transform(df['Fault_Type'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, "models/fault_predictor.pkl")
        joblib.dump(self.label_encoder, "models/label_encoder.pkl")
        print("✅ Model training complete. Model saved!")
    
    def predict_faults(self, future_data):
        try:
            self.model = joblib.load("models/fault_predictor.pkl")
            self.label_encoder = joblib.load("models/label_encoder.pkl")
            predictions = self.model.predict(future_data)
            return self.label_encoder.inverse_transform(predictions)
        except FileNotFoundError:
            print("⚠️ No trained model found. Please train the model first.")
            return None

class System:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        print("\n✅ Data loaded. First rows:")
        print(self.data.head())
        self.fault_analyzer = FaultAnalyzer(self.data)
        self.predictive_model = PredictiveModel()
    
    def run(self):
        print("\n✅ Classifying faults...")
        self.data['Fault_Type'] = self.data.apply(self.fault_analyzer.classify_faults, axis=1)
        print("\n✅ Classification complete. First rows with Fault_Type:")
        print(self.data[['V_A (kV)', 'V_B (kV)', 'V_C (kV)', 'Fault_Type']].head())
        self.data.to_csv("processed_data.csv", index=False)
        print("\n✅ Processed data saved to processed_data.csv")
        self.predictive_model.train_model(self.data)
        self.generate_predictions()
    
    def generate_predictions(self):
        print("\n🔮 Generating future fault predictions...")
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
        future_faults = self.predictive_model.predict_faults(simulated_data)
        next_week_faults = self.predictive_model.predict_faults(next_week_data)
        simulated_data['Fault_Type'] = future_faults
        next_week_data['Fault_Type'] = next_week_faults
        simulated_data.to_csv("predicted_faults_08_01.csv")
        next_week_data.to_csv("predicted_faults_next_week.csv")
        print("✅ Predictions saved for 08/01 and next week!")

if __name__ == "__main__":
    system = System("grte_data.csv")
    system.run()
