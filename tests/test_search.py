from models import Objects, Object ,Message
from pytest import raises

def test_get_search(client_info):
    g_test = client_info.get("v1.1/search")
    assert g_test.status_code == 200

    res_test = Objects.model_validate(g_test.json(), context=g_test.url)
    assert type(res_test.model_dump()["total"]) is int

    copy_g_test = g_test.json()
    copy_g_test["total"] = 10
    with raises(ValueError, match="Количество общедоступных объектов не совпадает с фактическим количеством"):
        Objects.model_validate(copy_g_test, context=g_test.url)

def test_get_not_found_search(client_info):
    g_test = client_info.get("v1.1/searc")
    assert g_test.status_code == 404

    res_test = Message.model_validate(g_test.json())
    assert type(res_test.model_dump()["message"]) is str

def test_get_null_search(client_info):
    g_test = client_info.get("v1.1/search?q=fomaler")
    assert g_test.status_code == 200

    res_test = Objects.model_validate(g_test.json())
    assert type(res_test.model_dump()["total"]) is int

def test_get_search_medium_q(client_info):
    g_test = client_info.get("v1.1/search?medium=Quilts|Silk|Bedcovers&q=quilt")
    assert g_test.status_code == 200

    res_test = Objects.model_validate(g_test.json(), context=g_test.url)
    assert type(res_test.model_dump()["total"]) is int

    count1 = 0
    for i in res_test.model_dump()["objectIDs"]:
        g_test1 = client_info.get(f"v1/objects/{i}")
        res_test1 = Object.model_validate(g_test1.json())
        text1 = res_test1.model_dump()["objectName"] + res_test1.model_dump()["title"] + res_test1.model_dump()["artistDisplayName"]
        medium1 = res_test1.model_dump()["medium"]
        if ("quilt" in text1.lower()) and (("silk" in medium1.lower()) or ("quilts" in medium1.lower()) or ("bedcover" in medium1.lower())):
            count1+=1
    assert count1 == res_test.model_dump()["total"]

def test_get_search_limit(client_info):
    g_test = client_info.get("v1.1/search?q=sunflower&limit=50")
    assert g_test.status_code == 200

    res_test = Objects.model_validate(g_test.json(), context=g_test.url)
    assert type(res_test.model_dump()["total"]) is int

    g_test1 = client_info.get("v1.1/search?q=sunflower&limit=250")
    assert g_test1.status_code == 200

    res_test1 = Objects.model_validate(g_test1.json(), context=g_test1.url)
    assert type(res_test1.model_dump()["total"]) is int

def test_get_search_errors_limit(client_info):
    g_test = client_info.get("v1.1/search?q=sunflower&limit=-50")
    assert g_test.status_code == 200

    res_test = Objects.model_validate(g_test.json(), context=g_test.url)
    assert type(res_test.model_dump()["total"]) is int

    g_test1 = client_info.get("v1.1/search?q=sunflower&limit=10000")
    assert g_test1.status_code == 200

    res_test1 = Objects.model_validate(g_test1.json(), context=g_test1.url)
    assert type(res_test1.model_dump()["total"]) is int

    g_test2 = client_info.get("v1.1/search?q=sunflower&limit=gfgf")
    assert g_test2.status_code == 200

    res_test2 = Objects.model_validate(g_test2.json(), context=g_test2.url)
    assert type(res_test2.model_dump()["total"]) is int

    g_test3 = client_info.get("v1.1/search?q=sunflower&limit=+50")
    assert g_test3.status_code == 200

    res_test3 = Objects.model_validate(g_test3.json(), context=g_test3.url)
    assert type(res_test3.model_dump()["total"]) is int