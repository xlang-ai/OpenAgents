# Backend Environment Setup

The backend requires several setup steps, including the conda environment for running, database for storage, and environment variables for configuration.

But don't worry, we have provided a one-click setup script for you to get started quickly, you can simply run:
```bash
backend/setup_script.sh
```
which setups most of the things for you (work for both mac and linux). And then continue from [4. LLM Setup](#llm-setup) for further setup if needed.

Or you can follow README below to setup manually because there may be unexpected errors when running the script, and you can fix them manually step by step.

We recommend you to use conda virtual environments and install the dependencies:

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

For the mac environment, follow the instructions below to install MongoDB.
Assume you have [brew](https://brew.sh) installed in your mac.

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@6.0
brew services start mongodb-community@6.0
```

For the linux environment, install like this:

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

Then create collections in mongodb, ready for coming data!
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
For Mac environment:
```bash
brew services start redis
```
For Linux environment:
```bash
systemctl start redis-server &
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
export MONGO_SERVER=127.0.0.1
```

</details>


<details>
    <summary>
        <h2 id="llm-setup">
            4. LLM Setup
        </h2>
    </summary>

Set your OpenAI key (if you use OpenAI API):
```bash
export OPENAI_API_KEY=<OPENAI_API_KEY>
```
**Note** if you are using [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview) Service, you should choose:
```bash
export OPENAI_API_TYPE=azure
export OPENAI_API_BASE=<AZURE_API_BASE>
export OPENAI_API_VERSION=<AZURE_API_VERSION>
export OPENAI_API_KEY=<AZURE_API_KEY>
```
If you are starting your backend in docker, you should add these environment variables in `docker-compose.yml` as well.

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