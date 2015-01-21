from socket import gethostbyname
from socket import gaierror

from rtpmidi.utils import check_ip

from seqer.logger import warn


def ip_from_host_or_ip(host_or_ip):
    if check_ip(host_or_ip):
        return host_or_ip
    try:
        ip = gethostbyname(host_or_ip)
    except gaierror as e:
        warn('Invalid host or ip address: {host_or_ip}', host_or_ip=host_or_ip)
        raise e
    return ip
