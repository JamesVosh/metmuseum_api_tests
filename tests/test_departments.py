from models import Departments, Message

def test_get_departments(client_info):
    g_test = client_info.get("v1/departments")
    assert g_test.status_code == 200

    res_test = Departments.model_validate(g_test.json())
    for i in range(0, len(res_test.model_dump()["departments"])):
        assert res_test.model_dump()["departments"][i]["departmentId"] > 0
        assert type(res_test.model_dump()["departments"][i]["displayName"]) is str

def test_get_not_found_departments(client_info):
    g_test = client_info.get("v1/department")
    assert g_test.status_code == 404

    res_test = Message.model_validate(g_test.json())
    assert type(res_test.model_dump()["message"]) is str
