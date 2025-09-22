from prompt_template import system_template_text, user_template_text
import requests
from xiaohongshu_model import Xiaohongshu
import json

def generate_xiaohongshu(theme, siliconflow_api_key):
    # 构造请求数据
    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 构造完整的提示词
    prompt_content = system_template_text.format(
        parser_instructions="输出格式必须是JSON格式，包含titles数组和content字符串字段")
    user_content = user_template_text.format(theme=theme)

    messages = [
        {"role": "system", "content": prompt_content},
        {"role": "user", "content": user_content}
    ]

    payload = {
        "model": "Qwen/Qwen3-30B-A3B-Instruct-2507",
        "messages": messages,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }

    headers = {
        "Authorization": f"Bearer {siliconflow_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        # 获取模型返回的JSON内容
        response_content = result['choices'][0]['message']['content']

        # 解析JSON
        response_data = json.loads(response_content)

        # 创建Xiaohongshu对象
        xiaohongshu = Xiaohongshu(**response_data)

        return xiaohongshu

    except Exception as e:
        # 如果解析失败，尝试使用默认的处理方式
        raise Exception(f"API调用失败或解析失败: {str(e)}")
