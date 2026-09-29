"""Start the viewer on a free port for integration tests and make requests to it."""

import http.client
import json
import threading
import unittest
from pathlib import Path

import specview

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "project"


class ServerTestCase(unittest.TestCase):
    start: Path = FIXTURE
    maxDiff = 2000

    @classmethod
    def setUpClass(cls):
        cls.server = specview.make_server(cls.start, "127.0.0.1", 0)
        cls.server.RequestHandlerClass.log_message = lambda *a, **k: None  # keep test output quiet
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path: str, host: str | None = None) -> tuple[int, str]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        headers = {"Host": host or "localhost:%d" % self.port}
        conn.putrequest("GET", path, skip_host=True, skip_accept_encoding=True)
        for key, value in headers.items():
            conn.putheader(key, value)
        conn.endheaders()
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        conn.close()
        return response.status, body

    def refs(self, page: str) -> dict:
        start = page.index('<script type="application/json" id="refs">') + len('<script type="application/json" id="refs">')
        return json.loads(page[start : page.index("</script>", start)])
