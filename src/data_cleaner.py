import re
from typing import List
class DataCleaner:
    def clean(self, raw_code: str) -> str:
        lines = raw_code.splitlines()
        cleaned_lines = []
        
        for line in lines:
            # 1. Remove COBOL comments (Column 7 '*')
            if len(line) >= 7 and line[6] == '*':
                continue
                
            # 2. Trim whitespace
            clean_line = line.strip()
            
            if clean_line:
                cleaned_lines.append(clean_line)
                
        return "\n".join(cleaned_lines)

    def identify_risks(self, code: str) -> List[str]:
        issues = []
        if "GO TO" in code:
            issues.append("Contains 'GO TO' statements (Anti-pattern)")
        if code.count("PERFORM") > 10:
            issues.append("High nesting/loop complexity detected")
        return issues