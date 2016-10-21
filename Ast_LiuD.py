# auto generated

from GDL_common import *

class LiuD_main:
    def __init__(self, vlst):
        self.vlst = vlst
    def walkabout(self, visitor):
        return visitor.visit_main(self)

class LiuD_stmt1:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_stmt1(self)

class LiuD_options:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_options(self)

class LiuD_option1:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_option1(self)

class LiuD_state1:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_state1(self)

class LiuD_stmt:
    def __init__(self, s, v):
        self.s = s
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_stmt(self)

class LiuD_stmt_value:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_stmt_value(self)

class LiuD_values_or:
    def __init__(self, slst):
        self.slst = slst
    def walkabout(self, visitor):
        return visitor.visit_values_or(self)

class LiuD_string_or:
    def __init__(self, slst):
        self.slst = slst
    def walkabout(self, visitor):
        return visitor.visit_string_or(self)

class LiuD_series:
    def __init__(self, vlst):
        self.vlst = vlst
    def walkabout(self, visitor):
        return visitor.visit_series(self)

class LiuD_jiap:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
    def walkabout(self, visitor):
        return visitor.visit_jiap(self)

class LiuD_litname:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_litname(self)

class LiuD_litstring:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_litstring(self)

class LiuD_value1:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_value1(self)

class LiuD_enclosed:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_enclosed(self)

class LiuD_value:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_value(self)

class LiuD_itemd:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_itemd(self)

class LiuD_Parser(Parser00):

    def handle_main(self):
        vlst = []
        savpos = self.pos
        while True:
            v = self.handle_stmt1()
            if not v:
                break
            self.skipspace()
            if not self.handle_NEWLINE():
                break
            vlst.append(v)
            savpos = self.pos
            self.skipspace()
        self.restorepos(savpos)
        if not vlst:
            return None
        return LiuD_main(vlst)

    def handle_stmt1(self):
        v = self.handle_options()
        if not v:
            v = self.handle_stmt()
        if not v:
            return None
        return LiuD_stmt1(v)

    def handle_options(self):
        v = self.handle_option1()
        if not v:
            v = self.handle_state1()
        if not v:
            return None
        return LiuD_options(v)

    def handle_option1(self):
        savpos = self.pos
        if not self.handle_str('option.prefix'):
            return None
        self.skipspace()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspace()
        s = self.handle_NAME()
        if not s:
            return self.restorepos(savpos)
        return LiuD_option1(s)

    def handle_state1(self):
        savpos = self.pos
        if not self.handle_str('states.skip'):
            return None
        self.skipspace()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspace()
        s = self.handle_NAME()
        if not s:
            return self.restorepos(savpos)
        return LiuD_state1(s)

    def handle_stmt(self):
        savpos = self.pos
        s = self.handle_NAME()
        if not s:
            return None
        self.skipspace()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspace()
        v = self.handle_stmt_value()
        if not v:
            return self.restorepos(savpos)
        return LiuD_stmt(s, v)

    def handle_stmt_value(self):
        v = self.handle_values_or()
        if not v:
            v = self.handle_string_or()
        if not v:
            v = self.handle_jiap()
        if not v:
            v = self.handle_series()
        if not v:
            return None
        return LiuD_stmt_value(v)

    def handle_values_or(self):
        savpos = self.pos
        slst = []
        s = self.handle_NAME()
        if not s:
            return None
        slst.append(s)
        while True:
            self.skipspace()
            if not self.handle_str('|'):
                break
            self.skipspace()
            s = self.handle_NAME()
            if not s:
                break
            slst.append(s)
            savpos = self.pos
        self.restorepos(savpos)
        if len(slst) < 2:
            return None
        return LiuD_values_or(slst)

    def handle_string_or(self):
        savpos = self.pos
        slst = []
        s = self.handle_STRING()
        if not s:
            return None
        slst.append(s)
        while True:
            self.skipspace()
            if not self.handle_str('|'):
                break
            self.skipspace()
            s = self.handle_STRING()
            if not s:
                break
            slst.append(s)
            savpos = self.pos
        self.restorepos(savpos)
        if len(slst) < 2:
            return None
        return LiuD_string_or(slst)

    def handle_series(self):
        v = self.handle_value()
        if not v:
            return None
        savpos = self.pos
        vlst = [v]
        while True:
            self.skipspace()
            v = self.handle_value()
            if not v:
                break
            vlst.append(v)
            savpos = self.pos
        self.restorepos(savpos)
        return LiuD_series(vlst)

    def handle_jiap(self):
        savpos = self.pos
        s1 = self.handle_NAME()
        if not s1:
            return None
        self.skipspace()
        if not self.handle_str('^+'):
            return self.restorepos(savpos)
        self.skipspace()
        s2 = self.handle_STRING()
        if not s2:
            return self.restorepos(savpos)
        return LiuD_jiap(s1, s2)

    def handle_litname(self):
        s = self.handle_NAME()
        if not s:
            return None
        return LiuD_litname(s)

    def handle_litstring(self):
        s = self.handle_STRING()
        if not s:
            return None
        return LiuD_litstring(s)

    def handle_value1(self):
        v = self.handle_litname()
        if not v:
            v = self.handle_litstring()
        if not v:
            v = self.handle_enclosed()
        if not v:
            return None
        return LiuD_value1(v)

    def handle_enclosed(self):
        savpos = self.pos
        if not self.handle_str('('):
            return None
        self.skipspace()
        v = self.handle_stmt_value()
        if not v:
            return self.restorepos(savpos)
        self.skipspace()
        if not self.handle_str(')'):
            return self.restorepos(savpos)
        return LiuD_enclosed(v)

    def handle_value(self):
        v = self.handle_itemd()
        if not v:
            v = self.handle_value1()
        if not v:
            return None
        return LiuD_value(v)

    def handle_itemd(self):
        savpos = self.pos
        v = self.handle_value1()
        if not v:
            return None
        self.skipspace()
        if not self.handle_str('*'):
            return self.restorepos(savpos)
        return LiuD_itemd(v)
