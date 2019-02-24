import os
import argparse
from mutagen.mp3 import MP3

conv = [
    " ",
    "(",
    ")",
]

def change_audio_rate(dir_path, speed_rate=2):
    prefix = '{}'.format(speed_rate)
    if os.path.exists(dir_path):
        folder = dir_path.split('/')[-1]
        new_dir_path = '/'.join(dir_path.split('/')[:-1]) + '/' + prefix + '_r_' + folder
        os.mkdir(new_dir_path)
        l = list(os.listdir(dir_path))
        l.sort()
        for f in l: # f -> file
            fpath = dir_path + '/' + f
            fname = '_'.join(f.split('.')[:-1])
            new_fpath = new_dir_path + '/' + fname + '_r_' + prefix + '.mp3'
            '''
            if not os.path.exists(new_fpath):
                open(new_fpath, 'a').close()
            '''
            for c in conv:
                fpath = fpath.replace(c, "\{}".format(c))
                new_fpath = new_fpath.replace(c, "\{}".format(c))

            comm = 'ffmpeg -i {old_file} -filter:a "atempo={rate}" -vn {new_file} -y'.format(
                old_file=fpath,
                rate=speed_rate,
                new_file=new_fpath,
            )
            print('\n=======================\n',comm,'\n==========================\n')
            os.system(comm)
            print('# {} -> finished!'.format(new_fpath))


def video_to_audio_and_change_rate(dir_path, speed_rate=2):
    prefix = '_r_{}_r_{}'.format('ToA', speed_rate)
    if os.path.exists(dir_path):
        folder = dir_path.split('/')[-1]
        new_dir_path = '/'.join(dir_path.split('/')[:-1]) + '/' + folder + prefix
        os.mkdir(new_dir_path)
        l = list(os.listdir(dir_path))
        l.sort()
        for f in l: # f -> file
            fpath = dir_path + '/' + f
            new_fpath = new_dir_path + '/' + f.split('.')[0] + prefix + '.mp3'
            '''
            if not os.path.exists(new_fpath):
                open(new_fpath, 'a').close()
            '''
            for c in conv:
                fpath = fpath.replace(c, "\{}".format(c))
                new_fpath = new_fpath.replace(c, "\{}".format(c))

            comm = 'ffmpeg -i {old_file} -f mp3 -ab 192000 -filter:a "atempo={rate}" -vn {new_file}'.format(
                old_file=fpath,
                rate=speed_rate,
                new_file=new_fpath,
            )
            print(comm)
            os.system(comm)
            print('# {} -> finished!'.format(new_fpath))


def video_to_audio(dir_path):
    prefix = '{}_r_'.format('ToAudio')
    if os.path.exists(dir_path):
        folder = dir_path.split('/')[-1]
        new_dir_path = '/'.join(dir_path.split('/')[:-1]) + '/' + prefix + folder
        os.mkdir(new_dir_path)
        l = list(os.listdir(dir_path))
        l.sort()
        for f in l: # f -> file
            fpath = dir_path + '/' + f
            new_fpath = new_dir_path + '/' + prefix + f.split('.')[0] + '.mp3'
            '''
            if not os.path.exists(new_fpath):
                open(new_fpath, 'a').close()
            '''
            for c in conv:
                fpath = fpath.replace(c, "\{}".format(c))
                new_fpath = new_fpath.replace(c, "\{}".format(c))

            comm = 'ffmpeg -i {old_file} -f mp3 -ab 192000 -vn {new_file}'.format(
                old_file=fpath,
                new_file=new_fpath,
            )
            print(comm)
            os.system(comm)
            print('# {} -> finished!'.format(new_fpath))

def get_files(bp):
    files = []
    for d in os.listdir(bp):
        if os.path.isfile(os.path.join(bp,d)):
            files.append(os.path.join(bp,d))
        elif os.path.isdir(os.path.join(bp,d)):
            _files = get_files(os.path.join(bp,d))
            files.extend(_files)
    return files

def get_audio_details(p):
    l = get_files(p)
    d = {i: MP3(i).info.length/60 for i in l}
    return d

