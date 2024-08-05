
from cfw_proxy.cf_proxy import CloudflareProxy
from cfw_proxy.certmgr import CertCache
from cfw_proxy.http_conn import HTTPBody, HTTPResponse, HTTPServer, create_http_socket, readline
from cfw_proxy.logconfig import get_logger

from cfw_proxy import cli

def test_proxy():
    cert_cache = CertCache(
        "./cert_cache",
        "./ca.crt",
        "./ca.key"
    )

    server = HTTPServer(
        CloudflareProxy,
        listen=("127.0.0.1", 8843),
        hdl_extra={
            "cert_cache": cert_cache,
            "cf_auth": "hello authentication",
            "cf_url": "http://127.0.0.1:8787/proxy/"
        }
    )
    server.serve_forever()


def test_post():
    cf_sock = create_http_socket("http://127.0.0.1:8787")

    blob = """helloworld""".encode("utf-8")

    cf_sock.sendall(b"POST /proxy/http://127.0.0.1:8787/ HTTP/1.1\r\n")
    cf_sock.sendall(b"x-proxy-host: 127.0.0.1\r\n")
    cf_sock.sendall(b"x-proxy-user-agent: curl/7.68.0\r\n")
    cf_sock.sendall(f"Content-Length: {len(blob)}\r\n".encode("utf-8"))
    cf_sock.sendall(b"\r\n")
    cf_sock.sendall(blob)

    # read response header
    res = HTTPResponse()
    res.parse(cf_sock)
    res.headers.log(get_logger("."))

    # read response body
    body = HTTPBody(res.headers, cf_sock)
    for chunk in body.itr_data():
        print(chunk)



if __name__ == "__main__":
    cli()