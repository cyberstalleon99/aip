# **************************************************************
# START dongilay
# **************************************************************

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.utils import construct_change_message

# ***************************************************
# ***************LogEntry Helpers********************

def do_log(user, modelIns, obj, flag, msg=""):
    if flag == ADDITION:
        log_entry = LogEntry.objects.log_action(
                        user_id=user.id,
                        content_type_id=ContentType.objects.get_for_model(model=modelIns).pk,
                        object_id=obj.id,
                        # object_repr=f'{obj.item.item_name} ({str(obj)})',
                        object_repr=str(obj),
                        action_flag=flag,
                        change_message="Added from Forms.")

    elif flag == CHANGE:
        log_entry = LogEntry.objects.log_action(
                        user_id=user.id,
                        content_type_id=ContentType.objects.get_for_model(model=modelIns).pk,
                        object_id=obj.id,
                        # object_repr=f'{obj.item.item_name} ({str(obj)})',
                        object_repr=str(obj),
                        action_flag=flag,
                        change_message=msg)
    return log_entry

def add_log(user, modelIns, obj):
    do_log(user, modelIns, obj, ADDITION)

def change_log(user, modelIns, obj, form):
    msg = construct_change_message(form, None, False)
    do_log(user, modelIns, obj, CHANGE, msg)

# ***************************************************

# **************************************************************
# END dongilay
# **************************************************************