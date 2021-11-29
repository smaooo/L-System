# L-System Tree Generator Blender Add-On
L-System Tree Generator is an add-on that produces different types of trees based on the given 

[L-System](https://en.wikipedia.org/wiki/L-system) (which is limited to only 8 systems in this version). This add-on gives you the ability to generate different tree forms from a single system using different variables and drivers.



## Installation

For installing this add-on inside Blender download the [L-System.zip](https://github.com/smaooo/L-System/raw/main/L-System.zip) and install it using the following steps:

1. Select the Edit menu from the top toolbar and then select Preferences from the menu.

   ![Screenshot (53)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(53).png)

2. In the Blender Preference select the Add-ons section from the left sidebar. 

   ![Screenshot (54)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(54).png)

3. Select the In![Screenshot (56)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(56).png)stall... from top the Preferences.

4. Navigate to the download location of the [L-System.zip](https://github.com/smaooo/L-System/blob/main/L-System.zip) and select it and press the Install Add-on.

   ![Screenshot (57)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(57).png)

5. Now using "Shift + A" or from the Add menu in you can add a tree.

   ![Screenshot (58)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(58).png)

6. After adding tree a panel would open on the left side of the UI which gives you different options and drivers for the tree generation (if the panel is collapsed, click on it to open it up).

   ![Screenshot (60)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(60).png)



## How to use!



https://user-images.githubusercontent.com/31223968/143862479-bee888b3-21d6-42c4-86f2-3bba75c30d06.mp4



- For generating a tree, you have to press on the "Generate" button.

  ![image-20211129031109113](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129031109113.png)

  You can also select the "Real-time" option on the top, but it is not recommended, because in higher Generations number the mesh could get complicated which could result in the freezing the Blender.

- Using the "System" drop-down menu, you can switch between 8 different implemented systems.

  ![Screenshot (61)](https://github.com/smaooo/L-System/blob/main/imgs/Screenshot%20(61).png)

- The 2D / 3D button toggle between 2D and 3D form of generated tree.

- With increasing the "Generations" number, the tree would grow and the number of branches would increase. **Caution:** increment this variable with caution and step-by-step, otherwise it could result in Blender freezing.

- The "Angle" variable would define the rotation angle between branches.

- The "Draw Length" variable would define the distance between each vertex in the generate object. **Caution** : do not misinterpret this variable with scale!

- The "Show Mesh" check box would create surfaces around the vertices.

  ![image-20211129032526609](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032526609.png)

- The "Thickness" variable would appear when the "Show Mesh" option is active. It will define the general thickness factor of the mesh.

- The "Style" menu gives you the ability to switch the mesh style to a jagged stylized look.

- The "Show Leaves" check box would add leaves to the tree.

- The "Leaf Count" variable is a multiplication factor for the number of leaves on the tree.

- The "Leaf Size" variable is a scaling factor for the general scale of the leaves on the tree. 



## Tip

- If you accidentally clicked on the screen or on the panel and the panel closed, you can open up the panel again using **F9**.

## Examples

### 	2D Generated Trees

​		![image-20211129032719374](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032719374.png)![image-20211129032741952](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032741952.png)![image-20211129032812972](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032812972.png)

![image-20211129032831713](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032831713.png)![image-20211129032926989](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032926989.png)![image-20211129032950554](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129032950554.png)

![image-20211129033002787](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033002787.png)![image-20211129033022490](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033022490.png)



### 	3D Generated Trees

![image-20211129033103681](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033103681.png)![image-20211129033118534](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033118534.png)

![image-20211129033142336](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033142336.png)![image-20211129033158020](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033158020.png)

![image-20211129033213404](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033213404.png)![image-20211129033231901](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033241613.png)



![image-20211129033307382](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033307382.png)![image-20211129033354355](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033354355.png)

![image-20211129033404748](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033412756.png)![image-20211129033435234](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033435234.png)

![image-20211129033450083](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033450083.png)

![image-20211129033459318](https://github.com/smaooo/L-System/blob/main/imgs/image-20211129033459318.png)
