import re
import yaml
from dataclasses import dataclass, field
from typing import List

@dataclass
class COBOLProgram:
    name: str
    code_lines: int
    variables: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    sql_statements: List[str] = field(default_factory=list)
    logic_points: int = 0  # NEW: Counts IF, PERFORM, EVALUATE
    complexity_score: float = 0.0

class COBOLParser:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.cfg = yaml.safe_load(f)['parser']

    def parse(self, code: str) -> COBOLProgram:
        # Existing parsing logic...
        name_match = re.search(r"PROGRAM-ID\.\s+([\w-]+)\.", code, re.IGNORECASE)
        name = name_match.group(1) if name_match else "UNKNOWN"
        variables = re.findall(r"\d{2}\s+([\w-]+)\s+PIC", code, re.IGNORECASE)
        calls = re.findall(r"CALL\s+['\"]([\w-]+)['\"]", code, re.IGNORECASE)
        sql_blocks = re.findall(r"EXEC\s+SQL(.*?)END-EXEC", code, re.DOTALL | re.IGNORECASE)

        # NEW: Cyclomatic Complexity (Logic Branching)
        # We count IF, ELSE, PERFORM, EVALUATE, WHEN
        logic_keywords = ['IF', 'ELSE', 'PERFORM', 'EVALUATE', 'WHEN', 'UNTIL']
        logic_count = 0
        for word in logic_keywords:
            logic_count += len(re.findall(fr"\b{word}\b", code, re.IGNORECASE))

        # Advanced Scoring using Config weights
        w = self.cfg['weights']
        score = (
            (len(code.splitlines()) * w['line_weight']) +
            (len(variables) * w['var_weight']) +
            (len(sql_blocks) * w['sql_weight']) +
            (len(calls) * w['call_weight']) +
            (logic_count * w['logic_weight'])
        )

        return COBOLProgram(
            name=name,
            code_lines=len(code.splitlines()),
            variables=variables,
            calls=calls,
            sql_statements=sql_blocks,
            logic_points=logic_count,
            complexity_score=round(score, 2)
        )