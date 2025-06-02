from bisect import bisect_right as bisect
from json import dumps,loads
class SGV():
    def __init__(self):
        self.Data = {}
    def get_zipped_from_source(self, source,min_spacing_time=1):
        """从source中获取数据并压缩"""
        sorted_data = sorted(source, key=lambda x: x["date"])

        # 得到间隔时间
        temp_spacing = [[], []]
        for i in range(1, len(sorted_data)):
            t = sorted_data[i]["date"] - sorted_data[i - 1]["date"]
            if (t in temp_spacing[0]):
                temp_spacing[1][temp_spacing[0].index(t)] += 1
            else:
                temp_spacing[0].append(t)
                temp_spacing[1].append(1)
        max = -1
        max_index = -1
        for i in range(len(temp_spacing[1])):
            if temp_spacing[1][i] > max:
                max = temp_spacing[1][i]
                max_index = i
        spacing = temp_spacing[0][max_index]

        # 压缩数据
        result = {"data":{},"spacing":spacing}
        last = sorted_data[0]["date"]
        result["data"].update({last: [sorted_data[0]["sgv"]]})
        for i in range(len(sorted_data)):
            if sorted_data[i]["date"] - spacing == last:
                last = sorted_data[i]["date"]
                temp = list(result["data"])[-1]
                result["data"][temp] += [sorted_data[i]["sgv"]]
            else:
                if not sorted_data[i]["date"] - last < min_spacing_time * 60000:
                    last = sorted_data[i]["date"]
                    result["data"].update({last: [sorted_data[i]["sgv"]]})
        self.Data = result

    def merge_from_source(self, source, min_spacing_time=1):
        if self.Data == {}:
            self.get_zipped_from_source(source, min_spacing_time)
            return
        sorted_data = sorted(source, key=lambda x: x["date"])
        last = int(list(self.Data["data"].keys())[-1]) + len(list(self.Data["data"].keys())[-1]) * self.Data["spacing"]
        last_group = list(self.Data["data"].keys())[-1]
        for i in range(bisect(sorted_data, last, key=lambda x: x["date"]), len(sorted_data)):
            if sorted_data[i]["date"] - last == self.Data["spacing"]:
                if sorted_data[i]["date"] not in self.Data["data"]:
                    last = sorted_data[i]["date"]
                    self.Data["data"][last_group] += [sorted_data[i]["sgv"]]
            else:
                if not sorted_data[i]["date"] - last < min_spacing_time * 60000:
                    last = sorted_data[i]["date"]
                    last_group = last
                    self.Data["data"].update({last: [sorted_data[i]["sgv"]]})
    def get_a_value(self,number):
        if self.Data == {}:
            return 126
        if number <0:
            if (-number)-1 >= len(self.Data["data"][list(self.Data["data"].keys())[-1]]):
                return None
            return self.Data["data"][list(self.Data["data"].keys())[-1]][number]
        else:
            if number >= len(self.Data["data"][list(self.Data["data"].keys())[-1]].keys()):
                return None
            return self.Data["data"][list(self.Data["data"].keys())[-1]][number]

    def get(self):
        return self.Data
    def clear(self):
        self.Data = {}
    def save_data(self,indent = False):
        if indent:
            return dumps(self.Data,indent=4)
        else:
            return dumps(self.Data)
    def load_data(self,data):
        if type(data) != dict:
            self.Data = loads(data)
        else:
            self.Data = data


