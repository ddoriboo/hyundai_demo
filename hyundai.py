from openai import OpenAI
import streamlit as st
import time

assistant_id = "asst_ZQUokWWvBp5NYOdH3freDTmP"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password",)
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
      
    client = OpenAI(api_key=openai_api_key)

    thread_id = st.text_input("Thread ID")

    thread_btn = st.button("신규 스레드 생성")
    #"[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    #"[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    if thread_btn: 
        thread = client.beta.threads.create()
        thread_id = thread.id

        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("스레드가 생성되었습니다.")

st.title("💬 현대차 재경 R&D 챗봇")
st.caption("🚀 KPMG AI Center Demo")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 저는 현대차 재경 R&D 챗봇입니다. 저는 연구소 구성원들이 재경 업무와 관련된 다양한 질문에 신속하고 효율적으로 답변을 제공하기 위해 만들어졌습니다. 제가 도와드릴 수 있는 주요 업무는 다음과 같습니다:

예산집행: 예산 사용 및 관리에 대한 문의에 답변합니다.
전표처리: 전표 작성 및 처리 방법에 대한 안내를 제공합니다.
법인카드: 법인카드 사용 및 정산 관련 질문에 답변합니다.
정부과제: 정부과제 관련 재무 처리에 대한 정보를 제공합니다.
고정자산: 고정자산 관리 및 처리 방법에 대해 안내합니다."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
    if not thread_id:
        st.info("Please add your thread ID to continue.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.beta.threads.messages.create(
        thread_id, 
        role="user", 
        content=prompt,
    )
    
    run = client.beta.threads.runs.create(
       thread_id=thread_id,
     assistant_id=assistant_id
     )
    
    run_id = run.id
    
    while True: 
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
            )
        if run.status == "completed":
            break
        else: 
            time.sleep(2)
        print(run)
    
    thread_messages = client.beta.threads.messages.list(thread_id)
    print(thread_messages.data)

    msg = thread_messages.data[0].content[0].text.value
    print(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    
    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #msg = response.choices[0].message.content
    #st.session_state.messages.append({"role": "assistant", "content": msg})
    #st.chat_message("assistant").write(msg)
