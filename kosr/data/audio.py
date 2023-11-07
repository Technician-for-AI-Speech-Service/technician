import soundfile as sf
import numpy as np
import torch
torch.cuda.is_available()
import torchaudio
from ffmpy import FFmpeg
import os.path
def load_audio(path, sr=16000, out_tensor=True):
    ext = path.split('.')[-1]
    if ext=='pcm':
        #path = 'C:\\Users\\user\\Desktop\\works\\flask\\220223\\kosr\\testdata\\ID-03-34-N-JYN-02-010005-F-24-KK2.pcm'
        try:
            sig, sr = np.memmap(path, dtype='h', mode='r').astype('float32'), sr
        except:
            with open (path, 'rb') as f:
                buf = f.read()
                if len(buf)%2==1:
                    buf = buf[:-1]
            sig, sr = np.frombuffer(buf, dtype='int16'), sr
    else:
        '''
        if os.path.isfile(path.replace("wav", "pcm")):
            path = path.replace("wav", "pcm")
        else:

            f1 = FFmpeg(executable='/home/ujlee/Templates/Speech_disorder/recognition/ffmpeg.exe',
                inputs={path:None},
                outputs={path.replace("wav", "pcm"):"-f s16be -ar 16000 -ac 1 -acodec pcm_s16be"})
            f1.run()
            path = path.replace("wav", "pcm")
        #print(path)
        #sig, sr = sf.read(path, sr)
        try:
            sig, sr = np.memmap(path, dtype='h', mode='r').astype('float32'), sr
        except:
            with open (path, 'rb') as f:
                buf = f.read()
                if len(buf)%2==1:
                    buf = buf[:-1]
            sig, sr = np.frombuffer(buf, dtype='int16'), sr
        '''    
        sig, sr = sf.read(path, sr)
    if out_tensor:
        return torch.FloatTensor(sig), sr
    else:
        return sig, sr