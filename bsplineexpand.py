import FreeCAD as App
import math
import Draft

Gui.activateWorkbench("DraftWorkbench")

#distant to move point
n = 2

#does need to mirror normal:
# 1 - mirror
# 0 - do not mirror
mirror = 1

groupDefinded = False

objSelected = Gui.Selection.getSelection()
objInSelection = len(objSelected)
for c_obj in range(0, objInSelection):
  print("c_obj ",c_obj);
  object = objSelected[c_obj]
  print("[BSpline extender] Modifying ", object.Label)
  points = object.Points
  numPoints = len(points)
  pointA = points[0]*1
  pointA[2] = pointA[2] - 1
  for c_pts in range(0, numPoints):
    pointB = points[c_pts]*1
    if c_pts == 19:
      pointC = points[19]*1
      pointC[2] = pointC[2] - 1
    else:
      pointC = points[c_pts+1]*1
    #deep coping points
    AX = pointA[0]*1
    AY = pointA[1]*1
    AZ = pointA[2]*1
    pointA = pointB*1
    BX = pointB[0]*1
    BY = pointB[1]*1
    BZ = pointB[2]*1
    CX = pointC[0]*1
    CY = pointC[1]*1
    CZ = pointC[2]*1
    # ToDo: next calculation made fo XZ plane only. need to use cselected plane.
    #calculate angel for normal in midle point
    AB = math.sqrt(math.pow((AX-BX),2)+math.pow((AZ-BZ),2))
    BC = math.sqrt(math.pow((BX-CX),2)+math.pow((BZ-CZ),2))
    #print("AB=",AB, " BC=",BC)
    a = math.asin((BZ-AZ)/AB)*180/3.141593
    g = math.asin((CZ-BZ)/BC)*180/3.141593
    b = 180 - g + a
    p = g + b / 2 - 180 * mirror
    #calculate new point coordinates
    NX = BX - n * math.cos(p*3.141593/180)
    NZ = BZ - n * math.sin(p*3.141593/180)
    NY = BY
    #creeating new point
    point = points[c_pts]
    point = FreeCAD.Vector(NX, NY, NZ)
    points[c_pts] = point*1
    #ToDo: make parent linkage of points of two splines
  bspline = Draft.makeBSpline(points,False,object.Placement,True)
  bspline.Label=object.Label+"_Ext"
  listFolders = object.InList
  selFolder = listFolders[len(listFolders)-1]
  if groupDefinded == False:
    # Checking if Label "_Ext" exists,
    label = "_Ext"
    numeric=0
    groups = selFolder.Group
    numgroups = len(groups)
    for numobjs in range(0, numgroups):
      tmpobj = selFolder.Group[numobjs]
      if (tmpobj.TypeId == 'App::DocumentObjectGroup') | (tmpobj.TypeId == 'App::DocumentObjectGroupPython'):
        leftside=tmpobj.Label[0:4]
        if leftside == label:
          length = len(tmpobj.Label)
          rightside = tmpobj.Label[4:length]
          if rightside == '':
            rightside = '0'
            int(rightside)
          numeric = max(numeric, int(rightside))  
    numeric = numeric + 1
    label=label+str(numeric)
    print("-")
    # Now 'label' = first free name started with _Ext and numeric suffix
    # Creating Group with new name 'label'
    #selFolder.Label
    # selFolder.Group - contains all objects in group
    # Creating new Group
    doc = App.ActiveDocument
    newGroup = doc.addObject("App::DocumentObjectGroupPython", label)
    selFolder.addObject(newGroup)
    groupDefinded = True
  #Adding created spline to new group
  newGroup.addObject(bspline)
  #Creating linkage of splines
  bspline.addProperty("App::PropertyLink","LinkToParent")
  bspline.LinkToParent = object
  


    