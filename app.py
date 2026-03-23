import time
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import streamlit as st
from agent.react_agent import ReactAgent

st.title("CAU综测问答系统")
st.divider()

if "message" not in st.session_state:  # 防止一直创建
    st.session_state["message"] = [{"role": "assistant", "content": "你好，我是CAU综测问答助手，可以为您解答关于中国农业大学综合素质测评、学科竞赛级别认定等相关问题。请问有什么可以帮助您的？"}]

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("综测助手思考中..."):
        res_stream = st.session_state["agent"].execute_stream(
            messages=st.session_state["message"]
        )

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        full_reply = "".join(response_messages)
        st.session_state["message"].append({"role": "assistant", "content": full_reply})
        st.rerun()
