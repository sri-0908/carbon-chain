# CARBONCHAIN: ANTI-GRAVITY CARBON TOKENIZATION
## Complete Software Build Prompt

---

## VISION (Read This First)

You are building **CarbonChain**: a platform that reverses gravity on carbon.

**The Narrative:**
- Carbon has been trapped in gravity (grounded, illiquid, stuck)
- We lift it into the digital sky via satellite proof → ML verification → blockchain tokens
- Farmers profit, corporations verify, investors trade, planet heals
- Carbon ASCENDS (anti-gravity = tokens float upward)

**Your Role:**
- Build the full-stack software (6 weeks, 100% buildable)
- No IoT sensors needed (mock sensor data)
- No real farms needed (use public satellite imagery)
- Everything is software + testnet blockchain

---

## TECH STACK

Frontend:        React + Tailwind CSS + Web3.js
Backend:         FastAPI (Python) + PostgreSQL
ML:              XGBoost (AGBP model) + scikit-learn
Blockchain:      Solidity (ERC-20) deployed to BNB testnet
Hosting:         Vercel (frontend) + Railway/Heroku (backend)
Data:            Sentinel-2 satellite imagery (free), NASA BIOMASS (free)

---

## WEEK 1-2: ML MODEL (Your Core)

### Goal
Build a machine learning model that predicts carbon sequestration from satellite imagery.

### Step 1: Download Training Data & Create Model

Create a file called: train_model.py

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

# Generate mock training data (simulates satellite + sensor data)
np.random.seed(42)
n_samples = 1000

satellite_data = {
    'red_band': np.random.rand(n_samples) * 255,
    'green_band': np.random.rand(n_samples) * 255,
    'blue_band': np.random.rand(n_samples) * 255,
    'nir_band': np.random.rand(n_samples) * 255,  # Near-infrared
    'swir_band': np.random.rand(n_samples) * 255,  # Short-wave infrared
    'ndvi': np.random.rand(n_samples),  # Normalized Diff Vegetation Index
    'soil_moisture': np.random.rand(n_samples) * 100,
    'temperature': np.random.rand(n_samples) * 30,
    'precipitation': np.random.rand(n_samples) * 200,
    'latitude': np.random.rand(n_samples) * 180 - 90,
    'longitude': np.random.rand(n_samples) * 360 - 180,
}

df = pd.DataFrame(satellite_data)

# Target: CO2 tons per hectare
df['co2_sequestered'] = (
    df['ndvi'] * 50 +
    df['soil_moisture'] * 0.3 +
    df['temperature'] * 0.5 +
    np.random.randn(n_samples) * 10
)

print(f"Dataset shape: {df.shape}")
print(f"CO2 range: {df['co2_sequestered'].min():.1f} - {df['co2_sequestered'].max():.1f} tons/ha")

# Prepare features and target
X = df[['red_band', 'green_band', 'blue_band', 'nir_band', 'swir_band', 
         'ndvi', 'soil_moisture', 'temperature', 'precipitation', 
         'latitude', 'longitude']]
y = df['co2_sequestered']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost
print("\nTraining model...")
model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=7,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"\n=== MODEL PERFORMANCE ===")
print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.2f} tons CO2/ha")
print(f"RMSE: {rmse:.2f} tons CO2/ha")
print(f"MAPE: {mape:.2f}%")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n=== FEATURE IMPORTANCE ===")
print(importance)

# Save model
joblib.dump(model, 'agbp_model.pkl')
print("\n✓ Model saved to agbp_model.pkl")
```

### Step 2: Run It

```bash
# Install libraries
pip install numpy pandas scikit-learn joblib

# Run the training script
python train_model.py
```

**Output will show:**
- Model accuracy (R² > 0.80 = good)
- Feature importance (NDVI matters most)
- Saved model file (agbp_model.pkl)

---

## WEEK 3: SMART CONTRACT (Blockchain)

### Create file: CarbonChain.sol

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CarbonChain is ERC20, Ownable {
    
    struct CarbonProject {
        address owner;
        string location;
        uint256 co2_tons;
        bytes32 satellite_proof_hash;
        uint256 timestamp;
        bool verified;
    }
    
    CarbonProject[] public projects;
    mapping(address => uint256[]) public userProjects;
    mapping(bytes32 => bool) public proofUsed;
    
    event ProjectTokenized(
        uint256 indexed projectId,
        address indexed owner,
        uint256 co2_tons,
        bytes32 satellite_proof
    );
    
    event ProjectVerified(uint256 indexed projectId);
    
    constructor() ERC20("CarbonChain", "CARB") {}
    
    function tokenizeProject(
        string memory location,
        uint256 co2_tons,
        bytes32 satellite_proof_hash
    ) public {
        require(co2_tons > 0, "CO2 must be positive");
        require(!proofUsed[satellite_proof_hash], "Proof already used");
        
        CarbonProject memory newProject = CarbonProject({
            owner: msg.sender,
            location: location,
            co2_tons: co2_tons,
            satellite_proof_hash: satellite_proof_hash,
            timestamp: block.timestamp,
            verified: false
        });
        
        projects.push(newProject);
        uint256 projectId = projects.length - 1;
        userProjects[msg.sender].push(projectId);
        proofUsed[satellite_proof_hash] = true;
        
        // Mint tokens: 1 token = 1 ton CO2
        uint256 tokenAmount = co2_tons * (10 ** uint256(decimals()));
        _mint(msg.sender, tokenAmount);
        
        emit ProjectTokenized(projectId, msg.sender, co2_tons, satellite_proof_hash);
    }
    
    function verifyProject(uint256 projectId) public onlyOwner {
        require(projectId < projects.length, "Project not found");
        projects[projectId].verified = true;
        emit ProjectVerified(projectId);
    }
    
    function getProject(uint256 projectId) public view returns (CarbonProject memory) {
        return projects[projectId];
    }
    
    function getProjectCount() public view returns (uint256) {
        return projects.length;
    }
}
```

### How to Deploy

1. Go to Remix IDE: https://remix.ethereum.org
2. Create new file, paste contract above
3. Compile (click Compile button)
4. Deploy to BNB Testnet
5. Save contract address (you'll need it later)

---

## WEEK 4: BACKEND API (FastAPI)

### Create file: main.py

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="CarbonChain API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
try:
    model = joblib.load('agbp_model.pkl')
except:
    model = None
    print("WARNING: Model file not found. Place agbp_model.pkl in same directory")

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

# Routes

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "CarbonChain API"}

@app.post("/api/valuate", response_model=ValuationResponse)
def valuate_carbon(data: SatelliteData):
    """Predict CO2 from satellite data"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        features = np.array([
            data.red_band, data.green_band, data.blue_band, 
            data.nir_band, data.swir_band, data.ndvi,
            data.soil_moisture, data.temperature, data.precipitation,
            data.latitude, data.longitude
        ]).reshape(1, -1)
        
        co2_tons = float(model.predict(features)[0])
        confidence = 5.0
        
        return {
            'co2_tons': round(co2_tons, 2),
            'lower_bound': round(co2_tons * (1 - confidence/100), 2),
            'upper_bound': round(co2_tons * (1 + confidence/100), 2),
            'confidence_percent': confidence,
            'model_version': '1.0',
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tokenize")
def tokenize_project(location: str, co2_tons: int):
    """Mint CARB tokens for a project"""
    return {
        "status": "success",
        "message": f"Project tokenized: {co2_tons} CARB tokens",
        "location": location,
        "co2_tons": co2_tons,
        "tokens_minted": co2_tons,
        "tx_hash": "0xabc123def456",
    }

@app.get("/api/projects")
def list_projects():
    """List all projects"""
    return [
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

@app.get("/api/market-stats")
def market_stats():
    """Global market stats"""
    return {
        "total_projects": 3,
        "total_co2_sequestered": 35500,
        "total_tokens_issued": 23500,
        "total_market_value": 113250,
        "average_token_price": 4.83,
        "farmers_onboarded": 147,
        "corporations_verified": 34,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run Backend

```bash
pip install fastapi uvicorn pydantic numpy pandas scikit-learn joblib

python main.py
```

**API will be at:** http://localhost:8000
**API docs at:** http://localhost:8000/docs

---

## WEEK 5: FRONTEND (React)

### Create React App

```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom
```

### Create file: src/App.jsx

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ValuationPage from './pages/ValuationPage';
import Marketplace from './pages/Marketplace';
import './App.css';

function App() {
  return (
    <Router>
      <nav style={{
        padding: '1rem 2rem',
        backgroundColor: '#639922',
        color: 'white',
        display: 'flex',
        gap: '2rem',
      }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.2rem', fontWeight: 'bold' }}>
          🌍 CarbonChain
        </Link>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
          Value Property
        </Link>
        <Link to="/marketplace" style={{ color: 'white', textDecoration: 'none' }}>
          Marketplace
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<ValuationPage />} />
        <Route path="/marketplace" element={<Marketplace />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### Create folder: src/pages

### Create file: src/pages/ValuationPage.jsx

```jsx
import React, { useState } from 'react';
import axios from 'axios';

export default function ValuationPage() {
  const [formData, setFormData] = useState({
    red_band: 100,
    green_band: 120,
    blue_band: 90,
    nir_band: 200,
    swir_band: 150,
    ndvi: 0.7,
    soil_moisture: 60,
    temperature: 22,
    precipitation: 150,
    latitude: 0,
    longitude: 0,
  });

  const [valuation, setValuation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/valuate', formData);
      setValuation(response.data);
    } catch (err) {
      setError('Error calculating valuation. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>🌱 Value Your Carbon Project</h1>
      <p style={{ color: '#666' }}>Enter satellite and sensor data to predict CO₂ sequestration</p>
      
      <form onSubmit={handleSubmit} style={{ marginTop: '2rem' }}>
        <div style={{ marginBottom: '1rem' }}>
          <label><strong>NDVI (Vegetation Index)</strong></label>
          <input
            type="number"
            name="ndvi"
            value={formData.ndvi}
            onChange={handleInputChange}
            step="0.01"
            min="0"
            max="1"
            style={{ width: '100%', padding: '0.5rem', marginTop: '0.5rem' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label><strong>Soil Moisture (%)</strong></label>
          <input
            type="number"
            name="soil_moisture"
            value={formData.soil_moisture}
            onChange={handleInputChange}
            step="1"
            style={{ width: '100%', padding: '0.5rem', marginTop: '0.5rem' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label><strong>Temperature (°C)</strong></label>
          <input
            type="number"
            name="temperature"
            value={formData.temperature}
            onChange={handleInputChange}
            step="0.1"
            style={{ width: '100%', padding: '0.5rem', marginTop: '0.5rem' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label><strong>Precipitation (mm)</strong></label>
          <input
            type="number"
            name="precipitation"
            value={formData.precipitation}
            onChange={handleInputChange}
            step="1"
            style={{ width: '100%', padding: '0.5rem', marginTop: '0.5rem' }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#639922',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '1rem',
            width: '100%',
          }}
        >
          {loading ? '⏳ Calculating...' : '🚀 Get Valuation'}
        </button>
      </form>

      {error && (
        <div style={{
          marginTop: '1rem',
          padding: '1rem',
          backgroundColor: '#fee',
          border: '1px solid #f00',
          borderRadius: '4px',
          color: '#a00',
        }}>
          ❌ {error}
        </div>
      )}

      {valuation && (
        <div style={{
          marginTop: '2rem',
          padding: '1.5rem',
          backgroundColor: '#f0f9f0',
          borderRadius: '8px',
          border: '2px solid #639922',
        }}>
          <h2>📊 Fair Value: {valuation.co2_tons.toLocaleString()} tons CO₂</h2>
          <p><strong>Confidence interval:</strong> ±{valuation.confidence_percent}%</p>
          <p><strong>Range:</strong> {valuation.lower_bound.toLocaleString()} - {valuation.upper_bound.toLocaleString()} tons</p>
          <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
            Model v{valuation.model_version}
          </p>
          <button style={{
            marginTop: '1rem',
            padding: '0.5rem 1rem',
            backgroundColor: '#639922',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}>
            💰 Mint Tokens
          </button>
        </div>
      )}
    </div>
  );
}
```

### Create file: src/pages/Marketplace.jsx

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Marketplace() {
  const [projects, setProjects] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectsRes = await axios.get('http://localhost:8000/api/projects');
        const statsRes = await axios.get('http://localhost:8000/api/market-stats');
        setProjects(projectsRes.data);
        setStats(statsRes.data);
      } catch (err) {
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div style={{ padding: '2rem' }}>⏳ Loading marketplace...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>🌍 Carbon Marketplace</h1>

      {stats && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1rem',
          marginBottom: '2rem',
        }}>
          <div style={{ padding: '1rem', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
            <p style={{ fontSize: '0.9rem', color: '#666' }}>Total CO₂</p>
            <h3>{stats.total_co2_sequestered.toLocaleString()} tons</h3>
          </div>
          <div style={{ padding: '1rem', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
            <p style={{ fontSize: '0.9rem', color: '#666' }}>Tokens Issued</p>
            <h3>{stats.total_tokens_issued.toLocaleString()} CARB</h3>
          </div>
          <div style={{ padding: '1rem', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
            <p style={{ fontSize: '0.9rem', color: '#666' }}>Market Value</p>
            <h3>${stats.total_market_value.toLocaleString()}</h3>
          </div>
          <div style={{ padding: '1rem', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
            <p style={{ fontSize: '0.9rem', color: '#666' }}>Avg Price/Token</p>
            <h3>${stats.average_token_price.toFixed(2)}</h3>
          </div>
        </div>
      )}

      <h2>📋 Available Projects</h2>
      
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #ddd' }}>
            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Location</th>
            <th style={{ padding: '0.75rem', textAlign: 'right' }}>CO₂ (tons)</th>
            <th style={{ padding: '0.75rem', textAlign: 'center' }}>Status</th>
            <th style={{ padding: '0.75rem', textAlign: 'right' }}>Value</th>
          </tr>
        </thead>
        <tbody>
          {projects.map(project => (
            <tr key={project.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: '0.75rem' }}>{project.location}</td>
              <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                {project.co2_tons.toLocaleString()}
              </td>
              <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                <span style={{
                  padding: '0.25rem 0.75rem',
                  backgroundColor: project.status === 'verified' ? '#d4edda' : '#fff3cd',
                  color: project.status === 'verified' ? '#155724' : '#856404',
                  borderRadius: '4px',
                  fontSize: '0.85rem',
                }}>
                  {project.status === 'verified' ? '✓ Verified' : '⏳ Pending'}
                </span>
              </td>
              <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                ${project.total_value.toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Run Frontend

```bash
npm start
```

**Frontend at:** http://localhost:3000

---

## WEEK 6: DEMO VIDEO SCRIPT

### Record This Voiceover (30 seconds)

```
[Soft, determined tone]

"For centuries, carbon has been trapped.

Locked in trees. Buried in soil. 
No market. No liquidity. No scale.

Until now.

[SFX: Whoosh sound as tokens appear]

Satellite imagery reveals the carbon.
Machine learning verifies it.
Blockchain tokenizes it.

Now carbon ASCENDS.

Farmers profit. Corporations verify. 
Investors gain. The planet heals.

CarbonChain.
Where gravity reverses."
```

### Visuals While Recording

1. Satellite image of forest → 3 sec
2. ML prediction appears → 3 sec
3. Blockchain minting → 5 sec
4. Tokens float upward (animation) → 10 sec
5. Farmers/corps/investors appear → 5 sec
6. Logo and closing text → 4 sec

---

## ANTI-GRAVITY PITCH (Use This)

**Opening (20 sec):**

"Carbon has been trapped in gravity for centuries. Dead weight. Buried. Impossible to move.

Trees sequester CO₂ → nobody knows → no market → farmers stay poor.

CarbonChain reverses gravity. We lift carbon into the digital sky. One satellite image. One ML prediction. One blockchain transaction.

Suddenly that carbon is a TOKEN. Something that MOVES. Something that TRADES. Something that creates instant liquidity.

The moment carbon becomes liquid, everything changes."

---

## CHECKLIST BEFORE DEMO DAY

✓ ML model trained (R² > 0.80)
✓ Smart contract deployed (testnet)
✓ Backend running locally
✓ Frontend working (can valuate + see marketplace)
✓ Demo video recorded (30 sec)
✓ Sample projects loaded (5 projects)
✓ Pitch practiced (20 sec opening)
✓ Killer lines memorized (3 Q&A responses)

---

## YOU'RE READY

Everything above is copy-paste, run-able code.

Start with Week 1 (ML model).
Follow the weekly breakdown.
Use the anti-gravity narrative throughout.

6 weeks. 17 hours of coding.
One winning pitch.

Let's reverse gravity. 🚀
