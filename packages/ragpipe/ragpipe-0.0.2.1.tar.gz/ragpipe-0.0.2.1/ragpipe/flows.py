'''
rep_names:
    m64: m64encoder
    m128
    m256
    denseint8
    densef32
    sparse
    late

rep_maps:
    .paras[].text: m64, m128, m256, denseint8, densef32, sparse

bridges:
  $for(i in rep_names):
    b_$i: query.text#$i, .paras[].text#$i

    s1 = (b_m64 >> b_m128 >> b_m256)
    s2 = denseint8 >> densef32
    p1 = (s2 || bm25, rrf)
    p2 = (p1 || s1) #concat, concat-reverse
    end = (p2 >> late)



'''

from typing import List, Union, Optional
import json

class Op:
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)
        #return json.dumps(self.to_dict())
        
class Sequence(Op):
    def __init__(self, 
                 children: List[Union['Sequence', 'Parallel', 'Bridge']]):
        self.children = children
        self.name = ''
    def to_dict(self):
        return dict(op='sequence', name=self.name,
                children=[child.to_dict() for child in self.children])
    
class Parallel(Op):
    def __init__(self, 
                 children: List[Union['Sequence', 'Parallel', 'Bridge']], 
                 method: Optional[str] = None):
        self.children = children
        self.method = method
        self.name = ''
    
    def to_dict(self):
        return dict(op='parallel', name=self.name,
                    method = self.method,
                    children=[(child.to_dict()) for child in self.children])

    
class Bridge(Op):
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self):
        #return dict(bridge=self.name)
        return f'bri({self.name})'
    

from .parse import Transformer

class FlowFromText(Transformer):
    var2expr = {}
    def start(self, items):
        _var2expr = FlowFromText.var2expr
        #print('var2expr: ', _var2expr)
        for item in items:
            children = item.children
            upd_children = []
            for child in children:
                if  child.name in _var2expr:
                    upd_children.append(_var2expr[child.name])
                else: 
                    upd_children.append(child)
                    #print(f'{child.name} to be subst')
            item.children = upd_children
        return items[-1]
    def assignment(self, items):
        print('assign', items)
        res = items[1] 
        name = items[0]
        res.name = name
        FlowFromText.var2expr[name] = res
        return res

    def sequence(self, items):
        print('seq', items)
        #items = [items[1] for items in items]
        return Sequence(items)

    def parallel(self, items):
        print('par', items)

        method = None

        if len(items) == 3:
            method = items[-1]
            items = items[:-1]
        #items = [items[1] for items in items]
        return Parallel(items, method=method)

    def expression(self, items):
        return items[0]
    def VAR(self, items):
        #print('var', items, type(items))
        return str(items)
    def BRIDGE(self, items):
        return Bridge(items)
    def IDENTIFIER(self, items):
        return str(items)
        

def build_flow_from_text(statments):
    from .parse import flow_parser
    parse_tree = flow_parser.parse(statments)
    flow = FlowFromText().transform(parse_tree)
    return flow

'''
b = BridgeOp(name, bridge_config)
docs = b.run()

m = MergeOp(b1, b2, method='rrf')
m.execute()
'''

def test():
    input_data = """
    s1 = (b_m64 >> b_m128 >> b_m256)
    s2 = (b_denseint8 >> b_densef32)
    p1 = (s2 || bm25, rrf)
    p2 = (p1 || s1) 
    end = (p2 >> late)
    """

    dag = build_flow_from_text(input_data)
    print('DAG: ', dag)

if __name__ == '__main__':
    test()