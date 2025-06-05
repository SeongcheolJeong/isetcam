import numpy as np
from pathlib import Path
from colorfilter import read_color_filter, save_color_filter

def main():
    tmp = Path('temp_colorfilter.mat')
    wave = np.arange(400, 701, 10)
    data = np.stack([np.linspace(0, 1, wave.size), np.linspace(1, 0, wave.size)], axis=1)
    names = ['r', 'g']
    comment = 'test'

    save_color_filter(tmp, wave, data, names, comment)
    w, d, n, meta = read_color_filter(tmp)
    assert np.allclose(w, wave)
    assert np.allclose(d, data)
    assert n == names
    assert meta['comment'] == comment
    tmp.unlink()
    print('colorfilter test passed')

if __name__ == '__main__':
    main()
