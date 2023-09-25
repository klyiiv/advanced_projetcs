from yandex_testing_lesson import reverse
import pytest


def test_nothing():
    assert reverse('') == ''


def test_len1():
    assert reverse('f') == 'f'


def test_len_more_1():
    assert reverse('faf') == 'faf'


def test_len_more_1_nepalindrom():
    assert reverse('fact') == 'tcaf'


def test_exception():
    with pytest.raises(TypeError):
        reverse(1)


def test_exception1():
    with pytest.raises(TypeError):
        reverse([1, 2, 3])


if __name__ == '__main__':
    pytest.main()
