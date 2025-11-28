import subprocess
import sys

def set_env_var(name, value, scope="User"):

    if scope not in ["User", "Machine"]:
        raise ValueError("scope 必須是 'User' 或 'Machine'")

    # 建立 PowerShell 指令
    ps_command = (
        f'[Environment]::SetEnvironmentVariable("{name}", "{value}", "{scope}")'
    )

    try:
        subprocess.run(["powershell", "-Command", ps_command], check=True)
        print(f"成功設定環境變數：{name} = {value} （範圍：{scope}）")
    except subprocess.CalledProcessError as e:
        print(f"設定環境變數失敗：{e}")
        sys.exit(1)

def get_path():
    path = subprocess.run(["powershell", "-Command", "pwd"], capture_output=True, text=True).stdout.strip()
    return path

print(get_path())


set_env_var("ffmpeg", "C:\\ffmpeg\\bin", scope="User")
