from time import sleep
from requests import get
from threading import Thread
from library import *
from os.path import exists
from bisect import bisect
from datetime import datetime


def get_config():
    global config
    if exists("./config.json"):
        config = load_config("./config.json")
    else:
        config = {
            "gui":{
            "low_line" : 72,
            "high_line" : 180,
            "color_scheme" : 0,
            "unit" : 1,
            "max":270,
            "NS-url": ""
        },
            "time_range":6,
            "SGV":{}
        }
        save_config("./config.json", config)


def one_refresh():
    global app,sgv,config
    last_value = sgv.get_a_value(-1)
    second_last_value = sgv.get_a_value(-2)
    if config["gui"]["unit"] == 0:
        app.update_values(last_value)
    else:
        app.update_values(format(last_value / 18, ".1f"))

    if second_last_value == None:
        app.update_direction("→")
    else:
        if last_value - second_last_value > 5:
            if last_value - second_last_value > 9:
                if last_value - second_last_value > 18:
                    if last_value - second_last_value > 27:
                        app.update_direction("↑↑↑")
                    else:
                        app.update_direction("↑↑")
                else:
                    app.update_direction("↑")
            else:
                app.update_direction("↗")
        elif last_value - second_last_value < -5:
            if last_value - second_last_value < -9:
                if last_value - second_last_value < -18:
                    if last_value - second_last_value < -27:
                        app.update_direction("↓↓↓")
                    else:
                        app.update_direction("↓↓")
                else:
                    app.update_direction("↓")
            else:
                app.update_direction("↘")
        else:
            app.update_direction("→")
    height_unit = 60 / config["gui"]["max"]
    weight_unit = float(format(200 / (60*config["time_range"]),".8f"))
    dots = []
    percent_cnt = [0,0,0]
    sgv_data = sgv.Data
    now = int(datetime.now().timestamp()*1000-60)
    first_group = bisect(list(sgv_data["data"].keys()),now-60*60000*config["time_range"],key=lambda x: int(x))-1
    for i in list(sgv_data["data"].keys())[first_group:]:
        last = int(i)-sgv_data["spacing"]
        print(i)

        for j in sgv_data["data"][i]:
            last+=sgv_data["spacing"]
            if last > now-60*60000*config["time_range"]:
                if j > config["gui"]["high_line"]:
                    percent_cnt[0] += 1
                elif j < config["gui"]["low_line"]:
                    percent_cnt[2] += 1
                else:
                    percent_cnt[1] += 1
                w = float(format((now-last)/60000*weight_unit,".3f"))
                h = float(format(j*height_unit,".3f"))
                if 0<=w<=200 and 0<=h<=60:
                    dots.append((w, h))

    app.update_dots(dots)
    dot_sum = percent_cnt[0]+percent_cnt[1]+percent_cnt[2]
    t_high = float(format(percent_cnt[0]/dot_sum*100,".1f"))
    t_low = float(format(percent_cnt[2]/dot_sum*100,".1f"))
    t_range = float(format(100-t_high-t_low,".1f"))
    app.update_percent([t_high,t_range,t_low])
def refresh():
    global app,config,sgv
    sgv = SGV()
    sgv.load_data(config["SGV"])
    try:
        sgv.merge_from_source(get(config["gui"]["NS-url"]).json())
    except Exception as e:
        pass
    config["SGV"] = sgv.get()
    save_configs()
    while True:
        one_refresh()
        sleep(2*60)

def save_configs():
    global config,app
    config["gui"].update(app.get_settings())
    save_config("./config.json", config)
    one_refresh()



def time_range_change(serial_number):
    global app,config
    if serial_number == 0:
        config["time_range"] = 1
    elif serial_number == 1:
        config["time_range"] = 6
    elif serial_number == 2:
        config["time_range"] = 12
    else:
        config["time_range"] = 24
    save_configs()

if __name__ == '__main__':
    config = {}
    get_config()
    app = GUI()
    app.set_button_check(time_range_change)
    app.update_settings(config["gui"])
    refresh_thread = Thread(target=refresh)
    refresh_thread.daemon = True
    refresh_thread.start()
    app.set_save_setting(save_configs)
    app.run()
