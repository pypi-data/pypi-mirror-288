
from time import sleep
from threading import Lock

from  pygame import mixer
from os import environ, path, makedirs, getcwd
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

mixer.init()

script_dir = path.dirname(path.abspath(__file__))

tempo_de_estudo_finalizado = path.join(script_dir, 'tempo_de_estudo_finalizado.wav')

def gen_pygame_sound(sound_name, volume):
    try:
        sound = mixer.Sound(sound_name)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError as f:
        # print(f)
        # print("o arquivo '*.wav' não foi encontrado")
        print(f)



class Metronomo:
        #para bloquear a criação e mais de uma intãncia da classe Metronomo
    _instancia = None
    _lock = Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instancia is None:
                cls._instancia = super(Metronomo, cls).__new__(cls)
                # Inicialize os atributos da instância aqui
        return cls._instancia 
    


    temp = 2
    def __init__(self):



        # parâmetros do metrônomo
        self.wav1 = path.join(script_dir, '1.wav')
        self.wav2 = path.join(script_dir, '2.wav')
        self.__bpm = 120
        self.__volume = 1
        self.__on = False
        self.__att = False
        self.tipo_compasso = 4
        self.qtd_compassos = 1
        self.cont_tempos = 0
        self.cont_compassos = 0
        self.pause = False

       
    @classmethod       
    def Juntar(self, a, b):
        return path.join(a, b)

    @property
    def __sound_data(self):
        # self.__sound_name = path.join(self.pasta, "1.wav")
        self.__sound_name = self.wav1
        som = gen_pygame_sound(self.__sound_name, self.__volume)
        return som    
    @__sound_data.setter
    def __sound_data(self, volume):
        # self.__sound_name = path.join(self.pasta, "1.wav")
        self.__sound_name = self.wav1
        som = gen_pygame_sound(self.__sound_name, volume)
            


    @property
    def __sound_data2(self):
        # self.__sound_name2 = path.join(self.pasta, "2.wav")
        self.__sound_name2 = self.wav2
        som =  gen_pygame_sound(self.__sound_name2, self.__volume) 
        return som    
    @__sound_data2.setter
    def __sound_data2(self, volume):
        # self.__sound_name2 = path.join(self.pasta, "2.wav")
        self.__sound_name2 = self.wav2
        som =  gen_pygame_sound(self.__sound_name2, volume)    
           
    # Getters & Setters
    @property
    def nometarefastxt(self):
        return self.Juntar(getcwd(), 'tarefas.txt')
   
    @property
    def getBpm(self):
        return self.__bpm

    def setBpm(self, bpm):
        self.__bpm = bpm
        self.__att = True

    @property
    def getVolume(self):
        return self.__volume

    def setVolume(self, volume):
        self.__volume = volume
        self.reload

    def getOn(self):
        return self.__on
    
    @property
    def setOn(self):
        return self.__on
      
    @setOn.setter
    def setOn(self, on):
        self.__on = on


    @property
    def reload(self):
        self.__sound_data = self.__volume
        self.__sound_data2 = self.__volume

    def Atualizar(self, valor=True):
        self.__att = valor

    def beep(self):
        t = 60/self.__bpm
        self.cont_tempos = 0
        self.cont_compassos = 0
        while self.__on:
            while self.pause:
                sleep(0.1)

            if self.__att:
                t = 60/self.__bpm
            self.__att = False
# 

            if self.cont_tempos in [0, 4, 8, 12, 16, 20, 24, 28, 32,36,40,44,48,52,56,60]:
                self.__sound_data2.play()

            else:
                self.__sound_data.play()


            if self.cont_tempos == self.tipo_compasso*self.qtd_compassos:
                sleep(t)
                self.cont_tempos = 0
            else:
                sleep(t)
            self.cont_tempos += 1


if __name__ == '__main__':
    m = Metronomo()
    m.setBpm(60)
    m.setOn = True
    m.beep()

