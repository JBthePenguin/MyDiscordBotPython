from discord.utils import get as get_obj
from .settings import error_msgs


def param_command(list_obj, obj_name_or_id, obj_type):
    """ Check if obj is founded, return obj or a no exist message """
    obj = get_obj(list_obj, name=obj_name_or_id)
    if obj is None:
        try:
            obj = get_obj(list_obj, id=int(obj_name_or_id))
        except ValueError:  # no obj with this name
            return error_msgs['no_exist'].format(
                obj_type + ' name', obj_name_or_id)
        else:
            if obj is None:  # no obj with this id
                return error_msgs['no_exist'].format(
                    obj_type + ' id', obj_name_or_id)
    return obj
