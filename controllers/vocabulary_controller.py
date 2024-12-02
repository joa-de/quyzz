import os


class VocabularyController:
    def __init__(self, vocabulary_model, view, lang_manager):
        self.vocabulary_model = vocabulary_model
        self.view = view
        self.lang_manager = lang_manager

    def load_vocabulary(self):
        directory = self.vocabulary_model.directory
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]

        if not files:
            print(self.lang_manager.get("vocabulary_management.no_files_found"))
            return {}, []

        min_id, max_id = self.vocabulary_model.get_word_id_range(files)

        while True:
            self.view.display_available_files(files, min_id, max_id, self.lang_manager)
            choice = self.view.get_user_vocabulary_choice(self.lang_manager)

            if choice is None:
                continue

            if 0 < choice <= len(files):
                filenames = [files[choice - 1]]
                return self.vocabulary_model.load(filenames), filenames
            elif choice == 0:
                return self.vocabulary_model.load(files), files
            elif choice == -1:
                custom_range = self.view.get_custom_range(
                    min_id, max_id, self.lang_manager
                )
                if custom_range:
                    return self.vocabulary_model.load(files, custom_range), files
            else:
                print(self.lang_manager.get("vocabulary_management.invalid_choice"))
