

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def get_info_from_request(request):
    info = {}
    info['ip_address'] = get_client_ip(request)
    info['user_agent'] = request.META.get('HTTP_USER_AGENT', '<unknown>')
    return info
