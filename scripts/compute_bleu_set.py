from compute_bleu import compute_bleu
import argparse

'''
reference_path = 'C:/Users/alexantonov/t2t_data_he3/tmp/test1000/en.test.txt'
translation_dir = 'C:/Users/alexantonov/t2t_data_he3/tmp/test1000/'
checkpoint_dir = 'C:/Users/alexantonov/t2t_data_he3/t2t_train_he3/'
'''

def compute_bleu_set(reference_path, translation_dir, checkpoint_dir):
  checkpoint_file = checkpoint_dir + "checkpoint"
  checkpoint_paths = []
  with open(checkpoint_file, encoding='utf-8', newline='') as fckpt:
    for line in fckpt:
      ckpt_type, ckpt_name = line.split(':')	
      if ckpt_type == 'all_model_checkpoint_paths':
        checkpoint_paths.append(ckpt_name.strip(' \n\"'))  
  
  for checkpoint_elem in checkpoint_paths:
    bleu = compute_bleu(reference_path, translation_dir + checkpoint_elem)
    print(bleu)

# example: compute_bleu_set.py --translation_dir=../t2t_data_he3/tmp/test1000/ --reference=../t2t_data_he3/tmp/test1000/en.test.txt --checkpoint_dir=../t2t_data_he3/t2t_train_he3/
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--translation_dir', type=str, help='directory to translation')
    parser.add_argument('--reference', type=str,
                        help='Path to file with references. Several references separated by tab')   
    parser.add_argument('--checkpoint_dir', type=str, help='directory to set of checkpoints')
    args = parser.parse_args()
    bleu = compute_bleu_set(args.reference, args.translation_dir, args.checkpoint_dir)
    print(bleu)