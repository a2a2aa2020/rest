"""
FastAPI Backend for Restaurant Inspection System
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from typing import List
import os
import shutil
from datetime import datetime
import json

from ai_engine_vision import InspectionAIEngine  # Google Cloud Vision API
from pdf_generator import generate_inspection_report

app = FastAPI(title="Restaurant Inspection System")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Engine
ai_engine = InspectionAIEngine()

# Ensure directories exist
UPLOAD_DIR = "../uploads"
REPORTS_DIR = "../reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Serve static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")


@app.get("/")
async def root():
    return {"message": "Restaurant Inspection API", "version": "1.0.0"}


@app.post("/api/analyze")
async def analyze_inspection(
    restaurant_name: str = Form(...),
    commercial_register: str = Form(...),
    ceiling_image: UploadFile = File(...),
    wall_image: UploadFile = File(...),
    floor_general_image: UploadFile = File(...),
    floor_prep_image: UploadFile = File(...),
    lighting_image: UploadFile = File(...),
):
    """
    Main inspection endpoint
    Accepts 6 images and restaurant info
    Returns AI analysis results
    """
    try:
        # Create unique inspection ID
        inspection_id = f"INS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        inspection_dir = os.path.join(UPLOAD_DIR, inspection_id)
        os.makedirs(inspection_dir, exist_ok=True)
        
        image_paths = {}
        for key, image_file in images.items():
            file_path = os.path.join(inspection_dir, f"{key}.jpg")
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
            image_paths[key] = file_path
        
        # Run AI Analysis
        results = ai_engine.analyze_inspection(image_paths)
        
        # Add metadata
        results["inspection_id"] = inspection_id
        results["restaurant_name"] = restaurant_name
        results["commercial_register"] = commercial_register
        results["timestamp"] = datetime.now().isoformat()
        
        # Generate PDF Report
        pdf_path = await generate_inspection_report(results, inspection_id)
        results["pdf_report"] = f"/reports/{os.path.basename(pdf_path)}"
        
        # Save results JSON
        json_path = os.path.join(inspection_dir, "results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/inspection/{inspection_id}")
async def get_inspection(inspection_id: str):
    """Get inspection results by ID"""
    json_path = os.path.join(UPLOAD_DIR, inspection_id, "results.json")
    
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    with open(json_path, "r", encoding="utf-8") as f:
        results = json.load(f)
    
    return JSONResponse(content=results)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_engine": "loaded",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


