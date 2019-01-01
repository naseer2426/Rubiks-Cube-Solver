from tkinter import *
from solution import *
import time
import rubiks_cube_3d as cube_3d
index = 0
curr_face = []
err = 0
sol_index = 0
just_front = 0
cube_sol = []
cube_input = []
cube_loc = []
#test
def takeInput():
    global index, curr_face, err, cube_sol, cube_input
    root = Tk()
    init_box_pos = (95,20)
    len = 85
    index = 0
    err = 0
    box_loc = [init_box_pos, (init_box_pos[0]+len,init_box_pos[1]), (init_box_pos[0]+2*len,init_box_pos[1]), (init_box_pos[0],init_box_pos[1]+len), (init_box_pos[0]+len,init_box_pos[1]+len), (init_box_pos[0]+2*len,init_box_pos[1]+len), (init_box_pos[0],init_box_pos[1]+2*len), (init_box_pos[0]+len,init_box_pos[1]+2*len), (init_box_pos[0]+2*len,init_box_pos[1]+2*len)]
    curr_colour = StringVar()
    cube_faces = [('blue','yellow'),('white','blue'),('red','blue'),('yellow','blue'),('orange','blue'),('green','white')]
    instruction = "Hold the rubik's cube such that the blue centre piece is facing you and the yellow centre piece is on top.\n Fill in the colours on this face."
    cube=[['grey','grey','grey','grey','blue','grey','grey','grey','grey'], ['grey','grey','grey','grey','white','grey','grey','grey','grey'], ['grey','grey','grey','grey','red','grey','grey','grey','grey'], ['grey','grey','grey','grey','yellow','grey','grey','grey','grey'], ['grey','grey','grey','grey','orange','grey','grey','grey','grey'], ['grey','grey','grey','grey','green','grey','grey','grey','grey']]
    cube_input = cube
    cube_sol = []
    curr_face = cube[index]



    root.title("Rubik's Cube Solver")
    hframe = Frame(root)
    hframe.grid(row=0, columnspan = 2)
    heading = Label(hframe, text = "Rubik's Cube Solver", font = ("Algerian", 30))
    heading.pack()
    intsructions_frame = Frame(root)
    intsructions_frame.grid(row = 1, columnspan = 2, pady = 20)
    instructions = Label(intsructions_frame, text = instruction, font = ("Arial",18))
    instructions.pack()
    body_frame = Frame(root)
    body_frame.grid(row = 2, column = 0)
    canvas = Canvas(body_frame)
    canvas.pack()
    button_frame = Frame(root)
    button_frame.grid(row = 2, column = 1)
    error_frame = Frame(root)
    error_frame.grid(row = 3, columnspan = 2)
    error = Label(error_frame, text = "Please input all the colours", font = ('Arial',18))
    lower_button_frame = Frame(root)
    lower_button_frame.grid(row = 4, columnspan = 2)




    red_button = Radiobutton(button_frame,fg = 'red', bg = 'cyan', text = 'Red',  height = 3, width = 30, value = 'red', variable = curr_colour, indicatoron	= 0)
    red_button.grid(row = 0, pady = 10)

    white_button = Radiobutton(button_frame,fg = 'black', bg = 'cyan', text = 'White',  height = 3, width = 30, value = 'white', variable = curr_colour, indicatoron	= 0)
    white_button.grid(row = 1, pady = 10)

    blue_button = Radiobutton(button_frame,fg = 'blue', bg = 'cyan', text = 'Blue',  height = 3, width = 30, value = 'blue', variable = curr_colour, indicatoron	= 0)
    blue_button.grid(row = 2, pady = 10)

    orange_button = Radiobutton(button_frame,fg = 'orange', bg = 'cyan', text = 'Orange',  height = 3, width = 30, value = 'orange', variable = curr_colour, indicatoron	= 0)
    orange_button.grid(row = 3, pady = 10)

    yellow_button = Radiobutton(button_frame,fg = 'orange', bg = 'cyan', text = 'Yellow',  height = 3, width = 30, value = 'yellow', variable = curr_colour, indicatoron	= 0)
    yellow_button.grid(row = 4, pady = 10)

    green_button = Radiobutton(button_frame,fg = 'green', bg = 'cyan', text = 'Green',  height = 3, width = 30, value = 'green', variable = curr_colour, indicatoron	= 0)
    green_button.grid(row = 5, pady = 10)




    def makeBox(canv,len):
        colour = cube[index]
        for i in range(9):
            canv.create_rectangle(box_loc[i][0],box_loc[i][1],box_loc[i][0]+len,box_loc[i][1]+len, fill = colour[i])
        canv.create_rectangle(box_loc[1][0],box_loc[1][1]-len/8,box_loc[1][0]+len,box_loc[1][1], fill = cube_faces[index][1])


    def find_box(x,y):
        index = -1
        for i in range(9):
            if box_loc[i][0]<x<box_loc[i][0]+len and box_loc[i][1]<y<box_loc[i][1]+len:
                index = i
                break
        return index


    def fill_colour(event):

        x = root.winfo_pointerx()-canvas.winfo_rootx()
        y = root.winfo_pointery()-canvas.winfo_rooty()
        #print((x,y))
        #print((canvas.winfo_rootx(),canvas.winfo_rooty()))
        if find_box(x,y)!=-1:
            i = find_box(x,y)
            if i!=4:
                canvas.create_rectangle(box_loc[i][0],box_loc[i][1],box_loc[i][0]+len,box_loc[i][1]+len, fill = curr_colour.get())
                curr_face[i] = curr_colour.get()

    def goBack():
        global index,curr_face
        if err:
            error.pack_forget()
        cube[index] = curr_face
        if index>0:
            index-=1
        makeBox(canvas,len)
        curr_face = cube[index]
        instruction = "Hold the rubik's cube such that the "+cube_faces[index][0]+" centre piece is facing you and the "+cube_faces[index][1]+" centre piece is on top.\n Fill in the colours on this face."
        instructions.config(text = instruction)
    def clearFace():
        for i in range(9):
            if i!=4:
                curr_face[i] = 'grey'
        makeBox(canvas,len)

    def goNext():
        global index,curr_face,err, cube_sol, cube_input
        go = 1
        for i in curr_face:
            if i=='grey':
                go = 0
        if go:
            if err:
                error.pack_forget()
            cube[index] = curr_face
            if index<5:
                index+=1
                makeBox(canvas,len)
                curr_face = cube[index]
                instruction = "Hold the rubik's cube such that the "+cube_faces[index][0]+" centre piece is facing you and the "+cube_faces[index][1]+" centre piece is on top.\n Fill in the colours on this face."
                instructions.config(text = instruction)
            else:
                cube_input = []
                for i in range(6):
                    face = []
                    for j in range(9):
                        cube[i][j]=cube[i][j][0]
                        face.append(cube[i][j][0])
                    cube_input.append(face)
                f=first_layer(cube)
                s=second_layer(cube)
                t=third_layer(cube)
                if type(f)==str or type(s)==str or type(t)==str:
                    err = 1
                    error.config(text = "Unsolvable cube!! It might be broken!!")
                    error.pack()
                else:
                    efficient(f)
                    efficient(s)
                    efficient(t)
                    cube_sol = f+s+t
                    root.destroy()
        else:
            error.pack()
            err = 1

    back_button = Button(lower_button_frame,fg = 'black', bg = 'grey', text = 'Back',  height = 3, width = 30, command = goBack)
    back_button.grid(row = 0, column = 0, padx = 10, pady = 10)

    clear_button = Button(lower_button_frame,fg = 'black', bg = 'grey', text = 'Clear',  height = 3, width = 30, command = clearFace)
    clear_button.grid(row = 0, column = 1, padx = 10, pady = 10)

    next_button = Button(lower_button_frame,fg = 'black', bg = 'grey', text = 'Next',  height = 3, width = 30, command = goNext)
    next_button.grid(row = 0, column = 2, padx = 10, pady = 10)



    root.bind('<Button-1>',fill_colour)
    makeBox(canvas,len)
    root.mainloop()

    return [cube_input,cube_sol]


def sol_cube(cube_input,cube_sol):
    global sol_index,just_front,cube_loc
    sol_index = 0
    just_front = 0

    def reverse_sol(sol):
        r_sol = []
        for step in sol:
            if len(step)==2:
                r_sol.append(step[0])
            else:
                r_sol.append(step+"'")
        return r_sol

    r_sol = reverse_sol(cube_sol)

    sol = Tk()
    c = Canvas(sol, width = 400, height = 400)
    c.grid(row = 0, column = 2)

    rubiks_cube = cube_3d.rubiks_cube
    cube_3d.colourCube(rubiks_cube,cube_input)
    cube2d = cube_3d.convert(rubiks_cube)
    cube_loc = cube_3d.draw_part_of_cube(cube2d[:3],c)

    def go_back():
        back_button.config(state = DISABLED)
        global sol_index,just_front,cube_loc
        if just_front:
            cube_loc = cube_3d.three_d_cube_moves(rubiks_cube,cube_input,0.5,[r_sol[sol_index]],c,cube_loc)
            just_front = 0
        elif sol_index!=0:
            sol_index-=1
            cube_loc = cube_3d.three_d_cube_moves(rubiks_cube,cube_input,0.5,[r_sol[sol_index]],c,cube_loc)
        back_button.config(state = NORMAL)

    def go_next():
        next_button.config(state = DISABLED)
        global sol_index,just_front,cube_loc
        if sol_index<len(cube_sol):
            if not(just_front):
                cube_loc = cube_3d.three_d_cube_moves(rubiks_cube,cube_input,0.5,[cube_sol[sol_index]],c,cube_loc)
                just_front = 1
            elif sol_index<len(cube_sol)-1:
                sol_index+=1
                cube_loc = cube_3d.three_d_cube_moves(rubiks_cube,cube_input,0.5,[cube_sol[sol_index]],c,cube_loc)
        next_button.config(state = NORMAL)

    def change_input():
        sol.destroy()
        main()
    back_button = Button(sol,fg = 'black', bg = 'grey', text = 'Back',  height = 3, width = 30, command = go_back)
    back_button.grid(row = 1, column = 0, padx = 10, pady = 10)

    change_button = Button(sol,fg = 'black', bg = 'grey', text = 'Change cube input',  height = 3, width = 30, command = change_input)
    change_button.grid(row = 1, column = 2, padx = 10, pady = 10)

    next_button = Button(sol,fg = 'black', bg = 'grey', text = 'Next',  height = 3, width = 30, default = DISABLED, command = go_next)
    next_button.grid(row = 1, column = 3, padx = 10, pady = 10)



    sol.mainloop()

def main():
    input_cube = takeInput()
    if input_cube[0][0][0]!='grey':
        sol_cube(input_cube[0],input_cube[1])

if __name__ =='__main__':
    main()
