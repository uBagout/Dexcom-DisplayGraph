# Dexcom-DisplayGraph
Minimalistic Graph Overlay that plots Dexcom data to screen, convenient for focusing on tasks as checking phone for dexcom data is no longer required, minimising potential distractions.
It does not block clicking, except on the icon used to drag the graph around into position.
The graph stays on the top level of your screen and you should see it at all times, unless you are inside a fullscreen application.
Keep it superimposed ontop a white background for the most aesthetic interface.

I personally use this to help me study without having to look at my phone to view my dexcom data.
![ezgif-4-a740b1b922](https://user-images.githubusercontent.com/59146220/171528206-28f7dbd1-646d-4749-ae5b-6b532a32fb56.gif)

I encourage any suggestions/pull requests to fix the white outline that surrounds all elements on the graph, though I believe this would require a module change (from Tkinter).

To use this, you need to install pydexcom - https://github.com/gagebenne/pydexcom  
And insert your dexcom account information inside the .env file. 

This project is done in mmol/L units, but it does not affect the graph if your country primarily uses mg/dL.
If you intend on changing the height of the hyper/hypo bars you will need to convert into mmol/L. 1 mmol/L = 18 mg/dL

Beware that if no one follows you through the share API your dexcom application will not upload data to it.
If you do not have anyone following you through the share API you can download the dexcom follow app and invite yourself to make sure your data gets uploaded.

I intend to work on this every now and then, I have more ideas to implement, especially for ease of use.
