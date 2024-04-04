import json
import matplotlib.pyplot as plt

def main():
    with open("githubs.txt") as f:
        packages = f.read().strip().split('\n')
        one_percents = []
        two_percents = []
        three_percents = []
        four_percents = []
        with open("contrib_top.txt", "w") as top_f:
            for package in packages:
                try:
                    with open("./repos/" + package.strip() + "/contributors.json") as contrib:
                        dct = json.load(contrib)
                        total = 0
                        for entry in dct:
                            total += entry["contributions"]
                        running = 0
                        try:
                            running += dct[0]["contributions"]
                        except:
                            pass
                        one_percents.append(float(running) / float(total))

                        try:
                            running += dct[1]["contributions"]
                        except:
                            pass
                        two_percents.append(float(running) / float(total))
                        if (float(running) / float(total) > 0.8):
                            print(package, file=top_f)

                        try:
                            running += dct[2]["contributions"]
                        except:
                            pass
                        three_percents.append(float(running) / float(total))

                        try:
                            running += dct[3]["contributions"]
                        except:
                            pass
                        four_percents.append(float(running) / float(total))

                except:
                    pass
        
        fig, ax = plt.subplots(2,2)
        fig.tight_layout()
        plt.setp(ax, ylim=[0, 4500])
        plt.subplot(221)
        ax[0,0].set_title("Top 1 contributors")
        plt.hist(one_percents)
        plt.subplot(222)
        ax[0,1].set_title("Top 2 contributors")
        plt.hist(two_percents)
        plt.subplot(223)
        ax[1,0].set_title("Top 3 contributors")
        plt.hist(three_percents)
        plt.subplot(224)
        ax[1,1].set_title("Top 4 contributors")
        plt.hist(four_percents)
        plt.savefig("plot.png")


        print("Top 1 > 80%:", sum(1 for i in one_percents if i >= 0.8) / len(one_percents))
        print("Top 2 > 80%:", sum(1 for i in two_percents if i >= 0.8) / len(one_percents))
        print("Top 3 > 80%:", sum(1 for i in three_percents if i >= 0.8) / len(one_percents))
        print("Top 4 > 80%:", sum(1 for i in four_percents if i >= 0.8) / len(one_percents))

main()
