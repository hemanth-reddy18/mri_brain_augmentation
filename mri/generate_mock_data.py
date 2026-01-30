import os
import numpy as np
import nibabel as nib

def create_mock_data(base_path, num_subjects=3):
    print(f"Generating mock data in {base_path}...")
    
    # Create train directory
    train_dir = os.path.join(base_path, 'train')
    os.makedirs(train_dir, exist_ok=True)
    
    # Create fake BraTS data structure
    # Structure from user logs: MICCAI_BraTS2020_TrainingData/BraTS20_Training_XXX/BraTS20_Training_XXX_type.nii
    
    data_root = os.path.join(train_dir, 'MICCAI_BraTS2020_TrainingData')
    
    modalities = ['t1', 't1ce', 't2', 'flair', 'seg']
    
    for i in range(1, num_subjects + 1):
        subject_name = f"BraTS20_Training_{i:03d}"
        subject_dir = os.path.join(data_root, subject_name)
        os.makedirs(subject_dir, exist_ok=True)
        
        for mod in modalities:
            file_name = f"{subject_name}_{mod}.nii"
            file_path = os.path.join(subject_dir, file_name)
            
            # Create a small random 3D image (e.g., 32x32x32)
            # Real MRI is much larger (e.g., 240x240x155), but this is for testing code logic
            data = np.random.rand(32, 32, 32).astype(np.float32)
            
            # Create Nifti image
            img = nib.Nifti1Image(data, np.eye(4))
            
            # Save
            nib.save(img, file_path)
            print(f"Created: {file_path}")

    print("\nMock data generation complete.")

if __name__ == '__main__':
    # Generate data in 'mri_data' subdirectory of current script location
    base_dir = os.path.join(os.path.dirname(__file__), 'mri_data')
    create_mock_data(base_dir)
