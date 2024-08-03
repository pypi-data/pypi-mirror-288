#!/usr/bin/env python3
# coding:utf-8

from . import Parsec
from . import ParsecError, ParsecEof


@Parsec
def one(st):
    return st.next()


def eq(data):
    @Parsec
    def call(st):
        re = st.next()
        if re == data:
            return re
        else:
            raise ParsecError(st, "Expect {0} but got {1}".format(data, re))

    return call


def ne(data):
    @Parsec
    def call(st):
        re = st.next()
        if re != data:
            return re
        else:
            raise ParsecError(st, "Expect not equal {0}".format(data))

    return call


def one_of(data):
    @Parsec
    def call(st):
        re = st.next()
        if re in data:
            return re
        else:
            raise ParsecError(st, "Expect one item of {0} but got {1}".format(data, re))

    return call


def none_of(data):
    @Parsec
    def call(st):
        re = st.next()
        if re in data:
            raise ParsecError(st, "Expect none item of {0} but got {1}".format(data, re))
        else:
            return re

    return call


def pack(data):
    @Parsec
    def call(st):
        return data

    return call


def fail(message):
    @Parsec
    def call(st):
        raise ParsecError(st, message)

    return call


@Parsec
def eof(state):
    re = None
    try:
        re = state.next()
    except ParsecEof:
        return None
    raise ParsecError(state, "Expect eof but got {0}".format(re))
