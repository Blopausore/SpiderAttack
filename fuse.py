##
#%%
import os

repertoires=[
    "Initialisation",
    "Entitees",    
    "Populations",
    "Reactions/Comportements",
    "Reactions/Signaux",
    "Loop"
]

path_ = lambda f: "/home/smaug/Documents/CodingGames/SpiderAttack/" + f + ("/" if not "." in f else "")


def parcour(file_path : str):
    l=[]
    for file in os.listdir(file_path):
        path=file_path + file
        if os.path.isdir(path):
            l.extends(parcour(path+"/")) #afin de parcouri meme les fichiers présent dans celui mère
        elif  path.split(".")[-1] == "py": 
            l.append(path)
    return l


main = open("/home/smaug/Documents/CodingGames/SpiderAttack/main.py","w")

for repo in repertoires:
    print(repo)
    for script_path in parcour(path_(repo)):
        print("\t"+script_path)
        main.write("###" + script_path.split("/")[-1]+"\n")

        with open(script_path,"r") as script:   
            write_on = False
            for ligne in script.readlines():
                print("\t \t",ligne)
                if write_on:
                    main.write(ligne)
                if ligne[:len("#start-of-file")] == "#start-of-file":
                    write_on = True

            main.write("\n\n\n")



# %%
