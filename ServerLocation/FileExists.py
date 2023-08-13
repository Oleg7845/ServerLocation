import os

class Exists:
    def check(self, filename: str) -> bool:
        for _, _, files in os.walk('downloaded_files/'):
            for fname in files:
                if fname == filename:
                    return False
        return True