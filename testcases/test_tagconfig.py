from api.customer_tagconfig import TagConfig


class TestTagconfig:
    def test_list_tag(self):
        assert TagConfig().get_configlist().status_code == 200
        assert TagConfig().get_configlist().json()['errcode'] == 0

    def test_add_tag(self):
        assert TagConfig().add_tag().status_code == 200
        assert TagConfig().add_tag().json()['errcode'] == 0

    def test_add_fail(self):
        pass

    def test_del_tag(self):
        assert TagConfig().del_tag().status_code == 200
        assert TagConfig().del_tag().json()['errcode'] == 0