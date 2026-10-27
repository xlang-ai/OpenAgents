"""Execution-boundary regressions, using real IPython and mocked remote I/O.

Load leaf modules by path: package __init__ files eagerly import unrelated LLM,
database and plugin integrations. No evaluator/policy code is stubbed out.
"""

import ast
import importlib.util
import os
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml

from real_agents.execution_policy import configured_code_execution_mode


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evaluator_module = load_module(
    "execution_policy_test_evaluator", "real_agents/data_agent/evaluation/python_evaluator.py"
)
PythonEvaluator = evaluator_module.PythonEvaluator


@pytest.fixture(autouse=True)
def clean_policy_environment(monkeypatch):
    monkeypatch.delenv("CODE_EXECUTION_MODE", raising=False)
    monkeypatch.delenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION", raising=False)


def load_app():
    return load_module("execution_policy_test_app", "backend/app.py").app


def test_default_flask_and_evaluator_are_disabled():
    assert configured_code_execution_mode() == "disabled"
    assert load_app().config["CODE_EXECUTION_MODE"] == "disabled"
    assert PythonEvaluator().code_execution_mode == "disabled"


@pytest.mark.parametrize("method", ["run", "run_program_local", "run_program_docker"])
def test_disabled_blocks_all_entry_points_without_side_effects(method, tmp_path, monkeypatch):
    marker = tmp_path / "must-not-exist"
    shell = Mock(side_effect=AssertionError("must not create IPython"))
    monkeypatch.setattr(evaluator_module.InteractiveShell, "instance", shell)
    network = Mock(side_effect=AssertionError("must not contact interpreter"))
    monkeypatch.setattr(evaluator_module.requests, "post", network)
    evaluator = PythonEvaluator()
    evaluator.r = Mock()
    result = getattr(evaluator, method)(f"open({str(marker)!r}, 'w').write('executed')")
    assert result["success"] is False
    assert "disabled" in result["error_message"]
    assert not marker.exists()
    shell.assert_not_called()
    network.assert_not_called()
    evaluator.r.pubsub.assert_not_called()


@pytest.mark.parametrize("value", [None, "false", "1", "yes", "TRUE", ""])
def test_local_requires_exact_operator_acknowledgement(value, monkeypatch):
    monkeypatch.setenv("CODE_EXECUTION_MODE", "local")
    if value is not None:
        monkeypatch.setenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION", value)
    with pytest.raises(ValueError, match="ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=true"):
        load_app()
    with pytest.raises(ValueError, match="ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=true"):
        PythonEvaluator("local")


def test_acknowledgement_alone_does_not_enable_execution(monkeypatch):
    monkeypatch.setenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION", "true")
    assert load_app().config["CODE_EXECUTION_MODE"] == "disabled"
    assert PythonEvaluator().run("2 + 2")["success"] is False


@pytest.mark.parametrize("mode", ["", "LOCAL", "locla", "sandbox", " local "])
def test_bad_mode_fails_closed_at_startup_and_constructor(mode, monkeypatch):
    monkeypatch.setenv("CODE_EXECUTION_MODE", mode)
    with pytest.raises(ValueError, match="CODE_EXECUTION_MODE must be"):
        load_app()
    with pytest.raises(ValueError, match="CODE_EXECUTION_MODE must be"):
        PythonEvaluator(mode)


def test_local_startup_emits_privilege_warning(monkeypatch, caplog):
    monkeypatch.setenv("CODE_EXECUTION_MODE", "local")
    monkeypatch.setenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION", "true")
    assert load_app().config["CODE_EXECUTION_MODE"] == "local"
    assert "backend process" in caplog.text
    assert "credentials" in caplog.text


def test_docker_startup_warns_about_isolation(monkeypatch, caplog):
    monkeypatch.setenv("CODE_EXECUTION_MODE", "docker")
    assert load_app().config["CODE_EXECUTION_MODE"] == "docker"
    assert "not a verified sandbox" in caplog.text


def test_direct_local_call_cannot_bypass_docker_policy():
    result = PythonEvaluator("docker").run_program_local("2 + 2")
    assert result["success"] is False
    assert "local execution is not enabled" in result["error_message"]


def test_revoked_local_acknowledgement_blocks_execution(monkeypatch):
    monkeypatch.setenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION", "true")
    evaluator = PythonEvaluator("local")
    monkeypatch.delenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION")
    assert evaluator.run_program_local("2 + 2")["success"] is False
    assert evaluator.run("2 + 2")["success"] is False


@pytest.fixture(scope="module")
def ipython_session():
    # Inline matplotlib caches hooks for the active shell; keep one real shell,
    # as the backend does, rather than replacing it between smoke tests.
    evaluator_module.InteractiveShell.clear_instance()
    yield
    evaluator_module.InteractiveShell.clear_instance()


@pytest.fixture
def trusted_local(monkeypatch, tmp_path, ipython_session):
    monkeypatch.setenv("ALLOW_UNSAFE_LOCAL_CODE_EXECUTION", "true")
    monkeypatch.chdir(tmp_path)
    user_dir = tmp_path / "backend" / "data" / ("u" * 24)
    user_dir.mkdir(parents=True)
    yield PythonEvaluator("local"), user_dir


def test_real_ipython_arithmetic(trusted_local):
    evaluator, _ = trusted_local
    original_cwd = os.getcwd()
    result = evaluator.run("print(sum(range(1, 11)))\n6 * 7")
    assert result["success"] is True, result
    assert "55" in result["stdout"].splitlines()
    assert result["result"] == 42
    assert os.getcwd() == original_cwd


def test_real_ipython_csv_dataframe_and_output_file(trusted_local):
    evaluator, user_dir = trusted_local
    (user_dir / "input.csv").write_text("value\n2\n3\n")
    result = evaluator.run(
        "import pandas as pd\n"
        "df = pd.read_csv('input.csv')\n"
        "df['double'] = df['value'] * 2\n"
        "df.to_csv('output.csv', index=False)\n"
        "df"
    )
    assert result["success"] is True, result
    assert result["result"]["double"].tolist() == [4, 6]
    assert (user_dir / "output.csv").read_text() == "value,double\n2,4\n3,6\n"


def test_real_ipython_chart_output(trusted_local):
    evaluator, _ = trusted_local
    result = evaluator.run("import matplotlib.pyplot as plt\nplt.plot([1, 2], [3, 4])\nplt.show()")
    assert result["success"] is True, result
    assert any("image/png" in output.data for output in result["outputs"])


def test_local_restores_cwd_after_generated_code_changes_it_and_fails(trusted_local):
    evaluator, user_dir = trusted_local
    (user_dir / "nested").mkdir()
    original_cwd = os.getcwd()
    result = evaluator.run("import os\nos.chdir('nested')\nraise RuntimeError('test failure')")
    assert result["success"] is False
    assert "test failure" in result["error_message"]
    assert os.getcwd() == original_cwd


def test_local_restores_cwd_after_shell_setup_failure(trusted_local, monkeypatch):
    evaluator, _ = trusted_local
    original_cwd = os.getcwd()
    monkeypatch.setattr(evaluator_module.InteractiveShell, "instance", Mock(side_effect=RuntimeError("setup")))
    assert evaluator.run("2 + 2")["success"] is False
    assert os.getcwd() == original_cwd


def test_syntax_check_is_not_a_safety_filter():
    assert evaluator_module.check_python_syntax("import os\nprint(os.getcwd())") is None
    assert evaluator_module.check_python_syntax("%matplotlib inline\n2 + 2") is None
    assert evaluator_module.check_python_syntax("if :") is not None


@pytest.fixture
def remote_evaluator(monkeypatch):
    pool = Mock()
    pool.get_pool_info_with_id.return_value = {"kid": "kernel-test"}
    evaluator = PythonEvaluator("docker", jupyter_kernel_pool=pool)
    evaluator.base_url = "http://interpreter.test:8100"
    evaluator.r = Mock()
    evaluator.r.pubsub.return_value.listen.return_value = iter([{"data": 1}, {"data": "chat-test"}])
    monkeypatch.setattr(evaluator_module.requests, "get", Mock(side_effect=[
        Mock(json=Mock(return_value={"exists": True})),
        Mock(json=Mock(return_value={"list": ["kernel-test"]})),
    ]))
    # If any future fallback tries to execute locally, the test must fail.
    evaluator.run_program_local = Mock(side_effect=AssertionError("no local fallback"))
    return evaluator


def test_remote_protocol_and_outputs_are_preserved(remote_evaluator, monkeypatch):
    response = {"status": "ok", "shell": {"status": "ok"}, "output": [
        {"type": "stream", "content": {"name": "stdout", "text": "55\n"}},
        {"type": "execute_result", "content": {"data": {"text/plain": "42"}}},
        {"type": "display_data", "content": {"data": {"image/png": "test-image"}, "metadata": {}}},
    ]}
    post = Mock(return_value=Mock(json=Mock(return_value=response)))
    monkeypatch.setattr(evaluator_module.requests, "post", post)
    result = remote_evaluator.run("6 * 7", user_id="user-test", chat_id="chat-test")
    assert result["success"] is True
    assert result["result"] == "42"
    assert result["stdout"] == "55\n"
    assert result["outputs"][0].data["image/png"] == "test-image"
    assert post.call_args.kwargs["json"] == {
        "username": "user-test", "kid": "kernel-test", "code": "%matplotlib inline\n6 * 7"
    }
    remote_evaluator.run_program_local.assert_not_called()


def test_remote_failure_never_falls_back_to_local(remote_evaluator, monkeypatch):
    monkeypatch.setattr(evaluator_module.requests, "post", Mock(side_effect=ConnectionError("offline")))
    result = remote_evaluator.run("6 * 7", user_id="user-test", chat_id="chat-test")
    assert result["success"] is False
    assert "offline" in result["error_message"]
    remote_evaluator.run_program_local.assert_not_called()


def test_all_internal_defaults_use_disabled_policy():
    # Wiring contract for eager-import modules outside this focused runtime suite.
    paths = [
        "backend/api/chat_copilot.py",
        "real_agents/data_agent/python/base.py",
        "real_agents/data_agent/executors/code_generation_executor.py",
    ]
    for path in paths:
        tree = ast.parse((ROOT / path).read_text())
        defaults = []
        for node in ast.walk(tree):
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.target.id == "code_execution_mode":
                    defaults.append(node.value)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg, default in zip(node.args.args[::-1], node.args.defaults[::-1]):
                    if arg.arg == "code_execution_mode":
                        defaults.append(default)
        assert defaults, path
        assert all(isinstance(d, ast.Name) and d.id == "DEFAULT_CODE_EXECUTION_MODE" for d in defaults), path


def test_compose_safe_defaults_and_explicit_override_wiring():
    config = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
    backend = config["services"]["backend"]
    assert "CODE_EXECUTION_MODE=${CODE_EXECUTION_MODE:-disabled}" in backend["environment"]
    assert "ALLOW_UNSAFE_LOCAL_CODE_EXECUTION=${ALLOW_UNSAFE_LOCAL_CODE_EXECUTION:-false}" in backend["environment"]
    assert backend["ports"] == ["127.0.0.1:8000:8000"]
    assert config["services"]["frontend"]["ports"] == ["127.0.0.1:3000:3000"]
    assert "code_interpreter" not in config["services"]
