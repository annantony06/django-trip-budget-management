import os

def remove_null_bytes_from_file(filepath):
    with open(filepath, 'rb') as file:
        content = file.read()

    # Remove null bytes
    cleaned_content = content.replace(b'\x00', b'')

    with open(filepath, 'wb') as file:
        file.write(cleaned_content)
    print(f'Cleaned: {filepath}')

def clean_project_files(directory):
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            with open(filepath, 'rb') as f:
                if b'\x00' in f.read():
                    remove_null_bytes_from_file(filepath)

clean_project_files(r'C:\Users\augustine\Documents\djangoaug')

