import os
import shutil
import yaml

# Paths to the original image and label directories
train_image_dir = '../data/train/images/'
train_label_dir = '../data/train/labels/'
val_image_dir = '../data/valid/images/'
val_label_dir = '../data/valid/labels/'

# Create new directories for subset
train_subset_image_dir = '../data_subset/train/images/'
train_subset_label_dir = '../data_subset/train/labels/'
val_subset_image_dir = '../data_subset/valid/images/'   
val_subset_label_dir = '../data_subset/valid/labels/'

# Create the directories if they don't exist
os.makedirs(train_subset_image_dir, exist_ok=True)
os.makedirs(train_subset_label_dir, exist_ok=True)
os.makedirs(val_subset_image_dir, exist_ok=True)
os.makedirs(val_subset_label_dir, exist_ok=True)

# Function to copy every nth file (e.g., every 20th file)
def copy_subset(image_dir, label_dir, subset_image_dir, subset_label_dir, step=20):
    image_files = sorted(os.listdir(image_dir))
    for i in range(0, len(image_files), step):
        image_file = image_files[i]
        label_file = image_file.replace('.jpg', '.txt')  # assuming labels are .txt files
        # Copy image and corresponding label file
        shutil.copy(os.path.join(image_dir, image_file), os.path.join(subset_image_dir, image_file))
        shutil.copy(os.path.join(label_dir, label_file), os.path.join(subset_label_dir, label_file))

# Copy every 20th image from the training set
copy_subset(train_image_dir, train_label_dir, train_subset_image_dir, train_subset_label_dir)

# Optionally, you can do the same for the validation set, if you want to create a subset for validation as well
copy_subset(val_image_dir, val_label_dir, val_subset_image_dir, val_subset_label_dir)

# Define the new data.yaml for the subset
data_yaml_path = '../data_subset/data_subset.yaml'
# Check if the file already exists and remove it
if os.path.exists(data_yaml_path):
    os.remove(data_yaml_path)

# Create the data.yaml content
names = [
    'Amoeba', 'Arcella', 'Aspidisca', 'Chaetonotus', 'Chaetopira', 'Chilodonella', 'Cyclidium', 
    'Euglypha', 'Euplotes', 'Flagellates', 'Giardia', 'Microalgae', 'Nematode', 'Paramecium', 
    'Pediastrum_10', 'Pediastrum_1F0', 'Pediastrum_1T', 'Pediastrum_1TH', 'Pediastrum_75FI', 
    'Pediastrum_75FO', 'Pediastrum_75O', 'Pediastrum_75T', 'Pediastrum_75TH', 'Pediastrum_CF', 
    'Pediastrum_CFI', 'Pediastrum_CO', 'Pediastrum_CT', 'Pediastrum_CTH', 'Pristina', 'Rodbacteria', 
    'Rotatoria', 'Rotifer', 'Sphericalbacteria', 'Sprialbacteria', 'Stylonychia', 'Suctorida', 
    'Vorticella', 'Yeast'
]

# Prepare the data structure
data_yaml = {
    'train': "../train/images/",
    'val': "../valid/images/",
    'test': "../test/images/",
    'nc': len(names),
    'roboflow': {
        'workspace': 'protozoadetectionj',
        'project': 'protozoadataset',
        'version': 2,
        'license': 'CC BY 4.0',
        'url': 'https://universe.roboflow.com/protozoadetectionj/protozoadataset/dataset/2'
    }
}

# Save to data.yaml file using yaml.dump() to ensure proper formatting
with open(data_yaml_path, 'w') as file:
    yaml.dump(data_yaml, file, default_flow_style=False, sort_keys=False)

    # Now explicitly write the names in flow style (square brackets)
    file.write("\nnames: " + str(names).replace('[', '[').replace(']', ']') + '\n')

print(f"data.yaml has been created at {data_yaml_path}")
