#!/usr/bin/python3
__author__ = 'Trifon Trifonov'

import time 
from pathos.multiprocessing import freeze_support
freeze_support()

import numpy as np
import sys, os, traceback 
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import webbrowser
 
es_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(es_path, 'lib')

print(lib_path)
sys.path.insert(0,lib_path)
os.chdir(os.path.dirname(os.path.abspath(__file__)))


if QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
sys.excepthook = excepthook

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

import pyqtgraph as pg
 
from print_info_window import print_info
from symbols_window import show_symbols
 
#import terminal
import ntpath
import pg_hack

from scipy.signal import argrelextrema
from scipy.stats.stats import pearsonr   
import scipy.stats as stat
from scipy.interpolate import interp1d
 
import dill
dill._dill._reverse_typemap['ObjectType'] = object
#os.system("taskset -p %s" %os.getpid())
os.environ["OPENBLAS_MAIN_FREE"] = "1"
#os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_DEVICE_PIXEL_RATIO"] = "1"
 

try:
    from DetExCal import Ui_MainWindow 
except (ImportError, KeyError) as e:
    qtCreatorFile = "%s/UI/DetExCal.ui"%lib_path 
    Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

 
pg.setConfigOption('background', '#ffffff')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)
#pg.setConfigOptions(useOpenGL=True) 




global colors
#arguments = len(sys.argv) - 1

#if '-debug' in sys.argv:
#    debug = True
#else:
#    debug = False
 
colors           = ['#0066ff','#ff0000','#66ff66','#00ffff','#cc33ff','#ff9900','#cccc00','#3399ff','#990033','#339933','#ff0000']               
symbols = ['o','t','t1','t2','t3','s','p','h','star','+','d'] 


QtWidgets.QApplication.processEvents()



class DetExCal(QtWidgets.QMainWindow, Ui_MainWindow):    
 



################################## System #######################################


    def set_Win_widget_Style(self, widget):
        QtWidgets.QApplication.setStyle(QtGui.QStyleFactory.create('Windows'))
    def set_Fus_widget_Style(self, widget):
        QtWidgets.QApplication.setStyle(QtGui.QStyleFactory.create('Fusion'))
    def set_Mac_widget_Style(self, widget):
        if sys.platform != "darwin":
            self.tabWidget_helper.setCurrentWidget(self.tab_info)
            print("\n 'Macintosh' window style is only available on MAC OS !!!\n")
            return
        else:
            QtWidgets.QApplication.setStyle(QtGui.QStyleFactory.create('Macintosh'))

    def initialize_color_dialog(self):

        self.colorDialog = QtWidgets.QColorDialog()
        self.colorDialog.setOption(QtWidgets.QColorDialog.ShowAlphaChannel, True)
        self.colorDialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog, True)

################################## Plots #######################################

    def initialize_plots(self):
        global p1,p2

        p1  = self.graphicsView_CCD_SNR
        p2  = self.graphicsView_CCD_SNR_2

        xaxis = ['Integration time [sec.]','V-band magnitude']
        yaxis = ['SNR','SNR']
        xunit = ['','']
        yunit = ['','']

        zzz = [p1,p2]

        for i in range(len(zzz)):

            zzz[i].setAxisItems({'bottom': pg_hack.CustomAxisItem('bottom')})
            #zzz[i].getAxis("bottom").tickFont = self.plot_font
            zzz[i].getAxis("bottom").setStyle(tickTextOffset = 12, tickFont = self.plot_font)
            zzz[i].getAxis("top").setStyle(tickTextOffset = 12, tickFont = self.plot_font)
            zzz[i].getAxis("left").setStyle(tickTextOffset = 12, tickFont = self.plot_font)
            zzz[i].getAxis("right").setStyle(tickTextOffset = 12, tickFont = self.plot_font)
            zzz[i].getAxis('left').setWidth(50)
            zzz[i].getAxis('right').setWidth(10)
            zzz[i].getAxis('top').setHeight(10)
            zzz[i].getAxis('bottom').setHeight(50)
                        
            zzz[i].setLabel('bottom', '%s'%xaxis[i], units='%s'%xunit[i],  **{'font-size':self.plot_font.pointSize()})
            zzz[i].setLabel('left',   '%s'%yaxis[i], units='%s'%yunit[i],  **{'font-size':self.plot_font.pointSize()})       
            zzz[i].showAxis('top') 
            zzz[i].showAxis('right') 
            zzz[i].getAxis('bottom').enableAutoSIPrefix(enable=False)
            #zzz[i].autoRange()
            zzz[i].getViewBox().parentItem().ctrlMenu.actions()[-4].setVisible(False) #removes the "Avarage" junk

        #p1.getViewBox().setAspectLocked(True)
        p1.showGrid(x=True, y=True,alpha=0.2)
        p2.showGrid(x=True, y=True,alpha=0.2) 

        return



    def set_widget_font(self, widget):

        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            QtWidgets.QApplication.setFont(font)

            for topLevel in QtWidgets.QApplication.allWidgets():
                topLevel.setFont(font)
 
    def set_plot_font(self):

        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.plot_font.setFamily(font.family())
            self.plot_font.setPointSize(font.pointSize())
          
        self.update_font_plots()   

            
    def initialize_font_plot(self):  

        self.plot_font = QtGui.QFont()
        self.plot_font.setPointSize(9)
        self.plot_font.setBold(False)
              

    def closeEvent(self, event):

        choice = QtWidgets.QMessageBox.information(self, 'Warning!',
                                            "Do you want to Quit?",
                                            QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes)

        if choice == QtWidgets.QMessageBox.Yes:
            self.removeEventFilter(self)
            event.accept()

        elif choice == QtWidgets.QMessageBox.Cancel:
            event.ignore()

################################## View Actions #######################################

    def grab_screen(self):
        p = QtWidgets.QWidget.grab(self)
 
        img, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Save image",
                                            filter="PNG(*.png);; JPEG(*.jpg)", options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if img[-3:] == "png":
            p.save(img, "png")
        elif img[-3:] == "jpg":
            p.save(img, "jpg")


    def print_info_credits(self, image=False, es_version='0.01'):
 
        self.dialog_credits.setFixedSize(700, 700)
        self.dialog_credits.setWindowTitle('Credits')  
 
        text = ''
        self.dialog_credits.text.setText(text) 
        
        text = "You are using 'The DetExCal' (ver. %s) \n developed by Trifon Trifonov"%es_version
        
        self.dialog_credits.text.append(text)

        text = "\n"*15 +"CREDITS:"+"\n"*2 + "This tool uses the publically \n available packages: \n" 
        self.dialog_credits.text.append(text)
        
        text = "* " + "<a href='https://github.com/pyqtgraph/pyqtgraph'>pyqtgraph</a>"
        self.dialog_credits.text.append(text)

        text = "(And many 'standard' Python libraries like \n PyQt5, matplotlib, numpy, scipy, and pathos) \n" 
        self.dialog_credits.text.append(text)   
        
        text = "\n"*5 + """Note:
Please keep in mind that this software is developed 
mostly for my needs and for fun. I hope, however, 
that you may find it capable of solving your scientific 
problems, too.

Feedback and help in further development 
will be highly appreciated!
"""
        self.dialog_credits.text.append(text)
        self.dialog_credits.text.setReadOnly(True)       
        self.dialog_credits.show()

######################## Plot Opt. ######################################

    def get_model_color(self):

        #but_ind = self.buttonGroup_color_picker.checkedId()
        colorz = self.colorDialog.getColor(options=QtWidgets.QColorDialog.DontUseNativeDialog) #|QtWidgets.QColorDialog.ShowAlphaChannel,)
 
        if colorz.isValid():
            colors[-1]=colorz.name()  
            self.update_color_picker()
            self.update_SNR_plot()
 
        else:
            return

    def update_color_picker(self):

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)

        #for i in range(11):
        self.snr_model_color.setStyleSheet("color: %s;"%colors[-1])
        self.snr_model_color.setText("%s"%colors[-1])
        self.snr_model_color.setFont(font)
 
######################## Cross hair and label picks ######################################


    def cross_hair(self, plot_wg, log=False, alias = [False, 365.250,'#666699']):

        vLine = pg.InfiniteLine(angle=90, movable=False)#, pos=0)
        hLine = pg.InfiniteLine(angle=0,  movable=False)#, pos=2450000)
        plot_wg.addItem(vLine, ignoreBounds=True)
        plot_wg.addItem(hLine, ignoreBounds=True)
        label = pg.TextItem()

        plot_wg.addItem(label, ignoreBounds=True)  
         
        vb = plot_wg.getViewBox()   
        viewrange = vb.viewRange()
        
        if alias[0] == True:
            v2aLine = pg.InfiniteLine(angle=90, movable=False, pen=alias[2])#, pos=0)
            v2bLine = pg.InfiniteLine(angle=90, movable=False, pen=alias[2])#, pos=0)

            plot_wg.addItem(v2aLine, ignoreBounds=True)
            plot_wg.addItem(v2bLine, ignoreBounds=True)

            v3aLine = pg.InfiniteLine(angle=90, movable=False, pen=alias[2])#, pos=0)
            v3bLine = pg.InfiniteLine(angle=90, movable=False, pen=alias[2])#, pos=0)

            plot_wg.addItem(v3aLine, ignoreBounds=True)
            plot_wg.addItem(v3bLine, ignoreBounds=True)

        def mouseMoved(evt):

            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if plot_wg.sceneBoundingRect().contains(pos):

                mousePoint = vb.mapSceneToView(pos)

                if log == True:
                    label.setText("x=%0.3f,  y=%0.3f"%(10**mousePoint.x(), mousePoint.y()))
                else:
                    label.setText("x=%0.3f,  y=%0.3f"%(mousePoint.x(), mousePoint.y()))
                    #label.rotateAxis=(1, 0)

                vLine.setPos(mousePoint.x())
                hLine.setPos(mousePoint.y())
                
                if alias[0] == True:
                    if log == True:
                        v2aLine.setPos(np.log10((1.0 / ( (1.0/(10**mousePoint.x()) ) + 1.0/alias[1] )) ))
                        v2bLine.setPos(np.log10((1.0 / ( (1.0/(10**mousePoint.x()) ) - 1.0/alias[1] )) ))
                        v3aLine.setPos(np.log10((1.0 / ( 1.0/alias[1] + (1.0/(10**mousePoint.x()) ) )) ))
                        v3bLine.setPos(np.log10((1.0 / ( 1.0/alias[1] - (1.0/(10**mousePoint.x()) ) )) ))
                    else:
                        v2aLine.setPos(  (mousePoint.x()  + 1.0/alias[1]) )  
                        v2bLine.setPos(  (mousePoint.x()  - 1.0/alias[1]) )  
                        v3aLine.setPos(  (1.0/alias[1] + mousePoint.x() ))   
                        v3bLine.setPos(  (1.0/alias[1] - mousePoint.x() ))                         
                        

                if mousePoint.x() < (viewrange[0][1]+viewrange[0][0])/2.0:
                    label.setAnchor((0,1))
                else:
                    label.setAnchor((1,1))
                label.setPos(mousePoint.x(), mousePoint.y())
                #fit.label = label

        plot_wg.getViewBox().setAutoVisible(y=True)

        proxy = pg.SignalProxy(plot_wg.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
        plot_wg.proxy = proxy

    def cross_hair_remove(self, plot_wg):
 
        for kk in plot_wg.items():
            if kk.__class__.__name__ == "InfiniteLine":
                if kk._name != "zero":
                    plot_wg.removeItem(kk)
            elif kk.__class__.__name__ == "TextItem":
                plot_wg.removeItem(kk)
                
    def mag2flux(self,magnitude):
        return 9.6e10*(10**(-magnitude/2.5))

    def flux2mag(self,flux):
        return -2.5*np.log10(flux/9.6e10)



    def update_SNR_plot(self):
        global p1,p2
 
        if not self.hold_old_plot.isChecked():    
            p1.plot(clear=True,)
            p2.plot(clear=True,)
        else:
            p1.plot(clear=False,)
            p2.plot(clear=False,)

        #p1.addLine(x=None, y=0,   pen=pg.mkPen('#ff9933', width=0.8))
        time       = np.arange(1,self.Max_int_time.value(),1)
        magnitudes = np.arange(0,self.V_band.value()+0.1,0.1)

        flux = self.mag2flux(self.V_band.value()) #airmass?
        bgr  = self.mag2flux(self.Sky.value() -2.5*np.log10((self.CCD_px.value()/self.plate_scale.value())**2))  
     
        npix = np.pi* (self.seeing.value()* self.plate_scale.value() / self.CCD_px.value() ) **2
        dark_current = self.mag2flux(self.Dark_current.value())

        signal  = flux*(np.pi*self.Aperture.value()**2)*(self.Throughput.value()/100.0)*(self.Bandwidth.value()/1000.0)*self.Quant_eff.value()
        bg_noise = bgr*(np.pi*self.Aperture.value()**2)*(self.Throughput.value()/100.0)*(self.Bandwidth.value()/1000.0)*self.Quant_eff.value()
        Idc       = dark_current*self.seeing.value()* self.plate_scale.value()
        readnoise = self.Read_noise.value()*self.seeing.value()* self.plate_scale.value()

        snr_vs_time = self.ccd_SNR_vs_time(signal=signal,bgnd=bg_noise, Idc =Idc, time=time, readnoise=readnoise, npix=npix)

        model_curve = p1.plot(time,snr_vs_time, 
        pen={'color': colors[-1], 'width': self.rv_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
        viewRect=True, labels =  {'left':'RV', 'bottom':'JD'}) 
        
        model_curve.setZValue(self.RV_model_z.value()) 

        snr_vs_mag = self.ccd_SNR_vs_mag(signal=signal,bgnd=bg_noise, Idc =Idc, time=self.Max_int_time.value(), readnoise=readnoise, npix=npix,mag=magnitudes)

        model_curve_mag = p2.plot(magnitudes,snr_vs_mag, 
        pen={'color': colors[-1], 'width': self.rv_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
        viewRect=True, labels =  {'left':'RV', 'bottom':'JD'}) 
        
        model_curve_mag.setZValue(self.RV_model_z.value()) 
 
        p2.getViewBox().invertX(True)
        p2.setYRange(0, snr_vs_mag[int((self.V_band.value() - self.V_band.value()-3)*10)], padding=0.01)
        p2.setXRange(self.V_band.value()-3, self.V_band.value(), padding=0.01) 

        if self.SNR_plot_autorange.isChecked():
            p1.autoRange() #padding=0
            p2.autoRange() 
        if self.SNR_plot_cross_hair.isChecked():
            self.cross_hair(p1,log=False)  
        if self.SNR_plot_cross_hair_2.isChecked():
            self.cross_hair(p2,log=False)  


 
    def ccd_SNR_vs_time(self,signal=1,bgnd=0,readnoise=0,Idc=0,npix=1,time=1,gain=1):
        """
        This is the famous CCD equation.
        """
        snr = []
        time = np.asarray(time)
        warnings.filterwarnings("error")
 
        try:        
            for i in range(len(time)):
                CtG = signal*gain*time[i]
                snr.append(CtG/(np.sqrt( (signal+bgnd*npix+Idc*npix)*time[i]+(readnoise**2)*npix )))                
        except RuntimeWarning:
            print("Error: cannot handle time = 0. Try again.")
        return np.array(snr)

    def ccd_SNR_vs_mag(self,signal=1,bgnd=0,readnoise=0,Idc=0,npix=1,time=1,gain=1,mag=0):
        """
        This is the famous CCD equation.
        """
        snr = []
        mag = np.asarray(mag)
        warnings.filterwarnings("error")
         
        try:        
            for i in range(len(mag)):
                flux = self.mag2flux(mag[i]) #airmass?
                signal  = flux*(np.pi*self.Aperture.value()**2)*(self.Throughput.value()/100.0)*(self.Bandwidth.value()/1000.0)*self.Quant_eff.value()
                CtG = signal*gain*time
                snr.append(CtG/(np.sqrt( (signal+bgnd*npix+Idc*npix)*time+(readnoise**2)*npix )))                
        except RuntimeWarning:
            print("Error: cannot handle time = 0. Try again.")
        return np.array(snr)

 
################################################################################################

 

    def __init__(self):
        
        DEC_version = "0.01"
 
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
 
        self.setupUi(self)
        self.initialize_font_plot()
        self.initialize_plots()

        #################### credits  ########################
        
        self.dialog           = print_info(self)
        self.dialog_credits   = print_info(self) 
        self.initialize_color_dialog()

        ############ Set Widget Style #################

        self.actionWindows.triggered.connect(self.set_Win_widget_Style)
        self.actionMacintosh.triggered.connect(self.set_Mac_widget_Style)
        self.actionLinux_Fusion.triggered.connect(self.set_Fus_widget_Style)

        self.actionSet_GUI_Font.triggered.connect(self.set_widget_font)
        self.actionSet_plots_font.triggered.connect(self.set_plot_font) 


        self.actiongrab_screen.triggered.connect(self.grab_screen) 
        self.actionvisit_DEC_on_GitHub.triggered.connect(lambda: webbrowser.open('https://github.com/3fon3fonov/DetExCal'))
        self.actionCredits.triggered.connect(lambda: self.print_info_credits())

 
        self.update_SNR_plot()

        self.SNR_plot_cross_hair.stateChanged.connect(self.update_SNR_plot)
        self.SNR_plot_cross_hair_2.stateChanged.connect(self.update_SNR_plot)

        self.V_band.valueChanged.connect(self.update_SNR_plot)
        self.Aperture.valueChanged.connect(self.update_SNR_plot)
        self.Bandwidth.valueChanged.connect(self.update_SNR_plot)
        self.Quant_eff.valueChanged.connect(self.update_SNR_plot)
        self.Max_int_time.valueChanged.connect(self.update_SNR_plot) 
        self.plate_scale.valueChanged.connect(self.update_SNR_plot) 
        self.Sky.valueChanged.connect(self.update_SNR_plot) 
        self.Dark_current.valueChanged.connect(self.update_SNR_plot) 
        self.Read_noise.valueChanged.connect(self.update_SNR_plot) 
        self.CCD_px.valueChanged.connect(self.update_SNR_plot) 
        self.seeing.valueChanged.connect(self.update_SNR_plot) 
        #self.CCD_dimentions.valueChanged.connect(self.update_SNR_plot) 
        self.Throughput.valueChanged.connect(self.update_SNR_plot) 


        self.rv_model_width.valueChanged.connect(self.update_SNR_plot) 

        #self.SNR_plot_autorange.valueChanged.connect(self.update_SNR_plot) 
  

        self.snr_model_color.clicked.connect(self.get_model_color)
 
        #print("""Here you can get some more information from the tool's workflow, stdout/strerr, and piped results.""")




  


def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion') #The available styles depend on your platform but are usually 'Fusion', 'Windows', 'WindowsVista' (Windows only) and 'Macintosh' (Mac only). 
 
    window = DetExCal()
  
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    #print(width, height)
    if height < 920:
        window.setMinimumWidth(width*0.6)
        window.setMinimumHeight(height*0.6)
        window.resize(width*0.8, height*0.8)
    else:
        pass
 
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 


