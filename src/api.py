from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from src.cobol_parser import COBOLParser
from src.genai_converter import GenAIConverter
from src.dl_risk_model import DeepRiskModel
import uvicorn

app = FastAPI(title="IBM COBOL Modernization API")

# Initialize engines
parser = COBOLParser()
converter = GenAIConverter()
risk_model = DeepRiskModel()

@app.get("/health")
def health():
    return {"status": "healthy", "engine": "TensorFlow 2.x"}

@app.post("/modernize")
async def modernize_code(file: UploadFile = File(...)):
    try:
        content = (await file.read()).decode("utf-8")
        
        # 1. Parse
        analysis = parser.parse(content)
        
        # 2. Risk (Deep Learning)
        features = [[analysis.code_lines, len(analysis.variables), 
                    len(analysis.sql_statements), len(analysis.calls), analysis.logic_points]]
        risk = risk_model.predict(features)
        
        # 3. Convert (GenAI)
        meta = vars(analysis)
        meta['risk_level'] = risk
        java_code = converter.convert_to_java(content, meta)
        
        return {
            "program_name": analysis.name,
            "risk_assessment": risk,
            "complexity": analysis.complexity_score,
            "java_output": java_code[:500] + "..." # Preview
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)