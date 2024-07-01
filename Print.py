import matplotlib.pyplot as plt


def plot_imgs(data_list, title_list, n_cols = 2, size=(10,8)):
    fig = plt.figure(figsize=size) 
    
    # setting values to rows and column variables 
    rows = (len(data_list) // n_cols) + (1 if len(data_list) % n_cols != 0 else 0)
    columns = n_cols

    count = 0
    for i in range(len(data_list)):
        count += 1
        fig.add_subplot(rows, columns, count) 
    
        plt.imshow(data_list[count - 1], cmap='gray', vmin=0, vmax=255) 
        plt.axis('off') 
        plt.title(title_list[count - 1], fontsize=2 * min(7, min(size)))
        
    plt.show()
    
def plot_img(fig, titulo):
    plt.figure(figsize=(6,6))
    plt.imshow(fig, cmap='gray', vmin=0, vmax=255)
    plt.title(titulo)
    plt.axis('off')
    plt.show()
