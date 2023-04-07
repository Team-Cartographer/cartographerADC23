# ui -> User Interface Helper File
from __future__ import annotations
import PySimpleGUI as sg
from utils import show_error, are_you_sure
from os import getcwd, listdir
from sys import exit


def path_fetcher():
    layout = [
        [
            sg.FileBrowse("Upload Latitude File", size=(20, 1), key="-LatIN-", file_types=(("CSV file", "*.csv"),)),
            sg.Input(size=(100, 1), disabled=True)
        ], [
            sg.FileBrowse("Upload Longitude File", size=(20, 1), key="-LongIN-", file_types=(("CSV file", "*.csv"),)),
            sg.Input(size=(100, 1), disabled=True)
        ], [
            sg.FileBrowse("Upload Height File", size=(20, 1), key="-HeightIN-", file_types=(("CSV file", "*.csv"),)),
            sg.Input(size=(100, 1), disabled=True)
        ], [
            sg.FileBrowse("Upload Slope File", size=(20, 1), key="-SlopeIN-", file_types=(("CSV file", "*.csv"),)),
            sg.Input(size=(100, 1), disabled=True)
        ], [
            sg.OK("Submit")
        ],
    ]

    window = sg.Window("PathFetcher", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            show_error("No Pathing Given", "Ending Program")
            exit(0)
            break

        elif event == "Submit":
            # Latitude, Longitude, Height, Slope, Dist_Between_Points #
            window.close()
            return values["-LatIN-"], values["-LongIN-"], values["-HeightIN-"], values["-SlopeIN-"]


# noinspection PyPep8Naming
def get_pathfinding_endpoints(save):
    cur_state = 0  # 0 is no set, 1 is set start, 2 is set goal.
    # There should be an easier way to do this, but this works for now

    SIZE_CONSTANT = save.size

    start_circle_pos = None
    end_circle_pos = None
    layout = [

        [
            sg.Column(
                [[
                    sg.Graph(canvas_size=(500, 500), graph_top_right=(SIZE_CONSTANT, 0),
                             graph_bottom_left=(0, SIZE_CONSTANT),  # background_color=None,
                             key="-GraphIN-", enable_events=True, drag_submits=False)
                ]], justification="center")
        ],
        [
            sg.Text("Current Start Position:"),
            sg.Input(default_text="None", key="-StartOUT-", disabled=True),
            sg.Button("Set", key="-StartIN-", enable_events=True)
        ],
        [
            sg.Text("Current Goal Position:"),
            sg.Input(default_text="None", key="-GoalOUT-", disabled=True),
            sg.Button("Set", key="-GoalIN-", enable_events=True)
        ],
        [
            sg.Combo(["Moon Texture", "Slopemap", "Heightkey"], default_value="Moon Texture",
                     enable_events=True, key="-Map-"),
            sg.Checkbox("Add comm checkpoints?", default=False, key="-CommIN-"),
            sg.OK("Submit", key="-Submit-")
        ]
    ]

    window = sg.Window("A* UI", layout, finalize=True)
    window["-GraphIN-"].draw_image(save.interface_texture_image, location=(0, 0))

    while True:
        event, values = window.read(timeout=500)

        if event == "-Map-":
            map_canvas = values["-Map-"]

            if map_canvas == 'Moon Texture':
                window["-GraphIN-"].draw_image(save.interface_texture_image, location=(0, 0))
            elif map_canvas == 'Slopemap':
                window["-GraphIN-"].draw_image(save.interface_slopemap_image, location=(0, 0))
            elif map_canvas == 'Heightkey':
                window["-GraphIN-"].draw_image(save.interface_heightkey_image, location=(0, 0))
            if start_circle_pos is not None:
                window["-GraphIN-"].draw_circle(start_circle_pos, radius=10, fill_color="blue")
            if end_circle_pos is not None:
                window["-GraphIN-"].draw_circle(end_circle_pos, radius=10, fill_color="blue")

        if event == "-StartIN-":
            cur_state = 1

        if event == "-GoalIN-":
            cur_state = 2

        if event == "-GraphIN-":
            mouse_pos = values["-GraphIN-"]
            if cur_state == 1:
                window["-StartOUT-"].update(value=mouse_pos)
                start_circle_pos = mouse_pos
                map_canvas = values["-Map-"]

                if map_canvas == 'Moon Texture':
                    window["-GraphIN-"].draw_image(save.interface_texture_image, location=(0, 0))
                elif map_canvas == 'Slopemap':
                    window["-GraphIN-"].draw_image(save.interface_slopemap_image, location=(0, 0))
                elif map_canvas == 'Heightkey':
                    window["-GraphIN-"].draw_image(save.interface_heightkey_image, location=(0, 0))
                if start_circle_pos is not None:
                    window["-GraphIN-"].draw_circle(start_circle_pos, radius=10, fill_color="blue")
                if end_circle_pos is not None:
                    window["-GraphIN-"].draw_circle(end_circle_pos, radius=10, fill_color="blue")

                window["-GraphIN-"].draw_circle(start_circle_pos, radius=10, fill_color="blue")
                cur_state = 0

            if cur_state == 2:
                window["-GoalOUT-"].update(value=mouse_pos)
                end_circle_pos = mouse_pos
                map_canvas = values["-Map-"]

                if map_canvas == 'Moon Texture':
                    window["-GraphIN-"].draw_image(save.interface_texture_image, location=(0, 0))
                elif map_canvas == 'Slopemap':
                    window["-GraphIN-"].draw_image(save.interface_slopemap_image, location=(0, 0))
                elif map_canvas == 'Heightkey':
                    window["-GraphIN-"].draw_image(save.interface_heightkey_image, location=(0, 0))
                if start_circle_pos is not None:
                    window["-GraphIN-"].draw_circle(start_circle_pos, radius=10, fill_color="blue")
                if end_circle_pos is not None:
                    window["-GraphIN-"].draw_circle(end_circle_pos, radius=10, fill_color="blue")

                window["-GraphIN-"].draw_circle(end_circle_pos, radius=10, fill_color="blue")
                cur_state = 0

        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            raise TypeError("You closed A*")

        if event == "-Submit-":
            if are_you_sure("Endpoint Submission", "Are you sure these are the points you want?"):
                if values["-StartOUT-"] != "None" and values["-GoalOUT-"] != "None":
                    window.close()
                    return eval(values["-StartOUT-"]), eval(values["-GoalOUT-"]), bool(values["-CommIN-"])
                else:
                    show_error("Incomplete Data Error", "Please select a start and end point")


# on start functions and helper functions

def load_site() -> tuple[str | None, int]:
    save_folder = getcwd() + "/Saves"
    files = listdir(save_folder)

    if len(files) == 0:
        if are_you_sure("Save Loading Error", "No previous saves exist. Press OK to make a new save"):
            return None, 0
        else:
            exit(0)

    parsed_sites = []
    for file in files:
        parsed_sites.append(file.removeprefix("Save_"))

    layout = [
        [
            sg.Combo(parsed_sites, key="-FileIN-", default_value=parsed_sites[0]), sg.OK("Submit", key="-Submit-")
        ]
    ]

    window = sg.Window("Load Site", layout, finalize=True)
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            return None, 1

        if event == "-Submit-":
            window.close()
            return getcwd() + "/Saves/Save_" + values["-FileIN-"], 0


def on_start():
    layout = [
        [
            sg.Text("The Team Cartographer Lunar Visualizer")
        ],
        [
            sg.Button("Load a Site", key="-Load-"),
            sg.Button("New Site", key="-New-")
        ]
    ]
    window = sg.Window("Welcome", layout, element_justification='c', finalize=True)
    while True:
        event, values = window.read()
        if event == "-Load-":
            window.disappear()
            path, check = load_site()
            if check == 1:
                window.reappear()
            elif check == 0:
                window.close()
                return path
            else:
                show_error("Load Error", "Something went wrong, and we aren't sure what. Please contact a dev.")

        if event == "-New-":
            window.close()
            return None

        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            exit()


def new_site_name() -> str:
    layout = [
        [
            sg.Text("Insert site name "), sg.Input(key="-SaveNameIN-"), sg.OK("Submit")
        ]
    ]
    window = sg.Window("New Site Name", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            exit()

        elif event == "Submit":
            name = values["-SaveNameIN-"]
            invalids = r'#%&{}\$!:@;<>*?/+`|=' + '\"\''
            check = 0

            for letter in name:
                if letter in invalids:
                    show_error("Save Error", f"Invalid File Name, Please remove: {letter}")
                    check = 1
                    break

            if not check == 1:
                window.close()
                return name

            check -= 1
            window.reappear()


if __name__ == "__main__":
    # print(new_site_name())
    pass
