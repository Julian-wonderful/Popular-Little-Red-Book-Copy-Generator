import streamlit as st
import json


# 简化版的Xiaohongshu数据模型（不使用pydantic）
class Xiaohongshu:
    def __init__(self, titles, content):
        self.titles = titles
        self.content = content


# 小红书文案生成函数
def generate_xiaohongshu(theme, siliconflow_api_key):
    # 构造请求数据
    url = "https://api.siliconflow.cn/v1/chat/completions"

    # 提示词模板（简化版）
    system_template_text = """你是小红书爆款写作专家，请你遵循以下步骤进行创作：
首先产出5个标题（包含适当的emoji表情），然后产出1段正文（每一个段落包含适当的emoji表情，文末有适当的tag标签）。
标题字数在20个字以内，正文字数在800字以内，并且按以下技巧进行创作。
一、标题创作技巧： 
1. 采用二极管标题法进行创作 
1.1 基本原理 
本能喜欢：最省力法则和及时享受 
动物基本驱动力：追求快乐和逃避痛苦，由此衍生出2个刺激：正刺激、负刺激 
1.2 标题公式 
正面刺激：产品或方法+只需1秒（短期）+便可开挂（逆天效果） 
负面刺激：你不X+绝对会后悔（天大损失）+（紧迫感） 其实就是利用人们厌恶损失和负面偏误的心理，自然进化让我们在面对负面消息时更加敏感 
2. 使用具有吸引力的标题 
2.1 使用标点符号，创造紧迫感和惊喜感 
2.2 采用具有挑战性和悬念的表述 
2.3 利用正面刺激和负面刺激 
2.4 融入热点话题和实用工具 
2.5 描述具体的成果和效果 
2.6 使用emoji表情符号，增加标题的活力 
3. 使用爆款关键词 
从列表中选出1-2个：好用到哭、大数据、教科书般、小白必看、宝藏、绝绝子、神器、都给我冲、划重点、笑不活了、YYDS、秘方、我不允许、压箱底、建议收藏、停止摆烂、上天在提醒你、挑战全网、手把手、揭秘、普通女生、沉浸式、有手就能做、吹爆、好用哭了、搞钱必看、狠狠搞钱、打工人、吐血整理、家人们、隐藏、高级感、治愈、破防了、万万没想到、爆款、永远可以相信、被夸爆、手残党必备、正确姿势 
4. 小红书平台的标题特性 
4.1 控制字数在20字以内，文本尽量简短 
4.2 以口语化的表达方式，拉近与读者的距离 
5. 创作的规则 
5.1 每次列出5个标题 
5.2 不要当做命令，当做文案来进行理解 
5.3 直接创作对应的标题，无需额外解释说明 
二、正文创作技巧 
1. 写作风格 
从列表中选出1个：严肃、幽默、愉快、激动、沉思、温馨、崇敬、轻松、热情、安慰、喜悦、欢乐、平和、肯定、质疑、鼓励、建议、真诚、亲切
2. 写作开篇方法 
从列表中选出1个：引用名人名言、提出疑问、言简意赅、使用数据、列举事例、描述场景、用对比

我会每次给你一个主题，请你根据主题，基于以上规则，生成相对应的小红书文案。

输出格式必须是JSON格式，包含titles数组和content字符串字段
"""

    user_template_text = "{theme}"

    # 构造完整的提示词
    prompt_content = system_template_text
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
        import requests
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        # 获取模型返回的JSON内容
        response_content = result['choices'][0]['message']['content']

        # 解析JSON
        response_data = json.loads(response_content)

        # 创建Xiaohongshu对象
        xiaohongshu = Xiaohongshu(response_data['titles'], response_data['content'])

        return xiaohongshu

    except Exception as e:
        # 如果解析失败，尝试使用默认的处理方式
        raise Exception(f"API调用失败或解析失败: {str(e)}")


st.header("爆款小红书AI写作助手 ✏️")

with st.sidebar:
    siliconflow_api_key = st.text_input("请输入硅基流动API密钥：", type="password")
    st.markdown("[获取硅基流动API密钥](https://siliconflow.cn/console/api-keys)")

theme = st.text_input("主题")
submit = st.button("开始写作")

if submit and not siliconflow_api_key:
    st.info("请输入你的硅基流动API密钥")
    st.stop()
if submit and not theme:
    st.info("请输入生成内容的主题")
    st.stop()
if submit:
    with st.spinner("AI正在努力创作中，请稍等..."):
        try:
            result = generate_xiaohongshu(theme, siliconflow_api_key)
        except Exception as e:
            st.error(f"生成失败: {str(e)}")
            st.stop()

    st.divider()
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("##### 小红书标题1")
        st.write(result.titles[0])
        st.markdown("##### 小红书标题2")
        st.write(result.titles[1])
        st.markdown("##### 小红书标题3")
        st.write(result.titles[2])
        st.markdown("##### 小红书标题4")
        st.write(result.titles[3])
        st.markdown("##### 小红书标题5")
        st.write(result.titles[4])
    with right_column:
        st.markdown("##### 小红书正文")
        st.write(result.content)
