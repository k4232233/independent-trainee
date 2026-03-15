"""
@Author：haoran.xu
"""
import asyncio

from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，开发环境可以这样设置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建路由分组
demo_router = APIRouter()


# 创建路由
# @app.get('/')
# async def root():
#     return {'message': 'Hello,World!'}


# 路径参数
@app.get('/user/{user_id:str}')
async def getUserID_str(user_id: str):
    return {'message': user_id}


@app.get('/user/{user_id:int}')
async def getUserID_int(user_id: int):
    return {'message': user_id}


# 匹配多级路径
# @app.get('/{path:path}')
# async def Paths(path: str):
#     return {'message': path}


@demo_router.get('/')
async def get_router_demo():
    """基于路由分组创建的处理函数"""
    return {'message': 'router_demo_test'}


# 注册路由分组到app对象
"""注册路由分组必须在定义路由之后进行，否则处理函数的无法生效的"""
app.include_router(demo_router, prefix='/router_demo')


# 支持HTTP协议中的所有方法
# 使用装饰器就行
@app.get('/')
async def handle_get():
    return {'message': 'GET'}


@app.post('/')
async def handle_post():
    return {'message': 'POST'}


"""
api文档地址
swagger: 127.0.0.1:{PID}/docs (首选)
redoc: 127.0.0.1:{PID}/redoc
"""


# SSE: 它是一个长连接，且发送的数据必须遵循 'data: 内容\n\n'的特定格式。
async def ai_response_generator():
    text = '你好！我是豆包，很高兴为你服务。'

    for char in text:
        await asyncio.sleep(0.05)  # 模拟 AI 思考和网络延迟
        # == 重点 == SSE 协议要求格式必须是 "data: <content>\n\n"
        yield f'data: {char}\n\n'


# sse 连接
@app.get('/sse')
async def sse_get():
    # media_type 必须设置为 text/event-stream
    return StreamingResponse(ai_response_generator(), media_type="text/event-stream",
                             headers={
                                 'Connection': 'keep-alive',
                                 'Cache-Control': 'no-cache'
                             })
    # 这当访问 /static 时，前端会 SSE 请求 /sse. 出现了 CORS 错误。
    # 开发环境，为了解决跨域问题，我们在前面中间件中配置允许访问
    # 注意：生产环境用 Nginx 反向代理就行
