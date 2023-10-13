import os
from flask import request, Response
from kaggle.api.kaggle_api_extended import KaggleApi

from backend.app import app
from backend.utils.utils import create_personal_folder
from backend.schemas import UNFOUND, INTERNAL, DEFAULT_USER_ID

api = KaggleApi()
api.authenticate()


@app.route("/api/kaggle/download_dataset", methods=["POST"])
def kaggle_dataset_download() -> dict | Response:
    """Use Kaggle-api to connect. """
    request_json = request.get_json()
    user_id = request_json.pop("user_id", DEFAULT_USER_ID)
    url = request_json["url"]
    if url.startswith("http"):
        return {"success": False,
                "message": "Please remove the http in your submitted URL."}
    kaggle_dataset_id = url.replace("www.kaggle.com/datasets/", "")
    if not kaggle_dataset_id:
        return {"success": False, "message": "Please input a valid Kaggle dataset URL."}
    root_path = create_personal_folder(user_id)
    if os.path.exists(root_path) and os.path.isdir(root_path):
        try:
            path = os.path.join(root_path, kaggle_dataset_id)
            api.dataset_download_files(kaggle_dataset_id, path=path, unzip=True)
            return {"success": True, "message": "Download {} successfully.",
                    "data_path": path}
        except Exception as e:
            return Response(response=None,
                            status=f"{INTERNAL} Error Downloading, please try another datasets")
    else:
        return Response(response=None, status=f"{UNFOUND} Missing User folder")
