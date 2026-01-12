import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class GenAIConverter:
    def __init__(self):
        # Loads key from .env file
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def convert_to_java(self, cobol_code: str, meta: Dict[str, Any]) -> str:
        """
        Converts COBOL to Java 17 using parsed metadata to guide the AI.
        """
        if not self.client:
            return "// [MOCK] OpenAI Key not found. Please add to .env to see real conversion."

        # Building a sophisticated Prompt for IBM-level quality
        prompt = f"""
        You are an IBM Senior Architect specializing in Mainframe Modernization.
        Convert this legacy COBOL program into modern, production-grade Java 17.

        --- PROGRAM METADATA ---
        Program Name: {meta.get('name')}
        Complexity: {meta.get('complexity_score')} (Risk: {meta.get('risk_level', 'UNKNOWN')})
        Variables Found: {meta.get('variables')}
        SQL Detected: {meta.get('sql_statements')}
        External Calls: {meta.get('calls')}
        Includes (Copybooks): {meta.get('copybooks')}

        --- ARCHITECTURAL REQUIREMENTS ---
        1. Use Spring Boot 3.x patterns.
        2. SQL Handling: Convert 'EXEC SQL' blocks into Spring Data JPA Repository methods or clean JDBC Template code.
        3. Dependency Injection: Convert 'CALL' statements into @Autowired Service calls.
        4. Data Structures: Use Java Records or Lombok @Data classes for Working-Storage variables.
        5. Error Handling: Replace COBOL 'INVALID KEY' or 'SQLCODE' checks with proper Try-Catch and Custom Exceptions.
        6. Clean Code: Use meaningful camelCase names instead of HYPHENATED-COBOL-NAMES.

        --- COBOL SOURCE CODE ---
        {cobol_code}

        --- OUTPUT ---
        Generate only the Java class code. Include helpful comments explaining the logic mapping.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert in COBOL and Java 17 refactoring."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2 # Lower temperature for more deterministic/stable code
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"// Error during conversion: {str(e)}"