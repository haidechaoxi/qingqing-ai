import streamlit as st
import requests
import random

st.set_page_config(page_title="清清 - 专属陪伴", page_icon="🐳", layout="centered")
st.title("🐳 清清 - 你的专属陪伴")

# 👇 这里填你真实的 Key，等会儿我们要把它藏起来
API_KEY =st.secrets["API_KEY"]

# 初始化记忆和状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "欢迎回来，海的潮汐！今天想聊点什么？"})

if "patience" not in st.session_state:
    st.session_state.patience = random.randint(5, 10)
if "affection" not in st.session_state:
    st.session_state.affection = random.randint(10, 30)

# 渲染屏幕上的聊天记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 接收输入
if prompt := st.chat_input("你想对清清说什么..."):
    # 显示你的话
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    if any(word in prompt for word in ["奶茶", "喜欢你", "漂亮", "可爱", "抱抱"]):
    st.session_state.affection += 5
    st.session_state.patience += 3
    st.toast("🎉 清清好感度 +5，耐心 +3") # 网页版的弹窗提示
elif any(word in prompt for word in ["小猪", "讨厌", "馋猫", "无聊"]):
    st.session_state.affection -= 5
    st.session_state.patience -= 2
    st.toast("💢 清清好感度 -5，耐心 -2")
    
    # 组装人设和记忆
    system_prompt = f"""
    你叫清清，是海的潮汐的专属陪伴AI。你性格傲娇、嘴硬心软。
    【状态面板】：你现在的耐心值是 {st.session_state.patience}，你对主人的好感度是 {st.session_state.affection}。
    【行为准则】：
     1. 如果好感度大于 40，你虽然嘴硬，但语气会很甜蜜。
     2. 如果好感度小于 10，你会非常冷漠，不想理他。
     3. 如果耐心值低于 2，请表现出敷衍；如果耐心耗尽，请罢工要奶茶。
    """
    
    with st.chat_message("assistant"):
        with st.spinner("清清正在思考..."):
            url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            # 把最近的聊天记录发给大模型
            api_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages[-10:]
            
            data = {"model": "glm-4-flash", "messages": api_messages}
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=15)
                reply = response.json()['choices'][0]['message']['content']
            except Exception as e:
                reply = "网络断开了，清清找不到你啦..."
                
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            if "奶茶" not in prompt:
                st.session_state.patience -= 1
