# ui -> User Interface Helper File

import PySimpleGUI as sg
from utils import show_error, are_you_sure


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
            break
        elif event == "Submit":
            # Latitude, Longitude, Height, Slope, Dist_Between_Points #
            return values["-LatIN-"], values["-LongIN-"], values["-HeightIN-"], values["-SlopeIN-"]


def get_pathfinding_endpoints(SIZE_CONSTANT, IMAGES_PATH):
    cur_state = 0  # 0 is no set, 1 is set start, 2 is set goal.
    # There should be an easier way to do this, but this works for now

    start_circle_pos = None
    end_circle_pos = None
    layout = [

        [
            sg.Graph(canvas_size=(500, 500), graph_top_right=(SIZE_CONSTANT, 0),
                     graph_bottom_left=(0, SIZE_CONSTANT), background_color="green",
                     key="-GraphIN-", enable_events=True, drag_submits=False)
        ],
        [
            sg.Text("Current Start Position:"),
            sg.Input(default_text="None", key="-StartOUT-", disabled=True),
            sg.Button("Set", key="-StartIN-", enable_events=True)
        ],
        [
            sg.Text("Current Start Position:"),
            sg.Input(default_text="None", key="-GoalOUT-", disabled=True),
            sg.Button("Set", key="-GoalIN-", enable_events=True)
        ],
        [
            sg.Combo(["Moon Texture", "Slopemap", "Heightkey"], default_value="Moon Texture",
                     enable_events=True, key="-Map-"),
            sg.OK("Submit", key="-Submit-")
        ]
    ]

    window = sg.Window("PathFetcher", layout, finalize=True)
    window["-GraphIN-"].draw_image(IMAGES_PATH + "/interface_texture.png", location=(0, 0))

    while True:
        event, values = window.read(timeout=500)

        if event == "-Map-":
            map_canvas = values["-Map-"]

            if map_canvas == 'Moon Texture':
                window["-GraphIN-"].draw_image(IMAGES_PATH + "/interface_texture.png", location=(0, 0))
            elif map_canvas == 'Slopemap':
                window["-GraphIN-"].draw_image(IMAGES_PATH + "/interface_slopemap.png", location=(0, 0))
            elif map_canvas == 'Heightkey':
                window["-GraphIN-"].draw_image(IMAGES_PATH + "/interface_heightkey.png", location=(0, 0))
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
                    window["-GraphIN-"].draw_image(images_path + "/interface_texture.png", location=(0, 0))
                elif map_canvas == 'Slopemap':
                    window["-GraphIN-"].draw_image(images_path + "/interface_slopemap.png", location=(0, 0))
                elif map_canvas == 'Heightkey':
                    window["-GraphIN-"].draw_image(images_path + "/interface_heightkey.png", location=(0, 0))
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
                    window["-GraphIN-"].draw_image(images_path + "/interface_texture.png", location=(0, 0))
                elif map_canvas == 'Slopemap':
                    window["-GraphIN-"].draw_image(images_path + "/interface_slopemap.png", location=(0, 0))
                elif map_canvas == 'Heightkey':
                    window["-GraphIN-"].draw_image(images_path + "/interface_heightkey.png", location=(0, 0))
                if start_circle_pos is not None:
                    window["-GraphIN-"].draw_circle(start_circle_pos, radius=10, fill_color="blue")
                if end_circle_pos is not None:
                    window["-GraphIN-"].draw_circle(end_circle_pos, radius=10, fill_color="blue")

                window["-GraphIN-"].draw_circle(end_circle_pos, radius=10, fill_color="blue")
                cur_state = 0

        if event == sg.WIN_CLOSED or event == "Exit":
            show_error("Incomplete Data Error", "By exiting the Pathfinding UI, A* did not receive endpoints for "
                                                "pathfinding. Please manually run programs or use the Launcher again.")
            return None

        if event == "-Submit-":
            if are_you_sure("Endpoint Submission", "Are you sure these are the points you want?"):
                if values["-StartOUT-"] != "None" and values["-GoalOUT-"] != "None":
                    window.close()
                    return eval(values["-StartOUT-"]), eval(values["-GoalOUT-"])
                else:
                    show_error("Incomplete Data Error", "Please select a start and end point")


if __name__ == "__main__":
    # path_fetcher()
    # get_pathfinding_endpoints()
    pass
