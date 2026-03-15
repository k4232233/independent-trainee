"""
@Author：haoran.xu
"""
import time

from fastapi import FastAPI, Query, Form, UploadFile, File, Header, Cookie, Request, BackgroundTasks
from fastapi.responses import Response, RedirectResponse, FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from starlette.staticfiles import StaticFiles

app = FastAPI()
# 静态文件服务，手动创建文件夹
app.mount('/static', StaticFiles(directory='static', html=True), name='static')


# 后台任务
# 后台任务在单独的线程中运行，使用后台任务我们可以避免阻塞HTTP请求的处理线程
# 场景：执行较慢的代码逻辑
def demo_background_task():
    for i in range(3):
        print('Background task running...')
        time.sleep(1)


@app.get('/task')
async def task(tasks: BackgroundTasks):
    """
    注入一个 BackgroundTasks 对象并调用它的 add_task() 方法来注册后台任务
    """
    tasks.add_task(demo_background_task)
    return {'message': 'success'}


# 中间件
# FastApi 通过中间件来实现 SpringBoot 中 AOP 的类似逻辑
# 默认就是 /* 全局拦截
@app.middleware('http')
# 1. 请求进入
async def calc_time(request: Request, call_next):
    """
    call_next，是 FastApi 框架约定熟成的参数，一个异步函数
    > 执行请求管道中的下一个环节，当前进入等待
    简单理解：SpringBoot 中的 Filter、拦截器
    """
    # 2. 前置逻辑
    start_time = time.time()
    # 3. 穿透核心
    # 3.1 此时，请求离开了中间件，进入了具体的 如：@app.get('/getuser') 函数。
    response = await call_next(request)
    # 3.2 函数运行完，生成了 response
    # 4. 后置逻辑 来到中间件的下一行
    process_time = time.time() - start_time
    # 5. 修改响应
    response.headers['X-Process-Time'] = str(process_time)
    # 6. 返回
    return response


@app.get('/')
async def root():
    """
    尽量使用原生的的异步并发编程模型开发，提高性能
    async : 异步函数
    不要在异步函数中使用同步阻塞操作，这样会阻塞事件循环，导致并发性能急剧下降
    """
    return {'message': 'Hello,world!'}


# 处理请求，url参数
@app.get('/queryUser')
async def query_user(user_code: int, username: str | None):
    return {'user_code': user_code, 'username': username}


# CamelCase 参数 --> SnakeCase风格
# 查询参数别名
@app.get('/queryUserCase')
async def query_user_case(username: str | None, user_code: int = Query(123456, alias='userCoder')):
    """
    Query是FastAPI提供的用于获取查询参数的函数
    > alias支持传入一个数组，指定多个别名
    """
    return {'user_code': user_code, 'username': username}


# 处理Restful风格的路径参数
@app.get('/user/{user_id:str}')
async def path(user_id: str):
    """路径名要和参数名保持一致"""
    return {'message': user_id}


# 读取请求体(可读性差)
@app.post('/user')
async def add_user(user: dict):
    return {'user': user}


# 封装(good)
class User(BaseModel):
    username: str
    user_code: int
    """
    Field是pydantic提供的类，用于对字段进行额外信息的指定，这里我们使用alias指定了别名。
    此时这个模型在接收和输出JSON数据时，都会采用这个别名。
    """
    user_age: int = Field(alias='userAge')


@app.post('/user/add')
async def user_add(user: User):
    return {'user': user}


# 接收表单请求
@app.post('/setting')
async def setting_user(username: str = Form(), user_code: str = Form(), userAge: int = Form()):
    """
    注意：请求体类型是表单，底层会使用python-multipart库进行处理。
    如果没有，要手动下载

    这里还有个知识点：自动类型转换
    user_code 入参是 str
    User封装的是 int 类型
    """
    user = User(username=username, user_code=user_code, userAge=userAge)
    return user


# 文件上传
@app.post('/upload')
async def upload(file: UploadFile = File()):
    content = await file.read()
    """
    大文件，分块写入
    这里以文本文件演示，其他文件编解码不同
    """
    content_str = content.decode('utf-8')
    return {'size': file.size, 'filename': file.filename, 'content': content_str}


# 所有CamelCase问题，都能指定别名解决


# 读取请求头信息
@app.get('/header')
async def get_head(user_agent: str | None = Header(default=None)):
    return user_agent


# 读取cookie信息
@app.get('/cookie')
async def get_cookie(request: Request, user_id: str | None = Cookie(default=None, alias='userId')):
    """注意
    swagger中设置的cookie只在文档展示，不会像 Header 或 Query 参数那样强制注入到浏览器的请求头中
    原因：swagger 通过 JS 发送 AJAX 请求, 除非当前域名下已存在 cookie，否则不会自动生成

    如需测试：当前域名下，f12 控制台输入 document.cookie = "userId=123456789; path=/"
    """
    print(dict(request.headers))
    return user_id


"""
HTTP 响应
"""


# 返回文本数据
@app.get('/foo')
async def foo():
    return Response(content='hello')


# 返回 JSON 数据
@app.get('/getuser', response_model=User, response_model_by_alias=True)
async def get_user(name: str, age: int, code: int):
    user = User(username=name, userAge=age, user_code=code)
    return user


# 设置 HTTP 状态码
@app.get('/resCode')
async def get_resCode(response: Response):
    response.status_code = 555
    """
    注入 Response 对象设置响应状态码
    """
    return {'message': '服务器错误'}


# 方式2
# return Response(status_code=555)


# 返回 HTTP 重定向
@app.get('/goto')
async def goto():
    return RedirectResponse(url='/foo')


# 输出文件
@app.get('/download_1')
async def download():
    """
    可指定 Content-Disposition 响应头，并使用 filename 属性
    浏览器识别并弹出下载对话框
    """
    return FileResponse(path='C:/Users/haoran.xu/Pictures/Gemini_Generated_Image_xrvhs1xrvhs1xrvh.png',
                        media_type='image/jpeg', filename='image_name')


# 输出数据流
@app.get('/download_2')
async def download():
    async def read_file():
        with open('C:/Users/haoran.xu/Pictures/Gemini_Generated_Image_xrvhs1xrvhs1xrvh.png', mode='rb') as fp:
            chunk = fp.read(1024)
            while chunk:
                yield chunk
                chunk = fp.read(1024)

    return StreamingResponse(read_file(), media_type='image/jpeg')


# SSE 输出
@app.get('/stream')
async def stream():
    async def output_data():
        for i in range(0, 5):
            yield f'data: {i}\n\n'

    return StreamingResponse(output_data(), media_type='text/event-stream')


# 设置响应头信息
@app.get('/setHeader')
async def set_header(r: Response):
    r.headers['JJJ'] = 'TEST'
    return {'message': 'ok'}


# 设置 Cookie
@app.get('/setCookie')
async def set_cookie(response: Response):
    response.set_cookie('token', 'T123456')
    # 删除
    # response.delete_cookie('token')
    return {'message': 'ok'}
