"""The .py file to control the plugin we use in the chatbot"""
import os
from enum import Enum

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class PluginName(str, Enum):
    """
    Enum class for plugin names
    each name is a plugin name 🔌 , each value is the folder name 📁 of the plugin
    """
    KLARNA = "klarna"
    ZAPIER = "zapier"
    COURSERA = "Coursera"
    JOBSEARCH = "jobsearch"
    SHOW_ME = "show_me"
    SPEAK = "speak"
    CREATE_QR_CODE = "create_qr_code"
    MAPS = "maps"
    ASKYOURPDF = "askyourpdf"
    OUTSCHOOL = "Outschool"
    NBA_STATS = "nba_stats"
    WOLFRAM = "wolfram"
    WEB_SCRAPER = "web_scraper"
    DREAMINTERPRETER = "DreamInterpreter"
    BIZTOC = "biztoc"
    XWEATHER = "XWeather"
