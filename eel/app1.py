#!/usr/bin/env python3

import sys
import webview
from subprocess import getoutput


class Api:
    def __init__(self):
        self.name = "js_api"

    def my_exec(self, a):
        print(window._http_port, window._server, window._server_args)
        window.hide()
        path = getoutput(f"{sys.executable} tools/askdir.py")
        path = path.split("\n")[-1]
        window.show()
        print("path", path)
        return {"message": path}


html_str = """
<!DOCTYPE html>
<html>
<head>
    <script>
        window.addEventListener('pywebviewready', function() {
        })
    
        function exec_python() {
            pywebview.api.my_exec(11).then((res) => {
                console.log(res)
                document.getElementById('response-container').innerText = res.message
            })
        }
    </script>
</head>
<body>
    <button onClick="exec_python()">button</button>
    <br/>
    <div id="response-container"></div>
</body>
</html>
"""

if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        "title",
        text_select=True,
        html=html_str,
        js_api=api,
        height=400,
        zoomable=True,
        draggable=True,
        server=None,
    )
    webview.start(debug=True)
