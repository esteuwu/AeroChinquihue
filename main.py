# pylint: disable=C0114
if __name__ == "__main__":
    import dotenv
    from mvvm import mvvm_model, mvvm_view_model, mvvm_view
    import os
    import pathlib

    dotenv.load_dotenv()
    DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")

    if not pathlib.Path(DATABASE_FILENAME).exists():
        raise FileNotFoundError("Database does not exist")
    model = mvvm_model.Model(DATABASE_FILENAME)
    viewModel = mvvm_view_model.ViewModel(model)
    view = mvvm_view.View(viewpip install PySide6

