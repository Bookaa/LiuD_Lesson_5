# auto generated

from GDL_common import *

class GDL01_main:
    def __init__(self, vlst):
        self.vlst = vlst
    def walkabout(self, visitor):
        return visitor.visit_main(self)

class GDL01_stmt:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_stmt(self)

class GDL01_datatype:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_datatype(self)

class GDL01_declare:
    def __init__(self, v, s):
        self.v = v
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_declare(self)

class GDL01_declare_with_value:
    def __init__(self, v1, s, v2):
        self.v1 = v1
        self.s = s
        self.v2 = v2
    def walkabout(self, visitor):
        return visitor.visit_declare_with_value(self)

class GDL01_value0:
    def __init__(self, s):
        self.s = s
    def walkabout(self, visitor):
        return visitor.visit_value0(self)

class GDL01_binvalue:
    def __init__(self, v1, s, v2):
        self.v1 = v1
        self.s = s
        self.v2 = v2
    def walkabout(self, visitor):
        return visitor.visit_binvalue(self)

class GDL01_value:
    def __init__(self, v):
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_value(self)

class GDL01_assign:
    def __init__(self, s, v):
        self.s = s
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_assign(self)

class GDL01_funccall:
    def __init__(self, s, v):
        self.s = s
        self.v = v
    def walkabout(self, visitor):
        return visitor.visit_funccall(self)

class GDL01_Parser(Parser00):

    def handle_main(self):
        v = self.handle_stmt()
        if not v:
            return None
        savpos = self.pos
        vlst = [v]
        while True:
            self.skipspacecrlf()
            v = self.handle_stmt()
            if not v:
                break
            vlst.append(v)
            savpos = self.pos
        self.restorepos(savpos)
        return GDL01_main(vlst)

    def handle_stmt(self):
        v = self.handle_declare_with_value()
        if not v:
            v = self.handle_declare()
        if not v:
            v = self.handle_assign()
        if not v:
            v = self.handle_funccall()
        if not v:
            return None
        return GDL01_stmt(v)

    def handle_datatype(self):
        s = self.handle_str('int')
        if not s:
            s = self.handle_str('long')
        if not s:
            return None
        return GDL01_datatype(s)

    def handle_declare(self):
        savpos = self.pos
        v = self.handle_datatype()
        if not v:
            return None
        self.skipspacecrlf()
        s = self.handle_NAME()
        if not s:
            return self.restorepos(savpos)
        return GDL01_declare(v, s)

    def handle_declare_with_value(self):
        savpos = self.pos
        v1 = self.handle_datatype()
        if not v1:
            return None
        self.skipspacecrlf()
        s = self.handle_NAME()
        if not s:
            return self.restorepos(savpos)
        self.skipspacecrlf()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v2 = self.handle_value()
        if not v2:
            return self.restorepos(savpos)
        return GDL01_declare_with_value(v1, s, v2)

    def handle_value0(self):
        s = self.handle_NUMBER()
        if not s:
            s = self.handle_NAME()
        if not s:
            return None
        return GDL01_value0(s)

    def handle_binvalue(self):
        savpos = self.pos
        v1 = self.handle_value0()
        if not v1:
            return None
        self.skipspacecrlf()
        s = self.handle_str('+')
        if not s:
            s = self.handle_str('-')
        if not s:
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v2 = self.handle_value0()
        if not v2:
            return self.restorepos(savpos)
        return GDL01_binvalue(v1, s, v2)

    def handle_value(self):
        v = self.handle_binvalue()
        if not v:
            v = self.handle_value0()
        if not v:
            return None
        return GDL01_value(v)

    def handle_assign(self):
        savpos = self.pos
        s = self.handle_NAME()
        if not s:
            return None
        self.skipspacecrlf()
        if not self.handle_str('='):
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v = self.handle_value()
        if not v:
            return self.restorepos(savpos)
        return GDL01_assign(s, v)

    def handle_funccall(self):
        savpos = self.pos
        s = self.handle_NAME()
        if not s:
            return None
        self.skipspacecrlf()
        if not self.handle_str('('):
            return self.restorepos(savpos)
        self.skipspacecrlf()
        v = self.handle_value()
        if not v:
            return self.restorepos(savpos)
        self.skipspacecrlf()
        if not self.handle_str(')'):
            return self.restorepos(savpos)
        return GDL01_funccall(s, v)
