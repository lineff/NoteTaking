import os

if __name__ == "__main__":
    for i in range(100):
        p = "E:\\PyProjects\\Notepad\\test\\%s.txt" % str(i)
        f = open(p, "w")
        f.close()