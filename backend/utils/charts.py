import json


def polish_echarts(echarts_str):
    """Polishes the echarts output into prettier format."""
    try:
        option = json.loads(echarts_str)

        # turn numeric axis into str
        category_flag = False
        for idx, series_data in enumerate(option["series"]):
            if series_data["type"] in ["bar", "line"]:
                category_flag = True
                break
        if category_flag:
            option["xAxis"][0]["data"] = [str(_) for _ in option["xAxis"][0]["data"]]
            for idx, series_data in enumerate(option["series"]):
                try:
                    option["series"][idx]["data"] = [[str(_[0]), _[1]] for _ in series_data["data"]]
                except:
                    continue
        for idx, series_data in enumerate(option["series"]):
            option["series"][idx]["label"]["show"] = False
        # set title position
        option["title"][0]["bottom"] = "bottom"
        option["title"][0]["left"] = "center"
        option["tooltip"]["alwaysShowContent"] = False

        return json.dumps(option)
    except Exception as e:
        print(e)
        return echarts_str
