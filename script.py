import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def display_data_model():
    """
    Load and display image
    """
    try:
        
        img = mpimg.imread('yanki_data_model.drawio.png')
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.axis('off')
        plt.title('Data Model')
        plt.show()
    except FileNotFoundError:
        print("Image file not found")
    except Exception as e:
        print('An Error occur while displaying the image', e)
    
    
def save_to_csv(dataframe: dict, folder="dataset/clean_data"):
    
    try:
        for name, df in dataframe.items():
            path = f"{folder}/{name}.csv"
            df.to_csv(path, index=False)
            print(f"{name} saved successfully to path:{path}")
    except Exception as e:
        print("Error Saving {name}.csv ", e)
    