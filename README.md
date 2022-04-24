
**Det**ector **Ex**posure **Cal**culator: **DetExCal** 
 


**DetExCal** is a simple SNR calculator with convinient GUI interface. It can calculate SNR vs. time and SNR vs. V-band magnitude. 



**Developer**

* Trifon Trifonov, MPIA Heidelberg.

 


Please keep in mind that this software is developed mostly for my needs and fun. I hope, however, that you may find it capable of solving your scientific problems, too. At the moment, there is NO documentation,
but as you will find, the GUI is self-explanatory.   

Feedback and help in further development will be highly appreciated!
A wish-list with your favorite tools and methods to be implemented is also welcome!    

Just open an "Issue" on the GitHub, or send a PM to trifonov@mpia.de.    


**Installation**

$ pip install git+https://github.com/3fon3fonov/DetExCal   

or git clone:

$ git clone https://github.com/3fon3fonov/DetExCal   
$ cd DetExCal   
$ python setup.py install   

However, please read the [Installation instructions](README_for_installation),
because some problems may occur depending on your OS system.   

Python3.6+ is strongly recommended. 

**Usage**

* To load the GUI, on a bash shell type: 

$ DetExCal (in case of pip install)

* or just do:

$ python DetExCal.py (inside of the git clone directory)
 


* If you want to use the library on the Python shell/script

In [1]: import DetExCal

* or e.g., to load the RV routines:

In [1]: import DetExCal   
     

**Credit**

If you made the use of DetExCal, make me happy and let me know :))) 
 

* The interactive plotting is done with a custom version of the "pyqtgraph": 

http://www.pyqtgraph.org/

* Additionally, DetExCal uses "standard" Python libraries like 
"PyQt5",  "numpy",  and  "dill".

 
