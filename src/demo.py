import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Import our specialized modules
from src.cobol_parser import COBOLParser
from src.data_cleaner import DataCleaner
from src.dl_risk_model import DeepRiskModel  # TensorFlow/Keras version
from src.genai_converter import GenAIConverter
from src.validator import ModernizationValidator
from src.analytics_engine import ModernizationAnalytics

def run_ultimate_pipeline():
    print("="*80)
    print("   IBM ENTERPRISE POC: AI-DRIVEN MAINFRAME MODERNIZATION (v2.0)")
    print("="*80)

    # 1. INITIALIZATION (Frameworks: TensorFlow, Pandas, OpenAI)
    cleaner = DataCleaner()
    parser = COBOLParser()
    converter = GenAIConverter()
    validator = ModernizationValidator()
    analytics = ModernizationAnalytics()
    
    # Initialize Deep Learning Model (TensorFlow/Keras)
    print("[AI] Initializing TensorFlow/Keras Neural Network...")
    dl_model = DeepRiskModel()
    
    # Mock Training: Demonstrate DL training loop logic
    # In production, this would load from a saved model or DB
    X_train = np.random.rand(10, 5) # 10 samples, 5 features
    y_train = np.random.randint(0, 3, 10) # 3 risk classes
    dl_model.train(X_train, y_train)

    # Data Store for Pandas EDA
    results_data = []

    # Define Paths
    input_dir = "data/sample_cobol"
    output_dir = "data/expected_output"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    # 2. BATCH PROCESSING LOOP
    files = [f for f in os.listdir(input_dir) if f.endswith(".cbl")]
    
    for filename in files:
        print(f"\n[PROCESS] Analyzing {filename}...")
        file_path = os.path.join(input_dir, filename)

        # PHASE A: CLEANING & NORMALIZATION
        with open(file_path, 'r') as f:
            raw_code = f.read()
        clean_code = cleaner.clean(raw_code)

        # PHASE B: ADVANCED STATIC ANALYSIS (Custom Parser)
        analysis = parser.parse(clean_code)

        # PHASE C: DEEP LEARNING RISK PREDICTION (TensorFlow)
        # Features: [Lines, Variables, SQL, Calls, LogicPoints]
        features = [[
            analysis.code_lines, 
            len(analysis.variables), 
            len(analysis.sql_statements), 
            len(analysis.calls),
            analysis.logic_points
        ]]
        risk_category = dl_model.predict(features)

        # PHASE D: GEN-AI CONVERSION (GPT-4)
        metadata = vars(analysis)
        metadata['risk_level'] = risk_category
        
        print(f"    - Executing GenAI Refactoring...")
        java_output = converter.convert_to_java(clean_code, metadata)

        # PHASE E: AUTOMATED AUDIT & VALIDATION
        audit = validator.validate(java_output, metadata)

        # PHASE F: LOGGING DATA FOR PANDAS EDA
        results_data.append({
            "name": analysis.name,
            "complexity_score": analysis.complexity_score,
            "logic_points": analysis.logic_points,
            "risk_level": risk_category,
            "sql_count": len(analysis.sql_statements),
            "validation_score": audit['validation_score'],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        # Save Java Output
        with open(os.path.join(output_dir, f"{analysis.name}.java"), "w") as f:
            f.write(java_output)
        
        print(f"    - Analysis Complete. Risk: {risk_category} | Audit Score: {audit['validation_score']}")

    # 3. PANDAS DATA ANALYSIS & VISUALIZATION (Matplotlib/Seaborn)
    print("\n" + "="*40)
    print("PHASE 3: ANALYTICS & STAKEHOLDER REPORTING")
    print("="*40)
    
    df = pd.DataFrame(results_data)
    
    # Generate Visualizations (Communicating to Non-Technical Audiences)
    analytics.generate_dashboard(results_data)

    # 4. EXECUTIVE SUMMARY GENERATION (Stakeholder Communication)
    summary = f"""
# EXECUTIVE MODERNIZATION REPORT
**Generated:** {datetime.now()}
**Frameworks Used:** TensorFlow (DL), Scikit-Learn (ML), Pandas (EDA), OpenAI (GenAI)

## 1. Portfolio Overview
- **Total Programs Analyzed:** {len(df)}
- **Average Complexity Score:** {df['complexity_score'].mean():.2f}
- **Conversion Success Rate:** {df['validation_score'].mean():.1f}%

## 2. Risk Distribution (Deep Learning Classification)
{df['risk_level'].value_counts().to_string()}

## 3. Technical Recommendations
- High-risk programs identified: {len(df[df['risk_level'] == 'HIGH'])}.
- Automated Refactoring Confidence is **{df['validation_score'].mean()}%**.
- Deployment Target: Containerized Environment (Docker/OpenShift).
    """
    
    with open("docs/EXECUTIVE_SUMMARY.md", "w") as f:
        f.write(summary)

    print("\n[SUCCESS] Modernization Complete.")
    print(">> Dashboard: docs/modernization_dashboard.png")
    print(">> Summary: docs/EXECUTIVE_SUMMARY.md")
    print("="*80)

if __name__ == "__main__":
    run_ultimate_pipeline()