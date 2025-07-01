import requests
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config_path = Path(__file__).parent.parent / 'config.ini'
config.read(config_path, encoding='utf-8')
webhook_url = config.get('WeCom', 'webhook_url', fallback=None)

def send_wecom_message(content: str):
    if not webhook_url:
        print("企业微信 Webhook URL 未配置，跳过发送。")
        return
    headers = {"Content-Type": "application/json"}
    payload = {"msgtype": "markdown", "markdown": {"content": content}}
    try:
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        print("企业微信通知发送成功。")
    except requests.exceptions.RequestException as e:
        print(f"企业微信通知发送失败: {e}")