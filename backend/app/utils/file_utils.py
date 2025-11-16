import os

def ensure_storage_path(path):
    os.makedirs(path, exist_ok=True)
    return path

def get_file_extension(file_name: str):
    return os.path.splitext(file_name)[1][1:]  # without dot

def get_user_folder(base_path: str, user_id: str):
    folder = os.path.join(base_path, user_id)
    os.makedirs(folder, exist_ok=True)
    return folder
