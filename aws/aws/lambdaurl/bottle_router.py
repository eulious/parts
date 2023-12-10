#!/usr/bin/env python
"""
Bottle is a fast and simple micro-framework for small web applications. It
offers request dispatching (Routes) with URL parameter support, templates,
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and
template engines - all in a single file and with no dependencies other than the
Python Standard Library.

Homepage and documentation: http://bottlepy.org/

Copyright (c) 2009-2018, Marcel Hellkamp.
License: MIT (see LICENSE for details)
"""

import re, warnings
from urllib.parse import urlencode

DEBUG = False


class BottleException(Exception):
    pass


class HTTPError(Exception):
    def __init__(
        self, status=500, body=None, exception=None, traceback=None, **more_headers
    ):
        self.status = status
        self.body = body
        self.exception = exception
        self.traceback = traceback
        self.more_headers = more_headers


class RouteError(BottleException):
    pass


class RouteReset(BottleException):
    pass


class RouterUnknownModeError(RouteError):
    pass


class RouteSyntaxError(RouteError):
    pass


class RouteBuildError(RouteError):
    pass


def debug(mode=True):
    """Change the debug level.
    There is only one debug level supported at the moment."""
    global DEBUG
    if mode:
        warnings.simplefilter("default")
    DEBUG = bool(mode)


def _re_flatten(p):
    """Turn all capturing groups in a regular expression pattern into
    non-capturing groups."""
    if "(" not in p:
        return p
    return re.sub(
        r"(\\*)(\(\?P<[^>]+>|\((?!\?))",
        lambda m: m.group(0) if len(m.group(1)) % 2 else m.group(1) + "(?:",
        p,
    )


def depr(major, minor, cause, fix):
    text = (
        "Warning: Use of deprecated feature or API. (Deprecated in Bottle-%d.%d)\n"
        "Cause: %s\n"
        "Fix: %s\n" % (major, minor, cause, fix)
    )
    if DEBUG == "strict":
        raise DeprecationWarning(text)
    warnings.warn(text, DeprecationWarning, stacklevel=3)
    return DeprecationWarning(text)


class Router(object):
    default_pattern = "[^/]+"
    default_filter = "re"
    _MAX_GROUPS_PER_PATTERN = 99

    def __init__(self, strict=False):
        self.rules = []
        self._groups = {}
        self.builder = {}
        self.static = {}
        self.dyna_routes = {}
        self.dyna_regexes = {}
        self.strict_order = strict
        self.filters = {
            "re": lambda conf: (_re_flatten(conf or self.default_pattern), None, None),
            "int": lambda conf: (r"-?\d+", int, lambda x: str(int(x))),
            "float": lambda conf: (r"-?[\d.]+", float, lambda x: str(float(x))),
            "path": lambda conf: (r".+?", None, None),
        }

    def add_filter(self, name, func):
        self.filters[name] = func

    rule_syntax = re.compile(
        "(\\\\*)"
        "(?:(?::([a-zA-Z_][a-zA-Z_0-9]*)?()(?:#(.*?)#)?)"
        "|(?:<([a-zA-Z_][a-zA-Z_0-9]*)?(?::([a-zA-Z_]*)"
        "(?::((?:\\\\.|[^\\\\>])+)?)?)?>))"
    )

    def _itertokens(self, rule):
        offset, prefix = 0, ""
        for match in self.rule_syntax.finditer(rule):
            prefix += rule[offset : match.start()]
            g = match.groups()
            if g[2] is not None:
                depr(
                    0,
                    13,
                    "Use of old route syntax.",
                    "Use <name> instead of :name in routes.",
                )
            if len(g[0]) % 2:
                prefix += match.group(0)[len(g[0]) :]
                offset = match.end()
                continue
            if prefix:
                yield prefix, None, None
            name, filtr, conf = g[4:7] if g[2] is None else g[1:4]
            yield name, filtr or "default", conf or None
            offset, prefix = match.end(), ""
        if offset <= len(rule) or prefix:
            yield prefix + rule[offset:], None, None

    def add(self, rule, method, target, name=None):
        """Add a new rule or replace the target for an existing rule."""
        anons = 0
        keys = []
        pattern = ""
        filters = []
        builder = []
        is_static = True

        for key, mode, conf in self._itertokens(rule):
            if mode:
                is_static = False
                if mode == "default":
                    mode = self.default_filter
                mask, in_filter, out_filter = self.filters[mode](conf)
                if not key:
                    pattern += "(?:%s)" % mask
                    key = "anon%d" % anons
                    anons += 1
                else:
                    pattern += "(?P<%s>%s)" % (key, mask)
                    keys.append(key)
                if in_filter:
                    filters.append((key, in_filter))
                builder.append((key, out_filter or str))
            elif key:
                pattern += re.escape(key)
                builder.append((None, key))

        self.builder[rule] = builder
        if name:
            self.builder[name] = builder

        if is_static and not self.strict_order:
            self.static.setdefault(method, {})
            self.static[method][self.build(rule)] = (target, None)
            return

        try:
            re_pattern = re.compile("^(%s)$" % pattern)
            re_match = re_pattern.match
        except re.error as e:
            raise RouteSyntaxError("Could not add Route: %s (%s)" % (rule, e))

        if filters:

            def getargs(path):
                url_args = re_match(path).groupdict()
                for name, wildcard_filter in filters:
                    try:
                        url_args[name] = wildcard_filter(url_args[name])
                    except ValueError:
                        raise HTTPError(400, "Path has wrong format.")
                return url_args

        elif re_pattern.groupindex:

            def getargs(path):
                return re_match(path).groupdict()

        else:
            getargs = None

        flatpat = _re_flatten(pattern)
        whole_rule = (rule, flatpat, target, getargs)

        if (flatpat, method) in self._groups:
            if DEBUG:
                msg = "Route <%s %s> overwrites a previously defined route"
                warnings.warn(msg % (method, rule), RuntimeWarning)
            self.dyna_routes[method][self._groups[flatpat, method]] = whole_rule
        else:
            self.dyna_routes.setdefault(method, []).append(whole_rule)
            self._groups[flatpat, method] = len(self.dyna_routes[method]) - 1

        self._compile(method)

    def _compile(self, method):
        all_rules = self.dyna_routes[method]
        comborules = self.dyna_regexes[method] = []
        maxgroups = self._MAX_GROUPS_PER_PATTERN
        for x in range(0, len(all_rules), maxgroups):
            some = all_rules[x : x + maxgroups]
            combined = (flatpat for (_, flatpat, _, _) in some)
            combined = "|".join("(^%s$)" % flatpat for flatpat in combined)
            combined = re.compile(combined).match
            rules = [(target, getargs) for (_, _, target, getargs) in some]
            comborules.append((combined, rules))

    def build(self, _name, *anons, **query):
        """Build an URL by filling the wildcards in a rule."""
        builder = self.builder.get(_name)
        if not builder:
            raise RouteBuildError("No route with that name.", _name)
        try:
            for i, value in enumerate(anons):
                query["anon%d" % i] = value
            url = "".join([f(query.pop(n)) if n else f for (n, f) in builder])
            return url if not query else url + "?" + urlencode(query)
        except KeyError as E:
            raise RouteBuildError("Missing URL argument: %r" % E.args[0])

    def match(self, environ):
        """Return a (target, url_args) tuple or raise HTTPError(400/404/405)."""
        verb = environ["REQUEST_METHOD"].upper()
        path = environ["PATH_INFO"] or "/"

        methods = (
            ("PROXY", "HEAD", "GET", "ANY")
            if verb == "HEAD"
            else ("PROXY", verb, "ANY")
        )

        for method in methods:
            if method in self.static and path in self.static[method]:
                target, getargs = self.static[method][path]
                return target, getargs(path) if getargs else {}
            elif method in self.dyna_regexes:
                for combined, rules in self.dyna_regexes[method]:
                    match = combined(path)
                    if match:
                        target, getargs = rules[match.lastindex - 1]
                        return target, getargs(path) if getargs else {}

        allowed = set([])
        nocheck = set(methods)
        for method in set(self.static) - nocheck:
            if path in self.static[method]:
                allowed.add(method)
        for method in set(self.dyna_regexes) - allowed - nocheck:
            for combined, rules in self.dyna_regexes[method]:
                match = combined(path)
                if match:
                    allowed.add(method)
        if allowed:
            allow_header = ",".join(sorted(allowed))
            raise HTTPError(405, "Method not allowed.", Allow=allow_header)

        raise HTTPError(404, "Not found: " + repr(path))
