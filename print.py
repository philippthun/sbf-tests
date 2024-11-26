from sbf.service_binding_files import get_service_binding_root, get_service_binding_files, as_plain_list

def print_service_binding_files():
    service_binding_root = get_service_binding_root()
    service_binding_files = get_service_binding_files(service_binding_root)
    print(as_plain_list(service_binding_files))
