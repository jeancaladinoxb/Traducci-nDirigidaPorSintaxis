import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
import uuid


class Node:
    def __init__(self, name, val=None, inh=None):
        self.name = name
        self.val = val
        self.inh = inh
        self.hijo = []

    def añadir_hijo(self, node):
        self.hijo.append(node)

tokens = []
pos = 0

def token_actual():
    return tokens[pos] if pos < len(tokens) else '$'

def match(expected):
    global pos
    if token_actual() == expected:
        pos += 1
    else:
        raise SyntaxError(f"Se esperaba '{expected}' pero se encontró '{token_actual()}'")


def F():
    node = Node("F")
    if token_actual() == '(':
        match('(')
        e_node = E()
        match(')')
        node.añadir_hijo(Node("("))
        node.añadir_hijo(e_node)
        node.añadir_hijo(Node(")"))
        node.val = e_node.val
    else:
        value = float(token_actual())
        node.añadir_hijo(Node("num", val=value))
        match(token_actual())
        node.val = value
    return node

def T_fact(inh):
    node = Node("T'", inh=inh)
    if token_actual() == '*':
        match('*')
        f_node = F()
        t1 = T_fact(inh * f_node.val)
        node.añadir_hijo(Node("*"))
        node.añadir_hijo(f_node)
        node.añadir_hijo(t1)
        node.val = t1.val
    elif token_actual() == '/':
        match('/')
        f_node = F()
        t1 = T_fact(inh / f_node.val)
        node.añadir_hijo(Node("/"))
        node.añadir_hijo(f_node)
        node.añadir_hijo(t1)
        node.val = t1.val
    else:
        node.val = inh
    return node

def T():
    node = Node("T")
    f_node = F()
    t_fact_node = T_fact(f_node.val)
    node.añadir_hijo(f_node)
    node.añadir_hijo(t_fact_node)
    node.val = t_fact_node.val
    return node

def E_fact(inh):
    node = Node("E'", inh=inh)
    if token_actual() == '+':
        match('+')
        t_node = T()
        e1 =E_fact(inh + t_node.val)
        node.añadir_hijo(Node("+"))
        node.añadir_hijo(t_node)
        node.añadir_hijo(e1)
        node.val = e1.val
    elif token_actual() == '-':
        match('-')
        t_node = T()
        e1 = E_fact(inh - t_node.val)
        node.añadir_hijo(Node("-"))
        node.añadir_hijo(t_node)
        node.añadir_hijo(e1)
        node.val = e1.val
    else:
        node.val = inh
    return node

def E():
    node = Node("E")
    t_node = T()
    e_fac_node = E_fact(t_node.val)
    node.añadir_hijo(t_node)
    node.añadir_hijo(e_fac_node)
    node.val = e_fac_node.val
    return node


def parser(expr):
    global tokens, pos
    expr = expr.replace('(', ' ( ').replace(')', ' ) ')
    tokens = expr.split()
    pos = 0
    root = E()
    if token_actual() != '$':
        raise SyntaxError("Error: tokens sin consumir")
    return root


def hierarchy_pos(G, root=None, width=1., vert_gap=0.3, vert_loc=0, xcenter=0.5):
    pos = {}
    def _hierarchy_pos(G, root, leftmost, width, vert_gap, vert_loc, xcenter, pos, parent=None):
        hijo = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            hijo.remove(parent)
        if len(hijo) != 0:
            dx = width / len(hijo)
            nextx = leftmost - width/2 - dx/2
            for child in hijo:
                nextx += dx
                pos = _hierarchy_pos(G, child, nextx, dx, vert_gap, vert_loc-vert_gap, xcenter, pos, root)
        pos[root] = (xcenter, vert_loc)
        return pos
    return _hierarchy_pos(G, root, xcenter, width, vert_gap, vert_loc, xcenter, pos)


def build_graphviz(node, graph=None, parent_name=None, counter=None):
    if counter is None:
        counter = [0]
    if graph is None:
        graph = Digraph(format='png')
        graph.attr('node', shape='circle', style='filled', color='lightblue2', fontname='Arial', fontsize='10')

    node_id = str(counter[0])
    counter[0] += 1
    label = f"{node.name}\nval={node.val if node.val is not None else ''}"
    graph.node(node_id, label)

    if parent_name is not None:
        graph.edge(parent_name, node_id)

    for child in node.hijo:
        build_graphviz(child, graph, node_id, counter)

    return graph

def plot_tree(root, expr):
    dot = build_graphviz(root)
    dot.attr(label=f"Árbol Decorado: {expr}\nResultado = {root.val}", labelloc="t", fontsize='12', fontcolor='darkblue')
    filename = f"arbol_{uuid.uuid4().hex[:5]}"
    dot.render(filename=filename, cleanup=True, view=True)
    print(f"Árbol decorado generado: {filename}.png")

    dot.render(filename='arbol', cleanup=True, view=True)

class TablaSimbolos:
    def __init__(self):
        self.tabla = {}

    def agregar(self, nombre, tipo, valor=None):
        self.tabla[nombre] = {"tipo": tipo, "valor": valor}

    def actualizar_valor(self, nombre, valor):
        if nombre in self.tabla:
            self.tabla[nombre]["valor"] = valor

    def obtener(self, nombre):
        return self.tabla.get(nombre, None)

    def mostrar(self):
        print("\nTabla de Símbolos:")
        for nombre, info in self.tabla.items():
            print(f"  {nombre} -> tipo: {info['tipo']}, valor: {info['valor']}")


if __name__ == "__main__":
    tabla = TablaSimbolos()

    with open("expresiones.txt", "r") as f:
        lineas = [line.strip() for line in f.readlines() if line.strip()]

    for i, expr in enumerate(lineas):
        print(f"\n Expresión: {expr}")
        try:
            root = parser(expr)
            print(f"Resultado: {root.val}")

            tabla.agregar(f"resultado_{i+1}", "float", root.val)


            plot_tree(root, expr)
        except Exception as e:
            print(f" Error al analizar '{expr}': {e}")

    tabla.mostrar()