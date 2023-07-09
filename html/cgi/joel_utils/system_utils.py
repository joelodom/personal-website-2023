import inspect
import os

def get_absolute_path(base_path, relative_path):
    # Get the directory of the base file
    base_dir = os.path.dirname(base_path)

    # Join the base directory with the relative path to get the absolute path
    absolute_path = os.path.join(base_dir, relative_path)

    # Normalize the path to handle any '..' or '.' in the relative path
    absolute_path = os.path.normpath(absolute_path)

    # Return the absolute path
    return absolute_path


def get_caller_path():
    '''
    To be used in my utilities to get the path to the file of the caller.

    So this actually looks up two places in the stack because it returns its
    caller's caller.
    '''

    caller_frame = inspect.currentframe().f_back.f_back
    caller_filename = inspect.getframeinfo(caller_frame).filename
    return caller_filename

