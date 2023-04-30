import matplotlib.pyplot as plt


def plot_pomo_yesterday_today(total_pomo_yesterday, total_pomo_today, yesterday=None, today=None, save_image=False):

    if yesterday == None:
        raise Exception("Yesterday cannot be None")
    
    if today == None:
        raise Exception("Today cannot be None")

    x = [yesterday.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')]
    y = [total_pomo_yesterday, total_pomo_today]

    # create a plot
    plt.figure(figsize=(3, 3))
    plt.bar(x, y, width=0.25)
    plt.xticks([0, 1], x)

    # for i, label in enumerate(x):
    #     label = 'yesterday' if i == 0 else 'today'
    #     plt.text(i, -1.25, label, ha='center', va='baseline', fontsize=8)

    plt.title('Pomo Yesterday-Today Comparison')
    plt.ylabel('Pomo Count')
    plt.show()

    if save_image and today is not None:
        plt.savefig(f"{today.strftime('%Y-%m-%d')}.png")
