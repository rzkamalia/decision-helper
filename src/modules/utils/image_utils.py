def are_options_text_only(options: list[str]) -> bool:
    """
    Check if options are text-only or contain file paths.
    Returns True if all options are plain text, False if any contain file paths.
    """
    if not options:
        return True

    all_are_files = all(option.startswith("data:image/") for option in options)

    return not all_are_files
