from api.customer_tagconfig import TagConfig


class TestTagconfig:
    def test_list_tag(self):
        res = TagConfig().get_configlist()
        assert res.status_code == 200
        assert res.json()['errcode'] == 0

    def test_add_tag(self):
        res = TagConfig().add_tag()
        assert res.status_code == 200
        assert res.json()['errcode'] == 0

    def test_add_fail(self):
        pass

    def test_del_tag(self):
        res = TagConfig().del_tag()
        assert res.status_code == 200
        assert res.json()['errcode'] == 0