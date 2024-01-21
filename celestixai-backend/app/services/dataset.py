import os


def delete_st_dataset(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    os.remove(os.path.join(root, file))
            os.rmdir(path)
        else:
            print(f"Invalid path: {path}")

        print(f"Successfully deleted: {path}")
    except Exception as e:
        print(f"Error deleting {path}: {e}")
