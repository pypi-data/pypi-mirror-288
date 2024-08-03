#!/usr/bin/env python3
# coding:utf-8

from .error import ParsecError
from . import Parsec, pack


def attempt(p):
    @Parsec
    def call(state):
        tran = state.begin()
        try:
            re = p(state)
            state.commit(tran)
            return re
        except Exception as err:
            state.rollback(tran)
            raise err

    return call


def choice(x, y):
    @Parsec
    def call(st):
        prev = st.index
        try:
            return x(st)
        except:
            if st.index == prev:
                return y(st)
            else:
                raise

    return call


def choices(*psc):
    if len(psc) < 2:
        raise Exception("choices need more args than one.")

    @Parsec
    def call(st):
        for p in psc[:-1]:
            prev = st.index
            try:
                return p(st)
            except:
                if st.index != prev:
                    raise
        else:
            return psc[-1](st)

    return call


def many(p):
    return choice(attempt(many1(p)), pack([]))


def many1(p):
    @Parsec
    def call(st):
        re = [p(st)]
        try:
            while True:
                re.append(attempt(p)(st))
        except Exception as err:
            pass
        finally:
            return re

    return call


def skip(p):
    @Parsec
    def call(state):
        while True:
            tran = state.begin()
            try:
                p(state)
                state.commit(tran)
            except ParsecError:
                state.rollback(tran)
                return

    return call


def skip1(p):
    @Parsec
    def call(state):
        p(state)
        skip(p)(state)

    return call


def sep_by(s, p):
    return choice(attempt(sep1_by(s, p)), pack([]))


def sep1_by(s, p):
    @Parsec
    def call(state):
        re = [p(state)]
        try:
            while True:
                re.append(attempt(s.then(p))(state))
        except Exception as err:
            pass
        finally:
            return re

    return call


def many_till(p, t):
    @Parsec
    def call(state):
        re = []
        end = attempt(t)
        while True:
            try:
                end(state)
                return re
            except Exception as err:
                re.append(p(state))

    return call


def sep_till(s, p, t):
    @Parsec
    def call(state):
        re = []
        end = attempt(t)
        while True:
            try:
                end(state)
                return re
            except Exception as err:
                re.extend(many(s.then(p))(state))

    return call


def sep1_till(s, p, t):
    @Parsec
    def call(state):
        re = [p(state)]
        end = attempt(t)
        while True:
            try:
                end(state)
                return re
            except Exception as err:
                re.extend(many(s.then(p))(state))

    return call


def between(openp, closep, psc):
    @Parsec
    def call(state):
        openp(state)
        re = psc(state)
        closep(state)
        return re

    return call


def ahead(psc):
    @Parsec
    def call(state):
        tran = state.begin()
        try:
            return psc(state)
        finally:
            state.rollback(tran)

    return call
