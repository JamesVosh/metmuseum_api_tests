import pytest
from models import Object, Message

@pytest.mark.parametrize("o_id", [101152, 48, 467300, 906767, 547392, 294333, 1488, 777707, 832722, 200278])
def test_get_object(client_info, o_id):
    g_test = client_info.get(f"v1/objects/{o_id}")
    assert g_test.status_code == 200

    res_test = Object.model_validate(g_test.json())
    assert res_test.model_dump()["objectID"] == o_id

def test_get_not_found_object(client_info):
    g_test = client_info.get("v1/objects/999999")
    assert g_test.status_code == 404

    res_test = Message.model_validate(g_test.json())
    assert type(res_test.model_dump()["message"]) is str

def test_get_date_error_object(client_info):
    g_test = client_info.get("v1/objects/838793")
    assert g_test.status_code == 200

    res_test = Object.model_validate(g_test.json())
    assert res_test.model_dump()["objectID"] == 838793

    copy_g_test = g_test.json()
    copy_g_test["objectBeginDate"] = 1957
    with pytest.raises(ValueError, match="Год окончания не может быть меньше года начала"):
        Object.model_validate(copy_g_test)

    copy2_g_test = g_test.json()
    copy2_g_test["artistBeginDate"] = "1952"
    with pytest.raises(ValueError, match="Год окончания не может быть меньше года начала"):
        Object.model_validate(copy2_g_test)
