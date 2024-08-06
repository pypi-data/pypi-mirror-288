class LanguageNameExistError(Exception):
    def __init__(self, language_name: str, message: str = 'Language you are trying to add is already exist!'):
        self.language_name = language_name
        self.message = message

        super().__init__(self.message)


class LanguageNotExistError(Exception):
    def __init__(self, language_name: str, message: str = 'Language you are trying to delete is not exist!'):
        self.language_name = language_name
        self.message = message

        super().__init__(self.message)


class PytFileNotFoundError(Exception):
    def __init__(self, language_name: str, message: str = 'File not found'):
        self.language_name = language_name
        self.message = message

        super().__init__(self.message)


class PytFolderNotFoundError(Exception):
    def __init__(self, message: str = 'Folder not found'):
        self.message = message

        super().__init__(self.message)


class FileFormatValidationError(Exception):
    def __init__(self, language_name: str,
                 message: str = 'File format not valid'):
        self.language_name = language_name
        self.message = message

        super().__init__(self.message)


class FileIsEmptyError(Exception):
    def __init__(self, language_name: str,
                 message: str = 'File is empty'):
        self.language_name = language_name
        self.message = message

        super().__init__(self.message)


class NoTranslationError(Exception):
    def __init__(self,
                 text: str,
                 language_name: str,
                 message: str = 'There is no translation for text'):
        self.text = text
        self.language_name = language_name
        self.message = message

        super().__init__(self.message)
