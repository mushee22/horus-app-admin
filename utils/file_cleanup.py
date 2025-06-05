def delete_file(field_file):
    """
    Deletes the file associated with the given field_file if it exists.
    """
    try:
        if field_file and field_file.name:
            field_file.delete(save=False)
    except Exception as e:
        print(f"Error deleting file {field_file.name}: {e}")