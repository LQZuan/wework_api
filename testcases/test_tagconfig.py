import json

import pytest
import yaml

from api.customer_tagconfig import TagConfig


class TestTagconfig:

    def setup_class(self):
        self.tagConfig = TagConfig()
        # 获取token
        self.tagConfig.get_token()
        # 数据清理
        self.tagConfig.clear_env()

    # 用yaml来作为数据驱动
    """
    test_list_tag:
    case1:带tagid查询
    case2:tagid为空查询
    """

    @pytest.mark.parametrize("testcase", yaml.safe_load(open("cases/get.yaml", encoding="utf-8")).values())
    def test_list_tag(self, testcase):
        res = self.tagConfig.get_configlist(testcase)
        assert res.status_code == 200
        assert res.json()['errcode'] == 0

    """
    test_add_tag:
    case1:只带tag.name
    case2:tag.name长度为30,并添加到已存在的标签组
    case3:带上所有非必须optional
    case4:group.name长度为30
    case5:order/tag.order为0
    case6:order/tag.order为2^32
    """

    @pytest.mark.parametrize("tag_list", yaml.safe_load(open("cases/add_tag.yaml", encoding="utf-8")).values())
    def test_add_tag(self, tag_list):
        # self.test_flag = 0
        res = self.tagConfig.add_tag(tag_list)
        assert res.status_code == 200
        assert res.json()['errcode'] == 0

        # 获取插入数据后的tag数据
        res_list = self.tagConfig.get_configlist({"tag_id": []})
        assert res_list.status_code == 200
        assert res_list.json()['errcode'] == 0

        # 获取add的tag name list
        expect_list = [{'name': tag['name']} for tag in tag_list['tag']]

        group = [group for group in res_list.json()['tag_group'] if group['group_name'] == tag_list['group_name']][0]
        tags = [{'name': tag['name']} for tag in group['tag']]

        # 断言插入的组名是否存在
        assert group['group_name'] == tag_list['group_name']
        # 断言插入的tag name是否存在
        for item in expect_list:
            assert (item in tags)

    """
    test_add_fail:
    case1:tag.name长度>30
    case2:group.name长度>30
    case3:tag.name为空
    case4:group.name为空
    case5:order边界值<0
    case6:order边界值>2^32
    """

    @pytest.mark.parametrize("testcases", yaml.safe_load(open("cases/add_exception.yaml", encoding="utf-8")).values())
    def test_add_fail(self, testcases):
        res = self.tagConfig.add_tag(testcases)
        print("#########获取原始数据", json.dumps(res.json(), indent=2))
        assert res.status_code == 200
        assert res.json()['errcode'] != 0

    """
    test_del_tag:
    case1:json只带tagid
    case2:json只带groupid
    case3:json带tagid和groupid
    """

    @pytest.mark.parametrize("testcases", yaml.safe_load(open("./cases/delete.yaml", encoding="utf-8")).values())
    def test_del_tag(self, testcases):
        res = self.tagConfig.del_tag(testcases)
        assert res.status_code == 200
        assert res.json()['errcode'] == 0

        # 获取插入数据后的tag数据
        res_tag_list = self.tagConfig.get_configlist({"tag_id": []})
        print(json.dumps(res_tag_list.json(), indent=2))
        assert res_tag_list.status_code == 200
        assert res_tag_list.json()['errcode'] == 0

        # 获取返回数据中的id
        group_id_list = [{'group_id': group['group_id']} for group in res_tag_list.json()['tag_group']]
        tag_id_list = [{'id': tag['id']} for tag_group in res_tag_list.json()['tag_group'] for tag in tag_group['tag']]

        if dict(testcases).keys() == 'tag_id':
            assert (testcases not in tag_id_list)
        elif dict(testcases).keys() == 'group_id':
            assert (testcases not in group_id_list)

    """
    case1:del一个不存在的tag.id
    case2:del一个不存在的group.id
    """
    @pytest.mark.parametrize("testcases", yaml.safe_load(open("cases/del_exception.yaml", encoding="utf-8")).values())
    def test_del_fail(self, testcases):
        res = self.tagConfig.add_tag(testcases)
        print("#########获取原始数据", json.dumps(res.json(), indent=2))
        assert res.status_code == 200
        assert res.json()['errcode'] != 0