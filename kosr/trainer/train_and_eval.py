import torch
import torch.nn as nn
from tqdm import tqdm
import os
import numpy as np
from kosr.utils.metrics import metrics
#from kosr.utils import make_chk, train_log, valid_log, epoch_log, chk_path, logger
from kosr.trainer.checkpoint import save
torch.cuda.is_available()
import os 
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '0,1'


'''
def csv_save_trian(train_y_hats1,train_y_hats2,train_y_hats3,train_y_hats4,train_target1,train_target2,train_target3,train_target4):
    import csv
    f = open('/home/ujlee/Templates/kosr/kosr/train_1019.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for b in range(len(train_y_hats1)):
        wr.writerow([train_y_hats1[b],train_y_hats2[b],train_y_hats3[b],train_y_hats4[b],train_target1[b],train_target2[b],train_target3[b],train_target4[b]])    
    f.close() 

def csv_save_val(val_y_hats1,val_y_hats2,val_y_hats3,val_y_hats4,val_target1,val_target2,val_target3,val_target4):
    import csv
    f = open('/home/ujlee/Templates/kosr/kosr/val_1019.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for b in range(len(val_y_hats1)):
        wr.writerow([val_y_hats1[b],val_y_hats2[b],val_y_hats3[b],val_y_hats4[b],val_target1[b],val_target2[b],val_target3[b],val_target4[b]])    
    f.close() 
'''   
    
def train_and_eval(epochs, model, optimizer, criterion, train_dataloader, valid_dataloader, loss_type='label_smoothing', max_norm=5, saved_epoch=None, print_step=100, epoch_save=True):
    best_loss = 10101.0
    bl_epoch = 0
    best_wer = 10101.0
    bw_epoch = 0
    
    logger.info("checkpoint saves in {} directory".format(chk_path))
    os.makedirs(chk_path, exist_ok=True)
    if saved_epoch is not None:
        saved_epoch = saved_epoch + 1
    else:
        saved_epoch = 0
    
    for epoch in range(saved_epoch, epochs):
        train_loss, train_wer = train(model, optimizer, criterion, train_dataloader, epoch, loss_type, max_norm, print_step)
        valid_loss, valid_wer = valid(model, criterion, valid_dataloader, epoch, loss_type)
        if best_loss>valid_loss:
            best_loss = valid_loss
            bl_epoch = epoch
            save(os.path.join(chk_path, 'best_loss.pth'), epoch, model, optimizer, train_loss)
            
        if best_wer>valid_wer:
            best_wer = valid_wer
            bw_epoch = epoch
            save(os.path.join(chk_path, 'best_wer.pth'), epoch, model, optimizer, valid_loss)
        
        if epoch_save:
            save(os.path.join(chk_path, f"{epoch}_.pth"), epoch, model, optimizer, valid_loss)
            
        save(os.path.join(chk_path, 'last.pth'), epoch, model, optimizer, valid_loss)
        logger.info(epoch_log.format("info", epoch, bw_epoch, best_wer, bl_epoch, best_loss))
            
            

def train(model, optimizer, criterion, dataloader, epoch, loss_type, max_norm=400, print_step=100):
    losses = 0.
    cer = 0.
    wer = 0.
    step = 0
    model.train()
    train_y_hats1= []
    train_y_hats2= []
    train_y_hats3= []
    train_y_hats4= []
    train_target1=[]
    train_target2=[]
    train_target3=[]
    train_target4=[]
    pbar = tqdm(dataloader)
    for batch in pbar:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        optimizer.zero_grad()

        inputs, targets, input_length, target_length = batch
        
        if torch.cuda.is_available():
            inputs = inputs.cuda()
            targets = targets.cuda()
            net = nn.DataParallel(inputs).to(device)
            net2 = nn.DataParallel(targets).to(device)
        
        if loss_type=='label_smoothing':
            preds, targets = model(inputs, input_length, targets)
            loss = criterion(preds, targets)
        else:
            preds, att_targets, ctc_out, ctc_targets, input_length, target_length = model(inputs, input_length, targets)
            loss = criterion(preds, att_targets, ctc_out, ctc_targets, input_length, target_length)
        #loss = criterion(preds.view(-1,preds.size(-1)), targets.view(-1))
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_norm)
        optimizer.step()
        
        losses += loss.item()
        
        y_hats = preds.max(-1)[1]
        #print(y_hats[0], targets[0])
       # print(targets , np.shape(targets))
        _cer, _wer = metrics(y_hats, targets)
      #  print(targets , np.shape(targets))
        cer += _cer
        wer += _wer
        step += 1
        pbar.set_description(train_log.format('training', epoch, losses/step, cer/step, optimizer._rate))
        '''
        train_y_hats1.append(y_hats[0])
        train_y_hats2.append(y_hats[1])
        train_y_hats3.append(y_hats[2])
        train_y_hats4.append(y_hats[3])
        train_target1.append(targets[0])
        train_target2.append(targets[1])
        train_target3.append(targets[2])
        train_target4.append(targets[3])
        '''
        #if step%print_step==0:
        #    logger.info(train_log.format('training', epoch, losses/step, cer/step, optimizer._rate))
    #csv_save_trian(train_y_hats1,train_y_hats2,train_y_hats3,train_y_hats4,train_target1,train_target2,train_target3,train_target4)       
    return losses/step, wer/step
        
def valid(model, criterion, dataloader, epoch, loss_type, search='greedy'):
    losses = 0.
    cer = 0.
    wer = 0.
    step = 0
    model.eval()
    pbar = tqdm(dataloader)
    val_y_hats1= []
    val_y_hats2= []
    val_y_hats3= []
    val_y_hats4= []
    val_target1=[]
    val_target2=[]
    val_target3=[]
    val_target4=[]
    with torch.no_grad():
        for batch in pbar:
            inputs, targets, input_length, target_length = batch

            if torch.cuda.is_available():
                inputs = inputs.cuda()
                targets = targets.cuda()
            
            preds, targets, y_hats = model.recognize(inputs, input_length, targets, search)
                #loss = criterion(preds, targets)
                #loss = criterion(preds, targets)

            #losses += loss.item()

            _cer, _wer = metrics(y_hats, targets)
            cer += _cer
            wer += _wer
            step += 1
            '''
            val_y_hats1.append(y_hats[0])
            val_y_hats2.append(y_hats[1])
            val_y_hats3.append(y_hats[2])
            val_y_hats4.append(y_hats[3])
            val_target1.append(targets[0])
            val_target2.append(targets[1])
            val_target3.append(targets[2])
            val_target4.append(targets[3])
            '''
            pbar.set_description(valid_log.format('valid', epoch, cer/step, wer/step))
    logger.info(valid_log.format('valid', epoch, cer/step, wer/step))
  #  csv_save_val(val_y_hats1,val_y_hats2,val_y_hats3,val_y_hats4,val_target1,val_target2,val_target3,val_target4)
    return losses/step, wer/step