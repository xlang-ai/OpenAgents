# Backend Environment Setup

We recommend you to using conda virtual environments and install the dependencies:

```bash
conda create -n openagents python=3.10
conda activate openagents
pip install -r backend/requirements.txt
```

---

As a systematic demo including backend and frontend, we need persistent data management. Here we use MongoDB as the database and Redis as the cache. To setup the database, follow the instructions below:

<details>
    <summary>
        <h2>
            1. MongoDB setup
        </h2>
    </summary>

For the mac environment, following the instructions below to install MongoDB.
Assume you have [brew](https://brew.sh) installed in your mac.

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@6.0
```


Start the mongodb

```bash
brew services start mongodb-community@6.0
```


Create collections.
```bash
mongosh
> use xlang
> db.createCollection("user")
> db.createCollection("message")
> db.createCollection("conversation")
> db.createCollection("folder")
> show collections
```
</details>


<details>
    <summary>
        <h2>
            2. Redis Setup
        </h2>
    </summary>

For MAC environment:
```bash
brew install redis
```

For Linux environment:
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```

To start redis:
For Linux environment:
```bash
systemctl start redis-server &
```
For Mac environment:
```bash
brew services start redis
```
</details>


<details>
    <summary>
        <h2>
            3. Environment Variables
        </h2>
    </summary>
Set these environment variables in your terminal to use redis & database, otherwise just stored in python global variables.
The max redis memory is now set to 500MB, when the memory is full, LRU data will be removed.
Redis serves as cache, the persistent data will be stored in MongoDB and will be retrieved when cache miss.

```bash
export VARIABLE_REGISTER_BACKEND=redis
export MESSAGE_MEMORY_MANAGER_BACKEND=database
export JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND=database
```

</details>


<details>
    <summary>
        <h2>
            4. LLM Setup
        </h2>
    </summary>

Set your OpenAI key (if you use OpenAI API):
```bash
export OPENAI_API_KEY=<OPENAI_API_KEY>
```

Set your Anthropic key (if you use Anthropic API):
```bash
export ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>
```

</details>



<details>
    <summary>
        <h2>
            5. Others (Optional)
        </h2>
    </summary>

**5.1 Kaggle Setup for Kaggle Search Tool (Necessary if you use KaggleSearchTool in data agent)**

Please follow [Kaggle Public API page](https://www.kaggle.com/docs/api#installation) and save your API token to your device, which should be save in `~/.kaggle/kaggle.json`.

**5.2 Auto Tool Selection (Necessary if you use "Auto" in plugins agent)**

We also have auto tool selection for plugin system, to use, you can set up the environment use the following commands:

```bash
git clone https://github.com/xlang-ai/instructor-embedding
cd instructor-embedding
pip install -r requirements.txt
pip install InstructorEmbedding
cd ..
```

**5.3 Code Execution Docker (Necessary if you want the code executed in sandbox)**

If you want to start sandbox docker instead of on local OS to execute Python programs safely and avoid co-current conflicts caused by multi-users/kernels, follow the instructions below.

First, start the Python code interpreter docker we built for the data agent(see instructions under [code-interpreter-docker](https://github.com/xlang-ai/xlang-code-interpreter)) repository. The default docker port is `localhost:8100`.
```bash
docker pull xlanglab/xlang-code-interpreter-python
docker run -d --rm \
    --name codeint \
    --env-file real_agents/data_agent/.code_interpreter_docker_env \
    --mount type=bind,source=<PATH_TO_PROJECT>/backend/data,target=/home \
    -p 8100:8100 \
    --ip=10.1.1.2 \
    --cap-add SYS_RESOURCE \
    --cap-add SYS_PTRACE \
    --cap-add NET_ADMIN \
    xlanglab/xlang-code-interpreter-python
```

Next, set code execution mode to docker ("local" by default):
```bash
export CODE_EXECUTION_MODE="docker"
```
</details>



---
## 🎉🎉Congratulations!

Now you feel free to start the platform on default port 8000, using the following scripts:

```bash
export FLASK_APP=backend.main.py
flask run -p 8000
```