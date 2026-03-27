from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
import uvicorn
from model_service import CarbonPredictor

app = FastAPI(title="CarbonChain API", version="1.0")

# CORS (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML model
try:
    predictor = CarbonPredictor('agbp_model.pkl')
except Exception as e:
    print(f"Warning: Could not initialize predictor. Falling back to dummy logic. Error: {e}")
    predictor = None

# Mock Project Data
projects = [
    {
        "id": 1,
        "location": "Amazon Rainforest, Brazil",
        "co2_tons": 15000,
        "status": "verified",
        "tokens_issued": 15000,
        "price_per_token": 5.0,
        "total_value": 75000,
    },
    {
        "id": 2,
        "location": "Wetlands, Southeast Asia",
        "co2_tons": 8500,
        "status": "verified",
        "tokens_issued": 8500,
        "price_per_token": 4.5,
        "total_value": 38250,
    },
    {
        "id": 3,
        "location": "Reforestation Site, Africa",
        "co2_tons": 12000,
        "status": "pending_verification",
        "tokens_issued": 0,
        "price_per_token": 0,
        "total_value": 0,
    }
]

# Request/Response Models
class SatelliteData(BaseModel):
    red_band: float
    green_band: float
    blue_band: float
    nir_band: float
    swir_band: float
    ndvi: float
    soil_moisture: float
    temperature: float
    precipitation: float
    latitude: float
    longitude: float

class ValuationResponse(BaseModel):
    co2_tons: float
    lower_bound: float
    upper_bound: float
    confidence_percent: float
    model_version: str

class ProjectTokenizeRequest(BaseModel):
    location: str
    co2_tons: float
    satellite_proof_hash: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CarbonChain API"}

@app.post("/api/valuate", response_model=ValuationResponse)
def valuate_carbon(data: SatelliteData):
    """
    Predict CO2 sequestration from satellite data
    """
    try:
        if predictor:
            satellite_dict = data.dict()
            result = predictor.predict(satellite_dict)
            return result
        else:
            # Fallback mock logic
            co2_tons = data.ndvi * 50 + data.soil_moisture * 0.3 + data.temperature * 0.5
            return {
                'co2_tons': round(co2_tons, 2),
                'lower_bound': round(co2_tons * 0.95, 2),
                'upper_bound': round(co2_tons * 1.05, 2),
                'confidence_percent': 5.0,
                'model_version': '1.0-fallback'
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tokenize")
def tokenize_project(request: ProjectTokenizeRequest):
    """
    Mint CARB tokens for a verified carbon project
    """
    try:
        # Mock TX hash
        tx_hash = f"0x{'abcd1234' * 8}"
        
        # Add to mock project list
        new_id = len(projects) + 1
        projects.append({
            "id": new_id,
            "location": request.location,
            "co2_tons": request.co2_tons,
            "status": "pending_verification",
            "tokens_issued": 0,
            "price_per_token": 0,
            "total_value": 0,
        })
        
        return {
            "status": "success",
            "message": f"Project tokenized: {request.co2_tons} CARB tokens requested",
            "location": request.location,
            "co2_tons": request.co2_tons,
            "tokens_minted": request.co2_tons,
            "tx_hash": tx_hash,
            "explorer_url": f"https://testnet.bscscan.com/tx/{tx_hash}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects")
def list_projects(skip: int = 0, limit: int = 10):
    return projects[skip:skip+limit]

@app.get("/api/market-stats")
def market_stats():
    total_co2 = sum(p["co2_tons"] for p in projects)
    total_tokens = sum(p["tokens_issued"] for p in projects)
    total_value = sum(p["total_value"] for p in projects)
    
    return {
        "total_projects": len(projects),
        "total_co2_sequestered": total_co2,
        "total_tokens_issued": total_tokens,
        "total_market_value": total_value,
        "average_token_price": 4.83,
        "farmers_onboarded": 147,
        "corporations_verified": 34,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
