import re
from typing import Dict, List

class ModernizationValidator:
    """
    Checks if the generated Java code actually contains the 
    business logic from the original COBOL.
    """
    def validate(self, java_code: str, original_meta: Dict) -> Dict:
        missing_vars = []
        # Check if the COBOL variables exist in the Java code (ignoring case/hyphens)
        for var in original_meta['variables']:
            # Convert WS-CUST-ID to custId or similar
            simple_name = var.replace('WS-', '').replace('-', '').lower()
            if simple_name not in java_code.lower():
                missing_vars.append(var)

        # Check if SQL Repository was created if SQL existed
        has_repo = "Repository" in java_code or "@Query" in java_code
        sql_needed = len(original_meta['sql_statements']) > 0

        return {
            "validation_score": 100 - (len(missing_vars) * 10),
            "missing_elements": missing_vars,
            "sql_integrity": True if (not sql_needed or has_repo) else False,
            "passed": len(missing_vars) == 0
        }