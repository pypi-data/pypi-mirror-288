import logging
import xarray as xr

# set up the logger and set the logging level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# generate a handler
stream_handler = logging.StreamHandler()
# handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
# set the log level displayed in the handler
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


for dd in [2009100701 + hh for hh in range(0, 1)]:
    mdls = xr.open_dataset(f"./data/fcst_mdl.nus/ZSSTD1/{dd:10d}00",
                          engine="pynus", chunks={"x": 19, "y": 17},)

    print(mdls)
