import GenerateDataForGame as gen_data
import FileWorker as fw

count = 200000
dic = {}

for _ in range(count):
    game, res = gen_data.create_random_game()
    dic[tuple(game)] = res

print(len(dic.keys()))
fw.save_dict_to_file(dic)
