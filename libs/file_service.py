from datetime import datetime

# from config.config import BASE_DIR
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def move_user_video(user_id, file_path: Path):
    user_folder = Path(BASE_DIR / "static" / str(user_id))
    user_folder.mkdir(exist_ok=True)
    target_folder = Path(BASE_DIR / "static" / str(user_id) / "videos")
    target_folder.mkdir(exist_ok=True)
    file = file_path.rename(target_folder / Path(str(datetime.now().strftime("%I_%M_%S_")) + file_path.name))
    size = file.stat().st_size
    file_name_for_db = f"/static/{user_id}/videos/{file.name}"
    return file_name_for_db, size


def move_user_picture(user_id, file_path: Path):
    user_folder = Path(BASE_DIR / "static" / str(user_id))
    user_folder.mkdir(exist_ok=True)
    target_folder = Path(BASE_DIR / "static" / str(user_id)/"pictures")
    target_folder.mkdir(exist_ok=True)
    file = file_path.rename(target_folder / Path(str(datetime.now().strftime("%I_%M_%S_")) + file_path.name))
    size = file.stat().st_size
    file_name_for_db = f"/static/{user_id}/pictures/{file.name}"
    return file_name_for_db, size

def move_user_document(user_id, file_path: Path):
    user_folder = Path(BASE_DIR / "static" / str(user_id))
    user_folder.mkdir(exist_ok=True)
    target_folder = Path(BASE_DIR / "static" / str(user_id)/"documents")
    target_folder.mkdir(exist_ok=True)
    file = file_path.rename(target_folder / Path(str(datetime.now().strftime("%I_%M_%S_")) + file_path.name))
    size = file.stat().st_size
    file_name_for_db = f"/static/{user_id}/documents/{file.name}"
    return file_name_for_db, size

def move_user_file(user_id, file_path: Path):
    user_folder = Path(BASE_DIR / "static" / str(user_id))
    user_folder.mkdir(exist_ok=True)
    target_folder = Path(BASE_DIR / "static" / str(user_id)/"files")
    target_folder.mkdir(exist_ok=True)
    file = file_path.rename(target_folder / Path(str(datetime.now().strftime("%I_%M_%S_")) + file_path.name))
    size = file.stat().st_size
    file_name_for_db = f"/static/{user_id}/files/{file.name}"
    return file_name_for_db, size

def delete_user_file(path):
    filename = Path(f'{BASE_DIR}{path}')
    try:
        filename.unlink()
    except FileNotFoundError as err:
        print(err)