from flask import request, jsonify, Response

from backend.api.chat_plugin import plugins
from backend.main import app, api_key_pool
from backend.schemas import DEFAULT_USER_ID

@app.route("/api/tool_list", methods=["POST"])
def get_tool_list() -> Response:
    """parameters:
    {
      user_id: id of the user
    }
    return value:
    [{
        id: id of a plugin,
        name: name of a plugin,
        description: description of the plugin,
        icon: icon of the plugin,
        require_api_key: whether the plugin requires api_key,
        api_key: the api key of the plugin, None if no api key
    }]
    """
    user_id = DEFAULT_USER_ID
    api_key_info = api_key_pool.get_pool_info_with_id(user_id, [])
    tool_list = []
    for plugin in plugins:
        plugin_info = {
            "id": plugin["id"],
            "name": plugin["name"],
            "name_for_human": plugin["name_for_human"],
            "description": plugin["description"],
            "icon": plugin["icon"],
            "require_api_key": plugin["require_api_key"],
        }
        search_plugin = [i for i in api_key_info if i["tool_id"] == plugin["id"]]
        if len(search_plugin) > 0:
            plugin_info["api_key"] = search_plugin[0]["api_key"]
        else:
            plugin_info["api_key"] = None
        tool_list.append(plugin_info)
    return jsonify(tool_list)


@app.route("/api/api_key", methods=["POST"])
def post_tool_api_key() -> Response:
    """parameters:
    {
      user_id: id of the user,
      tool_id: id of the tool,
      tool_name: name of the tool,
      api_key: api_key of the tool
    }
    """
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    tool_id = request_json["tool_id"]
    tool_name = request_json["tool_name"]
    api_key = request_json["api_key"]
    api_key_info = api_key_pool.get_pool_info_with_id(user_id, [])
    flag = False
    for i in api_key_info:
        if i["tool_id"] == tool_id:
            flag = True
            i["api_key"] = api_key
    if not flag:
        api_key_info.append({"tool_id": tool_id, "tool_name": tool_name, "api_key": api_key})
    api_key_pool.set_pool_info_with_id(user_id, api_key_info)
    return Response("Success", status=200)
