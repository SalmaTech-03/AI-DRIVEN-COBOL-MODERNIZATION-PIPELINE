import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from typing import Dict, Any

class RiskModel:
    """
    ML-based Risk Assessment for COBOL modernization.
    Uses a Random Forest Classifier to predict if a program 
    is LOW, MEDIUM, or HIGH risk to refactor.
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train_mock_model(self):
        """
        Creates a synthetic dataset to demonstrate ML capabilities in the POC.
        Features: [code_lines, variables_count, sql_count, calls_count, complexity_score]
        """
        # Feature sets: 
        # [Lines, Vars, SQL, Calls, Complexity]
        X_train = [
            [20, 2, 0, 0, 5.0],      # Example: Small, simple program (Low)
            [1500, 80, 25, 12, 95.0], # Example: Massive legacy monster (High)
            [400, 20, 5, 2, 45.0],    # Example: Average business logic (Medium)
            [50, 5, 0, 1, 10.0],      # Example: Simple utility (Low)
            [800, 45, 15, 8, 75.0]    # Example: Complex batch job (High)
        ]
        
        # Labels: 0 = LOW, 1 = MEDIUM, 2 = HIGH
        y_train = [0, 2, 1, 0, 2]
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("Model trained successfully with 5-feature set.")

    def predict_risk(self, program_data: Dict[str, Any]) -> str:
        """
        Predicts the risk level of a given COBOL program.
        """
        if not self.is_trained:
            self.train_mock_model()
        
        # We must provide exactly 5 features in the same order as training:
        features = [[
            program_data.get('code_lines', 0),
            len(program_data.get('variables', [])),
            program_data.get('sql_count', 0),
            len(program_data.get('calls', [])),
            program_data.get('complexity_score', 0.0)
        ]]
        
        # Perform prediction
        prediction_id = self.model.predict(features)[0]
        
        # Map ID back to human-readable string
        risk_mapping = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        return risk_mapping.get(prediction_id, "UNKNOWN")

    def save_model(self, path: str = "models/risk_model.pkl"):
        """Saves the trained model to the models directory."""
        if self.is_trained:
            joblib.dump(self.model, path)
            print(f"Model saved to {path}")