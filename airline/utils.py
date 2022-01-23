def format_serializers_error(error_dict={}):
    """
    [{
        "errorField": <field_name>,
        "error": <error_message>
    },]
    """
    return_list = []
    for key, value in error_dict.items():
        try:
            return_dict = {"errorField": key, "error": value[0]}
            return_list.append(return_dict)
        except Exception as e:
            pass
    return return_list
