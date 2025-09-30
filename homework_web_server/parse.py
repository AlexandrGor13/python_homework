import re
from urllib.parse import unquote

def parse_request(request):
    method, path, headers, body = None, None, {}, ''
    if request:
        lines = request.split('\n')    
        line = lines.pop(0).strip()

        #method and path
        line = unquote(line)
        match = re.match('([A-Z]+)\\s+(\\S+)\\s+', line)
        if match:
            method, path = match.groups()

        #headers
        while True:
            line = lines.pop(0).strip()
            if not line:
                break
            header_name, header_value = line.split(':', 1)
            headers[header_name.lower()] = header_value.strip()

        #body
        if len(lines) > 0:
            body = '\n'.join(lines)

    return  {
        "method": method,
        "path": path,
        "headers": headers,
        "body": body,
        }
