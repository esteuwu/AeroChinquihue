if __name__ == "__main__":
    import dotenv
    from mvvm import mvvmModel, mvvmViewModel, mvvmView
    import os
    import pathlib

    dotenv.load_dotenv()
    DATABASE_FILENAME = os.getenv("DATABASE_FILENAME")

    if not pathlib.Path(DATABASE_FILENAME).exists():
        raise FileNotFoundError("Database does not exist")
    model = mvvmModel.Model(DATABASE_FILENAME)
    viewModel = mvvmViewModel.ViewModel(model)
    view = mvvmView.View(viewModel)
    print(view.__str__())
