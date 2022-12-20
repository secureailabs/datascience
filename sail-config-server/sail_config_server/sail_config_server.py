import json
import os

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/get_config")
async def get_config(config_id: str):
    path_dir_config = os.environ["PATH_DIR_CONFIG"]
    path_file_config = os.path.join(path_dir_config, config_id + ".json")
    if not os.path.isfile(path_file_config):
        raise HTTPException(status_code=500, detail="No config for config_id: {config_id}")
    try:
        with open(path_dir_config, "r") as file:
            config = json.load(file)
        return config
    except:
        raise HTTPException(status_code=500, detail="Could not read config for config_id: {config_id}")


@app.post("/set_config")
async def set_config(config_id: str, config: dict):
    path_dir_config = os.environ["PATH_DIR_CONFIG"]
    path_file_config = os.path.join(path_dir_config, config_id + ".json")
    with open(path_dir_config, "r") as file:
        json.dump(config, file)
