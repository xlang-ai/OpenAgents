FROM python:3.10.4-slim
WORKDIR /app
COPY backend ./backend
COPY real_agents ./real_agents
RUN set -eux; \
    pip install --no-cache-dir -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple; \
    pip install --no-cache-dir pyecharts -i https://pypi.tuna.tsinghua.edu.cn/simple; \
    savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends git; \
    git clone https://github.com/xlang-ai/instructor-embedding ; \
    cd instructor-embedding ;\
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple; \
    pip install --no-cache-dir InstructorEmbedding; \
    cd .. ;\
    rm -rf instructor-embedding;\
    apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	rm -rf /var/lib/apt/lists/*

ENV VARIABLE_REGISTER_BACKEND=redis \
    MESSAGE_MEMORY_MANAGER_BACKEND=database \
    JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND=database \
    FLASK_APP=backend.main.py
# it is important to use kaggle dataset
ENV KAGGLE_USER="" \
    KAGGLE_KEY="" 
RUN mkdir /root/.kaggle && \
    echo "{\"username\":\"$KAGGLE_USER\",\"key\":\"$KAGGLE_KEY\"}" > /root/.kaggle/kaggle.json && \
    chmod 600 /root/.kaggle/kaggle.json
EXPOSE 8000
CMD ["flask", "run", "-p 8000", "--host=0.0.0.0"]

