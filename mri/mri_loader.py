import os
import glob
import numpy as np
import nibabel as nib
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms

class MRIDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the MRI studies.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.root_dir = root_dir
        self.transform = transform
        self.file_list = []
        
        # Recursively find all .nii files
        # Based on user's code: for root, _, files in os.walk(base_dir)...
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.nii') or file.endswith('.nii.gz'):
                    self.file_list.append(os.path.join(root, file))
        
        print(f"Found {len(self.file_list)} MRI files.")

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        img_path = self.file_list[idx]
        
        # Load the image using nibabel
        try:
            img_obj = nib.load(img_path)
            img_data = img_obj.get_fdata()
            
            # Convert to float32 for PyTorch
            img_data = img_data.astype(np.float32)
            
            # Basic normalization or processing could go here
            # For now, just converting to tensor
            # Note: MRI data is often 3D (H, W, D) or 4D (H, W, D, C)
            # PyTorch expects (C, D, H, W) or (C, H, W) usually.
            # We'll just convert to tensor for demonstration.
            
            sample = torch.from_numpy(img_data)
            
            if self.transform:
                sample = self.transform(sample)
                
            return sample, img_path
            
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
            return torch.zeros(1), img_path

def main():
    # Define the data directory path (local mock path)
    # In the user's code this was '/content/drive/MyDrive/mri/train'
    base_dir = os.path.join(os.path.dirname(__file__), 'mri_data', 'train')
    
    if not os.path.exists(base_dir):
        print(f"Directory not found: {base_dir}")
        print("Please run 'generate_mock_data.py' first.")
        return

    print(f"Loading data from: {base_dir}")

    # Create Dataset
    mri_dataset = MRIDataset(root_dir=base_dir)

    if len(mri_dataset) == 0:
        print("No .nii files found. Exiting.")
        return

    # Create DataLoader
    dataloader = DataLoader(mri_dataset, batch_size=4, shuffle=True, num_workers=0)

    # Iterate through one batch to demonstrate
    print("\nIterating through DataLoader...")
    for i, (images, paths) in enumerate(dataloader):
        print(f"Batch {i+1}:")
        print(f"  Image Batch Shape: {images.shape}")
        print(f"  Files: {paths}")
        
        # Break after first batch for demonstration
        break

if __name__ == '__main__':
    main()
