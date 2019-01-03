import GenerateDataForGame as genData

count = 10
dic = {}

for _ in range(count):
    game, res = genData.createRandomGame()
    # dic[tuple(game)] = res

# print(dic)
