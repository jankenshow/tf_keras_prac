from keras import backend as K
from keras.engine.topology import Input, Container
from keras.models import Model
from keras.layers import *
from keras.optimizers import *

K.set_image_dim_ordering("tf")
print("image_dim_ordering:tf")

def get_feature_extract_model(size, channels):
    inputs = Input(shape=(size,size,channels))
    
    midout = Conv2D(32, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(inputs)
    midout = BatchNormalization()(midout)
    midout = MaxPooling2D(pool_size=(2,2), padding="same")(midout)
    midout = Conv2D(48, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(midout)
    midout = BatchNormalization()(midout)
    midout = MaxPooling2D(pool_size=(2,2), padding="same")(midout)
    midout = Conv2D(64, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(midout)
    midout = BatchNormalization()(midout)
    midout = MaxPooling2D(pool_size=(2,2), padding="same")(midout)
    
    diff1 = Conv2D(64, 1, padding="same", activation="relu",
                    kernel_initializer="he_normal")(midout)
    
    diff2 = Conv2D(64, 1, padding="same", activation="relu",
                    kernel_initializer="he_normal")(midout)
    diff2 = Conv2D(64, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(diff2)
    
    diff3 = Conv2D(64, 1, padding="same", activation="relu",
                    kernel_initializer="he_normal")(midout)
    diff3 = Conv2D(64, 5, padding="same", activation="relu",
                    kernel_initializer="he_normal")(diff3)
    
    midout = concatenate([diff1, diff2, diff3], -1)
    
    return Model(inputs=inputs, outputs=midout)


def get_distance_model(size, channels=192):
    size = size // 8
    
    inputsA = Input(shape=(size,size,channels), dtype="float32", name="A")
    inputsB = Input(shape=(size,size,channels), dtype="float32", name="B")
    
    AsubB = subtract([inputsA, inputsB])
    BsubA = subtract([inputsB, inputsA])
    
    AB = Conv2D(192, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(AsubB)
    AB = BatchNormalization()(AB)
    AB = Conv2D(192, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(AB)
    AB = BatchNormalization()(AB)
    AsubB = add([AsubB, AB])
    AsubB = MaxPool2D(pool_size=(2,2), padding="same")(AsubB)
    
    BA = Conv2D(192, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(BsubA)
    BA = BatchNormalization()(BA)
    BA = Conv2D(192, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(BA)
    BA = BatchNormalization()(BA)
    BsubA = add([BsubA, BA])
    BsubA = MaxPool2D(pool_size=(2,2), padding="same")(BsubA)
    
    out = concatenate([BsubA, AsubB], -1)
    out = Conv2D(512, 1, padding="same", activation="relu",
                    kernel_initializer="he_normal")(out)
    
    path = Conv2D(512, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(out)
    path = BatchNormalization()(path)
    path = Conv2D(512, 3, padding="same", activation="relu",
                    kernel_initializer="he_normal")(path)
    path = BatchNormalization()(path)
    out = add([out, path])
    out = MaxPool2D(pool_size=(2,2), padding="same")(out)
    
    # out = GlobalAveragePooling2D()(out)
    out = Flatten()(out)
    out = Dense(1, activation="sigmoid")(out)
    
    return Model(inputs=[inputsA, inputsB], outputs=out)


def get_net(size, channels, optimizer=Adam(lr=1e-4), session=None):
    K.clear_session()
    
    encode_layers = get_feature_extract_model(size, channels)
    distance_layers = get_distance_model(size)
    
    inputsA = Input(shape=(size,size,channels), name="A")
    inputsB = Input(shape=(size,size,channels), name="B")

#     first_input = Input(shape=(size,size,3))
#     midout = feature_extract_model(first_input)
#     encode_layers = Container(first_input, midout, name="shared")
    
    midA = encode_layers(inputsA)
    midB = encode_layers(inputsB)
    
    out = distance_layers([midA, midB])
    
#     min_midA = Lambda(lambda x: -x)(midA)
#     min_midB = Lambda(lambda x: -x)(midB)
    
#     AsubB = add([midA, min_midB])
#     BsubA = add([midB, min_midA])

#     AsubB = subtract([midA, midB])
#     BsubA = subtract([midB, midA])
    
#     AB = Conv2D(192, 3, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(AsubB)
#     AB = BatchNormalization()(AB)
#     AB = Conv2D(192, 3, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(AB)
#     AB = BatchNormalization()(AB)
#     AsubB = add([AsubB, AB])
#     AsubB = MaxPool2D(pool_size=(2,2), padding="same")(AsubB)
    
#     BA = Conv2D(192, 3, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(BsubA)
#     BA = BatchNormalization()(BA)
#     BA = Conv2D(192, 3, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(BA)
#     BA = BatchNormalization()(BA)
#     BsubA = add([BsubA, BA])
#     BsubA = MaxPool2D(pool_size=(2,2), padding="same")(BsubA)
    
# #     out = concatenate([BsubA, AsubB], -1)
# #     out = Conv2D(256, 1, padding="same", activation="relu",
# #                     kernel_initializer="he_normal")(out)
    
# #     path = Conv2D(256, 3, padding="same", activation="relu",
# #                     kernel_initializer="he_normal")(out)
# #     path = BatchNormalization()(path)
# #     path = Conv2D(256, 3, padding="same", activation="relu",
# #                     kernel_initializer="he_normal")(path)
# #     path = BatchNormalization()(path)
# #     out = add([out, path])
# #     out = MaxPool2D(pool_size=(2,2), padding="same")(out)
    
#     out = concatenate([BsubA, AsubB], -1)
#     out = Conv2D(512, 1, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(out)
    
#     path = Conv2D(512, 3, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(out)
#     path = BatchNormalization()(path)
#     path = Conv2D(512, 3, padding="same", activation="relu",
#                     kernel_initializer="he_normal")(path)
#     path = BatchNormalization()(path)
#     out = add([out, path])
#     out = MaxPool2D(pool_size=(2,2), padding="same")(out)
    
#     # out = GlobalAveragePooling2D()(out)
#     out = Flatten()(out)
#     out = Dense(1, activation="sigmoid")(out)

    
    
    if session is not None:
        K.set_session(session)
    model = Model(inputs=[inputsA, inputsB], outputs=out)
    model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["accuracy"])
    return(model)
