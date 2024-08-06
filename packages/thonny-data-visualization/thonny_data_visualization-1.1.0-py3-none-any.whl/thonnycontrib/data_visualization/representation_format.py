from re import sub

'''Permet de formater proprement la représentation générale de l'objet en une représentation simplifiée'''
def repr_format(self, st):
    at_bool = False
    homemade = False

    if (st.startswith('<')):
            s_ret, at_bool, homemade = little_format(st, self)
    else:
        lst = st.split('<')
        s_ret = ""
        i = 0
        for s in lst:
            lst2 = s.split('>')
            j = len(lst2)
            for s_bis in lst2:
                t = "<"+s_bis+">"
                if (t in self.repr_db.keys()):
                    s_ret += self.repr_db[t]
                else :
                    if (i > 0 and (j > 1 or t.endswith("…>"))):
                        s_r, at, h = little_format(t, self)
                        if (s_r.endswith("…") and "<"+s_r+">" == t):
                            s_ret += "…"
                        else:
                            s_ret += s_r
                        if (at and self.name == "HV"):
                            s_ret += " unnamed"
                    else:
                        s_ret += s_bis
                j-=1
            i+=1

    s_ret = sub(r'\s+', ' ', s_ret)
    
    return s_ret, at_bool, homemade


def little_format(st, self):
    at_bool = False
    homemade = False

    if (st.startswith("<class '__main__.")):
        s_ret = "class '" + st[17:-1]
        homemade = True
    elif (st.startswith('<__main__.')):
        homemade = True
        s_ret = st[10:-1]
    else:
        s_ret = st[1:-1]

    if (" at " in s_ret): 
        at_bool = True
        s_ret = " ".join(s_ret.split()[:-2])
    elif (" from " in s_ret):
        s_ret = " ".join(s_ret.split()[:-2])

    if (self.name == "GV" and s_ret.split()[-1] == "object"):
        s_ret = " ".join(s_ret.split()[:-1])

    return s_ret, at_bool, homemade