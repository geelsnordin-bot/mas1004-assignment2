"""Your Track A recipe: how the fixed model is trained on your selection.

src/official.py imports this file and calls the functions below. Change
anything in it. The grader copies this one file and your selection.csv to its
own computer and runs src/official.py with them, so everything your recipe
needs has to be in this file: it cannot read other files, download anything,
or load another model.

What you cannot change, because official.py decides it:
  - the model: ResNet18 with the ImageNet weights, a new last layer of 5
  - the photos: only the ones in selection.csv, with the city of their folder
  - how many photos go through the network in training: rules.TRACK_A_BUDGET
    (250,000). A bigger batch means fewer steps, not more photos.
  - the image size the model sees, 224 x 224
  - mixed precision (float16), and the seed

This is the recipe the starter code came with. It is the baseline on the
leaderboard.
"""

import collections
import copy

import torch
import torch.nn.functional as F
from torchvision import transforms as T

BATCH_SIZE = 64


def train_transform():
    """A function that turns one training photo (a PIL image) into a 224 x 224 one.

    It may return a PIL image or a float tensor (3, 224, 224) with values
    0..1. official.py normalises it afterwards. It runs once every time a
    photo is drawn, so the same photo looks different every time.
    """
    return T.Compose([
        T.RandomResizedCrop(224, scale=(0.35, 1.0)),
        T.ColorJitter(0.2, 0.2, 0.2),
    ])


def sample_weights(cities, paths):
    """How often each photo in your selection is drawn.

    cities and paths are lists, one entry per row of selection.csv. Return a
    list of positive numbers of the same length, where a photo with weight 2
    is drawn twice as often as one with weight 1. Return None to go through
    the selection in a new random order each time, every photo once per round.
    """
    counts = collections.Counter(cities)
    return [1.0 / counts[c] for c in cities]


def make_optimizer(model):
    return torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.05)


def make_scheduler(optimizer, total_steps):
    """Stepped once after every training step. total_steps is BUDGET // BATCH_SIZE."""
    return torch.optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=3e-4, total_steps=total_steps, pct_start=0.15)


def mix(images, labels):
    """Change a batch on the GPU before the model sees it.

    images is (BATCH_SIZE, 3, 224, 224), normalised; labels is (BATCH_SIZE,)
    city numbers. Return images of the same shape and the targets for
    loss_fn: the labels, or probabilities (BATCH_SIZE, 5) if you mix photos.
    """
    return images, labels


def loss_fn(logits, targets):
    return F.cross_entropy(logits, targets, label_smoothing=0.1)


EMA_DECAY = 0.999  # the average covers roughly the last 1000 steps
_ema = {}


def on_step(step, total_steps, model, optimizer):
    """Called after every step, with the step number from 0. Returns nothing."""
    # Keep a running average of the weights next to the model (EMA).
    with torch.no_grad():
        if "model" not in _ema:
            _ema["model"] = copy.deepcopy(model)
            return
        decay = min(EMA_DECAY, (1 + step) / (10 + step))
        avg = _ema["model"].state_dict()
        for name, value in model.state_dict().items():
            if value.dtype.is_floating_point:
                avg[name].mul_(decay).add_(value, alpha=1 - decay)
            else:
                avg[name].copy_(value)


def final_model(model):
    """The model to hand in, at the end of training. It must still be the same ResNet18."""
    # Hand in the averaged weights instead of the last ones.
    return _ema.get("model", model)
