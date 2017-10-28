"""
author mio kinno
date 2017.10.26
file datgenerator.py
"""

class DatGenerator:
    """
    BRITEParserが提供するデータフォーマットからdatファイルを生成する
    """
    
    def __init__(self, nodes, edges, datfile):
        self.nodes = nodes
        self.edges = edges
        self.datfile_name = datfile
        self.traffic = list(permutations(nodes, 2))

    def write_parameters(self):
        self.datfile = open(self.datfile_name, "w+")
        self.datfile.write("/* name {} */\n\n".format(self.datfile_name))

        # dk, m, n
        self.datfile.write("param dk:=1\n")
        self.datfile.write("param m:={}\n".format(len(self.traffic)-1))
        self.datfile.write("param n:={}\n".format(len(self.nodes)-1))

        # HOP
        self.datfile.write("\n/* HOP */\n")
        self.datfile.write("param : EN :HOP:=\n")
        for edge in self.edges:
            self.datfile.write("{} {} 1\n".format(edge[0], edge[1]))
            self.datfile.write("{} {} 1\n".format(edge[1], edge[0]))
        self.datfile.write(";\n")

        # COST
        self.datfile.write("\n/* cost metric:delay */\n")
        self.datfile.write("param : EM :COST:=\n")
        for edge in self.edges:
            self.datfile.write("{} {} {}\n".format(edge[0], edge[1], edge[2]))
            self.datfile.write("{} {} {}\n".format(edge[1], edge[0], edge[2]))
        self.datfile.write(";\n")

        # Capacity
        self.datfile.write("\n/* link capacity:bandwidth */\n")
        self.datfile.write("param : E :C:=\n")
        for edge in self.edges:
            self.datfile.write("{} {} {}\n".format(edge[0], edge[1], edge[3]))
            self.datfile.write("{} {} {}\n".format(edge[1], edge[0], edge[3]))
        self.datfile.write(";\n")

        # traffic start node
        self.datfile.write("\n/* traffic matrix:start node */\n")
        self.datfile.write("param : SK :s:=\n")
        for i,t in enumerate(self.traffic):
            self.datfile.write("{} {}\n".format(i, t[0]))
        self.datfile.write(";\n")
        # traffic start node
        self.datfile.write("\n/* traffic matrix:target node */\n")
        self.datfile.write("param : TK :t:=\n")
        for i,t in enumerate(self.traffic):
            self.datfile.write("{} {}\n".format(i, t[1]))
        self.datfile.write(";\n")

        # DK
        self.datfile.write("\n/* traffic matrix:traffic demand */\n")
        self.datfile.write("param : DK :d:=\n")
        for i,t in enumerate(self.traffic):
            self.datfile.write("{} {}\n".format(i, 100.00))
        self.datfile.write(";\n")

        self.datfile.write("end;\n")

        self.datfile.close()
