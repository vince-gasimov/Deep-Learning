import os
import shutil
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Split dataset into train, validation, and test sets")
    parser.add_argument('--train', type=int, required=True, help="Train dataset percentage")
    parser.add_argument('--validation', type=int, required=True, help="Validation dataset percentage")
    parser.add_argument('--test', type=int, required=True, help="Test dataset percentage")
    parser.add_argument('--folder', type=str, required=True, help="Source dataset folder")
    parser.add_argument('--dest', type=str, required=True, help="Destination folder for split data")
    return parser.parse_args()

def copy_image(file, set_type, dest_folder):
    source_file = os.path.join(args.folder, file)
    destination_folder = os.path.join(dest_folder, set_type)
    destination_file = os.path.join(destination_folder, file)

    # Create destination folder if it does not exist
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the file
    shutil.copy(source_file, destination_file)

def split_dataset():
    # List all jpg files in the source folder
    files = [f for f in os.listdir(args.folder) if f.endswith('.jpg')] 

    # Shuffle the files to ensure randomness
    random.shuffle(files)

    # Calculate split indices
    total_files = len(files)
    train_size = int(args.train / 100 * total_files)
    validation_size = int(args.validation / 100 * total_files)
    test_size = total_files - train_size - validation_size

    # Split the dataset
    train_files = files[:train_size]
    validation_files = files[train_size:train_size + validation_size]
    test_files = files[train_size + validation_size:]

    # Copy files to respective folders
    for file in train_files:
        copy_image(file, 'train', args.dest)

    for file in validation_files:
        copy_image(file, 'validation', args.dest)

    for file in test_files:
        copy_image(file, 'test', args.dest)

    print(f"Total Train Files: {len(train_files)}")
    print(f"Total Validation Files: {len(validation_files)}")
    print(f"Total Test Files: {len(test_files)}")

if __name__ == "__main__":
    args = parse_args()  # Fix here: parantez doğru şekilde kapatılmalı
    split_dataset()
