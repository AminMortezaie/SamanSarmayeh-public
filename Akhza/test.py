import os

# for i in range(2, 30):
#     # Directory
directory = "stock"+str(2)

#     # Parent Directory path
parent_dir = "DetailsData"

#     # Path
path = os.path.join(parent_dir, directory)

#     # Create the directory
#     # 'GeeksForGeeks' in
#     # '/home / User / Documents'
#     os.mkdir(path)


for f in os.listdir(path):

    for stockName in range(1, 36):
        directory = "stock"+str(stockName)
        parent_dir = "DetailsData\\"+"stock"+str(stockName)
        path = os.path.join(parent_dir, directory)
        name = ''
        e = ''
        for i in f.split("-")[1:]:
            e += "-"+i
        name = "stock"+str(stockName)+e
        path = os.path.join(parent_dir, name)
        file1 = open(path, 'a')
        file1.close()
