from multiprocessing import Process, Manager

def g(d):
        d['{}-{}'.format(1,2)]['1'] = True


if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        e = manager.dict()
        for i in range(2):
            e[str(i)] = False
        print(e)
        d['1-2'] = e
        d['2-1'] = e
        e = manager.dict()
        print('Valor de 0: {}, Valor de 1: {}'.format(d['1-2']['0'], d['1-2']['1']))
        p = Process(target=g, args=(d,))
        p.start()
        p.join()
        print('Valor de 0: {}, Valor de 1: {}'.format(d['1-2']['0'], d['1-2']['1']))
        print('Valor de 0: {}, Valor de 1: {}'.format(d['1-2']['0'], d['1-2']['1']))
        print(e)
