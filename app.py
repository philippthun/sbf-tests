import os
from flask import Flask, request
from sbf.service_binding_files import get_service_binding_root, get_service_binding_files, as_plain_list

app = Flask(__name__)

port = int(os.getenv("PORT", 8080))

def is_true(value):
    return value.lower() == 'true'

def as_html_list(service_binding_files):
    out = '<dl>'
    for file_path, content in service_binding_files.items():
        out += f"<dt>{file_path}</dt><dd>{content}</dd>"
    out += '</dl>'
    return out

@app.route('/')
def root():
    plain = request.args.get('plain', default=False, type=is_true)

    service_binding_root = get_service_binding_root()
    if not service_binding_root:
        return 'SERVICE_BINDING_ROOT env var not set'

    service_binding_files = get_service_binding_files(service_binding_root)
    if not service_binding_files:
        return 'no service binding files found'
    else:
        if plain:
            return as_plain_list(service_binding_files)
        else:
            return as_html_list(service_binding_files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
