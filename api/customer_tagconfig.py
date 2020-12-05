import json

import requests

CORPID = 'wwaa7408f7b2a969d9'
CORSECRET = '6r6i1urQJBPURvUyVFmklyZXRN8P409Xn74n1ia6FPk'


class TagConfig:
    def __init__(self):
        self.token = ""

    def get_token(self):
        res = requests.get(
            'https://qyapi.weixin.qq.com/cgi-bin/gettoken',
            params={
                'corpid': CORPID,
                'corpsecret': CORSECRET
            }
        )

        self.token = res.json()['access_token']

    def clear_env(self):
        print("######开始做清理数据啦~~~")
        group_id_list = []
        # 获取插入数据后的tag数据
        res_tag_list = self.get_configlist({"tag_id": []})
        print("#########获取原始数据", json.dumps(res_tag_list.json(), indent=2))
        # 判断一下拿到的数据有没有问题
        assert res_tag_list.status_code == 200
        assert res_tag_list.json()['errcode'] == 0

        # 获取返回数据中的group id
        group_id_l = [{'group_id': group['group_id']} for group in res_tag_list.json()['tag_group']]
        # 将group id转换成数组
        for group_id in group_id_l:
            group_id_list.append(group_id['group_id'])
        print("#####group_id_list is", group_id_list)

        # 如果我的数据本来就是空，那我不做任何处理，否则才会去删除
        if len(group_id_list) == 0:
            print("############列表为空，不做任何处理")
            pass
        else:
            res = requests.post(
                'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag',
                params={'access_token': self.token},
                json={
                    "group_id": group_id_list
                }
            )
            print("#########处理结果", json.dumps(res.json(), indent=2))

    def get_configlist(self, testcase):
        res = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/get_corp_tag_list',
            params={'access_token': self.token},
            json=testcase
        )

        # print(json.dumps(res.json(), indent=2))
        return res

    def add_tag(self, tag_list):
        res = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/add_corp_tag',
            params={'access_token': self.token},
            json=tag_list
        )
        # print(json.dumps(res.json(), indent=2))
        return res

    def del_tag(self, testcases):
        res = requests.post(
            'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/del_corp_tag',
            params={'access_token': self.token},
            json=testcases
        )
        # print(json.dumps(res.json(), indent=2))
        return res
