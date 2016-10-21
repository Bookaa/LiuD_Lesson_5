# LiuD Lesson Five
# this file is based on LiuD_LessonFour

import Ast_LiuD as GDL
from Ast_LiuD import LiuD_Parser

type_none = 0
type_v = 1
type_s = 2
type_vlst = 3
type_slst = 4

type_to_prefix = {type_v : 'v', type_s : 's', type_vlst : 'vlst', type_slst : 'slst'}

class gen_common:
    def __init__(self, lst):
        self.itemlst = lst
        self.predefines0 = ('NEWLINE',)
        self.predefines = ('NAME', 'STRING', 'NUMBER')
    def get_type0(self, name):
        if name in self.itemlst:
            return type_v
        if name in self.predefines0:
            return type_none
        if name in self.predefines:
            return type_s
        assert False
    def tolst(self, t):
        if t == type_v:
            return type_vlst
        if t == type_s:
            return type_slst
        assert False
    def get_type(self,node):
        if isinstance(node, GDL.LiuD_litstring):
            return type_none
        if isinstance(node, GDL.LiuD_litname):
            name = node.s
            return self.get_type0(name)
        if isinstance(node, GDL.LiuD_value1):
            return self.get_type(node.v)
        if isinstance(node, GDL.LiuD_enclosed):
            return self.get_type(node.v)
        if isinstance(node, GDL.LiuD_value):
            return self.get_type(node.v)
        if isinstance(node, GDL.LiuD_itemd):
            t = self.get_type(node.v)
            return self.tolst(t)
        if isinstance(node, GDL.LiuD_series):
            lst = []
            for v1 in node.vlst:
                t = self.get_type(v1)
                if t == type_none:
                    continue
                lst.append(t)
            assert len(lst) == 1
            assert False
            return type_v
        if isinstance(node, GDL.LiuD_stmt_value):
            lst = self.get_types(node)
            assert len(lst) == 1
            return lst[0]
        assert False
    def get_types(self,node):
        assert isinstance(node, GDL.LiuD_stmt_value)
        lst = []
        v = node.v
        if isinstance(v, GDL.LiuD_series):
            for v1 in v.vlst:
                t = self.get_type(v1)
                if t == type_none:
                    continue
                lst.append(t)
            return lst
        if isinstance(v, GDL.LiuD_values_or):
            typ = None
            for name in v.slst:
                typ1 = self.get_type0(name)
                if typ is None:
                    typ = typ1
                else:
                    assert typ == typ1
            return [typ]
        if isinstance(v, GDL.LiuD_string_or):
            return [type_s]
        if isinstance(v, GDL.LiuD_jiap):
            typ = self.get_type0(v.s1)
            typ2 = self.tolst(typ)
            return [typ2]

        assert False
    def get_prefix(self, types):
        #prefix = [type_to_prefix[b] for b in args]
        if len(types) > 1:
            pass
        lst = []
        for i,typ in enumerate(types):
            s = type_to_prefix[typ]
            if types.count(typ) == 1:
                lst.append(s)
                continue
            n = types[:i+1].count(typ)
            s2 = '%s%d' % (s, n)
            lst.append(s2)
        return lst

class cls_Gen00(gen_common):
    def __init__(self, lst):
        gen_common.__init__(self, lst)
        self.outtxt = ''
        self.prefix = 'XX'
    def visit_main(self, node):
        for v in node.vlst:
            v.walkabout(self)
    def visit_stmt1(self, node):
        node.v.walkabout(self)
    def visit_options(self, node):
        node.v.walkabout(self)
    def visit_option1(self, node):
        s = node.s
        self.prefix = s
    def visit_stmt1(self, node):
        node.v.walkabout(self)

class cls_Gen01(cls_Gen00):
    def __init__(self, lst, prefix):
        cls_Gen00.__init__(self, lst)
        self.prefix = prefix
    def visit_state1(self, node):
        pass
    def visit_stmt(self, node):
        name = node.s
        txt = '''class %s_%s:
    def __init__(self, %s):
'''
        types = self.get_types(node.v)
        prefix = self.get_prefix(types)
        argstr = ', '.join(prefix)
        self.outtxt += txt % (self.prefix, name, argstr)
        for s in prefix:
            self.outtxt += '        self.%s = %s\n' % (s, s)

        txt2 = '''    def walkabout(self, visitor):
        return visitor.visit_%s(self)
''' % name
        self.outtxt += txt2 + '\n'
        #node.v.walkabout(self)

def GetItemList(mod):
    lst = []
    prefix = 'XX'
    for v in mod.vlst:
        if isinstance(v.v, GDL.LiuD_options):
            if isinstance(v.v.v, GDL.LiuD_option1):
                prefix = v.v.v.s
        if isinstance(v.v, GDL.LiuD_stmt):
            name = v.v.s
            lst.append(name)
    return lst, prefix


def Gen01(mod):

    lst, prefix = GetItemList(mod)

    the = cls_Gen01(lst, prefix)
    mod.walkabout(the)
    # print the.outtxt
    return the.outtxt

pos_onlyme = 1
pos_first = 2
pos_end = 3
pos_mid = 4

class cls_Gen02(cls_Gen00):
    def __init__(self, lst, prefix):
        cls_Gen00.__init__(self, lst)
        self.prefix = prefix
        self.outtxt = 'class %s_Parser(Parser00):\n' % prefix
        self.curpos = None
        self.curtyp = None
        self.curtypno = 0
        self.ntab = 2
        self.curskip = 'no'
    def visit_state1(self, node):
        s = node.s
        self.curskip = s
    def skipspace(self):
        if self.curskip == 'no':
            return
        if self.curskip == 'space':
            self.outp('self.skipspace()')
        elif self.curskip == 'crlf':
            self.outp('self.skipspacecrlf()')
    def visit_stmt(self, node):
        name = node.s
        if name == 'datatype':
            pass
        txt = '''
    def handle_%s(self):
''' % name
        #txt += '        pass\n'
        self.outtxt += txt
        self.curname = name

        types = self.get_types(node.v)
        prefix = self.get_prefix(types)
        self.curtyp = (types, prefix)
        self.curpos = pos_onlyme; self.curtypno = 0

        node.v.walkabout(self)

        self.outp('return %s_%s(%s)' % (self.prefix, name, ', '.join(prefix)))
        self.curtyp = None

    def visit_stmt_value(self, node):
        node.v.walkabout(self)

    def visit_series(self, node):
        assert self.curpos == pos_onlyme

        if len(node.vlst) == 1:
            self.curpos = pos_onlyme; self.curtypno = 0
            v = DirectToV(node.vlst[0])
            v.walkabout(self)
            self.curpos = None
            return
        j = 0
        for i,v in enumerate(node.vlst):
            self.curtypno = None
            typ = self.get_type(v)
            if typ != type_none:
                self.curtypno = j
                assert self.curtyp[0][j] == typ
                j += 1
            if i == 0:
                self.outp('savpos = self.pos')
                self.curpos = pos_first
            elif i == len(node.vlst) - 1:
                self.skipspace()
                self.curpos = pos_end
            else:
                self.skipspace()
                self.curpos = pos_mid
            v1 = DirectToV(v)
            v1.walkabout(self)
            self.curpos = None
    def visit_litname(self, node):
        name = node.s
        if name in self.predefines:
            vname = self.curtyp[1][self.curtypno]
            if self.curpos in (pos_onlyme, pos_first):
                self.outp('%s = self.handle_%s()' % (vname, name))
                self.outp('if not %s:' % vname)
                self.outp('return None', 1)
            else:
                self.outp('%s = self.handle_%s()' % (vname, name))
                self.outp('if not %s:' % vname)
                self.outp('return self.restorepos(savpos)', 1)
            return
            assert False
        if name in self.itemlst:
            vname = self.curtyp[1][self.curtypno]
            if self.curpos in (pos_onlyme, pos_first):
                self.outp('%s = self.handle_%s()' % (vname, name))
                self.outp('if not %s:' % vname)
                self.outp('return None', 1)
            else:
                self.outp('%s = self.handle_%s()' % (vname, name))
                self.outp('if not %s:' % vname)
                self.outp('return self.restorepos(savpos)', 1)
            return

        pass
    def visit_litstring(self, node):
        s = node.s
        if self.curpos in (pos_onlyme, pos_first):
            self.outp("if not self.handle_str(%s):" % s)
            self.outp('return None', 1)
            return
        self.outp("if not self.handle_str(%s):" % s)
        self.outp('return self.restorepos(savpos)', 1)
    def visit_value(self, node):
        node.v.walkabout(self)
    def visit_string_or(self, node):
        vname = self.curtyp[1][self.curtypno]
        for i,s in enumerate(node.slst):
            if i == 0:
                self.outp('%s = self.handle_str(%s)' % (vname, s))
            else:
                self.outp('if not %s:' % vname)
                self.outp('%s = self.handle_str(%s)' % (vname, s), 1)
        self.outp('if not %s:' % vname)
        if self.curpos in (pos_onlyme, pos_first):
            self.outp('return None', 1)
        else:
            self.outp('return self.restorepos(savpos)', 1)
        pass
    def visit_values_or(self, node):
        vname = self.curtyp[1][self.curtypno]
        for i,s in enumerate(node.slst):
            if s in self.itemlst:
                if i == 0:
                    self.outp('%s = self.handle_%s()' % (vname, s))
                else:
                    self.outp('if not %s:' % vname)
                    self.outp('%s = self.handle_%s()' % (vname, s), 1)
                continue
            if s in self.predefines:
                if i == 0:
                    self.outp('%s = self.handle_%s()' % (vname, s))
                else:
                    self.outp('if not %s:' % vname)
                    self.outp('%s = self.handle_%s()' % (vname, s), 1)
                continue
            assert False
        self.outp('if not %s:' % vname)
        self.outp('return None', 1)
    def visit_jiap(self, node):
        s1 = node.s1
        s2 = node.s2
        vname = self.curtyp[1][0]
        self.outp('savpos = self.pos')
        self.outp('%s = []' % vname)
        self.outp('s = self.handle_%s()' % s1)
        self.outp('if not s:')
        self.outp('return None', 1)
        self.outp('%s.append(s)' % vname)
        self.outp('while True:')
        self.ntab += 1
        self.skipspace()
        self.outp('if not self.handle_str(%s):' % s2)
        self.outp('break', 1)
        self.skipspace()
        self.outp('s = self.handle_%s()' % s1)
        self.outp('if not s:')
        self.outp('break', 1)
        self.outp('%s.append(s)' % vname)
        self.outp('savpos = self.pos')
        self.ntab -= 1
        self.outp('self.restorepos(savpos)')
        self.outp('if len(%s) < 2:' % vname)
        self.outp('return None', 1)
        '''
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
        '''
    def outp(self, s, ntab=0):
        self.outtxt += '    '*(self.ntab+ntab)+s+'\n'
    def visit_itemd(self, node):
        if self.curpos == pos_onlyme:
            lstname = self.curtyp[1][self.curtypno]
            v1 = DirectToV(node.v)
            if isinstance(v1, GDL.LiuD_litname):
                name = v1.s
                if name in self.itemlst:
                    self.outp('v = self.handle_%s()' % name)
                    self.outp('if not v:')
                    self.outp('return None', 1)
                    self.outp('savpos = self.pos')
                    self.outp('%s = [v]' % lstname)
                    self.outp('while True:')
                    self.ntab +=1
                    self.skipspace()
                    self.outp('v = self.handle_%s()' % name)
                    self.outp('if not v:')
                    self.outp('break', 1)
                    self.outp('%s.append(v)' % lstname)
                    self.outp('savpos = self.pos')
                    self.ntab -=1
                    self.outp('self.restorepos(savpos)')
                    return

            self.outp('%s = []' % lstname)
            self.outp('savpos = self.pos')
            self.outp('while True:')
            self.ntab +=1
            #self.outp('pass')
            self.inloop(node.v, lstname)
            self.ntab -=1
            self.outp('self.restorepos(savpos)')
            self.outp('if not %s:' % lstname)
            self.outp('return None', 1)
        #node.v.walkabout(self)
    def inloop(self, node, lstname):
        node1 = DirectToV(node)
        if isinstance(node1, GDL.LiuD_series):
            vname = None
            for i,v in enumerate(node1.vlst):
                if i != 0:
                    self.skipspace()
                v = DirectToV(v)
                if isinstance(v, GDL.LiuD_litname):
                    name = v.s
                    if name in self.itemlst:
                        self.outp('v = self.handle_%s()' % name)
                        self.outp('if not v:')
                        self.outp('break', 1)
                        vname = 'v'
                        continue
                    if name in self.predefines0:
                        self.outp('if not self.handle_%s():' % name)
                        self.outp('break', 1)
                        continue
                    assert False
            assert vname
            self.outp('%s.append(%s)' % (lstname, vname))
            self.outp('savpos = self.pos')
            self.skipspace()
            return
        if isinstance(node1, GDL.LiuD_litname):
            name = node1.s
            if name in self.itemlst:
                self.outp('v = self.handle_%s()' % name)
                self.outp('if not v:')
                self.outp('break', 1)
                vname = 'v'
            else:
                assert False
            self.outp('%s.append(v)' % lstname)
            self.outp('savpos = self.pos')
            self.skipspace()
            return
        assert False

'''
        savpos = self.pos
        vlst = []
        while True:
            v = self.handle_value()
            if not v:
                break
            vlst.append(v)
            savpos = self.pos
            self.skipspace()
        self.restorepos(savpos)
        if not vlst:
            return None
        return LiuD_series(vlst)

'''

def DirectToV(node):
    while True:
        if isinstance(node, GDL.LiuD_value):
            node = node.v
            continue
        if isinstance(node, GDL.LiuD_value1):
            node = node.v
            continue
        if isinstance(node, GDL.LiuD_enclosed):
            node = node.v
            continue
        if isinstance(node, GDL.LiuD_stmt_value):
            node = node.v
            continue
        break
    return node


def Gen02(mod):

    lst, prefix = GetItemList(mod)

    the = cls_Gen02(lst, prefix)
    mod.walkabout(the)
    # print the.outtxt
    return the.outtxt

def Gen_All(txt):
    the = LiuD_Parser(txt)
    mod = the.handle_main()

    s1 = Gen01(mod)
    s2 = Gen02(mod)

    s = '''# auto generated

from GDL_common import *

''' + s1 + s2
    return s


LiuD_syntax = '''option.prefix = LiuD
    states.skip = space
    main = (stmt1 NEWLINE)*
    stmt1 = options | stmt
    options = option1 | state1
        option1 = 'option.prefix' '=' NAME
        state1 = 'states.skip' '=' NAME
    stmt = NAME '=' stmt_value
    stmt_value = values_or | string_or | jiap | series
        values_or = NAME ^+ '|'
        string_or = STRING ^+ '|'
        series = value*
        jiap = NAME '^+' STRING

    litname = NAME
    litstring = STRING
    value1 = litname | litstring | enclosed
        enclosed = '(' stmt_value ')'
    value = itemd | value1
        itemd = value1 '*'
'''

import unittest
class Test(unittest.TestCase):
    def test1(self):
        s = Gen_All(LiuD_syntax)

        #open('Ast_LiuD.py', 'w').write(s)
        s2 = open('Ast_LiuD.py').read()
        self.assertEqual(s, s2)

    def test2(self):
        syntax = '''option.prefix = GDL01
            states.skip = crlf
            main = stmt*
            stmt = declare_with_value | declare | assign | funccall
            datatype = 'int' | 'long'
            declare = datatype NAME
            declare_with_value = datatype NAME '=' value
            value0 = NUMBER | NAME
            binvalue = value0 ('+' | '-') value0
            value = binvalue | value0
            assign = NAME '=' value
            funccall = NAME '(' value ')'
        '''
        s = Gen_All(syntax)
        #open('Ast_C.py', 'w').write(s)
        s2 = open('Ast_C.py').read()
        self.assertEqual(s, s2)

if __name__ == '__main__':
    print 'good'

