#!/usr/bin/env  python3
# -*- coding: utf8 -*-

import json

class json_test :
    def read_insp_config_json(self, insp_type_str) :
        with open("inspection_config.json", "r") as st_json:
            try :
                json_load = json.load(st_json)
                print(json_load.keys())
                insp_config_json_dic = json_load[insp_type_str]
                return insp_config_json_dic
            except :
                print("Inspection type is not exist in json file")
                return None
        return None


print("ddd")
insp_config_json_dic = json_test().read_insp_config_json('marking')
print(insp_config_json_dic['K'])