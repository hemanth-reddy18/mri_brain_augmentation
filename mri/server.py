from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import glob
import nibabel as nib
import numpy as np
import io
import matplotlib.pyplot as plt

app = FastAPI()

# Configuration
MRI_DATA_DIR = os.path.join(os.path.dirname(__file__), 'mri_data', 'train')
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__))) # Root dir to serve index.html

# Ensure data directory exists
if not os.path.exists(MRI_DATA_DIR):
    print(f"WARNING: MRI data directory not found at {MRI_DATA_DIR}")

@app.get("/")
async def read_index():
    index_path = os.path.join(STATIC_DIR, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "index.html not found"}

@app.get("/api/files")
async def get_files():
    """Returns a list of all .nii files relative to the data directory."""
    files = []
    # Walk through the directory to find all .nii files
    for root, _, filenames in os.walk(MRI_DATA_DIR):
        for filename in filenames:
            if filename.endswith('.nii') or filename.endswith('.nii.gz'):
                # Create a relative path for the client to identify the file
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, MRI_DATA_DIR)
                files.append(rel_path)
    return {"files": sorted(files)}

@app.get("/api/info/{file_path:path}")
async def get_mri_info(file_path: str):
    """Returns metadata about the MRI file (dimensions)."""
    full_path = os.path.join(MRI_DATA_DIR, file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        img = nib.load(full_path)
        shape = img.shape
        return {
            "shape": shape,
            "depth": shape[0] if len(shape) >= 3 else 1, # Assuming (D, H, W) or (H, W, D) - usually D is 0 or 2. 
            # Our mock data is (32, 32, 32), let's assume dim 0 is depth for now/slicing
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/slice/{file_path:path}/{slice_idx}")
async def get_slice(file_path: str, slice_idx: int):
    """Returns a PNG image of a specific slice."""
    full_path = os.path.join(MRI_DATA_DIR, file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        img = nib.load(full_path)
        data = img.get_fdata()
        
        # Handle dimensions. Mock data is (32, 32, 32).
        # We will slice along the 0th axis for this demo
        if slice_idx < 0 or slice_idx >= data.shape[0]:
             raise HTTPException(status_code=400, detail="Slice index out of bounds")
             
        slice_data = data[slice_idx, :, :]
        
        # Normalize to 0-1 for plotting
        if np.max(slice_data) != np.min(slice_data):
            slice_data = (slice_data - np.min(slice_data)) / (np.max(slice_data) - np.min(slice_data))
        
        # Convert to PNG using matplotlib
        plt.figure(figsize=(4, 4))
        plt.imshow(slice_data, cmap='gray')
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close()
        buf.seek(0)
        
        return StreamingResponse(buf, media_type="image/png")
        
    except Exception as e:
        print(f"Error serving slice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
