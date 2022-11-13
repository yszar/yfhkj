# 引入python版本
FROM python:3.11.0-alpine

# 设置时间
RUN ln -sf /usr/share/zoneinfo/Asia/Beijing/etc/localtime

# 输出时间
RUN echo 'Asia/Beijing' >/etc/timezone

# 设置工作目录
WORKDIR /app

# 复制该文件到工作目录中
COPY ./requirements.txt /app/requirements.txt

# 禁用缓存并批量安装包(后面的链接是利用豆瓣源安装，速度会加快)
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/

# 复制代码到工作目录
COPY ./ /app

# 放开端口
EXPOSE 8080

# 命令行运行，启动uvicorn服务，指定ip和端口(--reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。)
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]