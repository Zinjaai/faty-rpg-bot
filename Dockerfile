FROM python:3.14-slim
# get uv
RUN pip install uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app
# install requirements
COPY pyproject.toml uv.lock /app
RUN uv sync --frozen --no-install-project --no-dev
# install app
COPY . .
RUN uv sync --frozen --no-dev
CMD ["uv", "run", "python", "main.py"]
