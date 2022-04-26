
**Det**ector **Ex**posure **Cal**culator: **DetExCal** 
 

<p align="center">
  <img width="400" src=".docs/DetExCal.jpg">   <img width="400" src=".docs/DetExCal_2.jpg">
</p>
 
**DetExCal** is a simple CCD-SNR calculator with a convenient GUI interface. It can calculate SNR vs. time and SNR vs. V-band magnitude. 



**Developer**

* Trifon Trifonov, MPIA Heidelberg.

 
Please keep in mind that this software is developed mainly for my needs and for fun. I hope, however, that you may find it capable of solving your scientific problems, too. At the moment, there is NO documentation,
but as you will find, the GUI is self-explanatory.   

Feedback and help in further development will be highly appreciated!
A wish list with your favorite tools and methods to be implemented is also welcome!    

Just open an "Issue" on the GitHub, or send a PM to trifonov@mpia.de.    


**Installation**

Python3.6+ is strongly recommended. 

$ pip3 install git+https://github.com/3fon3fonov/DetExCal   

or git clone:

$ git clone https://github.com/3fon3fonov/DetExCal   
$ cd DetExCal   
$ python3 setup.py install   

Then, to load the GUI, on a bash shell type: 

$ DetExCal 


or, after git clone, simply:

$ git clone https://github.com/3fon3fonov/DetExCal   
$ cd DetExCal   
$ python3 DetExCal.py 



 

**Credit**

If you made the use of DetExCal, make me happy and let me know :))) 
 

* The interactive plotting is done with a custom version of the "pyqtgraph": 

http://www.pyqtgraph.org/

* Additionally, DetExCal uses "standard" Python libraries like 
"PyQt5", "numpy", and "scipy".

 
