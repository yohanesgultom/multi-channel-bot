from urllib.request import ssl, socket
from datetime import datetime, timezone
import OpenSSL

def get_num_days_before_expired(hostname: str, port: str = '443'):
    """
    Get number of days before an TLS/SSL of a domain expired
    """
    context = ssl.SSLContext()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname = hostname) as ssock:
            certificate = ssock.getpeercert(True)
            cert = ssl.DER_cert_to_PEM_cert(certificate)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            cert_expires = datetime.strptime(x509.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%S%z')
            num_days = (cert_expires - datetime.now(timezone.utc)).days
            # print(f'{hostname} expires in {num_days} day(s)')
            return num_days