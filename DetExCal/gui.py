#!/usr/bin/python3
__author__ = 'Trifon Trifonov, 25 April 2022'

import time 
from pathos.multiprocessing import freeze_support
freeze_support()

import numpy as np
import sys, os, traceback 
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import webbrowser
 
es_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(es_path, 'lib')

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
 
colors           = ['#ff0000','#66ff66','#00ffff','#cc33ff','#ff9900','#cccc00','#3399ff','#990033','#339933','#ff0000']               
symbols = ['o','t','t1','t2','t3','s','p','h','star','+','d'] 


QtWidgets.QApplication.processEvents()



class DetExCal(QtWidgets.QMainWindow, Ui_MainWindow):    
 



################################## System #######################################


    def set_Win_widget_Style(self, widget):
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Windows'))
    def set_Fus_widget_Style(self, widget):
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    def set_Mac_widget_Style(self, widget):
        if sys.platform != "darwin":
            print("\n 'Macintosh' window style is only available on MAC OS !!!\n")
            return
        else:
            QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Macintosh'))

    def initialize_color_dialog(self):

        self.colorDialog = QtWidgets.QColorDialog()
        self.colorDialog.setOption(QtWidgets.QColorDialog.ShowAlphaChannel, True)
        self.colorDialog.setOption(QtWidgets.QColorDialog.DontUseNativeDialog, True)

################################## Plots #######################################

    def initialize_plots(self):
        global p1,p2,leg1,leg2

        p1  = self.graphicsView_CCD_SNR
        p2  = self.graphicsView_CCD_SNR_2

        xaxis = ['Integration time [sec.]','V-band magnitude']
        yaxis = ['SNR','SNR']
        xunit = ['','']
        yunit = ['','']

        zzz = [p1,p2]

        for i in range(len(zzz)):

            zzz[i].setAxisItems({'bottom': pg_hack.CustomAxisItem('bottom')})
            zzz[i].setAxisItems({'left': pg_hack.CustomAxisItem('left')})

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

        leg1 = p1.plotItem.addLegend()
        leg2 = p2.plotItem.addLegend()

        return

    def update_font_plots(self):
        global p1,p2 

        zzz = [p1,p2]

        for i in range(len(zzz)):

            zzz[i].getAxis('left').setWidth(np.rint(50.0*(float(self.plot_font.pointSize())/11.0)))
            zzz[i].getAxis("left").tickFont = self.plot_font
            zzz[i].getAxis('bottom').setHeight(np.rint(50.0*(float(self.plot_font.pointSize())/11.0)))

            zzz[i].getAxis("bottom").tickFont = self.plot_font
            # zzz[i].getAxis("left").setStyle(tickTextOffset=20)        
            #  zzz[i].getAxis("bottom").setStyle(tickTextOffset=20)        

            zzz[i].setLabel('bottom', '%s'%zzz[i].getAxis("bottom").labelText, units='', **{'font-size':'%dpt'%self.plot_font.pointSize()})
            zzz[i].setLabel('left', '%s'%zzz[i].getAxis("left").labelText, units='', **{'font-size':'%dpt'%self.plot_font.pointSize()})


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
              
    def initialize_buttons(self):
        self.buttonGroup_color_picker.setId(self.snr_model_color,1)
        self.buttonGroup_color_picker.setId(self.signal_model_color,2)
        self.buttonGroup_color_picker.setId(self.PN_model_color,3)
        self.buttonGroup_color_picker.setId(self.BG_model_color,4)
        self.buttonGroup_color_picker.setId(self.DC_model_color,5)
        self.buttonGroup_color_picker.setId(self.RN_model_color,6)
        self.buttonGroup_color_picker.setId(self.TN_model_color,7)
 

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


    def print_info_credits(self, image=False, es_version='0.03'):
 
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
        but_ind = self.buttonGroup_color_picker.checkedId()

        print(but_ind)
        colorz = self.colorDialog.getColor(options=QtWidgets.QColorDialog.DontUseNativeDialog) #|QtWidgets.QColorDialog.ShowAlphaChannel,)
 
        if colorz.isValid():
            colors[but_ind-1]=colorz.name()  
            self.update_color_picker()
            self.update_SNR_plot()
 
        else:
            return

    def update_color_picker_old(self):

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)

        #for i in range(11):
        self.snr_model_color.setStyleSheet("color: %s;"%colors[-1])
        self.snr_model_color.setText("%s"%colors[-1])
        self.snr_model_color.setFont(font)

    def update_color_picker(self):

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        #font.setWeight(75)

        for i in range(7):
            self.buttonGroup_color_picker.button(i+1).setStyleSheet("color: %s;"%colors[i])
            self.buttonGroup_color_picker.button(i+1).setText("%s"%colors[i])
            self.buttonGroup_color_picker.button(i+1).setFont(font)
 
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
                
    def magnitude_to_flux(self,magnitude):
        return 9.6e10*(10**(-magnitude/2.5))  # phot. /(um m^2 sec)
 
 

    def update_SNR_plot(self):
        global p1,p2,leg1,leg2
 
        if not self.hold_old_plot.isChecked():    
            p1.plot(clear=True,)
            p2.plot(clear=True,)
        else:
            p1.plot(clear=False,)
            p2.plot(clear=False,)

        #p1.addLine(x=None, y=0,   pen=pg.mkPen('#ff9933', width=0.8))
        time       = np.linspace(0.1,self.Max_int_time.value(),300)
        magnitudes = np.linspace(-3,self.V_band.value()+0.1,300)
 


        radius = (self.seeing.value()*(self.plate_scale.value() / self.CCD_px.value()))/2.0 # [pix/"] 
        flux = self.magnitude_to_flux(self.V_band.value()) #airmass?
        bgr  = self.magnitude_to_flux(self.Sky.value()) * (self.CCD_px.value()/self.plate_scale.value())**2

        npix = np.pi* (radius**2)

        signal   = flux*(np.pi*self.Aperture.value()**2)*(self.Throughput.value()/100.0)*(self.Bandwidth.value())*(self.Quant_eff.value()/100.0)
        bg_noise = bgr*(np.pi*self.Aperture.value()**2)*(self.Throughput.value()/100.0)*(self.Bandwidth.value())*(self.Quant_eff.value()/100.0)  
        DCurent       = self.Dark_current.value() #* (self.CCD_px.value()/self.plate_scale.value())**2
        readnoise = self.Read_noise.value() #* (self.CCD_px.value()/self.plate_scale.value())**2
 
        snr_vs_time = self.ccd_SNR_vs_time(signal=signal,bgnd=bg_noise, DCurent =DCurent, time=time, readnoise=readnoise, npix=npix)

        
        if self.legend.isChecked()==True:
            leg1.clear()
            leg2.clear()            
            leg1.setVisible(True)
            leg2.setVisible(True)
        else:
            leg1.setVisible(False)
            leg2.setVisible(False)

        if self.radioButton_SNR.isChecked():
 
            if self.plot_snr.isChecked():
                model_curve = p1.plot(time,snr_vs_time[0], 
                pen={'color': colors[0], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="SNR") 
                
                model_curve.setZValue(self.snr_model_z.value()) 
            p1.setLabel('bottom', 'Integration time [sec.]', units='',  **{'font-size':self.plot_font.pointSize()})    
            p1.setLabel('left', 'SNR', units='',  **{'font-size':self.plot_font.pointSize()})    

        else:
            if self.plot_signal.isChecked():
                model_curve_SI = p1.plot(time,snr_vs_time[1], 
                pen={'color': colors[1], 'width': self.signal_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="Signal") 
                model_curve_SI.setZValue(self.signal_model_z.value()) 
            if self.plot_PN.isChecked():
                model_curve_SI_noise = p1.plot(time,snr_vs_time[2], 
                pen={'color': colors[2], 'width': self.PN_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="Photon noise")
                model_curve_SI_noise.setZValue(self.PN_model_z.value()) 
            if self.plot_BG.isChecked():
                model_curve_BG = p1.plot(time,snr_vs_time[3], 
                pen={'color': colors[3], 'width': self.BG_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="BG noise")
                model_curve_BG.setZValue(self.BG_model_z.value()) 
            if self.plot_DC.isChecked():
                model_curve_DC = p1.plot(time,snr_vs_time[4], 
                pen={'color': colors[4], 'width': self.DC_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="DC noise")
                model_curve_DC.setZValue(self.DC_model_z.value()) 
            if self.plot_RN.isChecked():
                model_curve_RN = p1.plot(time,snr_vs_time[5], 
                pen={'color': colors[5], 'width': self.RN_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="RN noise")      
                model_curve_RN.setZValue(self.RN_model_z.value())       
            if self.plot_TN.isChecked():
                model_curve_TN = p1.plot(time,snr_vs_time[6], 
                pen={'color': colors[6], 'width': self.TN_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="Total noise")          
                model_curve_TN.setZValue(self.TN_model_z.value())       

            p1.setLabel('bottom', 'Integration time [sec.]', units='',  **{'font-size':self.plot_font.pointSize()})    
            p1.setLabel('left', 'electrons [e-]', units='',  **{'font-size':self.plot_font.pointSize()})    


 

        snr_vs_mag = np.array(self.ccd_SNR_vs_mag(signal=signal,bgnd=bg_noise, DCurent =DCurent, time=self.Max_int_time.value(), readnoise=readnoise, npix=npix,mag=magnitudes))

        if self.radioButton_SNR_2.isChecked():    
            if self.plot_snr.isChecked():
                model_curve_mag = p2.plot(magnitudes,snr_vs_mag[0], 
                pen={'color': colors[0], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True) 
                
                model_curve_mag.setZValue(self.snr_model_z.value()) 

            p2.setLabel('bottom', 'V-band magnitude', units='',  **{'font-size':self.plot_font.pointSize()})    
            p2.setLabel('left', 'SNR', units='',  **{'font-size':self.plot_font.pointSize()})   
            sub_snr = snr_vs_mag[0][np.where(magnitudes > self.V_band.value()-3)]
            p2.setYRange(0, max(sub_snr) , padding=0.01)
        else:
            if self.plot_signal.isChecked():
                model_curve_SI_mag = p2.plot(magnitudes,snr_vs_mag[1], 
                pen={'color': colors[1], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="Signal")
                model_curve_SI_mag.setZValue(self.snr_model_z.value()) 
            if self.plot_PN.isChecked():
                model_curve_SI_noise_mag = p2.plot(magnitudes,snr_vs_mag[2], 
                pen={'color': colors[2], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="Photon noise")
            if self.plot_BG.isChecked():
                model_curve_BG_mag = p2.plot(magnitudes,snr_vs_mag[3], 
                pen={'color': colors[3], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="BG noise")
            if self.plot_DC.isChecked():
                model_curve_DC_mag = p2.plot(magnitudes,snr_vs_mag[4], 
                pen={'color': colors[4], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="DC noise")
            if self.plot_RN.isChecked():
                model_curve_RN_mag = p2.plot(magnitudes,snr_vs_mag[5], 
                pen={'color': colors[5], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="RN noise") 
            if self.plot_TN.isChecked():
                model_curve_TN_mag = p2.plot(magnitudes,snr_vs_mag[6], 
                pen={'color': colors[6], 'width': self.snr_model_width.value()},enableAutoRange=True, #symbolPen={'color': 0.5, 'width': 0.1}, symbolSize=1,symbol='o',
                viewRect=True, name="Total noise")      

            p2.setLabel('bottom', 'V-band magnitude', units='',  **{'font-size':self.plot_font.pointSize()})    
            p2.setLabel('left', 'electrons [e-]', units='',  **{'font-size':self.plot_font.pointSize()})    

            sub_snr = snr_vs_mag[0][np.where(magnitudes > self.V_band.value()-3)]
            p2.setYRange(0, max(sub_snr) , padding=0.01)
            
        p2.getViewBox().invertX(True)

        p2.setXRange(self.V_band.value()-3, self.V_band.value(), padding=0.01) 

        p1.setLogMode(self.snr_xaxis_log.isChecked(),self.snr_yaxis_log.isChecked())        
        p2.setLogMode(self.signal_xaxis_log.isChecked(),self.signal_yaxis_log.isChecked())        



        if self.SNR_plot_autorange.isChecked():
            p1.autoRange() #padding=0
            p2.autoRange() 
        if self.SNR_plot_cross_hair.isChecked():
            self.cross_hair(p1,log=self.snr_xaxis_log.isChecked())
        if self.SNR_plot_cross_hair_2.isChecked():
            self.cross_hair(p2,log=self.signal_xaxis_log.isChecked())  


 
    def ccd_SNR_vs_time(self,signal=1,bgnd=0,readnoise=0,DCurent=0,npix=1,time=1,gain=1):
        """
        CCD equation. Gain is ignorred for now.
        """
        snr = []
        Int_signal =[] 
        Int_photnoise =[] 
        Int_bgnd =[] 
        Int_DCurent =[] 
        Int_readnoise =[] 
        Total_noise = []
  
        RN = (readnoise**2)*npix

        for i in range(len(time)):
            SI = signal*gain*time[i]
            BG = bgnd*npix*time[i]
            DC = DCurent*npix*time[i]

            snr.append(SI / (np.sqrt( SI + BG + DC + RN )))   
    
            Int_signal.append(SI)
            Int_photnoise.append(np.sqrt(SI))  
            Int_bgnd.append(np.sqrt(BG))
            Int_DCurent.append(np.sqrt(DC))
            Int_readnoise.append(np.sqrt(RN))
            Total_noise.append( np.sqrt( SI + BG + DC + RN ))   

        return [np.array(snr),np.array(Int_signal),np.array(Int_photnoise),np.array(Int_bgnd),np.array(Int_DCurent),np.array(Int_readnoise),np.array(Total_noise)]

    def ccd_SNR_vs_mag(self,signal=1,bgnd=0,readnoise=0,DCurent=0,npix=1,time=1,gain=1,mag=0):
        """
        CCD equation. Gain is ignorred for now.
        """
        snr = []   

        snr = []
        Int_signal =[] 
        Int_photnoise =[] 
        Int_bgnd =[] 
        Int_DCurent =[] 
        Int_readnoise =[] 
        Total_noise = []

        RN = (readnoise**2)*npix
        BG = bgnd*npix*time
        DC = DCurent*npix*time

        for i in range(len(mag)):
            flux = self.magnitude_to_flux(mag[i]) #airmass?
            signal  = flux*(np.pi*self.Aperture.value()**2)*(self.Throughput.value()/100.0)*(self.Bandwidth.value())*(self.Quant_eff.value()/100.0)

            SI = signal*gain*time
            snr.append(SI / (np.sqrt( SI + BG + DC + RN ))) 

            Int_signal.append(SI)
            Int_photnoise.append(np.sqrt(SI))  
            Int_bgnd.append(np.sqrt(BG))
            Int_DCurent.append(np.sqrt(DC))
            Int_readnoise.append(np.sqrt(RN))
            Total_noise.append( np.sqrt( SI + BG + DC + RN ))   
 
        return [np.array(snr),np.array(Int_signal),np.array(Int_photnoise),np.array(Int_bgnd),np.array(Int_DCurent),np.array(Int_readnoise),np.array(Total_noise)]

 
################################################################################################

 

    def __init__(self):
        
        DEC_version = "0.03"
 
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
 
        self.setupUi(self)
        self.initialize_font_plot()
        self.initialize_plots()
        self.initialize_buttons()

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


        self.update_color_picker() 
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


        self.snr_model_width.valueChanged.connect(self.update_SNR_plot) 
        self.signal_model_width.valueChanged.connect(self.update_SNR_plot) 
        self.PN_model_width.valueChanged.connect(self.update_SNR_plot) 
        self.BG_model_width.valueChanged.connect(self.update_SNR_plot) 
        self.DC_model_width.valueChanged.connect(self.update_SNR_plot) 
        self.RN_model_width.valueChanged.connect(self.update_SNR_plot) 
        self.TN_model_width.valueChanged.connect(self.update_SNR_plot) 

        self.snr_model_z.valueChanged.connect(self.update_SNR_plot) 
        self.signal_model_z.valueChanged.connect(self.update_SNR_plot) 
        self.PN_model_z.valueChanged.connect(self.update_SNR_plot) 
        self.BG_model_z.valueChanged.connect(self.update_SNR_plot) 
        self.DC_model_z.valueChanged.connect(self.update_SNR_plot) 
        self.RN_model_z.valueChanged.connect(self.update_SNR_plot) 
        self.TN_model_z.valueChanged.connect(self.update_SNR_plot) 


        #self.snr_model_color.clicked.connect(self.get_model_color)
        self.buttonGroup_color_picker.buttonClicked.connect(self.get_model_color) 

        self.radioButton_SNR.toggled.connect(self.update_SNR_plot)
        self.radioButton_SNR_2.toggled.connect(self.update_SNR_plot)



        self.plot_snr.stateChanged.connect(self.update_SNR_plot)
        self.plot_signal.stateChanged.connect(self.update_SNR_plot)
        self.plot_PN.stateChanged.connect(self.update_SNR_plot)
        self.plot_BG.stateChanged.connect(self.update_SNR_plot)
        self.plot_DC.stateChanged.connect(self.update_SNR_plot)
        self.plot_RN.stateChanged.connect(self.update_SNR_plot)
        self.plot_TN.stateChanged.connect(self.update_SNR_plot)

        self.snr_xaxis_log.stateChanged.connect(self.update_SNR_plot)
        self.snr_yaxis_log.stateChanged.connect(self.update_SNR_plot)
        self.signal_xaxis_log.stateChanged.connect(self.update_SNR_plot)
        self.signal_yaxis_log.stateChanged.connect(self.update_SNR_plot)
        #print("""Here you can get some more information from the tool's workflow, stdout/strerr, and piped results.""")


        self.legend.stateChanged.connect(self.update_SNR_plot)

  


def main():

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion') #The available styles depend on your platform but are usually 'Fusion', 'Windows', 'WindowsVista' (Windows only) and 'Macintosh' (Mac only). 
 
    window = DetExCal()
  
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
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


