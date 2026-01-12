import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ModernizationAnalytics:
    def generate_dashboard(self, data):
        df = pd.DataFrame(data)
        plt.figure(figsize=(12, 6))
        sns.set_theme(style="whitegrid")
        
        # Plot Complexity vs Name
        sns.barplot(x='name', y='complexity_score', hue='risk_level', data=df)
        plt.title("Modernization Portfolio Analysis (IBM POC)")
        plt.ylabel("Complexity Score (Weighted)")
        plt.savefig("docs/modernization_dashboard.png")
        plt.close()