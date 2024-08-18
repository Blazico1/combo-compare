import os
from logic.u8archive import U8Archive

class Model:
    def __init__(self):
        self.selected_file = None

    def check_files(self):
        # Return True if both files exist, False otherwise
        if os.path.exists('bins/kartParam.bin') and os.path.exists('bins/driverParam.bin'):
            return True
        return False

    def set_selected_file(self, file_path):
        self.selected_file = file_path

    def extract_files(self):
        if not self.selected_file:
            raise Exception("No file selected")
        
        archive = U8Archive(self.selected_file)
        archive.extract_file('kartParam.bin')
        archive.extract_file('driverParam.bin')
