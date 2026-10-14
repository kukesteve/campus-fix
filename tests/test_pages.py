"""课15：用 Flask 测试客户端做请求级测试（不开服务器、不碰网络）。"""


def test_index(client):
    """首页应 200，并渲染 CampusFix 标题"""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "CampusFix" in resp.data.decode()


def test_detail(client):
    """详情页能正常渲染指定工单（先造一条，再查 id=1）"""
    client.post(
        "/tickets/new",
        data={"title": "测试详情页", "room": "A区101", "description": "灯坏了"},
    )
    resp = client.get("/tickets/1")
    assert resp.status_code == 200
    body = resp.data.decode()
    assert "测试详情页" in body
    assert "A区101" in body


def test_create(client):
    """POST 创建工单后跟随跳转，首页能看到新工单"""
    resp = client.post(
        "/tickets/new",
        data={"title": "测试工单", "room": "A区101", "description": "灯坏了"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "测试工单" in resp.data.decode()
