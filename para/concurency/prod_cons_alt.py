#! /usr/bin/python3

import time
import random
import sys
from multiprocessing import Process, Lock, Condition, Value, Array



### Monitor start
class Buffer:
    def __init__(self, nb_cases):
        self.verrou = Lock()
        self.nb_cases = nb_cases
        self.last_prod_type = Value('i',-1,lock=False)
        self.nb_elem = Value('i',0,lock=False)
        self.nb_cons_wait = Value('i',0,lock=False)
        self.storage_val = Array('i', [-1] * nb_cases,lock=False)
        self.storage_type = Array('i', [-1] * nb_cases,lock=False)
        self.ptr_prod = Value('i',0,lock=False)
        self.ptr_cons = Value('i',0,lock=False)
        self.access = [[Condition(self.verrou),Condition(self.verrou)],Condition(self.verrou)]

    def produce(self, msg_val, msg_type, msg_source):
        with self.verrou:
            while self.nb_elem.value == self.nb_cases or self.last_prod_type.value == msg_type:
                self.access[0][msg_type].wait()
            position = self.ptr_prod.value
            print('process %2d starts prod %2d (type:%d) in place %2d and the buffer is\t\t %s' %
                (msg_source, msg_val, msg_type, position, self.storage_val[:]))
            time.sleep(random.random())
            self.storage_val[position] = msg_val
            self.storage_type[position] = msg_type
            self.nb_elem.value += 1
            self.last_prod_type.value= msg_type
            self.ptr_prod.value = (position + 1) % self.nb_cases
            print('process %2d    produced %2d (type:%d) in place %2d and the buffer is\t\t %s' %
                (msg_source, msg_val, msg_type, position, self.storage_val[:]))
            print(self.nb_cons_wait.value)
            if self.nb_cons_wait.value >0:
                self.access[1].notify()
                print("unlock conso")
            else:
                self.access[0][(msg_type+1)%2].notify()


    def consume(self, id_cons):
        with self.verrou:
            while self.nb_elem.value == 0:
                self.nb_cons_wait.value += 1
                self.access[1].wait()
                self.nb_cons_wait.value -= 1
            position = self.ptr_cons.value
            result = self.storage_val[position]
            result_type = self.storage_type[position]
            print('\tprocess %2d starts cons %2d (type:%d) in place %2d and the buffer is\t %s' %
                  (id_cons, result, result_type, position, self.storage_val[:]))
            time.sleep(random.random())
            type_cons = self.storage_type[position] 
            self.storage_val[position] = -1
            self.storage_type[position] = -1
            self.nb_elem.value -= 1
            self.ptr_cons.value = (position + 1) % self.nb_cases
            print('\tprocess %2d    consumed %2d (type:%d) in place %2d and the buffer is\t %s' %
                  (id_cons, result, result_type, position, self.storage_val[:]))
            self.access[0][(self.last_prod_type.value+1)%2].notify()
            return result

#### Monitor end

def producer(msg_val, msg_type, msg_source, nb_times, buffer):
    for _ in range(nb_times):
        time.sleep(random.random())
        buffer.produce(msg_val, msg_type, msg_source)
        msg_val += 1


def consumer(id_cons, nb_times, buffer):
    for _ in range(nb_times):
        time.sleep(random.random())
        buffer.consume(id_cons)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: %s <Nb Prod <= 20> <Nb Conso <= 20> <Nb Cases <= 20> <Nb times prod> <Nb times cons>" % sys.argv[0])
        sys.exit(1)

    nb_prod = int(sys.argv[1])
    nb_cons = int(sys.argv[2])
    nb_cases = int(sys.argv[3])

    nb_times_prod = int(sys.argv[4])
    nb_times_cons = int(sys.argv[5])

    buffer = Buffer(nb_cases)
    
    producers, consumers = [], []
    
    for id_prod in range(nb_prod):
        msg_val_start, msg_type, msg_source = id_prod * nb_times_prod, id_prod % 2, id_prod
        prod = Process(target=producer, args=(msg_val_start, msg_type, msg_source, nb_times_prod, buffer))
        prod.start()
        producers.append(prod)

    for id_cons in range(nb_cons):
        cons=Process(target=consumer, args=(id_cons, nb_times_cons, buffer))
        cons.start()
        consumers.append(cons)

    for prod in producers:
        prod.join()

    for cons in consumers:
        cons.join()
