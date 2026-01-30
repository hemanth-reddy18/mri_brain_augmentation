import os
import torch
import matplotlib.pyplot as plt
import numpy as np
from mri_loader import MRIDataset
from torch.utils.data import DataLoader

def visualize_batch(output_dir='previews'):
    # Setup paths
    base_dir = os.path.join(os.path.dirname(__file__), 'mri_data', 'train')
    if not os.path.exists(base_dir):
        print("Data directory not found. Run generate_mock_data.py first.")
        return

    # Create output directory for images
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    dataset = MRIDataset(root_dir=base_dir)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    # Get one batch
    images, paths = next(iter(dataloader))
    
    print(f"Generating previews for batch of {len(images)} images...")
    
    # Visualize
    fig, axes = plt.subplots(1, 4, figsize=(15, 5))
    
    for i in range(len(images)):
        # Image shape is (D, H, W) or (1, D, H, W) depending on how it was loaded
        # Our mock data is (32, 32, 32)
        img_tensor = images[i]
        
        # Get middle slice along depth axis
        depth = img_tensor.shape[0]
        mid_slice_idx = depth // 2
        
        # Extract slice: (32, 32)
        slice_2d = img_tensor[mid_slice_idx, :, :].numpy()
        
        # Plot
        axes[i].imshow(slice_2d, cmap='gray')
        axes[i].set_title(f"Sample {i+1}\n{os.path.basename(paths[i])}")
        axes[i].axis('off')
    
    output_path = os.path.join(output_dir, 'mri_batch_preview.png')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    
    print(f"Preview saved to: {os.path.abspath(output_path)}")

if __name__ == '__main__':
    visualize_batch()
