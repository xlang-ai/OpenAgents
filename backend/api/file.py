import json
import os
import shutil
from typing import Dict, Any
from flask import Response, jsonify, request, send_file

from backend.app import app
from backend.main import (
    grounding_source_pool,
    logger,
    message_id_register,
    message_pool,
)
from backend.schemas import DEFAULT_USER_ID
from backend.utils.utils import create_personal_folder
from backend.utils.user_conversation_storage import get_user_conversation_storage
from backend.utils.utils import (
    allowed_file,
    get_data_model_cls,
    get_user_and_chat_id_from_request,
    get_user_and_chat_id_from_request_json,
    is_sqlite_file,
    is_table_file,
    is_image_file,
    load_grounding_source,
)
from backend.schemas import INTERNAL, UNFOUND

TABLE_HUMAN_SIDE_FORMAT = "material-react-table"


def _path_tree_for_react_dnd_treeview(tree: list, id_to_path_dict: dict, path: str,
                                      parent: int,
                                      highlighted_files: list = []) -> list:
    """
    {
        "id": 1,
        "parent": 0,
        "droppable": true,
        "text": "Folder 1"
    },
    {
        "id": 2,
        "parent": 1,
        "text": "File 1-1",
        "data": {
            "fileType": "csv",
            "fileSize": "0.5MB"
        }
    },
    """
    for item in os.listdir(path):
        if item.startswith("."):
            continue
        item_path = os.path.join(path, item)
        droppable = os.path.isdir(item_path)
        idx = len(tree) + 1
        tree.append({
            "id": idx,
            "parent": parent,
            "droppable": droppable,
            "text": item,
            "highlight": True if item_path in highlighted_files else False})
        id_to_path_dict[idx] = item_path
        if os.path.isdir(item_path):
            _path_tree_for_react_dnd_treeview(tree, id_to_path_dict, item_path, idx)

    return []

def secure_filename(filename: str) -> str:
    keep_characters = ('.', '_')
    filename = "".join(
        c for c in filename if c.isalnum() or c in keep_characters).rstrip()
    return filename


@app.route("/api/upload", methods=["POST"])
def create_upload_file() -> dict | Response:
    """Uploads a new file."""
    try:
        if "file" not in request.files:
            return {"error": "No file part in the request"}
        file = request.files["file"]
        (user_id, chat_id) = get_user_and_chat_id_from_request(request)
        folder = create_personal_folder(user_id)

        # Check if the file is allowed
        if not allowed_file(str(file.filename)):
            return {"error": "File type not allowed"}

        # Save and read the file
        file.filename = secure_filename(str(file.filename))
        file_path = os.path.join(folder, file.filename)
        file.save(file_path)
        response = {"success": file.filename}

        logger.bind(user_id=user_id, chat_id=chat_id, api="/upload",
                    msg_head="Upload file success").debug(file_path)

        return jsonify(response)
    except Exception as e:
        logger.bind(user_id=user_id, chat_id=chat_id, api="/upload",
                    msg_head="Upload file error").error(str(e))

        return Response(response=None, status=f"{INTERNAL} Upload File Error: {str(e)}")


def _generate_human_side_data_from_file(filename: str, data_model: Any) -> Dict:
    if is_table_file(filename):
        # Determine the format of the human side(frontend) table
        human_side_data = data_model.get_human_side_data(mode="FULL")
        if TABLE_HUMAN_SIDE_FORMAT == "markdown":
            human_side_data = human_side_data.to_markdown(index=False)
            human_side_data_type = "plain"
        elif TABLE_HUMAN_SIDE_FORMAT == "material-react-table":
            columns = list(map(lambda item: {"accessorKey": item, "header": item},
                               human_side_data.columns.tolist()))
            data = human_side_data.fillna("").to_dict(orient="records")
            human_side_data = json.dumps({"columns": columns, "data": data})
            human_side_data_type = "table"
        data = {"success": filename, "content": human_side_data,
                "type": human_side_data_type}
    elif is_sqlite_file(filename):
        data = {"success": filename, "content": filename, "type": "table"}
    elif is_image_file(filename):
        # Determine the format of human side(frontend) image
        human_side_data = data_model.get_human_side_data()
        data = {"success": filename, "content": human_side_data, "type": "image"}
    else:
        return {"error": "Document file type not supported"}
    return data


def _get_file_path_from_node(folder: str, file_node: dict) -> Any:
    path_tree_list: list = []
    id_to_path_dict = {0: folder}
    _path_tree_for_react_dnd_treeview(path_tree_list, id_to_path_dict, folder, 0)
    path = id_to_path_dict[file_node["id"]]
    return path


@app.route("/api/file_system/apply", methods=["POST"])
def apply_to_conversation() -> Response:
    """Applies data to the conversation."""
    try:
        request_json = request.get_json()
        (user_id, chat_id) = get_user_and_chat_id_from_request_json(request_json)
        file_node = request_json["activated_file"]
        parent_message_id = request_json["parent_message_id"]
        folder = create_personal_folder(user_id)

        # Modify the selected grounding sources
        grounding_source_dict = grounding_source_pool.get_pool_info_with_id(user_id,
                                                                            chat_id,
                                                                            default_value={})
        file_path = _get_file_path_from_node(folder, file_node)
        filename = file_node["text"]
        filename_no_ext = os.path.splitext(filename)[0]
        if file_path not in grounding_source_dict:
            data = load_grounding_source(file_path)
            data_model = get_data_model_cls(filename).from_raw_data(
                raw_data=data,
                raw_data_name=filename_no_ext,
                raw_data_path=file_path,
            )
            grounding_source_dict[file_path] = data_model
            # Add uploaded file in chat memory
            message_list = message_pool.get_pool_info_with_id(user_id, chat_id,
                                                              default_value=list())
            llm_side_data = data_model.get_llm_side_data()
            human_message_content = "[User uploaded a file {}]\n{}".format(filename,
                                                                           llm_side_data)
            human_message_id = message_id_register.add_variable(human_message_content)
            message_list.append(
                {
                    "message_id": human_message_id,
                    "parent_message_id": parent_message_id,
                    "message_type": "human_message",
                    "message_content": human_message_content,
                }
            )
            data = _generate_human_side_data_from_file(filename, data_model)
            message_pool.set_pool_info_with_id(user_id, chat_id, message_list)
            grounding_source_pool.set_pool_info_with_id(user_id, chat_id,
                                                        grounding_source_dict)
            # Dump to database
            db = get_user_conversation_storage()
            db_message = {
                "conversation_id": chat_id,
                "user_id": user_id,
                "message_id": human_message_id,
                "parent_message_id": parent_message_id,
                "version_id": 0,
                "role": "user",
                "data_for_human": {
                    "intermediate_steps": [],
                    "final_answer": [
                        {
                            "type": data["type"],
                            "text": data["content"],
                            "final": True,
                        }
                    ],
                },
                "data_for_llm": message_list[-1]["message_content"],
                "raw_data": None,
            }
            db.message.insert_one(db_message)
            response = {
                "success": True,
                "message_id": human_message_id,
                "parent_message_id": parent_message_id,
                "message": "Successfully apply {} to conversation {}".format(filename,
                                                                             chat_id),
                "content": {
                    "intermediate_steps": [],
                    "final_answer": [
                        {
                            "type": data["type"],
                            "text": data["content"],
                            "final": True,
                        }
                    ],
                },
            }

            logger.bind(user_id=user_id, chat_id=chat_id, api="/apply",
                        msg_head="Apply file success").debug(file_path)
            del db_message["data_for_human"]

            return jsonify(response)
        else:
            logger.bind(user_id=user_id, chat_id=chat_id, api="/apply",
                        msg_head="Apply file failed").debug(file_path)

            return jsonify({"success": False,
                            "message": "You have already import {} to the conversation".format(
                                filename)})
    except Exception as e:
        logger.bind(user_id=user_id, chat_id=chat_id, api="/apply",
                    msg_head="Apply file failed").error(file_path)
        import traceback
        traceback.print_exc()

        return Response(response=None,
                        status=f"{INTERNAL} Fail to apply file to chat: {str(e)}")


@app.route("/api/file_system/move", methods=["POST"])
def move_files() -> Response:
    """Moves file from source path from target source."""
    request_json = request.get_json()
    (user_id, chat_id) = get_user_and_chat_id_from_request_json(request_json)
    root_path = create_personal_folder(user_id)
    nodes = request_json["nodes"]
    try:
        if os.path.exists(root_path) and os.path.isdir(root_path):
            current_path_tree_list: list = []
            id_to_path_dict = {0: root_path}
            _path_tree_for_react_dnd_treeview(current_path_tree_list, id_to_path_dict,
                                              root_path, 0)
        for node in nodes:
            old_path = id_to_path_dict[node["id"]]
            new_path = id_to_path_dict[node["parent"]]
            shutil.move(old_path, new_path)

            logger.bind(user_id=user_id, chat_id=chat_id, api="/move",
                        msg_head="Move file success").debug(
                f"from {old_path} to {new_path}"
            )

            return jsonify({"success": True, "message": "File moved successfully"})
    except Exception as e:
        logger.bind(user_id=user_id, chat_id=chat_id, api="/move",
                    msg_head="Move file failed").error(str(e))

        return jsonify({"success": False, "message": str(e)})
    return Response(response=None, status=f"{INTERNAL} Fail to move file")


@app.route("/api/file_system/delete", methods=["POST"])
def delete_files() -> Response:
    """Deletes a file from the filesystem."""
    request_json = request.get_json()
    (user_id, chat_id) = get_user_and_chat_id_from_request_json(request_json)
    root_path = create_personal_folder(user_id)
    node = request_json["node"]
    try:
        if os.path.exists(root_path) and os.path.isdir(root_path):
            current_path_tree_list: list = []
            id_to_path_dict = {0: root_path}
            _path_tree_for_react_dnd_treeview(current_path_tree_list, id_to_path_dict,
                                              root_path, 0)
            path = id_to_path_dict[node["id"]]
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

        logger.bind(user_id=user_id, chat_id=chat_id, api="/delete",
                    msg_head="Delete file success").debug(path)

        return jsonify({"success": True, "message": "File is deleted successfully"})
    except Exception as e:
        logger.bind(user_id=user_id, chat_id=chat_id, api="/delete",
                    msg_head="Delete file failed").error(str(e))

        return Response(response=None,
                        status=f"{INTERNAL} Delete file failed: {str(e)}")


@app.route("/api/file_system/download", methods=["POST"])
def download_files() -> Response:
    """Downloads a file to local."""
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    root_path = create_personal_folder(user_id)
    node = request_json["node"]

    try:
        if os.path.exists(root_path) and os.path.isdir(root_path):
            current_path_tree_list: list = []
            id_to_path_dict = {0: root_path}
            _path_tree_for_react_dnd_treeview(current_path_tree_list, id_to_path_dict,
                                              root_path, 0)
            path = id_to_path_dict[node["id"]]

            if os.path.exists(path):
                logger.bind(user_id=user_id, api="/download",
                            msg_head="download file success").debug(path)
                return send_file(path, as_attachment=True)

        logger.bind(user_id=user_id, api="/download",
                    msg_head="download file failed").debug(path)
        return Response(response=None,
                        status=f"{INTERNAL} Download file failed: file not correctlt sent")

    except Exception as e:
        print(str(e))
        import traceback
        traceback.print_exc()

        logger.bind(user_id=user_id, api="/download",
                    msg_head="download file failed").error(str(e))

        return Response(response=None,
                        status=f"{INTERNAL} Download file failed: {str(e)}")


def _generate_directory_name(name: str, x:int=0) -> Any:
    dir_name = (name + ("_" + str(x) if x != 0 else "")).strip()
    if not os.path.exists(dir_name):
        return dir_name
    else:
        return _generate_directory_name(name, x + 1)


@app.route("/api/file_system/create_folder", methods=["POST"])
def create_folders() -> Response:
    """Creates a folder in the filesystem."""
    request_json = request.get_json()
    (user_id, chat_id) = get_user_and_chat_id_from_request_json(request_json)
    root_path = create_personal_folder(user_id)
    if os.path.exists(root_path) and os.path.isdir(root_path):
        try:
            new_path = _generate_directory_name(os.path.join(root_path, "Folder"))
            os.makedirs(new_path, exist_ok=False)

            logger.bind(
                user_id=user_id, chat_id=chat_id, api="/create_folder",
                msg_head="Create folder success"
            ).debug(new_path)

            return jsonify({"success": True, "message": "Folder created successfully"})
        except Exception as e:
            logger.bind(user_id=user_id, chat_id=chat_id, api="/create_folder",
                        msg_head="Create folder failed").error(
                str(e)
            )

            return jsonify({"success": False, "message": str(e)})
    else:
        logger.bind(user_id=user_id, chat_id=chat_id, api="/create_folder",
                    msg_head="Create folder failed").error(
            "Root path does not exist."
        )

        return Response(response=None, status=f"{INTERNAL} Root path does not exist")


@app.route("/api/file_system/update", methods=["POST"])
def rename_folder() -> Response:
    """Renames a folder in the filesystem."""
    request_json = request.get_json()
    (user_id, chat_id) = get_user_and_chat_id_from_request_json(request_json)
    root_path = create_personal_folder(user_id)
    node = request_json["node"]
    rename_value = request_json["rename_value"]
    if os.path.exists(root_path) and os.path.isdir(root_path):
        try:
            current_path_tree_list: list = []
            id_to_path_dict = {0: root_path}
            _path_tree_for_react_dnd_treeview(current_path_tree_list, id_to_path_dict,
                                              root_path, 0)
            path = id_to_path_dict[node["id"]]
            new_path = os.path.join(os.path.dirname(path), rename_value)
            shutil.move(path, new_path)

            logger.bind(user_id=user_id, chat_id=chat_id, api="/update",
                        msg_head="Rename folder success").debug(
                f"{path} to {new_path}"
            )

            return jsonify({"success": True, "message": "Folder created successfully"})
        except Exception as e:
            logger.bind(user_id=user_id, chat_id=chat_id, api="/update",
                        msg_head="Rename folder failed").error(str(e))

            return jsonify({"success": False, "message": str(e)})
    else:
        logger.bind(user_id=user_id, chat_id=chat_id, api="/update",
                    msg_head="Rename folder failed").error(
            "Root path does not exist."
        )

        return Response(response=None, status=f"{INTERNAL} Root path does not exist")


@app.route("/api/file_system/get_path_tree", methods=["POST"])
def get_path_tree() -> Response:
    """Gets a file path tree of one file."""
    try:
        request_json = request.get_json()
        user_id = request_json.pop("user_id", DEFAULT_USER_ID)
        if user_id == "":  # front-end may enter empty user_id
            return jsonify([])
        root_path = create_personal_folder(user_id)
        highlighted_files = request_json.get("highlighted_files", [])
        if root_path is None:
            return {"error": "root_path parameter is required", "error_code": 404}
        if os.path.exists(root_path) and os.path.isdir(root_path):
            current_path_tree_list: list = []
            id_to_path_dict = {0: root_path}
            _path_tree_for_react_dnd_treeview(current_path_tree_list, id_to_path_dict,
                                              root_path, 0,
                                              highlighted_files=highlighted_files)
            return jsonify(current_path_tree_list)
        else:
            return Response(response=None, status=f"{UNFOUND} Directory not found")
    except Exception as e:
        return Response(response=None, status=f"{INTERNAL} Directory not found")


@app.route("/api/set_default_examples", methods=["POST"])
def set_default_examples() -> Response:
    """Sets default files for each user."""
    try:
        # Should be called after auth is verified
        request_json = request.get_json()
        user_id = request_json.pop("user_id", DEFAULT_USER_ID)
        root_path = create_personal_folder(user_id)
        example_dir = os.path.dirname(os.path.dirname(app.config["UPLOAD_FOLDER"]))
        example_path = os.path.join(example_dir, "data/examples/")
        if os.path.exists(example_path):
            shutil.copytree(example_path, root_path, dirs_exist_ok=True)
            return jsonify(
                {"success": True, "message": "Default examples are set successfully"})
        else:
            return Response(response=None,
                            status=f"{UNFOUND} Directory not found at {example_dir}")
    except Exception as e:
        return Response(response=None,
                        status=f"{INTERNAL} Fail to Set Default Examples")
