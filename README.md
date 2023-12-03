# Music Suite

## Pet project

### Setting up the environment

In the task it is recommended to use Python as a programming language since it is important for the data scientists. Since I'm most fluently with R and JS right now I try to bridge Python code (to learn something new) with JS to use my skills in GUI design.

Pyglet seems to be a proper framework to catch multiple key presses and play multiple sounds at once so it might be useful for the live music app part of this project. But can it be integrated in the browsers view port? I will try Pyodide for this.

It might be better to not use a JS-Python bridge for easyness. Maybe this is just a architectural burden. The data processing and visualisation part might be low in this project and so Python benefits might be not used at all.

In the end I decided to go with the pyglet framework for the accordion simulator and don't use Pyodide for building the online dashboard structure because the accordion simulator might become handy for my hobby.

### Accordion Simulator

Right now you can press buttons on your computer keyboard which are mapped to the buttons of an button accordion with b-grip. The correct tone - sampled from a VST instrument - will get played while a button is pressed.

Things to add:

* display which notes are played on the staff
* show how the accord is named that is played when pressing multiple buttons
* import a music sheet and 
    * play it
    * color the button that should be pressed right now (help to learning play)

It would be aesome if there could be something like in Guitar Hero where notes move toward a play area and have to be pressed at the right time.

## The big idea

### UML diagrams

This use case diagram shows the whole music suite. The accordion simulator should be one of many simulators and should be used to

* practice
* play music together
* compose music
* analyse music

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
actor user
actor student
actor "music teacher" as teacher
actor manager
actor developer
actor support
user <|-- teacher
user <|-- student
rectangle "Music Learning Suite" as MLS {
  together {
    user --> (analyse music)
    user --> (compose music)
    student --> (learn music theory)
    user --> (rent a midi instrument)
    user --> (share compositions)
    student --> (book lessons)
    user --> (practice)
    user --> (play music together)
    teacher --> (billing)
    teacher --> (offer lessons)
    teacher --> (create learning content)
  }

  together {
    (accessing learning\npath information) <-- developer
    (add new instrument) <-- developer
    (managing user information) <-- support
    (seeing buisness stats) <-- manager
  }

  (analyse music) -[hidden]- (add new instrument)
}
@enduml
```

Beside the simulator a LMS would be handy to organize learning material by music teachers. Also a backend dashboard for accounting, business insights etc. is needed. Everything might be accessed by a unified dashboard where you have to log in first before accessing the services your role grants you access to or start a instrument simulator. A first draft is shown in this component diagram:

```plantuml
@startuml
database "MySQL" {
    [user data]
    [course data]
    [lessons]
}

component "Music Suite" {
    [Music Analyser]
    [Instrument Simulator]
}

[Accountmanagement] --> [user data]
[Authentification] --> [user data]
[Authentification] -- [Dashboard GUI]
[Lesson Booking] -- [Dashboard GUI]
[Learning Package] -- [Dashboard GUI]
[Learning Package] --> [course data]
[Learning Package] -- [lessons]
[Buisness Inteligence] -- [Dashboard GUI]
[Accountmanagement] -- [Dashboard GUI]
[Database Manager] -- [Dashboard GUI]
[Accounting] -- [Dashboard GUI]

[Music Suite] -- [Dashboard GUI]
@enduml
```

In the class diagram you find the classes of the accordion simulator and the used classes from pyglet and their depenencies:

```mermaid
---
title: Accordion Simulator
---
classDiagram
    ShapeBase <|-- Circle
    BorderedCircle "1" o-- "2" Circle
    Button "1" o-- "1" BorderedCircle
    Button "1" o-- "1" Label
    DocumentLabel <|-- Label
    ButtonBoard "1" o-- "*" Button
    TonePlayer "1" o-- "1" Player
    Window "1" -- "*" TonePlayer : controls
    Window "1" -- "1" ButtonBoard : controls
    ButtonBoard "1" -- "1" Batch

    namespace accordionSimulator {
        class BorderedCircle {
            +circle : Circle
            +innerCircle : Circle
            +changeFill()
        }
        
        class Button {
            +fill : int tuple
            +borderedCircle : BorderedCircle
            +label : Label
            +tone : int
            +pressButton()
            +releaseButton()
        }

        class ButtonBoard {
            +x : float
            +y : float
            +width : float
            +height : float
            +startingTone : int
            +buttonList : Button[]
            +pressButton()
            +releaseButton()
        }

        class TonePlayer {
            +midiTone : int
            +player : Player
            +music : Source
            +playTone()
            +stopTone()
            +getMidiTone()
        }
    }

    namespace pyglet {
        class Window {
            +width
            +height
            +caption
            +resizable
            +style
            +fullscreen
            +visible
            +vsynch
            +file_drops
            +display
            +screen
            +config
            +context
            +mode
            +activate()
            +clear()
            +close()
            +dispatch_event()
            +dispatch_events()
            +draw_mouse_cursor()
            +flip()
            +on_draw()
            +on_key_press()
            +on_key_release()
            ...
        }

        class Batch {
            +draw()
            +draw_subset()
            +get_domain()
            +invalidate()
            +migrate()
        }

        class Player {
            +play()
            +pause()
            +queue()
            +delete()
            ...
        }

            class Label {

        }

        class DocumentLabel {
            +bold : bool
            +font_name : str
            +font_size : float
            +opacity : int
            +text : str
            +get_style()
            +set_style()
        }

        class ShapeBase {
            +x : float
            +y : float
            +position : float tuple
            +rotation: flaot
            +anchor_x : float
            +anchor_y : float
            +anchor_position : float tuple
            +color : int tuple
            +opacity : int
            +visible : bool
            +batch : Batch
            +group : Group
            +draw()
            +delete()
        }

        class Circle {
            +radius : float
        }
    }
```