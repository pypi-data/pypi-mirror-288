import re

from localtrans.configuration import EXTENSION
from localtrans.models.exceptions import LanguageNameExistError, PytFileNotFoundError, FileFormatValidationError, \
    NoTranslationError, PytFolderNotFoundError, LanguageNotExistError
from localtrans.models.pytranslator import PytFile

import os
from pathlib import Path
import glob


class Translate:
    # raise_error just for translate
    def __init__(self, pyt_files: list[PytFile], raise_error: bool = True):
        self.raise_error = raise_error
        self.lang_names = set()

        for pyt_file in pyt_files:
            if pyt_file.language_name in self.lang_names:
                raise LanguageNameExistError(language_name=pyt_file.language_name)

            if not os.path.exists(pyt_file.file_path):
                raise PytFileNotFoundError(language_name=pyt_file.language_name)

            self.lang_names.add(pyt_file.language_name)

        self.lang_files = pyt_files

    def add_lang(self, pyt_file: PytFile):
        if pyt_file.language_name in self.lang_names:
            raise LanguageNameExistError(language_name=pyt_file.language_name)

        if not os.path.exists(pyt_file.file_path):
            raise PytFileNotFoundError(language_name=pyt_file.language_name)

        self.lang_names.add(pyt_file.language_name)
        self.lang_files.append(pyt_file)

    def delete_lang(self, lang_name: str):
        if lang_name not in self.lang_names:
            raise LanguageNotExistError(language_name=lang_name)

        self.lang_names.remove(lang_name)
        self.lang_files = [lang_file for lang_file in self.lang_files if lang_file.language_name != lang_name]

    def delete_lang_with_file(self, lang_name: str):
        if lang_name not in self.lang_names:
            raise LanguageNotExistError(language_name=lang_name)

        self.lang_names.remove(lang_name)

        lang_file = None
        for _lang_file in self.lang_files:
            if _lang_file.language_name == lang_name:
                lang_file = _lang_file
                break

        os.remove(lang_file.file_path)
        self.lang_files.remove(lang_file)

    @staticmethod
    def initialize(base_directory: str, raise_error=True):
        if not os.path.exists(base_directory):
            raise PytFolderNotFoundError()

        pyt_files_arr = glob.glob(os.path.join(base_directory, f'*.{EXTENSION}'))
        pyt_files = []

        for file in pyt_files_arr:
            pyt_path = Path(file)

            lang_name = pyt_path.stem
            lang_file_path = file

            pyt_file = PytFile(language_name=lang_name, file_path=lang_file_path)
            pyt_files.append(pyt_file)

        return Translate(pyt_files, raise_error=raise_error)

    def __process_file(self, lang_name: str, delimiter: str):
        if lang_name not in self.lang_names:
            raise LanguageNameExistError(language_name=lang_name, message='File not found')

        file_path = None
        for lang_file in self.lang_files:
            if lang_file.language_name == lang_name:
                file_path = lang_file.file_path
                break

        dictionary = {}
        translate_file = open(file_path, 'r')
        lines = translate_file.readlines()

        for line in lines:
            if not line.strip():
                continue

            pattern = re.compile(rf'(.+?){delimiter}(.+)')
            match = pattern.match(line)

            if not match:
                raise FileFormatValidationError(language_name=lang_name)

            dict_key = match.group(1).strip()
            dict_value = match.group(2).strip()

            if dict_key in dictionary:
                raise FileFormatValidationError(language_name=lang_name,
                                                message='There are 2 keys with the same name in the file')

            dictionary[dict_key] = dict_value

        translate_file.close()
        return dictionary

    def translate(self, to_lang: str, text: str, delimiter: str = '='):
        dictionary = self.__process_file(lang_name=to_lang, delimiter=delimiter)

        if text not in dictionary:
            if self.raise_error:
                raise NoTranslationError(text=text, language_name=to_lang)

            return None

        return dictionary[text]
