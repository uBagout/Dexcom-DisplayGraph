# Dexcom-DisplayGraph
Graph overlay that plots Dexcom data to pc screen, convenient for focusing on tasks whilst avoiding phone distraction.
It does not block clicking, except on the grid used to drag the graph around into position.

I personally use this to help me study without having to look at my phone to view my dexcom data.
![ezgif-4-232921c404](https://user-images.githubusercontent.com/59146220/169684683-453ff356-c556-4b92-9a4f-c3d1b3c1db3e.gif)
(Yes, it does move that slow on your screen. Feel free to suggest on how I can better smoothen the movement of the graph)

To use this, you need to install pydexcom - https://github.com/gagebenne/pydexcom

This project is done in mmol/L units, but it does not affect the graph if your country primarily uses mg/dL.
If you intend on changing the height of the hyper/hypo bars you will need to convert into mmol/L. 1 mmol/L = 18 mg/dL

Beware that if no one follows you through the share API your dexcom application will not upload data to it.
If you do not have anyone following you through the share API you can download the dexcom follow app and invite yourself to make sure your data gets uploaded.

I intend to work on this every now and then, I have more ideas to implement, especially for ease of use.