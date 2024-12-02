class CLIView:
    @staticmethod
    def display_available_files(files, min_id, max_id, lang_manager):
        print(f"\n{lang_manager.get('vocabulary_management.available_lists')}")
        print(
            f"-1: {lang_manager.get('vocabulary_management.custom_range').format(min_id=min_id, max_id=max_id)}"
        )
        print(f"0: {lang_manager.get('vocabulary_management.all_chapters')}")
        for i, file in enumerate(files):
            print(f"{i + 1}: {file[:-4]}")

    @staticmethod
    def get_user_vocabulary_choice(lang_manager):
        try:
            return int(input(lang_manager.get("vocabulary_management.file_selection")))
        except ValueError:
            print(lang_manager.get("vocabulary_management.enter_valid_number"))
            return None

    @staticmethod
    def get_custom_range(min_id, max_id, lang_manager):
        range_input = input(
            lang_manager.get("vocabulary_management.enter_range").format(
                min_id=min_id, max_id=max_id
            )
        )
        try:
            start, end = map(int, range_input.split("-"))
            if start < min_id or end > max_id:
                print(
                    lang_manager.get("vocabulary_management.invalid_range").format(
                        min_id=min_id, max_id=max_id
                    )
                )
            elif start > end:
                print(lang_manager.get("vocabulary_management.invalid_range_order"))
            else:
                return start, end
        except ValueError:
            print(lang_manager.get("vocabulary_management.invalid_range_format"))
        return None
