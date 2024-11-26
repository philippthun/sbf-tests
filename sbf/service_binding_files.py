import os

def get_service_binding_root():
    return os.getenv("SERVICE_BINDING_ROOT")

def get_service_binding_files(service_binding_root):
    sbf = {}
    if service_binding_root:
        for root, _, files in os.walk(service_binding_root):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    sbf[file_path] = f.read()
    return sbf

def as_plain_list(service_binding_files):
    out = ''
    for file_path, content in service_binding_files.items():
        out += f"{file_path}: {content}\n"
    return out

