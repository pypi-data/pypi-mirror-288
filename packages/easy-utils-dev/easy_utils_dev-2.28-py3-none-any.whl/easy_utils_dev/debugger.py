import logging
import os
import json 
import  sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from .utils import getRandomKey,  convert_bytes_to_mb , convert_mb_to_bytes 
from .custom_env import custom_env , setupEnvironment
from .Events import EventEmitter
from threading import Thread
from time import sleep

gEvent = EventEmitter()

def setGlobalHomePath( path ) :
    env = custom_env()
    env['debugger_homepath'] = path
    gEvent.dispatchEvent('update_home_path')

def setGlobalDisableOnScreen(on_screen=False) :
    env = custom_env()
    env['debugger_on_screen'] = on_screen
    if not on_screen :
        gEvent.dispatchEvent('disable_global_printing')
    else :
        gEvent.dispatchEvent('enable_global_printing')
        
    
def setGlobalDebugLevel(level='info') :
    env = custom_env()
    env['debugger_global_level'] = level
    gEvent.dispatchEvent('update_debug_level')


class DEBUGGER:
    def __init__(self, name, level='info', onscreen=True,log_rotation=3,homePath=None,id=getRandomKey(9) , global_debugger=None,disable_log_write=False,file_name=None):
        env = custom_env()
        env['debugger_on_screen'] = True
        self.env = env
        self.events = gEvent
        self.logger = logging.getLogger(f"{name}{getRandomKey(4)}")
        self.set_level(level)
        self.file_handler_class=None
        self.LOG_SIZE_THRESHOLD_IN_BYTES = 10 * 1024 * 1024
        self.BACKUP_COUNT = log_rotation
        self.homePath = homePath
        self.onScreen= onscreen
        self.id = id
        self.how_many_times_write= 0
        self.stream_service = None
        self.console = console_handler = logging.StreamHandler()
        self.logger.addHandler(self.console)
        self.name = name
        self.rotate_disabled=False
        self.isInPyinstaller = False
        self.log_iterations=0
        self.log_iterations_threshold = 200
        self.global_debugger = global_debugger
        self.isLogWriteDisabled = disable_log_write
        self.type = "CUSTOM_DEBUGGER"
        setupEnvironment( 'debugger' )
        env['debugger'][id] = self
        f = f"[%(asctime)s]-[{self.name}]-[%(levelname)s]: %(message)s"
        self.formatter = logging.Formatter(f , datefmt='%Y-%m-%d %H:%M:%S' )
        self.filename = file_name
        path = self.homepath(homePath)
        console_handler.setFormatter(self.formatter)
        if not disable_log_write :
            self.file_handler_class = self.createRotateFileHandler(path)
        if onscreen : 
            self.enable_print()
        elif not onscreen : 
            self.disable_print()

        self.events.addEventListener('disable_global_printing' , self.disable_print )
        self.events.addEventListener('enable_global_printing' , self.enable_print )
        self.events.addEventListener('update_home_path' , self.updateGlobalHomePath )
        self.events.addEventListener('update_debug_level' , self.updateGlobalSetLevel )

    def updateGlobalHomePath(self ) :
        if not self.isLogWriteDisabled :
            getFromEnv = self.env.get('debugger_homepath' , None )
            self.homepath(getFromEnv)
            if getFromEnv : 
                self.file_handler_class = self.createRotateFileHandler(self.homePath)

    def updateGlobalSetLevel( self ) :
        self.set_level(self.env['debugger_global_level'])

    def advertiseGlobalDebugLevel(self , level) :
        setGlobalDebugLevel(level)

    def disable_rotate(self) :
        self.rotate_disabled = True

    def enable_rotate(self) :
        self.rotate_disabled = False

    def createRotateFileHandler( self , path ) :
        old = self.file_handler_class
        if old :
            self.logger.removeHandler(old)
        file_handler = RotatingFileHandler(path ,  maxBytes=self.LOG_SIZE_THRESHOLD_IN_BYTES , backupCount=self.BACKUP_COUNT )
        self.file_handler= file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
        return file_handler

    def update_log_iterantions_threshold(self,threshold : int ):
        '''
        set value when rotation should be checked. when every on_log function called.
        by default rotation will be checked every 200 on_log function call.
        '''
        self.log_iterations_threshold = threshold

    def updateGlobalDebugger(self , logger ) :
        '''
        this function pass the log message to other logger to write the same log message to it.
        logger must be debugger class.
        '''
        if logger.type != 'CUSTOM_DEBUGGER' :
            raise Exception(f'Invalid logger type. must pass debugger class.')
        self.global_debugger = logger


    def getStreamServiceUrlPath(self) :
        return self.streampath

    def getStreamService(self) :
        return self.stream_service

    def isStreamServiceAvailable(self) :
        if self.stream_service :
            return True
        return False

    def addStreamService( self , socketio , streampath='/debugger/stream/log' ) :
        """
        This function takes a live socketio server. it emit the log message using default path which is /debugger/stream/log
        """
        self.stream_service = socketio
        self.streampath = streampath
        
    def updateLogName( self , name ) :
        self.name = name

    def disable_log_write(self) :
        '''
        this function is used to disable the log write to file. if onScreen is enabled, logs will be displayed only on screen.
        '''
        self.isLogWriteDisabled = True
        if self.file_handler_class :
            self.logger.removeHandler(self.file_handler_class)
    
    def enable_log_write(self) :
        self.createRotateFileHandler(self.homePath)
        
    def manage_file_rotation(self, record ) :
        handler = self.get_rotate_handler()
        if handler.shouldRollover(record) :
            handler.doRollover()
            self.log_iterations = 0

    def get_rotate_handler(self) :
        return self.file_handler_class
            
    def change_log_size(self, size) -> bool:
        '''
        change the size of each log file rotation.
        default is 10M
        size should be passed as MB
        '''
        size = convert_mb_to_bytes(size)
        self.LOG_SIZE_THRESHOLD_IN_BYTES = size
        handler = self.get_rotate_handler()
        handler.maxBytes = size
        
        return True

    def is_running_in_pyinstaller(self):
        # Check for the _MEIPASS attribute
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    

    def close(self) :
        try :
            logging.shutdown()
        except :
            pass

    def homepath(self , path=None ) :
        env = custom_env()
        getFromEnv = env.get('debugger_homepath' , None )
        if getFromEnv is not None :
            self.homePath = getFromEnv
        else :
            if path is not None :
                self.homePath = path
            else :
                self.homePath = os.getcwd()
        if not os.path.exists( self.homePath ) :
            os.makedirs( self.homePath )
        if self.filename :
            self.homePath = os.path.join( self.homePath, f'{self.filename}.log' ) 
        else :
            self.homePath = os.path.join( self.homePath, f'{self.name}.log' ) 
        return self.homePath

    def enable_print(self) :
        self.onScreen = True
        self.logger.addHandler(self.console)

    def disable_print(self) : 
        self.onScreen = False
        self.logger.removeHandler(self.console)

    def changeHomePath( self , path ) :
        p = self.homepath(path)
        self.file_handler_class = self.createRotateFileHandler(p)

    def isGlobalDebuggerDefined(self) :
        if self.global_debugger :
            return True
        else :
            return False

    def set_level(self, level : str):
        if 'info' in level.lower() : lvl = logging.INFO
        elif 'warn' in level.lower() : lvl = logging.WARNING
        elif 'warning' in level.lower() : lvl = logging.WARNING
        elif 'critical' in level.lower() : lvl = logging.CRITICAL
        elif 'debug' in level.lower() : lvl = logging.DEBUG
        elif 'error' in level.lower() : lvl = logging.ERROR
        else : raise ValueError('Unknown level, not one of [info,warn,warning,critical,debug,error]')
        self.logger.setLevel(lvl)

    def get_logger(self) : 
        return self.logger
    
    def before_log(self , message , level) :
        def __call_thread__() :
            if self.isStreamServiceAvailable() :
                d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.stream_service.emit( self.getStreamServiceUrlPath() , json.dumps({
                    'message' : message ,
                    'level' : level ,
                    'msg' : message,
                    'key' : getRandomKey(),
                    'date' : d ,
                    'id' : self.id,
                    'formate' : 'json'
                }))

        def __call_shutdown__() :
            sleep(10)
            self.close()

        t= Thread(target=__call_thread__)
        t.daemon=True
        t.start()
        t= Thread(target=__call_shutdown__)
        t.daemon=True
        t.start()
        params = {
                'screen' : True  ,
                'file': True
            }
        if self.env.get('debugger_global_level' , None) : 
            self.set_level( level=self.env.get('debugger_global_level') )
        if self.onScreen and self.env['debugger_on_screen'] == True :
            params['screen'] = True
        else :
            params['screen'] = False
        return params
        

    def info(self, message):
        def __call__() :
            self.before_log(message , 'info')
            self.logger.info(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.info(message)
        r = Thread(target=__call__)
        r.daemon=False
        r.start()
        r.join()

    def debug(self, message):
        def __call__() :
            self.before_log(message , 'debug')
            self.logger.debug(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.debug(message)
        r=Thread(target=__call__)
        r.daemon=True
        r.start()
        r.join()

    def warning(self, message):
        def __call__() :
            self.before_log(message , 'warning')
            self.logger.warning(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.warning(message)
        r=Thread(target=__call__)
        r.daemon=True
        r.start()
        r.join()
    def error(self, message):
        def __call__() :
            self.before_log(message , 'error')
            self.logger.error(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.error(message)
        r=Thread(target=__call__)
        r.daemon=True
        r.start()
        r.join()

    def critical(self, message):
        def __call__() :
            self.before_log(message , 'critical')
            self.logger.critical(message)
            if self.isGlobalDebuggerDefined() : 
                self.global_debugger.critical(message)
        r=Thread(target=__call__)
        r.daemon=True
        r.start()
        r.join()