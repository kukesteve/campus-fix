"""课14第二步：最简单的 pytest 例子。"""


def test_add():
    assert 1 + 1 == 3  # 故意改错！制造 CI 红灯


def test_sub():
    assert 5 - 3 == 2
