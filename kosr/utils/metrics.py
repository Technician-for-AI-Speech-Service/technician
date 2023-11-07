import Levenshtein as Lev
import torch
torch.cuda.is_available()
from kosr.utils.convert import char2id, id2char, PAD_TOKEN, SOS_TOKEN, EOS_TOKEN, UNK_TOKEN
#def csv_save_trian(train_y_hats1,train_y_hats2,train_y_hats3,train_y_hats4,train_target1,train_target2,train_target3,train_target4):
#    import csv
 #   f = open('/home/ujlee/Templates/kosr/kosr/train_6.csv', 'a', encoding='utf-8', newline='')
 #   wr = csv.writer(f)
 #   for b in range(len(train_y_hats1)):
  #      wr.writerow([train_y_hats1[b],train_y_hats2[b],train_y_hats3[b],train_y_hats4[b],train_target1[b],train_target2[b],train_target3[b],train_target4[b]])    
  #  f.close()
'''  
def csv_alltargetsave_trian(train_target1,train_y_hats1):
    import csv
    f = open('/home/ujlee/Templates/kosr/kosr/train_targetall_eval0222.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for b in range(len(train_target1)):
        wr.writerow([train_target1[b],train_y_hats1[b]])    
    f.close()   
def csv_allpredsave_trian(train_y_hats1):
    import csv
    f = open('/home/ujlee/Templates/kosr/kosr/train_predall.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for b in range(len(train_y_hats1)):
        wr.writerow([train_y_hats1[b]])    
    f.close()      
'''
def metrics(preds, targets):
    btz = targets.size(0)
    cers = 0.
    wers = 0.
    import numpy as np
    train_y_hats1= []
    train_y_hats2= []
    train_y_hats3= []
    train_y_hats4= []
    train_target1=[]
    train_target2=[]
    train_target3=[]
    train_target4=[]
    preds_str = seq_to_str(preds, id2char)
    golds_str = seq_to_str(targets, id2char)
   # print('preds_str',preds_str)
    #print(np.shape(preds_str))
    #print(np.shape(golds_str))
   # print('golds_str',golds_str)
    
    for aa1 in range(len(golds_str)):
        train_y_hats1.append(golds_str[aa1])
    for bb1 in range(len(preds_str)):
        train_target1.append(preds_str[bb1])
    print(preds_str)    
        
  #  train_y_hats2.append(golds_str[1])
  #  train_y_hats3.append(golds_str[2])
 #   train_y_hats4.append(golds_str[3])
    
   # train_target2.append(preds_str[1])
   # train_target3.append(preds_str[2])
   # train_target4.append(preds_str[3])
    for i, (pred,gold) in enumerate(zip(preds_str,golds_str)):
        if gold.strip()=="":
            """only unk token"""
            length = len(targets[i][1:-1])
            if length==0:
                length=1
                cers += cer(pred,gold)/length
                length = 1
                wers += wer(pred,gold)/length
            else:    
          #  print(cer(pred,gold))
            #print(length)
                cers += cer(pred,gold)/length
                length = 1
                wers += wer(pred,gold)/length
          #  print()
        else:
            try:
                length = len(gold.replace(' ',''))
                cers += cer(pred,gold)/length
                length = len(gold.split())
                wers += wer(pred,gold)/length
            except:
                """unknown errors"""
                btz -= 1
                continue
   # print(cers)
    #print('wers',wers)
   # csv_alltargetsave_trian(train_target1,train_y_hats1)
  #  csv_allpredsave_trian(train_y_hats1)
    #csv_save_trian(train_y_hats1,train_y_hats2,train_y_hats3,train_y_hats4,train_target1,train_target2,train_target3,train_target4)    
    return cers/btz, wers/btz, preds_str

def wer(s1, s2):
    """
    Computes the Word Error Rate, defined as the edit distance between the
    two provided sentences after tokenizing to words.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """

    b = set(s1.split() + s2.split())
    word2char = dict(zip(b, range(len(b))))

    w1 = [chr(word2char[w]) for w in s1.split()]
    w2 = [chr(word2char[w]) for w in s2.split()]
    return Lev.distance(''.join(w1), ''.join(w2))


def cer(s1, s2):
    """
    Computes the Character Error Rate, defined as the edit distance.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """
    s1, s2, = s1.replace(' ', ''), s2.replace(' ', '')
    return Lev.distance(s1, s2)

def seq_to_str(seqs, id2char):
    #assert len(seqs.shape)<=2, 'can not convert 3-dimensional sequence to string'
    pad_id = id2char.index(PAD_TOKEN)
    unk_id = id2char.index(UNK_TOKEN) if UNK_TOKEN in id2char else None 
    sos_id = id2char.index(SOS_TOKEN)
    eos_id = id2char.index(EOS_TOKEN)
    import numpy as np
    if isinstance(seqs, torch.Tensor):
        seq_dimension = len(seqs.shape)
    elif isinstance(seqs, list):
        seq_dimension = 0
        next_seq = seqs
        while isinstance(next_seq, list):
            seq_dimension += 1
            next_seq = next_seq[0]
    
    unk_cnt = 0
    if seq_dimension == 1:
        sentence = str()
        for idx in seqs:
            if isinstance(idx, torch.Tensor):
                idx = idx.item()
            if idx==sos_id or idx==pad_id or idx==unk_id:
                continue
            if idx==eos_id:
                break
            sentence += id2char[idx]
      #  print(sentences)
        return sentence
    
    elif seq_dimension == 2:
        sentences = list()
        for seq in seqs:
            sentence = str()
            for idx in seq:
                if isinstance(idx, torch.Tensor):
                    idx = idx.item()
                if idx==sos_id or idx==pad_id or idx==unk_id:
                    continue
                if idx==eos_id:
                    break
                sentence += id2char[idx]
            sentences.append(sentence)
       # print(len(sentence))
        return sentences