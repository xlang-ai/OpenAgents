import os
from typing import Any, List, Optional, Tuple, Dict
from pydantic import BaseModel
import requests
import time
import ast

import pandas as pd
from io import StringIO
import redis
from loguru import logger

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.getipython import get_ipython
from IPython.utils.capture import capture_output


# subscribed channels
SUBMIT_EVENT = "job_submitted"
RUNNING_EVENT = "job_started"
COMPLETE_EVENT = "job_completed"
# Error render prefix
ERROR_PREFIX = "[ERROR]: "


def check_danger_code(code):
    code_line = []
    for line in code.split("\n"):
        if not line.startswith("%"):
            code_line.append(line)
    code = "\n".join(code_line)

    def check_imports(code):
        ast_failed = False
        try:
            tree = ast.parse(code)
        except Exception as e:
            ast_failed = str(e)
            return ast_failed
        return ast_failed

    ast_failed = check_imports(code)
    return True, ast_failed, []


class DisplayData(BaseModel):
    """Both display_data and execute_result messages use this format."""

    data: Optional[dict] = None
    metadata: Optional[dict] = None

    @classmethod
    def from_tuple(cls, formatted: Tuple[dict, dict]):
        return cls(data=formatted[0], metadata=formatted[1])

    def to_dict(self) -> Dict:
        return {
            "data": self.data,
            "metadata": self.metadata,
        }


class PythonEvaluator:
    """
    Util class for Python code evaluation.
    """

    name = "Python Evaluator"
    base_url = "http://{0}:8100".format(os.getenv("CODE_INTER_SERVER"))
    r: redis.Redis = redis.Redis(host=os.getenv("REDIS_SERVER"), port=6379, decode_responses=True)

    def __init__(self, code_execution_mode: str = "local", jupyter_kernel_pool: Optional[Any] = None):
        self.code_execution_mode = code_execution_mode
        self.jupyter_kernel_pool = jupyter_kernel_pool

    @staticmethod
    def parse_command(program: str) -> List[str]:
        """patchify the code"""
        program_lines = program.strip().split("\n")
        return program_lines

    def run_program_local(self, program: str, user_id: Optional[str] = "u" * 24):
        """Run python program on the local machine using Ipython shell."""
        is_safe, ast_failed, danger_pcks = check_danger_code(program)
        if ast_failed != False:
            return {
                "success": False,
                "error_message": f"{ERROR_PREFIX}Error Code Parsing, please check code grammar!\n{ast_failed}",
            }
        try:
            # Run code using local ipython shell
            # Change working dir to data directory to load from pretty path
            #   Note! This is not thread safe, only for local use
            os.chdir(os.path.join("backend/data/", user_id))

            shell = InteractiveShell.instance()
            shell.enable_gui = lambda x: False
            with capture_output() as captured:
                ip = get_ipython()
                code = "%matplotlib inline\n" + program  # magic command to display matplotlib plots
                result = ip.run_cell(code)

            # Change working dir to project root
            os.chdir("../../../")

            if result.success:
                return {
                    "success": True,
                    "result": result.result,
                    "stdout": str(captured.stdout),
                    "stderr": str(captured.stderr),
                    "outputs": captured.outputs,
                }
            elif result.error_in_exec is not None:
                return {
                    "success": False,
                    "error_message": f"{ERROR_PREFIX}{str(result.error_in_exec)}",
                    "outputs": captured.outputs,
                }
            else:
                # error_before_exec
                return {
                    "success": False,
                    "error_message": f"{ERROR_PREFIX}{str(result.error_before_exec)}",
                    "outputs": captured.outputs,
                }
        except Exception as e:
            logger.bind(user_id=user_id, msg_head="Python evaluator running error").trace(e)
            import traceback

            traceback.print_exc()
            return {
                "success": False,
                "error_message": f"{ERROR_PREFIX}{str(e)}",
            }

    def _apply_for_kernel(self, kernel_id: Optional[str], user_id: str, chat_id: str):
        """Apply for a kernel in docker to run program."""
        if kernel_id is not None:
            # If kernel id is provided, use it directly
            cur_kid = kernel_id
        else:
            # If kernel id is not provided, apply for a new kernel
            kernel_info = self.jupyter_kernel_pool.get_pool_info_with_id(user_id, chat_id, None)
            cur_kid = kernel_info["kid"] if kernel_info is not None else None
            user_exists = requests.get(f"{self.base_url}/user/status/{user_id}").json()["exists"]

            logger.bind(user_id=user_id, chat_id=chat_id, msg_head="user exists").trace(user_exists)

            if not user_exists:
                response = requests.post(f"{self.base_url}/user/create", json={"username": user_id}).json()

                logger.bind(user_id=user_id, chat_id=chat_id, msg_head="user create").trace(response)

            response = requests.get(f"{self.base_url}/kernel/list/{user_id}").json()
            existing_kernel_list = response["list"]

            logger.bind(user_id=user_id, chat_id=chat_id, msg_head="kernel list").trace(response)

            if cur_kid not in existing_kernel_list:
                response = requests.post(f"{self.base_url}/kernel/create", json={"username": user_id}).json()
                if response["code"] != 0 and response["msg"] == "Too many kernels":
                    # kill oldest kernel
                    oldest_kernel_id = existing_kernel_list[0]
                    response = requests.post(
                        f"{self.base_url}/kernel/stop", json={"username": user_id, "kid": oldest_kernel_id}
                    ).json()

                    logger.bind(user_id=user_id, chat_id=chat_id, msg_head="kill oldest kernel").trace(response)

                    response = requests.post(f"{self.base_url}/kernel/create", json={"username": user_id}).json()
                cur_kid = response["id"]

                logger.bind(user_id=user_id, chat_id=chat_id, msg_head="create kernel id").trace(cur_kid)

                self.jupyter_kernel_pool.set_pool_info_with_id(
                    user_id, chat_id, {"kid": cur_kid, "ktime": time.time()}
                )

        logger.bind(user_id=user_id, chat_id=chat_id, msg_head="current kernel id").trace(cur_kid)

        return cur_kid

    def run_program_docker(
        self,
        program: str,
        kernel_id: Optional[str] = None,
        user_id: Optional[str] = "u" * 24,
        chat_id: Optional[str] = "c" * 24,
    ):
        """Run python program on the docker container(jupyter client)."""
        is_safe, ast_failed, danger_pcks = check_danger_code(program)
        if not is_safe:
            return {
                "success": False,
                "error_message": f"{ERROR_PREFIX}Unsafe Code Detected {str(danger_pcks)}, Execution Denied!",
            }
        elif ast_failed != False:
            return {
                "success": False,
                "error_message": f"{ERROR_PREFIX}Error Code Parsing, please check code grammar!\n{ast_failed}",
            }

        try:
            # Run code using remote docker jupyter kernel
            # Get the running id(i.e., a permission to run program) from redis running queue
            #  otherwise wait until a running_id is available
            p = self.r.pubsub()
            p.subscribe(RUNNING_EVENT)
            self.r.publish(SUBMIT_EVENT, chat_id)
            for message in p.listen():
                # the initial message for each channel is a message with an integer
                if isinstance(message["data"], int):
                    continue
                running_id = message["data"]
                if running_id == chat_id:
                    break
                time.sleep(1)
            # Get kernel id(i.e., the real jupyter kernel to run the program) to execute program
            cur_kid = self._apply_for_kernel(kernel_id, user_id, chat_id)
            # Execute program
            response = requests.post(
                f"{self.base_url}/kernel/exec", json={"username": user_id, "code": program, "kid": cur_kid}
            ).json()
            # Notify Redis that a job has been completed
            self.r.publish(COMPLETE_EVENT, chat_id)

            # Parse jupyter kernel output
            result, stdout, stderr, outputs, displays, error_message = None, "", "", None, [], None
            if response["status"] == "ok":
                output = response.get("output", None)
                if output is not None:
                    for output_dict in output:
                        if output_dict["type"] == "stream":
                            content = output_dict.get("content", None)
                            if content is not None:
                                if content["name"] == "stdout":
                                    stdout = content["text"]
                                if content["name"] == "stderr":
                                    stderr = content["text"]
                        elif output_dict["type"] == "execute_result":
                            content = output_dict.get("content", None)
                            if content is not None:
                                data = content.get("data", None)
                                if data is not None:
                                    if "text/plain" in data and "text/html" in data:
                                        try:
                                            # Try to recover a dataframe
                                            df = pd.read_csv(StringIO(data["text/plain"]))
                                            result = df
                                        except Exception as e:
                                            pass
                                    elif "text/plain" in data:
                                        result = data["text/plain"]
                                    else:
                                        # TODO: If not match any of the above, return the first value
                                        result = list(data.values())[0]
                        elif output_dict["type"] == "display_data":
                            content = output_dict.get("content", None)
                            if content is not None:
                                data = content.get("data", None)
                                metadata = content.get("metadata", None)
                                if data is not None and metadata is not None:
                                    if "image/png" in data:
                                        displays.append(DisplayData.from_tuple((data, metadata)))
                            if displays:
                                outputs = displays
            else:
                return {
                    "success": False,
                    "error_message": f"{ERROR_PREFIX}Error status returned by kernel",
                }
            # Check success status and return
            shell_msg = response["shell"]
            if shell_msg["status"] == "ok":
                return {
                    "success": True,
                    "result": result,
                    "stdout": stdout,
                    "stderr": stderr,
                    "outputs": outputs,
                }
            elif shell_msg["status"] == "error":
                error_message = f"{shell_msg['ename']}: {shell_msg['evalue']}"
                return {"success": False, "error_message": f"{ERROR_PREFIX}{error_message}", "outputs": outputs}
        except Exception as e:
            logger.bind(user_id=user_id, chat_id=chat_id, msg_head="Python evaluator running error").trace(e)
            import traceback

            traceback.print_exc()

            try:
                # Notify Redis that a job has been completed
                self.r.publish(COMPLETE_EVENT, chat_id)
            except:
                pass

            return {
                "success": False,
                "error_message": f"{ERROR_PREFIX}{str(e)}",
            }

    def run(
        self,
        program: str,
        environment: Optional[Any] = None,
        kernel_id: Optional[str] = None,
        user_id: Optional[str] = "u" * 24,
        chat_id: Optional[str] = "c" * 24,
    ) -> Any:
        """run generated code in certain environment"""

        lines_code = self.parse_command(program)
        program = "\n".join(lines_code)
        program = "%matplotlib inline\n" + program  # magic command to display matplotlib plots

        logger.bind(user_id=user_id, chat_id=chat_id, msg_head="Code execution mode").trace(self.code_execution_mode)

        if self.code_execution_mode == "local":
            return self.run_program_local(program, user_id)
        elif self.code_execution_mode == "docker":
            return self.run_program_docker(program, kernel_id, user_id, chat_id)
        else:
            raise ValueError("Invalid code execution mode")
