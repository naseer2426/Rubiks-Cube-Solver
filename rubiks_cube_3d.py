import tkinter as tk
import time
import math
import random
import solution as s

root_two = math.sqrt(2)
root_six = math.sqrt(6)




def convert3dTo2d(coord):
    x = coord[0]
    y = coord[1]
    z = coord[2]

    X = ((x-z)/root_two)*85+200
    Y = -(((2*y-x-z)/root_six)*85-200)

    return (X,Y)

def convert(coords):
    final = []
    for surface in coords:
        new_surface = []
        for box in surface:
            b = []
            for i in range(6):
                if i!=5:
                    b.append(convert3dTo2d(box[i]))
                else:
                    b.append(box[i])
            new_surface.append(b)
        final.append(new_surface)
    return final





def variance(p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    z1 = p1[2]

    x2 = p2[0]
    y2 = p2[1]
    z2 = p2[2]

    v = [x1+x2,y1+y2,z1+z2].index(0)
    if v==0:
        if x1<x2:
            return [0,1]
        else:
            return [0,-1]
    elif v==1:
        if y1<y2:
            return [1,1]
        else:
            return [1,-1]
    else:
        if z1<z2:
            return [2,1]
        else:
            return [2,-1]

def create_rubiks_cube(outline):
    len = 2/3
    rubiks_cube = []
    for side in outline:
        top_corner = side[0]
        x_info = variance(side[0],side[1])
        y_info = variance(side[1],side[2])
        x_change_index = x_info[0]
        x_change_value = x_info[1]*len
        y_change_index = y_info[0]
        y_change_value = y_info[1]*len

        surface = []
        for i in range(9):
            corner = list(top_corner)
            if i<3:
                corner[x_change_index] = corner[x_change_index]+x_change_value*i
            elif i<6:
                corner[y_change_index] = corner[y_change_index]+y_change_value
                corner[x_change_index] = corner[x_change_index]+x_change_value*(i-3)
            else:
                corner[y_change_index] = corner[y_change_index]+y_change_value*2
                corner[x_change_index] = corner[x_change_index]+x_change_value*(i-6)
            point1 = tuple(corner)
            corner[x_change_index] = corner[x_change_index]+x_change_value
            point2 = tuple(corner)
            corner[y_change_index] = corner[y_change_index]+y_change_value
            point3 = tuple(corner)
            corner[x_change_index] = corner[x_change_index]-x_change_value
            point4 = tuple(corner)
            surface.append([point1,point2,point3,point4,point1,''])
        rubiks_cube.append(surface)
    return rubiks_cube



def colourCube(cube,colour):
    c = {'b':'blue','w':'white','r':'red','y':'yellow','o':'orange','g':'green'}
    for i in range(6):
        for j in range(9):
            cube[i][j][5] = c[colour[i][j]]



def draw_part_of_cube(cube_coords,canvas):
    polygon_ids = []
    for surface in cube_coords:
        for box in surface:
            polygon_ids.append(canvas.create_polygon(box[:5], outline = 'black', fill = box[5]))
    return polygon_ids

def moveU(direction,existing_cube,cube_coords,cube_colours,t,canvas):
    for polygon in existing_cube:
        canvas.delete(polygon)

    angle_coeff = 1
    if direction=="u":
        angle_coeff = -1

    cube2d = convert(cube_coords)

    upper_layer = []
    for i in range(5):
        if i!=0:
            upper_layer.append(cube_coords[i][:3])
        else:
            upper_layer.append(cube_coords[i])

    remaining_layers = []
    for i in range(1,3):
        remaining_layers.append(cube2d[i][3:9])

    inside_remaining3d = [[[(-1,1-2/3,1),(1,1-2/3,1),(1,1-2/3,-1),(-1,1-2/3,-1),(-1,1-2/3,1),'grey']]]
    inside_remaining = convert(inside_remaining3d)

    remaining_layers+=inside_remaining


    remaining = draw_part_of_cube(remaining_layers,canvas)
    frames = 30*t
    full_angle = angle_coeff*math.pi/2
    frame_angle = full_angle/frames
    # temp_cube_coords = cube_coords
    cos_angle = math.cos(frame_angle)
    sin_angle = math.sin(frame_angle)
    angle_so_far = 0
    for i in range(int(frames)+1):
        temp_upperlayer = convert(upper_layer)
        if angle_so_far/angle_coeff<math.pi/4:
            upper = draw_part_of_cube(temp_upperlayer[:3],canvas)
        elif angle_coeff==1:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[0])
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[1])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        else:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[0])
            temp_upperlayer2.append(temp_upperlayer[2])
            temp_upperlayer2.append(temp_upperlayer[3])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        canvas.update()

        new_upper_layer = []
        for surface in upper_layer:
            new_surface = []
            for box in surface:
                new_box = []
                for k in range(5):
                    x = box[k][0]
                    y = box[k][1]
                    z = box[k][2]

                    X = x*cos_angle + z*sin_angle
                    Z = -x*sin_angle + z*cos_angle

                    new_box.append((X,y,Z))
                new_box.append(box[5])
                new_surface.append(new_box)
            new_upper_layer.append(new_surface)

        upper_layer = new_upper_layer
        angle_so_far+=frame_angle
        time.sleep(0.033)
        for polygon in upper:
            canvas.delete(polygon)
    # time.sleep(5)
    for polygon in remaining:
        canvas.delete(polygon)

    s.single_move(cube_colours,direction)
    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    return draw_part_of_cube(cube2d[:3],canvas)

def moveD(direction,existing_cube,cube_coords,cube_colours,t,canvas):
    for polygon in existing_cube:
        canvas.delete(polygon)

    angle_coeff = 1
    if direction=="d'":
        angle_coeff = -1

    cube2d = convert(cube_coords)

    upper_layer = []
    for i in range(1,5):
        upper_layer.append(cube_coords[i][6:9])

    inside_upper = [[[(-1,-1+2/3,1),(1,-1+2/3,1),(1,-1+2/3,-1),(-1,-1+2/3,-1),(-1,-1+2/3,1),'grey']]]
    upper_layer+=inside_upper

    remaining_layers = []
    for i in range(3):
        if i==0:
            remaining_layers.append(cube2d[i])
        else:
            remaining_layers.append(cube2d[i][:6])




    frames = 30*t
    full_angle = angle_coeff*math.pi/2
    frame_angle = full_angle/frames
    # temp_cube_coords = cube_coords
    cos_angle = math.cos(frame_angle)
    sin_angle = math.sin(frame_angle)
    angle_so_far = 0
    for i in range(int(frames)+1):
        temp_upperlayer = convert(upper_layer)
        if angle_so_far/angle_coeff<math.pi/4:
            upper = draw_part_of_cube(temp_upperlayer[:2]+[temp_upperlayer[4]],canvas)
        elif angle_coeff==1:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[3])
            temp_upperlayer2.append(temp_upperlayer[0])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        else:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[1])
            temp_upperlayer2.append(temp_upperlayer[2])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)

        remaining = draw_part_of_cube(remaining_layers,canvas)
        canvas.update()

        new_upper_layer = []
        for surface in upper_layer:
            new_surface = []
            for box in surface:
                new_box = []
                for k in range(5):
                    x = box[k][0]
                    y = box[k][1]
                    z = box[k][2]

                    X = x*cos_angle + z*sin_angle
                    Z = -x*sin_angle + z*cos_angle

                    new_box.append((X,y,Z))
                new_box.append(box[5])
                new_surface.append(new_box)
            new_upper_layer.append(new_surface)

        upper_layer = new_upper_layer
        angle_so_far+=frame_angle
        time.sleep(0.033)
        for polygon in upper:
            canvas.delete(polygon)

        for polygon in remaining:
            canvas.delete(polygon)


    s.single_move(cube_colours,direction)
    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    return draw_part_of_cube(cube2d[:3],canvas)

def moveR(direction,existing_cube,cube_coords,cube_colours,t,canvas):
    for polygon in existing_cube:
        canvas.delete(polygon)

    angle_coeff = 1
    if direction=="r":
        angle_coeff = -1

    cube2d = convert(cube_coords)

    upper_layer = []
    upper_layer.append(cube_coords[2])
    for i in [1,0,3,5]:
        if i==3:
            upper_layer.append([cube_coords[i][0],cube_coords[i][3],cube_coords[i][6]])
        else:
            upper_layer.append([cube_coords[i][2],cube_coords[i][5],cube_coords[i][8]])



    remaining_layers = []
    for i in range(2):
        surf = []
        for j in [0,1,3,4,6,7]:
            surf.append(cube2d[i][j])
        remaining_layers.append(surf)

    inside_remaining3d = [[[(1-2/3,1,1),(1-2/3,1,-1),(1-2/3,-1,-1),(1-2/3,-1,1),(1-2/3,1,1),'grey']]]
    inside_remaining = convert(inside_remaining3d)

    remaining_layers+=inside_remaining


    remaining = draw_part_of_cube(remaining_layers,canvas)
    frames = 30*t
    full_angle = angle_coeff*math.pi/2
    frame_angle = full_angle/frames
    # temp_cube_coords = cube_coords
    cos_angle = math.cos(frame_angle)
    sin_angle = math.sin(frame_angle)
    angle_so_far = 0
    for i in range(int(frames)+1):
        temp_upperlayer = convert(upper_layer)
        if angle_so_far/angle_coeff<math.pi/4:
            upper = draw_part_of_cube(temp_upperlayer[:3],canvas)
        elif angle_coeff==1:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[0])
            temp_upperlayer2.append(temp_upperlayer[2])
            temp_upperlayer2.append(temp_upperlayer[3])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        else:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[0])
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[1])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        canvas.update()

        new_upper_layer = []
        for surface in upper_layer:
            new_surface = []
            for box in surface:
                new_box = []
                for k in range(5):
                    x = box[k][0]
                    y = box[k][1]
                    z = box[k][2]

                    Y = y*cos_angle - z*sin_angle
                    Z = y*sin_angle + z*cos_angle

                    new_box.append((x,Y,Z))
                new_box.append(box[5])
                new_surface.append(new_box)
            new_upper_layer.append(new_surface)

        upper_layer = new_upper_layer
        angle_so_far+=frame_angle
        time.sleep(0.033)
        for polygon in upper:
            canvas.delete(polygon)
    # time.sleep(5)
    for polygon in remaining:
        canvas.delete(polygon)

    s.single_move(cube_colours,direction)
    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    return draw_part_of_cube(cube2d[:3],canvas)

def moveL(direction,existing_cube,cube_coords,cube_colours,t,canvas):
    for polygon in existing_cube:
        canvas.delete(polygon)

    angle_coeff = 1
    if direction=="l'":
        angle_coeff = -1

    cube2d = convert(cube_coords)

    upper_layer = []
    for i in [1,0,3,5]:
        if i==3:
            upper_layer.append([cube_coords[i][2],cube_coords[i][5],cube_coords[i][8]])
        else:
            upper_layer.append([cube_coords[i][0],cube_coords[i][3],cube_coords[i][6]])

    inside_upper = [[[(-1+2/3,1,1),(-1+2/3,1,-1),(-1+2/3,-1,-1),(-1+2/3,-1,1),(-1+2/3,1,1),'grey']]]
    upper_layer+=inside_upper

    remaining_layers = []
    remaining_layers.append(cube2d[2])
    for i in range(2):
        surf = []
        for j in [1,2,4,5,7,8]:
            surf.append(cube2d[i][j])
        remaining_layers.append(surf)




    frames = 30*t
    full_angle = angle_coeff*math.pi/2
    frame_angle = full_angle/frames
    # temp_cube_coords = cube_coords
    cos_angle = math.cos(frame_angle)
    sin_angle = math.sin(frame_angle)
    angle_so_far = 0
    for i in range(int(frames)+1):
        temp_upperlayer = convert(upper_layer)
        if angle_so_far/angle_coeff<math.pi/4:
            upper = draw_part_of_cube(temp_upperlayer[:2]+[temp_upperlayer[4]],canvas)
        elif angle_coeff==1:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[1])
            temp_upperlayer2.append(temp_upperlayer[2])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        else:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[3])
            temp_upperlayer2.append(temp_upperlayer[0])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)

        remaining = draw_part_of_cube(remaining_layers,canvas)
        canvas.update()

        new_upper_layer = []
        for surface in upper_layer:
            new_surface = []
            for box in surface:
                new_box = []
                for k in range(5):
                    x = box[k][0]
                    y = box[k][1]
                    z = box[k][2]

                    Y = y*cos_angle - z*sin_angle
                    Z = y*sin_angle + z*cos_angle

                    new_box.append((x,Y,Z))
                new_box.append(box[5])
                new_surface.append(new_box)
            new_upper_layer.append(new_surface)

        upper_layer = new_upper_layer
        angle_so_far+=frame_angle
        time.sleep(0.033)
        for polygon in upper:
            canvas.delete(polygon)

        for polygon in remaining:
            canvas.delete(polygon)


    s.single_move(cube_colours,direction)
    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    return draw_part_of_cube(cube2d[:3],canvas)

def moveF(direction,existing_cube,cube_coords,cube_colours,t,canvas):
    for polygon in existing_cube:
        canvas.delete(polygon)

    angle_coeff = 1
    if direction=="f":
        angle_coeff = -1

    cube2d = convert(cube_coords)

    upper_layer = []
    upper_layer.append(cube_coords[1])
    upper_layer.append([cube_coords[0][6],cube_coords[0][7],cube_coords[0][8]])
    upper_layer.append([cube_coords[2][0],cube_coords[2][3],cube_coords[2][6]])
    upper_layer.append([cube_coords[5][0],cube_coords[5][1],cube_coords[5][2]])
    upper_layer.append([cube_coords[4][2],cube_coords[4][5],cube_coords[4][8]])

    remaining_layers = []
    surf = []
    for i in range(6):
        surf.append(cube2d[0][i])
    remaining_layers.append(surf)
    surf = []
    for i in [1,2,4,5,7,8]:
        surf.append(cube2d[2][i])
    remaining_layers.append(surf)


    inside_remaining3d = [[[(-1,1,1-2/3),(1,1,1-2/3),(1,-1,1-2/3),(-1,-1,1-2/3),(-1,1,1-2/3),'grey']]]
    inside_remaining = convert(inside_remaining3d)

    remaining_layers+=inside_remaining


    remaining = draw_part_of_cube(remaining_layers,canvas)
    frames = 30*t
    full_angle = angle_coeff*math.pi/2
    frame_angle = full_angle/frames
    # temp_cube_coords = cube_coords
    cos_angle = math.cos(frame_angle)
    sin_angle = math.sin(frame_angle)
    angle_so_far = 0
    for i in range(int(frames)+1):
        temp_upperlayer = convert(upper_layer)
        if angle_so_far/angle_coeff<math.pi/4:
            upper = draw_part_of_cube(temp_upperlayer[:3],canvas)
        elif angle_coeff==1:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[0])
            temp_upperlayer2.append(temp_upperlayer[2])
            temp_upperlayer2.append(temp_upperlayer[3])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        else:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[0])
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[1])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        canvas.update()

        new_upper_layer = []
        for surface in upper_layer:
            new_surface = []
            for box in surface:
                new_box = []
                for k in range(5):
                    x = box[k][0]
                    y = box[k][1]
                    z = box[k][2]

                    X = x*cos_angle - y*sin_angle
                    Y = x*sin_angle + y*cos_angle

                    new_box.append((X,Y,z))
                new_box.append(box[5])
                new_surface.append(new_box)
            new_upper_layer.append(new_surface)

        upper_layer = new_upper_layer
        angle_so_far+=frame_angle
        time.sleep(0.033)
        for polygon in upper:
            canvas.delete(polygon)
    # time.sleep(5)
    for polygon in remaining:
        canvas.delete(polygon)

    s.single_move(cube_colours,direction)
    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    return draw_part_of_cube(cube2d[:3],canvas)

def moveB(direction,existing_cube,cube_coords,cube_colours,t,canvas):
    for polygon in existing_cube:
        canvas.delete(polygon)

    angle_coeff = 1
    if direction=="b'":
        angle_coeff = -1

    cube2d = convert(cube_coords)

    upper_layer = []
    upper_layer.append([cube_coords[0][0],cube_coords[0][1],cube_coords[0][2]])
    upper_layer.append([cube_coords[2][2],cube_coords[2][5],cube_coords[2][8]])
    upper_layer.append([cube_coords[5][6],cube_coords[5][7],cube_coords[5][8]])
    upper_layer.append([cube_coords[4][0],cube_coords[4][3],cube_coords[4][6]])

    inside_upper = [[[(-1,1,-1+2/3),(1,1,-1+2/3),(1,-1,-1+2/3),(-1,-1,-1+2/3),(-1,1,-1+2/3),'grey']]]
    upper_layer+=inside_upper

    remaining_layers = []
    remaining_layers.append(cube2d[1])
    surf = []
    for i in [3,4,5,6,7,8]:
        surf.append(cube2d[0][i])
    remaining_layers.append(surf)
    surf = []
    for i in [0,1,3,4,6,7]:
        surf.append(cube2d[2][i])
    remaining_layers.append(surf)




    frames = 30*t
    full_angle = angle_coeff*math.pi/2
    frame_angle = full_angle/frames
    # temp_cube_coords = cube_coords
    cos_angle = math.cos(frame_angle)
    sin_angle = math.sin(frame_angle)
    angle_so_far = 0
    for i in range(int(frames)+1):
        temp_upperlayer = convert(upper_layer)
        if angle_so_far/angle_coeff<math.pi/4:
            upper = draw_part_of_cube(temp_upperlayer[:2]+[temp_upperlayer[4]],canvas)
        elif angle_coeff==1:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[1])
            temp_upperlayer2.append(temp_upperlayer[2])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)
        else:
            temp_upperlayer2 = []
            temp_upperlayer2.append(temp_upperlayer[4])
            temp_upperlayer2.append(temp_upperlayer[3])
            temp_upperlayer2.append(temp_upperlayer[0])
            upper = draw_part_of_cube(temp_upperlayer2,canvas)

        remaining = draw_part_of_cube(remaining_layers,canvas)
        canvas.update()

        new_upper_layer = []
        for surface in upper_layer:
            new_surface = []
            for box in surface:
                new_box = []
                for k in range(5):
                    x = box[k][0]
                    y = box[k][1]
                    z = box[k][2]

                    X = x*cos_angle - y*sin_angle
                    Y = x*sin_angle + y*cos_angle

                    new_box.append((X,Y,z))
                new_box.append(box[5])
                new_surface.append(new_box)
            new_upper_layer.append(new_surface)

        upper_layer = new_upper_layer
        angle_so_far+=frame_angle
        time.sleep(0.033)
        for polygon in upper:
            canvas.delete(polygon)

        for polygon in remaining:
            canvas.delete(polygon)


    s.single_move(cube_colours,direction)
    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    return draw_part_of_cube(cube2d[:3],canvas)

def three_d_cube_moves(cube_coords,cube_colours,t,moves,canvas,exist_cube_loc = ''):
    if exist_cube_loc!='':
        for poly in exist_cube_loc:
            canvas.delete(poly)

    colourCube(cube_coords,cube_colours)
    cube2d = convert(cube_coords)
    poly_loc = draw_part_of_cube(cube2d[:3],canvas)
    for move in moves:
        if move[0]=='u':
            poly_loc = moveU(move,poly_loc,cube_coords,cube_colours,t,canvas)
        elif move[0]=='d':
            poly_loc = moveD(move,poly_loc,cube_coords,cube_colours,t,canvas)
        elif move[0]=='f':
            poly_loc = moveF(move,poly_loc,cube_coords,cube_colours,t,canvas)
        elif move[0]=='b':
            poly_loc = moveB(move,poly_loc,cube_coords,cube_colours,t,canvas)
        elif move[0]=='r':
            poly_loc = moveR(move,poly_loc,cube_coords,cube_colours,t,canvas)
        else:
            poly_loc = moveL(move,poly_loc,cube_coords,cube_colours,t,canvas)
    return poly_loc

rubik_cube_outline = [[(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)],[(-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)],[(1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1)],[(1,1,-1),(-1,1,-1),(-1,-1,-1),(1,-1,-1)],[(-1,1,-1),(-1,1,1),(-1,-1,1),(-1,-1,-1)],[(-1,-1,1),(1,-1,1),(1,-1,-1),(-1,-1,-1)]]
rubiks_cube = create_rubiks_cube(rubik_cube_outline)
solved_cube_colours=[['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'], ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y'], ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'], ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']]


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x500")
    canvas = tk.Canvas(root, height = 400, width = 400)
    canvas.pack()
    three_d_cube_moves(rubiks_cube,[['r', 'w', 'y', 'r', 'b', 'w', 'w', 'y', 'o'], ['r', 'b', 'w', 'w', 'w', 'g', 'r', 'r', 'w'], ['b', 'r', 'g', 'r', 'r', 'g', 'b', 'y', 'g'], ['o', 'b', 'y', 'o', 'y', 'g', 'o', 'y', 'y'], ['b', 'b', 'g', 'w', 'o', 'o', 'b', 'b', 'g'], ['y', 'y', 'r', 'o', 'g', 'g', 'o', 'o', 'w']],0.5,["f'","l'","b'",'f','d',"r'",'u'],canvas)
    root.mainloop()
