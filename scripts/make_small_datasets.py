import argparse
import numpy as np
import os


def make_small_datasets(datapath, train_size, test_size, dev_size):
    if datapath.endswith('/'):
        datapath = datapath[:-1]

    prefix = datapath.split('/')[-1]

    for filename in os.listdir(datapath):
        new_ix = None

        try:
            lang, token = filename.split('.')[:2]
        except IndexError:
            continue

        if token == 'train':
            train_data = np.loadtxt(os.path.join(datapath, filename), dtype='str', encoding='utf-8')

            assert (len(train_data) > train_size + test_size + dev_size)

            if not new_ix:
                np.random.seed(0)  # for compatibility

                new_ix = np.random.choice(
                    a=np.arange(len(train_data)), size=train_size + test_size + dev_size, replace=False
                )

            new_train_data = train_data[new_ix[:train_size]]
            new_test_data = train_data[new_ix[train_size: -dev_size]]
            new_dev_data = train_data[new_ix[-dev_size:]]

            new_prefix = "{}-{}k".format(prefix, train_size // 1000)

            new_datadir = os.path.join('/'.join(datapath.split('/')[:-1]), new_prefix)

            if not os.path.exists(new_datadir):
                os.makedirs(new_datadir)

            print("Saving to {}".format(new_datadir))

            np.savetxt(X=new_train_data, fname=os.path.join(
                new_datadir,
                "{}.train.txt".format(lang, train_size, new_prefix)
                ),
                delimiter='\n', fmt='%s', encoding='utf-8'
            )

            np.savetxt(X=new_test_data, fname=os.path.join(
                new_datadir,
                "{}.test.txt".format(lang, train_size, new_prefix)
                ),
                delimiter='\n', fmt='%s', encoding='utf-8'
            )

            np.savetxt(X=new_dev_data, fname=os.path.join(
                new_datadir,
                "{}.dev.txt".format(lang, train_size, new_prefix)
                ),
                delimiter='\n', fmt='%s', encoding='utf-8'
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datadir', action='store', type=str,
                        help='Directory of original dataset. Should have .test.txt, .dev.txt, .train.txt files in it.')
    parser.add_argument('train_size', action='store', type=int, help='train sample size')
    parser.add_argument('test_size', action='store', type=int, help='test sample size')
    parser.add_argument('dev_size', action='store', type=int, help='dev sample size')

    args = parser.parse_args()
    make_small_datasets(args.datadir, 1000*args.train_size, 1000*args.test_size, 1000*args.dev_size)
