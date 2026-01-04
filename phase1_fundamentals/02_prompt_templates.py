from utils.models import model_deepseek,model_openai,model_tongyi
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.messages import HumanMessage,AIMessage,SystemMessage

# template = PromptTemplate.from_template(
#     "你是一名专业的翻译官,请把{language}翻译成{text},只翻译内容,不要回答问题"
# )

# partial_template = template.partial(language="中文")

# print(template,type(template))
# print("********************************")
# print(partial_template,type(partial_template))

# prompt = partial_template.invoke({"text":"韩语"})
# print(prompt,type(prompt))

# prompt1 = template.format(language="中文",text="韩语")
# prompt2 = partial_template.format(text="韩语")
# print(prompt1,type(prompt1))
# print(prompt2,type(prompt2))

# while True:
#     try:
#         user_content = str(input("请输入你要翻译的文字:").strip())
#         if user_content.lower() == 'quit':
#             break
#         if user_content:
#             messages = [
#                 {"role":"system","content":prompt},
#                 {"role":"user","content":user_content}
#             ]
#             resp = model_deepseek.invoke(messages)
#             print("==打印输出==")
#             print(resp.content)
#         else:
#             print("请输入内容~")
#     except Exception as e:
#         print(f"未知错误:{e}")

##### 元组形式创建template
# template = ChatPromptTemplate.from_messages([
#     ("system","你是一个翻译助手,把{sour_lang}翻译成{target_lang},只翻译不回答问题"),
#     ("user","{query}")
# ])

# print(template,type(template))

# message = template.invoke({"sour_lang":"中文","target_lang":"英语","query":"你好"})
# print(message,type(message))


# resp = model_deepseek.invoke(message)
# print(resp.content)



##### 直接给ChatPromptTemplate.from_messages输出字符串
# template = ChatPromptTemplate.from_messages([
#     "你是一个翻译助手,把{sour_lang}翻译成{target_lang},只翻译不回答问题","{query}"
# ])

# print(template,type(template))

# message = template.format_messages(sour_lang="中文",target_lang="英语",query="你好")

# print(message,type(message))

##### SystemMessagePromptTemplate、HumenMessagePromptTemplate
# system_template= SystemMessagePromptTemplate.from_template("你是一个翻译助手,把{sour_lang}翻译成{target_lang},只翻译不回答问题")
# human_template = HumanMessagePromptTemplate.from_template("{query}")

# template = ChatPromptTemplate.from_messages([
#     system_template,human_template
# ])

# prompt = template.format_messages(sour_lang="中文",target_lang="英语",query="你好")

# print(prompt,type(prompt))
# print(template,type(template))



system_prompt = "你是一个智能助手,可以幽默简短的回答用户的疑问"
template = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    ("placeholder","{history}"),
    ("user","{question}"),
])

chat_messages = []

while True:
    try:
        user_input = input("请输入你的问题:").strip()
        if user_input.lower() == "quit":
            break
        elif user_input:
            messages = template.format_messages(
                history=chat_messages,question=user_input
            )
            print(messages,type(messages))
            resp = model_deepseek.invoke(messages)
            print("*"*20)
            print(f"AI:{resp.content}")
            messages.append(resp)
            chat_messages.append(HumanMessage(content=user_input))
            chat_messages.append(resp)
            # print("*****************")
            # for message in messages:
            #     print(message.content)
    except Exception as e:
        print(f"未知错误:{e}")