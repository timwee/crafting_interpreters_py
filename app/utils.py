from typing import Any

def stringify(val: Any):
    if val is None:
        return "nil"
    if isinstance(val, bool):
        if val:
            return "true"
        else:
            return "false"
    elif isinstance(val, (float, int)):
        # print(f'in print_val numeric: {val}')
        str_val = str(val)
        str_val = str_val.removesuffix(".0")
        if "." in str_val:
            str_val.removesuffix("0") 
        return str_val
    else:
        return str(val)