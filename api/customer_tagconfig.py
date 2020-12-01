import json

import requests


class TagConfig:
    def get_token(self):
        CORPID = 'wwaa7408f7b2a969d9'
        CORSECRET = '6r6i1urQJBPURvUyVFmklyZXRN8P409Xn74n1ia6FPk'
        res = requests.get(
            'https://qyapi.weixin.qq.com/cgi-bin/gettoken?',
            params={
                'corpid': CORPID,
                'corpsecret': CORSECRET
            }
        )

        # print(json.dumps(res.json(), indent=2))
        return res.json()['access_token']

    def get_configlist(self):
        token = self.get_token()
        res = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list?',
            params={'access_token': token},
            json={
                'tag_id': []
            }
        )

        print(json.dumps(res.json(), indent=2))
        return res

    def add_tag(self):
        token = self.get_token()
        res = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag?',
            params={'access_token': token},
            json={
                "group_name": "group_demo_12011",
                "tag": [{
                        "name": "tag_demo_12011",
                    }
                ]
            }
        )
        print(json.dumps(res.json(), indent=2))
        return res

    def del_tag(self):
        token = self.get_token()
        res = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag?',
            params={'access_token': token},
            json={
                "tag_id": [
                    "TAG_ID_1",
                    "TAG_ID_2"
                ],
                "group_id": [
                    "GROUP_ID_1",
                    "GROUP_ID_2"
                ]
            }
        )
        return res

