import os
import shutil

# Path to your Downloads folder (change if needed)
downloads_path = os.path.expanduser("~/Downloads")
nl_folder = os.getcwd() #os.path.join(downloads_path, "nl")

# Create nl folder if it doesn't exist
os.makedirs(nl_folder, exist_ok=True)

# Loop through files in Downloads
for filename in os.listdir(downloads_path):
    file_path = os.path.join(downloads_path, filename)
    
    # Separate name and extension
    name_without_ext, ext = os.path.splitext(filename)
    
    
    
    if os.path.isfile(file_path) and "_nl_revision" in name_without_ext.lower():
        shutil.move(file_path, os.path.join(nl_folder,'revision', filename))
        print(f"Moved: {filename}")

    # Check if "_nl" appears anywhere in the filename (excluding extension)
    if os.path.isfile(file_path) and "_nl" in name_without_ext.lower():
        shutil.move(file_path, os.path.join(nl_folder, filename))
        print(f"Moved: {filename}")
        
    

print("Done!")
