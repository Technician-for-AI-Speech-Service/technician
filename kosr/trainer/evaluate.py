import torch
import torch.nn as nn
from tqdm import tqdm
torch.cuda.is_available()
#from kosr.utils import eval_log, logger
from kosr.utils.metrics import metrics

def evaluate(model, dataloader, search='greedy'):
    losses = 0.
    cer = 0.
    wer = 0.
    step = 0
    model.eval()
    pbar = tqdm(dataloader)
    with torch.no_grad():
        for batch in pbar:
            inputs, targets, input_length, target_length = batch

            if torch.cuda.is_available():
                inputs = inputs.cuda()
                targets = targets.cuda()
            
            preds, targets, y_hats = model.recognize(inputs, input_length, targets,search)

            _cer, _wer , preds= metrics(y_hats, targets)
            cer += _cer
            wer += _wer
            step += 1
            #print('y_hats',y_hats)
            #print('targets,',targets)
            #pbar.set_description(eval_log.format('evaluate', cer/step, wer/step))
    #logger.info(eval_log.format('evaluate', cer/step, wer/step))
    
    return preds