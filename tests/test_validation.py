"""课14第四步：为"标题长度校验"缺陷写测试。

课15 追加了请求级测试；课16 追加等价类/边界值参数化测试。
"""
import pytest

from app import validate_ticket


def test_title_too_long():
    error = validate_ticket("A" * 21, "A101")
    assert error == "标题不能超过20个字符"


def test_post_title_too_long(client):
    """课15：同一规则走真实 HTTP 表单提交，验证路由确实调用了校验"""
    resp = client.post(
        "/tickets/new",
        data={"title": "A" * 21, "room": "A区101", "description": "测试"},
    )
    assert resp.status_code == 400
    assert "标题不能超过20个字符" in resp.data.decode()


# 课16：等价类划分 + 边界值分析
#   有效类 1-20 字：正常标题(4)、A*19、A*20
#   无效类 >20 字 ：A*21、A*100
# 边界卡在 20/21 之间，专门抓 len(title) >= 20 这种"差一个"的写法。
@pytest.mark.parametrize(
    "title,expected",
    [
        ("正常标题", 200),
        ("A" * 19, 200),    # 边界内
        ("A" * 20, 200),    # 恰好上限
        ("A" * 21, 400),    # 越界
        ("A" * 100, 400),   # 无效类代表值
    ],
)
def test_title_boundary(client, title, expected):
    # follow_redirects：合法标题创建成功后会 302 跳回首页，跟随之后才是 200；
    # 非法标题在校验处直接返回 400，不会重定向。
    resp = client.post(
        "/tickets/new",
        data={"title": title, "room": "A区101", "description": "测试"},
        follow_redirects=True,
    )
    assert resp.status_code == expected
