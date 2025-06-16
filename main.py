from src.services.app import App
from src.utils.enviroment import EnvironmentVariables

if __name__ == "__main__":
    app = App()
    app.run()
    print("Server is running ...")
