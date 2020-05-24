


# model
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.layers import BatchNormalization
from keras.layers import SpatialDropout2D
from keras.layers import Flatten
from keras.models import Sequential
from keras.layers import Dropout
from keras.preprocessing import image
from keras.models import load_model

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# visuao tools
import matplotlib
import matplotlib.pyplot as plt




class defects_classifier:

    def make_model(activation='relu', loss='categorical_crossentropy', optimizer='sgd', sp_dropout=0.1, dropout=0.1):
    
        conv_model_gaus_dr = Sequential()

        conv_model_gaus_dr.add(Conv2D(32, (3, 3), input_shape=(150, 150, 1), activation=activation))
        conv_model_gaus_dr.add(BatchNormalization())
        conv_model_gaus_dr.add(Conv2D(64, (3, 3), activation=activation))
        conv_model_gaus_dr.add(MaxPool2D((2, 2)))
        conv_model_gaus_dr.add(SpatialDropout2D(sp_dropout))
        conv_model_gaus_dr.add(Conv2D(128, (3, 3), activation=activation))
        conv_model_gaus_dr.add(MaxPool2D((2, 2)))
        conv_model_gaus_dr.add(SpatialDropout2D(sp_dropout))
        conv_model_gaus_dr.add(Conv2D(256, (3, 3), activation=activation))
        conv_model_gaus_dr.add(MaxPool2D((2, 2)))
        conv_model_gaus_dr.add(Flatten())
        conv_model_gaus_dr.add(Dropout(dropout))
        conv_model_gaus_dr.add(Dense(512, activation='relu'))
        conv_model_gaus_dr.add(Dense(4, activation='softmax'))



        conv_model_gaus_dr.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
    
        return conv_model_gaus_dr
    
    
    
    def plot_accuracy(self, history, title, x_width, label_size = 15, save=True):
    
        matplotlib.rcParams.update({'font.size': label_size})
    
        fig, ax = plt.subplots(figsize=(10, 8))
    
        plt.plot(history.history['accuracy'], c='r', label='Training')
        plt.plot(history.history['val_accuracy'], c='b', label='Validation')
        plt.xticks(np.arange(1, len(history.history['val_accuracy'])+1, x_width))
        plt.legend()
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title(title)
    
        if save:
            plt.savefig(title + '_accuracy.png')
        
        plt.show()
        
        
        
    def plot_loss(self, history, title, x_width, label_size = 15, save=True):
    
        matplotlib.rcParams.update({'font.size': label_size})
    
        fig, ax = plt.subplots(figsize=(10, 8))
    
        plt.plot(history.history['loss'], c='r', label='Training')
        plt.plot(history.history['val_loss'], c='b', label='Validation')
        plt.xticks(np.arange(1, len(history.history['val_accuracy'])+1 , x_width))
        plt.legend()
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title(title)
    
        if save:
            plt.savefig(title + '_loss.png')
        
        plt.show()
        
        
    def convert_class(self, y):
    
        lb_list = []
    
        for i in y:
        
            i = list(i)
        
            i_mx = max(i)
        
            i_id = i.index(i_mx)
        
            lb_list.append(i_id)
        
        return np.array(lb_list)
    
    
    def load_model(model):
        
        model_trd_aug = load_model(model)
        
        return model_trd_aug
    
    
    
    def cl_report(self, model, imgs, lbls_true, dataset):

        lbls_pred = model.predict(imgs)

        lbls_pred = convert_class(lbls_pred)
        lbls_tr = convert_class(lbls_true)

        print('{}'.format(dataset))
        print('')
        print('Confusion Matrix')
        print('')

        print(confusion_matrix(lbls_tr, lbls_pred))

        print('')

        print('Classification Report')
        print('')

        print(classification_report(lbls_tr, lbls_pred))