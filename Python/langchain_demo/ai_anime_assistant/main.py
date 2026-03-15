"""
@Author：haoran.xu
"""
import httpx
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from starlette.responses import StreamingResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("anime_assistant")

# 第三方整合模型配置常量
PROXY_URL = "http://10.143.10.132:8000"  # 魔法代理（用国内则设为 None 就行）
API_KEY = "sk-e3bad01c14a40e58be84fa83c6d4e7e8"  # api_key
BASE_URL = "https://apis.iflow.cn/v1"  # endpoint
DEFAULT_MODEL = "qwen3-vl-plus"  # model_id

custom_client = httpx.AsyncClient(
    timeout=30.0,
    proxy=PROXY_URL
)

app = FastAPI(title="Anime Assistant API")

llm: ChatOpenAI = ChatOpenAI(
    model=DEFAULT_MODEL,
    api_key=API_KEY,
    base_url=BASE_URL,
    streaming=True,
    http_async_client=custom_client,
    temperature=0.7
)


class ChatRequest(BaseModel):
    message: str


@app.get("/models")
async def get_models():
    response = await custom_client.get(
        f"{BASE_URL}/models",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )

    if response.status_code == 200:
        # 提取模型数据
        data = response.json()
        # 我们可以只返回 ID 列表，也可以返回完整对象
        model_ids = [m["id"] for m in data.get("data", [])]
        return {
            "status": "success",
            "total": len(model_ids),
            "models": model_ids,
            "raw_data": data.get("data", [])
        }
    else:
        logger.error(f"无法获取模型列表: {response.text}")


async def generate_ai_response(prompt: str):
    chain = llm | StrOutputParser()

    async for chunk in chain.astream([HumanMessage(content=prompt)]):
        yield chunk


@app.post("/chatString")
async def chatString(request: ChatRequest):
    return StreamingResponse(
        generate_ai_response(request.message),
        media_type="text/plain"
    )
