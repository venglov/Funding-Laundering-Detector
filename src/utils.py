

def extract_argument(event: dict, argument: str) -> any:
    """
    the function extract specified argument from the event
    :param event: dict
    :param argument: str
    :return: argument value
    """
    return event.get('args', {}).get(argument, "")


def get_full_info(object_inst):
    values = vars(object_inst)
    values['block'] = vars(values['block'])
    values['logs'] = [vars(log) for log in values['logs']]
    values['traces'] = [vars(trace) for trace in values['traces']]
    values['transaction'] = vars(values['transaction'])

    return values

