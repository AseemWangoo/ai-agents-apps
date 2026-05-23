from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

load_dotenv()
model = init_chat_model("gpt-4.1-mini")

message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Describe the contents of this image.",
        },
        {
            "type": "image",
            "url": "https://blog.fyndmyai.com/wp-content/uploads/elementor/thumbs/goal-r773f16o48hda370ud202xtwjzh57b6iko9yfk6w7c.webp",
        },
    ]
)

# message = {
#     "role": "user",
#     "content": [
#         {
#             "type": "text",
#             "text": "Describe the contents of this image.",
#         },
#         {
#             "type": "image",
#             "url": "https://blog.fyndmyai.com/wp-content/uploads/elementor/thumbs/goal-r773f16o48hda370ud202xtwjzh57b6iko9yfk6w7c.webp",
#         },
#     ],
# }


response = model.invoke([message])
print(response.content)
