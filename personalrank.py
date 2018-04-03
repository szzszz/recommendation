def PersonalRank(G, alpha, root, max_step):
    rank = dict()  
    for x in G.keys():
        rank[x] = 0

    rank[root] = 1

    for k in range(max_step):
        print(str(k))
        tmp = dict()
        for x in G.keys():
            tmp[x] = 0
        for i, ri in G.items():
            for j, wij in ri.items():
                tmp[j] += alpha * rank[i] / (1.0 * len(ri))  
                if j == root:
                    tmp[j] += (1 - alpha)
        # coverage
        check = []
        for k in tmp.keys():
            check.append(tmp[k] - rank[k])

        if sum(check) <= 0.0001:
            break

        rank = tmp

        for n in rank.keys():
            print("%s:%.3f \t"%(n, rank[n]))
        print
    return rank


if __name__ == '__main__' :
    G = {'A' : {'a' : 1, 'c' : 1},
        'B' : {'a' : 1, 'b' : 1, 'c':1, 'd':1},
        'C' : {'c' : 1, 'd' : 1},
        'a' : {'A' : 1, 'B' : 1},
        'b' : {'B' : 1},
        'c' : {'A' : 1, 'B' : 1, 'C':1},
        'd' : {'B' : 1, 'C' : 1}}

    items_dict = {'a':0,'b':0,'c':0,'d':0}

    rank = PersonalRank(G, 0.85, 'A', 50)
    for k in items_dict.keys():
        if k in rank:
            items_dict[k] = rank[k]
    #sort:
    result = sorted(items_dict.items(), key = lambda d: d[1], reverse=True)
    print("\nThe result:")
    for k in result:
        print("%s:%.3f \t"%(k[0], k[1]))
    print
