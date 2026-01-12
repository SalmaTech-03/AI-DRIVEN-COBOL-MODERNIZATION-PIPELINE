# Lessons Learned: Engineering the Modernization Pipeline

## 1. Handling Model Hallucinations
**Discovery**: Initial runs showed the AI creating Java variables that didn't exist in COBOL.
**Correction**: Implemented the **Modernization Validator**. By performing a "Post-Conversion Audit," we can now flag missing logic for human review, increasing system trust.

## 2. Pathing and Environment in Microservices
**Discovery**: Encountered `ModuleNotFoundError` during API and Pytest deployment.
**Solution**: Standardized on the `python -m` execution pattern and implemented `$PYTHONPATH` management in Docker to ensure cross-module visibility.

## 3. The Value of Deep Learning vs. Heuristics
**Discovery**: Simple "Lines of Code" counts don't accurately predict risk.
**Solution**: The **TensorFlow DNN** proved that weighted analysis of SQL and Program Calls is a much stronger predictor of refactoring effort.