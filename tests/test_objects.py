from models import Objects, Message
from pytest import raises

def test_get_full_list_objects(client_info):
    g_test = client_info.get("v1/objects")
    assert g_test.status_code == 200

    res_test = Objects.model_validate(g_test.json(), context=g_test.url)
    assert type(res_test.model_dump()["total"]) is int

    copy_g_test = g_test.json()
    copy_g_test["total"] = 100000
    with raises(ValueError, match="Количество общедоступных объектов не совпадает с фактическим количеством"):
        Objects.model_validate(copy_g_test, context=g_test.url)

def test_get_not_found_list_objects(client_info):
    g_test = client_info.get("v1/object")
    assert g_test.status_code == 404

    res_test = Message.model_validate(g_test.json())
    assert type(res_test.model_dump()["message"]) is str