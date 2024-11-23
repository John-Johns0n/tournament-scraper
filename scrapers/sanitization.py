def capitalize_multiple_names(first_name, last_name) -> tuple[str, str]:
    """
    Handles capitalization of multiple and/or hyphenated names.
    Also deals with 'Linden, van der' -type names.

    :param first_name: First name to capitalize
    :param last_name: Last name to capitalize
    :return: A tuple containing the properly formatted first name and last name
    """
    first_name = ' '.join('-'.join(part.capitalize() for part in group.split('-')) for group in first_name.split(' '))
    last_name = ' '.join('-'.join(part.capitalize() for part in group.split('-')) for group in last_name.split(' '))

    parts = last_name.split(', ')
    if len(parts) > 1:
        last_name = f'{parts[1]} {parts[0]}'

    return first_name, last_name
