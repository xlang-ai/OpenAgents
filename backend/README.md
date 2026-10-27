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

**5.3 Python execution configuration**

See [Python execution trust boundary](#python-execution-trust-boundary) below before enabling generated Python. The default is now `disabled`, including when using the setup script.
</details>



---
## 🎉🎉Congratulations!

Now you feel free to start the platform on default port 8000, using the following scripts:

```bash
export FLASK_APP=backend.main.py
flask run -p 8000
```

## Python execution trust boundary

**Migration:** Python execution is now **disabled by default**, both from source and in
Compose. Existing deployments that explicitly set `CODE_EXECUTION_MODE=local` must
also acknowledge the risk with `ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=true`; otherwise
startup fails with an explanation. Unknown or empty modes are rejected.

This is a demo/development platform. Neither local mode nor the legacy remote
interpreter is a supported security boundary for hostile, multi-tenant use.
A trusted user can still submit untrusted documents or receive malicious model
output. Treat generated code and every data source that can influence it as code
running with the selected interpreter's privileges.

| Mode | Behavior | Intended use |
| --- | --- | --- |
| `disabled` (default) | Returns a clear tool error without executing generated Python or contacting the interpreter | Start the platform without granting generated Python execution privileges |
| `local` + explicit acknowledgement | Runs IPython inside the Flask process | Trusted, single-user development only |
| `docker` | Sends code to the separately configured interpreter service; never falls back to local execution | Existing operator-managed installations after reviewing isolation |

Disabling generated Python disables PythonCodeBuilder analysis and Python-generated
Echarts/plots. It does not disable the entire Data Agent or certify other features
as safe: SQL execution, file parsing/uploads, plugin tools and web actions retain
their existing behavior and require separate review. A tool failure is returned
through the existing result format so the UI can show why Python is unavailable.

### Trusted local development

From the project root, after the normal dependency/database setup:

```bash
export CODE_EXECUTION_MODE=local
export ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=true
export FLASK_APP=backend.main.py
flask run --host=127.0.0.1 -p 8000
```

Or for Compose (the variables are explicitly forwarded to the backend container):

```bash
CODE_EXECUTION_MODE=local ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=true docker compose up -d
```

Local execution retains imports, uploaded-file access, dataframe analysis and chart
outputs. It also has access to backend credentials, the whole data volume, the
network and a shared IPython namespace. It changes the process working directory
and is not thread-safe. The acknowledgement and startup warning are safeguards
against accidental configuration, **not** restrictions on already-running code.
Do not expose this mode to untrusted users, even if the backend itself is in Docker.

To turn Python execution off again, set `CODE_EXECUTION_MODE=disabled` and restart
(or recreate the Compose backend). Environment changes require a restart.

### Existing remote interpreter deployments

`docker` is the historical name for the HTTP/Jupyter interpreter integration.
It separates generated Python from the Flask process, but is not automatically a
secure sandbox. The legacy example shares the entire `backend-data` volume,
uses a shared service/network, and asks for `SYS_RESOURCE`, `SYS_PTRACE` and
`NET_ADMIN`. The interpreter's own README documents Linux/x86 architecture
constraints in its resource limiter. Do not enable it blindly on macOS/ARM or
assume different kernels provide tenant isolation.

For an existing, reviewed interpreter, configure the backend with:

```bash
export CODE_EXECUTION_MODE=docker
export CODE_INTER_SERVER=127.0.0.1  # hostname only; the client uses HTTP port 8100
export REDIS_SERVER=127.0.0.1
```

When the backend is in Compose, use the service hostname `code_interpreter`
instead of `127.0.0.1`, and deliberately enable/provision that service (the legacy
example remains commented out in `docker-compose.yml`). Mount the intended data
at `/home` as required by that service, and ensure Redis and the backend kernel
publisher are running. Do not pass backend API keys or mount the Docker socket
into the interpreter. Keep port 8100 private. A failed remote execution is an
error; the application does not retry it in the Flask process. Existing remote
queue/HTTP waits are not hardened by this change.

The legacy interpreter and deployment instructions live in
[xlang-code-interpreter](https://github.com/xlang-ai/xlang-code-interpreter).
Its source was reviewed for this change, but its image and OS-level isolation
have not been certified. This is why this patch defaults to **disabled**, rather
than automatically enabling that service or adding an unverified new runtime.

### Before accepting untrusted users or content

The shipped Compose configuration binds frontend and backend ports to
`127.0.0.1`. Loopback binding reduces accidental exposure; it is not authentication,
and local programs, browsers, proxies or tunnels can still reach these ports.
Changing a frontend endpoint does not itself secure a network deployment.

A future supported untrusted execution service needs authenticated/authorized
requests and tenant ownership checks; separate per-tenant/job files and lifetimes;
no backend secrets or shared sensitive mounts; restricted egress and access to
metadata/internal services; enforced CPU, memory, process, disk and time limits;
and a reviewed container/VM security boundary with appropriate kernel controls.
The current shared interpreter should not be advertised as satisfying these
requirements without independent verification.

`check_python_syntax()` only reports syntax errors (skipping IPython line magics).
It does not restrict imports or calls, and AST parsing, deny-lists and model
refusals are not substitutes for isolation. The previous `check_danger_code()`
name and always-safe flag have been removed to avoid implying otherwise.

### Targeted regression checks

The focused suite runs without an LLM key, database or Docker daemon. It loads
the actual evaluator and Flask configuration without their packages' eager
imports of unrelated integrations. Local smoke checks execute real IPython in a
temporary data directory; remote protocol tests mock only Redis/HTTP.

```bash
python -m pip install -r tests/requirements-execution.txt
python -m pytest -q tests/test_python_execution_policy.py
```

These checks cover opt-in/denial, direct evaluator entry points, no local fallback,
arithmetic, CSV/dataframe operations, chart outputs and failure cleanup. They do
not replace a live full-stack Docker/LLM test or an isolation assessment.
