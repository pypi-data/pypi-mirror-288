#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   Peike Li
@Contact :   peike.li@yahoo.com
@File    :   simple_extractor.py
@Time    :   8/30/19 8:59 PM
@Desc    :   Simple Extractor
@License :   This source code is licensed under the license found in the
             LICENSE file in the root directory of this source tree.
"""

import os
import torch
import argparse
import numpy as np
from PIL import Image
import cv2
from tqdm import tqdm
import gdown
from collections import OrderedDict

from torch.utils.data import DataLoader
import torchvision.transforms as transforms

from .networks import init_model
from .utils.transforms import get_affine_transform, transform_logits
from .datasets.simple_extractor_dataset import SimpleImagelistDataset

dataset_settings = {
    'lip': {
        'input_size': [473, 473],
        'num_classes': 20,
        'label': ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat',
                  'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm',
                  'Left-leg', 'Right-leg', 'Left-shoe', 'Right-shoe']
    },
    'atr': {
        'input_size': [512, 512],
        'num_classes': 18,
        'label': ['Background', 'Hat', 'Hair', 'Sunglasses', 'Upper-clothes', 'Skirt', 'Pants', 'Dress', 'Belt',
                  'Left-shoe', 'Right-shoe', 'Face', 'Left-leg', 'Right-leg', 'Left-arm', 'Right-arm', 'Bag', 'Scarf']
    },
    'pascal': {
        'input_size': [512, 512],
        'num_classes': 7,
        'label': ['Background', 'Head', 'Torso', 'Upper Arms', 'Lower Arms', 'Upper Legs', 'Lower Legs'],
    }
}

class SCHP:
    def __init__(self, dataset_type, model_dir):
        self.dataset_type = dataset_type
        self.model_dir = model_dir
        self.model = None
        self.init_model()

        
    def init_model(self):
        num_classes = dataset_settings[self.dataset_type]['num_classes']

        self.model = init_model('resnet101', num_classes=num_classes, pretrained=None)

        if self.dataset_type == 'lip':
            url = 'https://drive.google.com/uc?id=1k4dllHpu0bdx38J7H28rVVLpU-kOHmnH'
        elif self.dataset_type == 'atr':
            url = 'https://drive.google.com/uc?id=1ruJg4lqR_jgQPj-9K0PP-L2vJERYOxLP'
        elif self.dataset_type == 'pascal':
            url = 'https://drive.google.com/uc?id=1E5YwNKW2VOEayK9mWCS3Kpsxf-3z04ZE'
        
        model_restore = os.path.join(self.model_dir, f'{self.dataset_type}_checkpoint.pth')
        if not os.path.exists(model_restore):
            os.makedirs(os.path.dirname(model_restore), exist_ok=True)
            gdown.download(url, model_restore, quiet=False)

        state_dict = torch.load(model_restore)['state_dict']
        
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = k[7:]  # remove `module.`
            new_state_dict[name] = v
        self.model.load_state_dict(new_state_dict)
        self.model.cuda()
        self.model.eval()


    def parse(self, images, logits_result=False):
        input_size = dataset_settings[self.dataset_type]['input_size']

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.406, 0.456, 0.485], std=[0.225, 0.224, 0.229])
        ])
        dataset = SimpleImagelistDataset(
            image_list=images, input_size=input_size, transform=transform
        )
        dataloader = DataLoader(dataset)

        result_list = []
        with torch.no_grad():
            for idx, batch in enumerate(tqdm(dataloader)):
                image, meta = batch
                img_name = 'test.png'
                c = meta['center'].numpy()[0]
                s = meta['scale'].numpy()[0]
                w = meta['width'].numpy()[0]
                h = meta['height'].numpy()[0]

                output = self.model(image.cuda())
                upsample = torch.nn.Upsample(
                    size=input_size, mode='bilinear', align_corners=True
                )
                upsample_output = upsample(output[0][-1][0].unsqueeze(0))
                upsample_output = upsample_output.squeeze()
                upsample_output = upsample_output.permute(1, 2, 0)  # CHW -> HWC

                result = transform_logits(
                    upsample_output.data.cpu().numpy(), 
                    c, s, w, h, 
                    input_size=input_size
                )
                if not logits_result:
                    result = np.argmax(result, axis=-1)
                result_list.append(result)

        results = np.stack(result_list)
        return results
        
        
    def get_label(self):
        label = dataset_settings[self.dataset_type]['label']
        
        return label




if __name__ == '__main__':
    image_path = 'inputs/3acb3342-43e5-46aa-a613-41798101ae62.png'
    dataset_type = "lip"
    model_dir = 'checkpoints'

    images = [
        cv2.imread(image_path, cv2.IMREAD_COLOR),
        cv2.imread(image_path, cv2.IMREAD_COLOR),
        cv2.imread(image_path, cv2.IMREAD_COLOR),
        cv2.imread(image_path, cv2.IMREAD_COLOR),
    ]
    images = np.stack(images)

    schp_model = SCHP(dataset_type, model_dir)
    
    human_parsing_results = schp_model.parse(
        images=images, 
    )
    print(human_parsing_results.shape)

    label = schp_model.get_label()
    print(label)
