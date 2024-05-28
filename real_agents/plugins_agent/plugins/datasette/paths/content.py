# Refer to Simon's guide: https://simonwillison.net/2023/Mar/24/datasette-chatgpt-plugin/
import json

import requests


def call_api(input_json):
    base_url = "https://datasette.io"
    query_endpoint = "/content.json"

    # Call the API
    response = requests.get(base_url + query_endpoint, params=input_json)

    # Return the JSON response
    if response.status_code == 200:
        return response.json()
    else:
        return {"status_code": response.status_code, "text": response.text}


# input_json = {
#     "sql": "select group_concat(sql, '; ') as sql from sqlite_master",
#     "_shape": "array"
# }
#
# CREATE TABLE [stats] (
#    [package] TEXT,
#    [date] TEXT,
#    [downloads] INTEGER,
#    PRIMARY KEY ([package], [date])
# ); CREATE TABLE [tutorials] (
#    [path] TEXT PRIMARY KEY,
#    [title] TEXT,
#    [body] TEXT
# ); CREATE TABLE [pypi_packages] (
#    [name] TEXT PRIMARY KEY,
#    [summary] TEXT,
#    [classifiers] TEXT,
#    [description] TEXT,
#    [author] TEXT,
#    [author_email] TEXT,
#    [description_content_type] TEXT,
#    [home_page] TEXT,
#    [keywords] TEXT,
#    [license] TEXT,
#    [maintainer] TEXT,
#    [maintainer_email] TEXT,
#    [package_url] TEXT,
#    [platform] TEXT,
#    [project_url] TEXT,
#    [project_urls] TEXT,
#    [release_url] TEXT,
#    [requires_dist] TEXT,
#    [requires_python] TEXT,
#    [version] TEXT,
#    [yanked] INTEGER,
#    [yanked_reason] TEXT
# ); CREATE TABLE [pypi_versions] (
#    [id] TEXT PRIMARY KEY,
#    [package] TEXT REFERENCES [pypi_packages]([name]),
#    [name] TEXT
# ); CREATE TABLE [pypi_releases] (
#    [md5_digest] TEXT PRIMARY KEY,
#    [package] TEXT REFERENCES [pypi_packages]([name]),
#    [version] TEXT REFERENCES [pypi_versions]([id]),
#    [packagetype] TEXT,
#    [filename] TEXT,
#    [comment_text] TEXT,
#    [digests] TEXT,
#    [has_sig] INTEGER,
#    [python_version] TEXT,
#    [requires_python] TEXT,
#    [size] INTEGER,
#    [upload_time] TEXT,
#    [upload_time_iso_8601] TEXT,
#    [url] TEXT,
#    [yanked] INTEGER,
#    [yanked_reason] TEXT
# ); CREATE INDEX [idx_pypi_versions_package]
#     ON [pypi_versions] ([package]); CREATE INDEX [idx_pypi_releases_version]
#     ON [pypi_releases] ([version]); CREATE INDEX [idx_pypi_releases_package]
#     ON [pypi_releases] ([package]); CREATE TABLE [news] (
#    [date] TEXT,
#    [body] TEXT
# ); CREATE TABLE [example_csvs] (
#    [url] TEXT,
#    [name] TEXT,
#    [table_name] TEXT,
#    [source] TEXT,
#    [source_url] TEXT,
#    [about] TEXT,
#    [about_url] TEXT,
#    [description] TEXT
# ); CREATE TABLE [plugin_repos] (
#    [repo] TEXT,
#    [tags] TEXT,
#    [extra_search] TEXT
# ); CREATE TABLE [tool_repos] (
#    [repo] TEXT,
#    [tags] TEXT,
#    [extra_search] TEXT
# );
#
# input_json = {
#     "sql": "select * from [pypi_releases] order by [upload_time] desc limit 1",
#     "_shape": "array"
# }
