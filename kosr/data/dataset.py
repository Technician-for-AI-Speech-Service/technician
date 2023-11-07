from ast import arg
from importlib.resources import path
import os
import yaml
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import Sampler

import numpy as np
from kosr.data.features import *
from kosr.data.audio import *
from kosr.utils.convert import char2id, id2char, PAD_TOKEN, SOS_TOKEN, EOS_TOKEN, UNK_TOKEN
torch.cuda.is_available()
file_path=''
def get_path(path):
    global file_path
    file_path =path
   # print(file_path)

    return file_path
#print('밖에',file_path)    
#get_path    
class SpectrogramDataset(Dataset):
    def __init__(self, trn, root_dir='', mode='train', conf=None):
        super(SpectrogramDataset, self).__init__()
        self.root_dir = root_dir
        with open(trn, 'r') as f:
            self.data = f.read().strip().split('\n')
            
        self.conf = conf
            
        self.prep_data(self.conf['model']['max_len'])
            
        self.transforms = Compose([
            Spectrogram(**self.conf['feature']['spec']),
            SpecAugment(prob=self.conf['feature']['augment']['spec_augment'])
        ])
        
    def prep_data(self, tgt_max_len=None, symbol=' :: '):
        """ 
        Data preparations.
        (A, B): Tuple => A: Audio file path, B: Transcript
        """
        temp = []
        i=0
        for line in self.data:
            fname, script = line.split(' :: ')
            fname = os.path.join(self.root_dir, fname)
            script = script.replace('[UNK] ','')
            if tgt_max_len is not None:
                if len(script)>tgt_max_len:
                    continue
            temp.append((fname,script))
        self.data = temp
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        fname, script = self.data[index]
        sig, sr = load_audio(fname)
        spec = self.transforms(sig).transpose(1,0)
        seq = self.scr_to_seq(script)
        return spec, seq
        
    def scr_to_seq(self, scr):
        seq = list()
        seq.append(char2id.get(SOS_TOKEN))
        for c in scr:
            if c in id2char:
                seq.append(char2id.get(c))
            else:
                if UNK_TOKEN is not None:
                    seq.append(char2id.get(UNK_TOKEN))
                else:
                    continue
        seq.append(char2id.get(EOS_TOKEN))
        return seq

class MelSpectrogramDataset(Dataset):
    def __init__(self, trn, root_dir='', mode='train', conf=None, library='torchaudio'):
        super(MelSpectrogramDataset, self).__init__()
        
        self.root_dir = root_dir
        with open(trn, 'r') as f:
            self.data = f.read().strip().split('\n')
            
        self.conf = conf
        self.library = library
        self.prep_data(self.conf['model']['max_len'])
            
        self.transforms = Compose([
            MelSpectrogram(**self.conf['feature']['spec'], library=self.library),
            SpecAugment(prob=self.conf['feature']['augment']['spec_augment'])
        ])
        
    def prep_data(self, tgt_max_len=None, symbol=' :: '):
        """ 
        Data preparations.
        (A, B): Tuple => A: Audio file path, B: Transcript
        """
        temp = []
        i=0
        for line in self.data:
            fname, script = line.split(' :: ')
            fname = os.path.join(self.root_dir, fname)
            script = script.replace('[UNK] ','')
            if tgt_max_len is not None:
                if len(script)>tgt_max_len:
                    continue
            temp.append((fname,script))
        self.data = temp
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        fname, script = self.data[index]
        if self.library=='librosa':
            sig, sr = load_audio(fname, out_tensor=False)
            spec = torch.FloatTensor(self.transforms(sig)).transpose(1,0)
        else:
            sig, sr = load_audio(fname)
            spec = self.transforms(sig).transpose(1,0)
        seq = self.scr_to_seq(script)
        return spec, seq
        
    def scr_to_seq(self, scr):
        seq = list()
        seq.append(char2id.get(SOS_TOKEN))
        for c in scr:
            if c in id2char:
                seq.append(char2id.get(c))
            else:
                if UNK_TOKEN is not None:
                    seq.append(char2id.get(UNK_TOKEN))
                else:
                    continue
        seq.append(char2id.get(EOS_TOKEN))
        return seq

class FBankDataset(Dataset):
    #
    global ct 
    ct =0
    def __init__(self, trn, root_dir='', mode='train', conf=None,path = path):
        super(FBankDataset, self).__init__()
        global ct
        print(ct)
        
        #if ct==0:
        self.path = path
        
        self.root_dir = root_dir
        with open('kosr/data/Ksponspeech/val_1125_.trn', 'r', encoding= 'cp949') as f:
            self.data = f.read().strip().split('\n')
            
        self.conf = conf
        self.prep_data(self.conf['model']['max_len'])
            
        self.transforms = Compose([
            FBank(**self.conf['feature']['spec']),
            SpecAugment(prob=self.conf['feature']['augment']['spec_augment'])
        ])
        #ct+=1
        
    global file_path
    def get_path(self,path):
        # file_path 
        file_path = path 
        self.path = file_path 
    def prep_data(self, tgt_max_len=None, symbol=' :: '):
        """ 
        Data preparations.
        (A, B): Tuple => A: Audio file path, B: Transcript
        """
        temp = []
        i=0
        for line in self.data:
         #   print(line)
           # asd =line.split(' :: ')
            line = line.replace('\t','')
          #  print(line)
           # print('asd',asd)
            zzz =  line.split(' :: ')
          #  print(zzz)
            line = zzz[0]
           # print(line)
            fname, script = line.split('::')
           # print(fname)
            fname = os.path.join(self.root_dir, fname)
            script = script.replace('[UNK] ','')
            if tgt_max_len is not None:
                if len(script)>tgt_max_len:
                    continue
            temp.append((fname,script))
        self.data = temp
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        fname, script = self.data[index]
        
        sig, sr = load_audio(self.path)
        #print(fname,np.shape(sig),sr)
      #  print(fname,sig)
        #print(si)
        spec = self.transforms(sig.unsqueeze(0)).transpose(1,0)
        seq = self.scr_to_seq(script)
        return spec, seq
  #  except
        
    def scr_to_seq(self, scr):
        seq = list()
        seq.append(char2id.get(SOS_TOKEN))
        for c in scr:
            if c in id2char:
                seq.append(char2id.get(c))
            else:
                if UNK_TOKEN is not None:
                    seq.append(char2id.get(UNK_TOKEN))
                else:
                    continue
        seq.append(char2id.get(EOS_TOKEN))
        return seq
    #get_dataloader(conf['dataset']['test'], batch_size=1, conf=conf, path)

def get_dataloader(trn, root_dir='', batch_size=16, mode='valid', conf=None,path=path ):
    shuffle = True if mode=='train' else False
    #print(path)
    #shuffle = False
    dataset = FBankDataset(trn, root_dir, conf=conf,path=path)
    #dataset = MelSpectrogramDataset(trn, root_dir, conf=conf)
    #It is used when debug.
    #if mode=='train':
    #    dataset.data = dataset.data[:16000]
    #else:
    #    dataset.data = dataset.data[:320]
    #SpeechDataset(trn, root_dir, conf=conf)
    #sampler = BucketingSampler(dataset, batch_size=batch_size) if mode=='train' else None
    #shuffle = True if sampler is None else False
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, pin_memory=True,
                              collate_fn=_collate_fn, num_workers=8)

        #FBankDataset(trn, root_dir, conf=conf)

def _collate_fn(batch):
    """ functions that pad to the maximum sequence length """
    def seq_length_(p):
        return len(p[0])

    def target_length_(p):
        return len(p[1])
    batch = sorted(batch, key=lambda sample: sample[0].size(0), reverse=True)

    seq_lengths = [len(s[0]) for s in batch]
    target_lengths = [len(s[1]) for s in batch]

    max_seq_sample = max(batch, key=seq_length_)[0]
    max_target_sample = max(batch, key=target_length_)[1]

    max_seq_size = max_seq_sample.size(0)
    max_target_size = len(max_target_sample)

    feat_size = max_seq_sample.size(1)
    batch_size = len(batch)

    seqs = torch.zeros(batch_size, max_seq_size, feat_size)

    targets = torch.zeros(batch_size, max_target_size).to(torch.long)

    for x in range(batch_size):
        sample = batch[x]
        tensor = sample[0]
        target = sample[1]
        seq_length = tensor.size(0)

        seqs[x].narrow(0, 0, seq_length).copy_(tensor)
        targets[x].narrow(0, 0, len(target)).copy_(torch.LongTensor(target))

    seq_lengths = torch.IntTensor(seq_lengths)
    return seqs, targets, seq_lengths, target_lengths