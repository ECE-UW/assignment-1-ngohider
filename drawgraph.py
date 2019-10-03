import sys
from intersection import get_intersect

def distnce(x1, y1, x2, y2):
    return ( (x2 - x1)**2 + (y2 - y1)**2 )

class Graph:

    def __init__(self):
        self.dict = {}
        self.vrtx_lst = {}
        self.edg_lst = {}
        self.intrsct_lst = {}
        self.vrtx_ID = 1
        self.edg_ID = 1

    def add_strt(self, st, coords):
        if st in self.dict:
           sys.stderr.write("Error: cannot add %s it is already in the streets database\n" % (st))
        else:
            if len(coords) < 2:
                sys.stderr.write("Error: missing coordinates, a segment needs at least 2 complete points\n")
                return
            self.dict[st] = coords

    def change_strt(self, st, coords):
        if st in self.dict:
            if len(coords) < 2:
                sys.stderr.write("Error: missing coordinates, a segment needs at least 2 complete points\n")
                return
            self.dict[st] = coords
        else:
            sys.stderr.write("Error: %s does not exist in the streets database\n" % (st))

    def remove_srtr(self, st):
        if st in self.dict:
            del self.dict[st]
        else:
            sys.stderr.write("Error: %s does not exist in the streets database\n" % (st))


    # Check if the segment already exist

    def check_edge(self, vrtx1, vrtx2):
        if (vrtx1, vrtx2) in self.edg_lst.values():
            return True
        elif (vrtx2, vrtx1) in self.edg_lst.values():
            return True
        else:
            return False

    def add_edge(self, vrtx1, vrtx2):
        if (vrtx1, vrtx2) in self.edg_lst.values():
            return
        elif (vrtx2, vrtx1) in self.edg_lst.values():
            return
        elif vrtx1 == vrtx2:
            return
        else:
            self.edg_lst[self.edg_ID] = (vrtx1, vrtx2)
            self.edg_ID += 1

    # Remove the current segment if it does not satisfy the given conditions

    def remove_edge(self, vrtx1, vrtx2):
        for key, value in self.edg_lst.items():
            if ((value == (vrtx1, vrtx2)) | (value == (vrtx2, vrtx1))):
                del self.edg_lst[key]

    def get_vrtx_ID(self, point):
        for id, pt in self.vrtx_lst.iteritems():
            if pt == point:
                return id
        return None


    def print_graph(self):
        st_database = self.dict.keys()
        remove = []
        self.vrtx_lst.clear()
        self.edg_lst.clear()
        self.intrsct_lst.clear()
        self.vrtx_ID = 1
        self.edg_ID = 1
        for st in st_database:
            other_strts = list(st_database)
            other_strts.remove(st)
            stCoords = self.dict.get(st)
    ## Get the nodes coordinates
            for k in range(len(stCoords)):
                endNode = len(stCoords) - 1
                if (endNode > k):
                    pt1 = stCoords[k].replace('(', '').replace(')', '').split(',')
                    pt2 = stCoords[k + 1].replace('(', '').replace(')', '').split(',')

                    x1 = pt1[0]
                    y1 = pt1[1]
                    x2 = pt2[0]
                    y2 = pt2[1]
   ## Once we finish all segments of the current street
                else:
                    break
         ## Check intersection through all streets in the database
                for st2 in other_strts: #loop through all other streets (to check intersections)
                    st2Coords = self.dict.get(st2)

                    for st2Pt in range(len(st2Coords)):
                        endNode = len(st2Coords) - 1
                        if (endNode > st2Pt):
                            #Extract (X1, Y1) and (X2, Y2)
                            pt1 = st2Coords[st2Pt].replace('(','').replace(')','').split(',')
                            pt2 = st2Coords[st2Pt+1].replace('(','').replace(')','').split(',')

                            x3 = pt1[0]
                            y3 = pt1[1]
                            x4 = pt2[0]
                            y4 = pt2[1]

                        else: #We reached the last line segment for st. Move to next st.
                            break

                        #Now we have coords for 4 points defining two line segments
                        #Check if those two line segments intersect:

                        intrsct_x, intrsct_y = get_intersect(x1, y1, x2, y2, x3, y3, x4, y4)

                        #if there is a new intersection, update vLst and eLst
                        if ((intrsct_x != None) & (intrsct_y != None)):
                            #ptID vars are to make sure we only work with vertices that are added
                            #to the vLst.
                            pt1ID =  pt2ID = pt3ID = pt4ID = pt5ID = None

                            x1 = float(x1)
                            x2 = float(x2)
                            x3 = float(x3)
                            x4 = float(x4)
                            intrsct_x = float(intrsct_x)

                            y1 = float(y1)
                            y2 = float(y2)
                            y3 = float(y3)
                            y4 = float(y4)
                            intrsct_y = float(intrsct_y)

                            pt1 = (x1, y1)
                            pt2 = (x2, y2)
                            pt3 = (x3, y3)
                            pt4 = (x4, y4)
                            pt5 = (intrsct_x, intrsct_y)

                            # Update intersection list
                            if (x1,y1,x2,y2) in self.intrsct_lst:
                                if pt5 not in self.intrsct_lst.get((x1, y1, x2, y2)):
                                    self.intrsct_lst[(x1, y1, x2, y2)].append(pt5)
                            else:
                                self.intrsct_lst[(x1, y1, x2, y2)] = [pt5]

                            # check duplicates from intrsct_lst
                            for idx,val in self.intrsct_lst.items():
                                tmpLst = val
                                del self.intrsct_lst[idx]
                                self.intrsct_lst[idx] = list(set(list(tmpLst)))

                            #create a temp list without vertexID for comparison in the below 5 if-statements
                            tmpVertices = []
                            for id in self.vrtx_lst.keys():
                                vertex = self.vrtx_lst.get(id) #tuple of floats
                                tmpVertices.append(vertex)

                            #add vertex to gloabl vertex list if it doesnt exist
                            if pt1 in tmpVertices:
                                pt1ID = self.get_vrtx_ID(pt1)

                            #if pt1 not in tmpVertices:
                            else:
                                self.vrtx_lst[self.vrtx_ID] = (pt1)
                                tmpVertices.append(pt1)
                                pt1ID = self.vrtx_ID
                                self.vrtx_ID += 1

                            if pt2 in tmpVertices:
                                pt2ID = self.get_vrtx_ID(pt2)
                            #if pt2 not in tmpVertices:
                            else:
                                self.vrtx_lst[self.vrtx_ID] = (pt2)
                                tmpVertices.append(pt2)
                                pt2ID = self.vrtx_ID
                                self.vrtx_ID += 1

                            if pt3 in tmpVertices:
                                pt3ID = self.get_vrtx_ID(pt3)
                            #if pt3 not in tmpVertices:

                            else:
                                self.vrtx_lst[self.vrtx_ID] = (pt3)
                                tmpVertices.append(pt3)
                                pt3ID = self.vrtx_ID
                                self.vrtx_ID += 1

                            if pt4 in tmpVertices:
                                pt4ID = self.get_vrtx_ID(pt4)
                            #if pt4 not in tmpVertices:
                            else:
                                self.vrtx_lst[self.vrtx_ID] = (pt4)
                                tmpVertices.append(pt4)
                                pt4ID = self.vrtx_ID
                                self.vrtx_ID += 1

                            if pt5 in tmpVertices:
                                pt5ID = self.get_vrtx_ID(pt5)
                            #if pt5 not in tmpVertices:
                            else:
                                self.vrtx_lst[self.vrtx_ID] = (pt5)
                                tmpVertices.append(pt5)
                                pt5ID = self.vrtx_ID
                                self.vrtx_ID += 1

                            #if no more intersections

                            if len(self.intrsct_lst[(x1, y1, x2, y2)]) <= 1:
                                if pt5 not in (pt1, pt2):
                                    self.add_edge(pt5ID, pt1ID)
                                    self.add_edge(pt5ID, pt2ID)

                        # if
                                if pt5 == pt1:
                                    self.add_edge(pt5ID, pt2ID)

                                if pt5 == pt2:
                                    self.add_edge(pt5ID, pt1ID)


                            #if we have more than a segment
                            else:
                                #first, remove existing edges beween all nodes in line segment
                                currentNodes = [pt1ID, pt2ID]
                                for i in self.intrsct_lst.get((x1, y1, x2, y2)):
                                    if i != (intrsct_x, intrsct_y):
                                        currentNodes.append(self.get_vrtx_ID(i))

                                for i in currentNodes:
                                    for j in currentNodes:
                                        if i != j:
                                            if self.check_edge(i, j):
                                                self.remove_edge(i, j)

                                 # connect the line segments that connect subsequent nodes
                                tmpLst = [(pt1ID, distnce(pt1[0], pt1[1], pt1[0], pt1[1])), (pt2ID, distnce(pt1[0], pt1[1], pt2[0], pt2[1]))]
                                for i in self.intrsct_lst.get((x1, y1, x2, y2)):
                                    tmpLst.append((self.get_vrtx_ID(i), distnce(pt1[0], pt1[1], i[0], i[1])))

                                tmpLst = sorted(tmpLst, key=lambda x: x[1])

                                for idx, i in enumerate(tmpLst):
                                    if idx <= len(tmpLst)-2:
                                        self.add_edge(i[0], tmpLst[idx + 1][0])


        print("V = {")
        for v in self.vrtx_lst.keys():
            print("  %s:  (%.2f,%.2f)" % (v, self.vrtx_lst.get(v)[0], self.vrtx_lst.get(v)[1]))
        print("}")

        print("E = {")
        for key, e in self.edg_lst.items():
            if e == None:
                break
            elif key == self.edg_lst.keys()[-1]:
                print("  <%s,%s>" % (e[0], e[1]))
            else:
                print("  <%s,%s>," % (e[0], e[1]))
        print("}")








