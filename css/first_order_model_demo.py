# -*- coding: utf-8 -*-
"""first-order-model-demo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/AliaksandrSiarohin/first-order-model/blob/master/demo.ipynb

# Demo for paper "First Order Motion Model for Image Animation"

**Clone repository**
"""

!git clone https://github.com/AliaksandrSiarohin/first-order-model

cd first-order-model

"""**Mount your Google drive folder on Colab**"""

from google.colab import drive
drive.mount('/content/gdrive')

"""**Add folder https://drive.google.com/drive/folders/1kZ1gCnpfU0BnpdU47pLM_TQ6RypDDqgw?usp=sharing  to your google drive.**

**Load driving video and source image**
"""

import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
from IPython.display import HTML
import warnings
warnings.filterwarnings("ignore")

source_image = imageio.imread('/content/gdrive/My Drive/first-order-motion-model/02.png')
driving_video = imageio.mimread('/content/gdrive/My Drive/first-order-motion-model/04.mp4')


#Resize image and video to 256x256

source_image = resize(source_image, (256, 256))[..., :3]
driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

def display(source, driving, generated=None):
    fig = plt.figure(figsize=(8 + 4 * (generated is not None), 6))

    ims = []
    for i in range(len(driving)):
        cols = [source]
        cols.append(driving[i])
        if generated is not None:
            cols.append(generated[i])
        im = plt.imshow(np.concatenate(cols, axis=1), animated=True)
        plt.axis('off')
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
    plt.close()
    return ani
    

HTML(display(source_image, driving_video).to_html5_video())

"""**Create a model and load checkpoints**"""

from demo import load_checkpoints
generator, kp_detector = load_checkpoints(config_path='config/vox-256.yaml', 
                            checkpoint_path='/content/gdrive/My Drive/first-order-motion-model/vox-cpk.pth.tar')

"""**Perfrorm image animation**"""

from demo import make_animation
from skimage import img_as_ubyte

predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)

#save resulting video
imageio.mimsave('../generated.mp4', [img_as_ubyte(frame) for frame in predictions])
#video can be downloaded from /content folder

HTML(display(source_image, driving_video, predictions).to_html5_video())

"""**In the cell above we use relative keypoint displacement to animate the objects. We can use absolute coordinates instead,  but in this way all the object proporions will be inherited from the driving video. For example Putin haircut will be extended to match Trump haircut.**"""

predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=False, adapt_movement_scale=True)
HTML(display(source_image, driving_video, predictions).to_html5_video())

"""## Running on your data

**First we need to crop a face from both source image and video, while simple graphic editor like paint can be used for cropping from image. Cropping from video is more complicated. You can use ffpmeg for this.**
"""

!ffmpeg -i /content/gdrive/My\ Drive/first-order-motion-model/07.mkv -ss 00:08:57.50 -t 00:00:08 -filter:v "crop=600:600:760:50" -async 1 hinton.mp4

"""**Another posibility is to use some screen recording tool, or if you need to crop many images at ones use face detector(https://github.com/1adrianb/face-alignment) , see https://github.com/AliaksandrSiarohin/video-preprocessing for preprcessing of VoxCeleb.**"""

source_image = imageio.imread('/content/gdrive/My Drive/first-order-motion-model/lak.JPG')
driving_video = imageio.mimread('hinton.mp4', memtest=False)


#Resize image and video to 256x256

source_image = resize(source_image, (256, 256))[..., :3]
driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True,
                             adapt_movement_scale=True)

HTML(display(source_image, driving_video, predictions).to_html5_video())

#for new drive video
!ffmpeg -i /content/gdrive/My\ Drive/first-order-motion-model/04.mp4 -ss 00:00:00.10 -t 00:00:04 -async 1 act.mp4

source_image = imageio.imread('/content/gdrive/My Drive/first-order-motion-model/lak.JPG')
driving_video = imageio.mimread('act.mp4', memtest=False)


#Resize image and video to 256x256

source_image = resize(source_image, (256, 256))[..., :3]
driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True,
                             adapt_movement_scale=True)

HTML(display(source_image, driving_video, predictions).to_html5_video())