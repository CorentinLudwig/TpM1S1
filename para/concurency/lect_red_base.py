#! /usr/bin/python3

import sys
import time
import random
from multiprocessing import Process, Lock, Condition, Value, Array

class RW:
    def __init__(self):
        self.verrou = Lock()
        self.nb_reader = 0
        self.nb_writer_wait = 0
        self.writing = False
        self.access = [Condition(self.verrou),Condition(self.verrou)]

    def start_read(self):
        with self.verrou:
            while self.writing:
                self.access[1].wait()
            self.nb_reader +=1

    def end_read(self):
        with self.verrou:
            self.nb_reader -=1
            if nb_reader == 0 and self.nb_writer_wait>0:
                self.access[0].notify()
            else:
                self.access[1].notify()

    def start_write(self):
        with self.verrou:
            while self.nb_reader>0 or  self.writing :
                self.nb_writer_wait += 1
                self.access[0].wait()
                self.nb_writer_wait -= 1
            self.writing = True

    def end_write(self):
        with self.verrou:
            self.writing = False
            
            if self.nb_writer_wait > 0:
                self.access[0].notify()
            else:
                self.access[1].notify()


def process_writer(identifier, synchro):
    synchro.start_write()
    for _ in range(5):
        with open('LectRed_shared', 'a') as file_id:
            txt=str(identifier)
            file_id.write(txt)
            print('Writer', identifier, 'just wrote', txt)
        time.sleep(.1 + random.random())            
    synchro.end_write()
    
def process_reader(identifier, synchro):
    synchro.start_read()
    position = 0
    result = ''
    while True:
        time.sleep(.1 + random.random())            
        with open('LectRed_shared', 'r') as file_id:
            file_id.seek(position, 0)
            txt = file_id.read(1)
            if len(txt) == 0:
                break
            print('Reader', identifier, 'just read', txt)
            result += txt
            position+=1
    print('Reader', str(identifier)+' has read:',result)
    synchro.end_read()
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: %s <Nb reader> <Nb writer> \n" % sys.argv[0])
        sys.exit(1)

    nb_reader = int(sys.argv[1])
    nb_writer = int(sys.argv[2])

    synchro = RW()

    # To initialize the common data
    with open('LectRed_shared', 'w') as file_id:
        file_id.write('')
    
    processes = []
    for id_writer in range(nb_writer):
        writer = Process(target=process_writer, args=(id_writer,synchro))
        writer.start()
        processes.append(writer)

    for id_reader in range(nb_reader):
        reader = Process(target=process_reader, args=(id_reader,synchro))
        reader.start()
        processes.append(reader)

    for process in processes:
        process.join()
