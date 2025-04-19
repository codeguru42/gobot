from utils.fileinfo import FileInfo


def decode_file_info(data):
    return FileInfo(tarfile=data['tarfile'], filename=data['filename'])
