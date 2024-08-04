"""Tests for `berhoel.helper`."""

import time

from berhoel import helper

__date__ = "2024/08/03 18:29:57 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


def test_swirl(capsys):
    """Test swirler."""
    swirl = helper.swirl()
    for expected in r"\|/-\|":
        next(swirl)
        res = capsys.readouterr()
        assert res.out == f"{expected}\r"


def test_swirl_dots(capsys):
    """Test swirler with (braille) dots."""
    swirl = helper.swirl(helper.SwirlSelect.DOTS)
    for expected in "⠇⡆⣄⣠⢰⠸⠙⠋":
        next(swirl)
        res = capsys.readouterr()
        assert res.out == f"{expected}\r"


def test_count_with_message_1(capsys):
    """Test counter with life message."""
    count = helper.count_with_msg()
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i == j
        assert res.out == f"loop {i + 1} \r"
        if i > 5:
            break


def test_count_with_message_2(capsys):
    """Test counter with life message."""
    count = helper.count_with_msg(start=10)
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i + 10 == j
        assert res.out == f"loop {i + 1} \r"
        if i > 5:
            break


def test_count_with_message_3(capsys):
    """Test counter with life message."""
    count = helper.count_with_msg(msg="msg")
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i == j
        assert res.out == f"msg {i + 1} \r"
        if i > 5:
            break


def test_count_with_message_4(capsys):
    """Test counter with life message."""
    count = helper.count_with_msg("alt", 5)
    for i, j in enumerate(count):
        res = capsys.readouterr()
        assert i + 5 == j
        assert res.out == f"alt {i + 1} \r"
        if i > 5:
            break


def test_process_msg_context(capsys):
    """Test process context."""
    with helper.process_msg_context("do something"):
        res = capsys.readouterr()
        assert res.out == "do something...\r"
    res = capsys.readouterr()
    assert res.out == "do something...done\n"


def test_timed_process_msg_context_1(capsys):
    """Test timed process context."""
    with helper.timed_process_msg_context("do something"):
        res = capsys.readouterr()
        time.sleep(1)
        assert res.out == "do something...\r"
    res = capsys.readouterr()
    assert res.out == "do something...done (0:00:01)\n"


def test_timed_process_msg_context_2(capsys):
    """Test timed process context."""
    with helper.timed_process_msg_context("do something", lambda t: f"{int(t):d}s"):
        res = capsys.readouterr()
        time.sleep(1)
        assert res.out == "do something...\r"
    res = capsys.readouterr()
    assert res.out == "do something...done (1s)\n"
