from urllib.parse import urlparse, parse_qs
import re
import requests

class Solver:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        }

    def solve(self, invisible, a, r) -> str:
        self.anchor = a
        self.reload = r
        uv = parse_qs(urlparse(self.anchor).query)

        r = requests.get(self.anchor, headers=self.headers)
        a = re.search(r'type="hidden" id="recaptcha-token" value="([^"]+)"', r.text).group(1)

        v = uv['v'][0]
        k = uv['k'][0]
        co = uv['co'][0]

        data = f"v={v}&reason=q&c={a}&k={k}&co={co}&hl=en&size={"invisible" if invisible else "visible"}"

        self.headers.update({
            "Referer": r.url,
            "Content-Type": "application/x-www-form-urlencoded"
        })

        r = requests.post(self.reload, headers=self.headers, data=data)
        return r.text.split('["rresp","')[1].split('"')[0]