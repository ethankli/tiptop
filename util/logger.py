class Logger:
    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def info(self, message: str):
        self.log(f"INFO: {message}")

    def warning(self, message: str):
        self.log(f"WARNING: {message}")

    def error(self, message: str):
        self.log(f"ERROR: {message}")
