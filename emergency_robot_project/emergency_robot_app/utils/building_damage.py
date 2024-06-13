import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torchvision.transforms as transforms

class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.double_conv(x)


class DownBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DownBlock, self).__init__()
        self.double_conv = DoubleConv(in_channels, out_channels)
        self.down_sample = nn.MaxPool2d(2)

    def forward(self, x):
        skip_out = self.double_conv(x)
        down_out = self.down_sample(skip_out)
        return (down_out, skip_out)


class UpBlock(nn.Module):
    def __init__(self, in_channels, out_channels, up_sample_mode):
        super(UpBlock, self).__init__()
        if up_sample_mode == 'conv_transpose':
            self.up_sample = nn.ConvTranspose2d(in_channels-out_channels, in_channels-out_channels, kernel_size=2, stride=2)
        elif up_sample_mode == 'bilinear':
            self.up_sample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        else:
            raise ValueError("Unsupported `up_sample_mode` (can take one of `conv_transpose` or `bilinear`)")
        self.double_conv = DoubleConv(in_channels, out_channels)

    def forward(self, down_input, skip_input):
        x = self.up_sample(down_input)
        x = torch.cat([x, skip_input], dim=1)
        return self.double_conv(x)


class UNet(nn.Module):
    def __init__(self, in_channels=6, out_classes=5, up_sample_mode='conv_transpose'):
        super(UNet, self).__init__()
        self.up_sample_mode = up_sample_mode
        # Downsampling Path
        self.down_conv1 = DownBlock(in_channels, 64)
        self.down_conv2 = DownBlock(64, 128)
        self.down_conv3 = DownBlock(128, 256)
        self.down_conv4 = DownBlock(256, 512)
        # Bottleneck
        self.double_conv = DoubleConv(512, 1024)
        # Upsampling Path
        self.up_conv4 = UpBlock(512 + 1024, 512, self.up_sample_mode)
        self.up_conv3 = UpBlock(256 + 512, 256, self.up_sample_mode)
        self.up_conv2 = UpBlock(128 + 256, 128, self.up_sample_mode)
        self.up_conv1 = UpBlock(128 + 64, 64, self.up_sample_mode)
        # Final Convolution
        self.conv_last = nn.Conv2d(64, out_classes, kernel_size=1)

    def forward(self, x):
        x, skip1_out = self.down_conv1(x)
        x, skip2_out = self.down_conv2(x)
        x, skip3_out = self.down_conv3(x)
        x, skip4_out = self.down_conv4(x)
        x = self.double_conv(x)
        x = self.up_conv4(x, skip4_out)
        x = self.up_conv3(x, skip3_out)
        x = self.up_conv2(x, skip2_out)
        x = self.up_conv1(x, skip1_out)
        x = self.conv_last(x)
        return x

# Load the pre-trained model
model_path = '/Users/egemeneroglu/Desktop/Files/Projects/CapstoneProject/emergency_robot_project/emergency_robot_app/best_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load(model_path, map_location=device)
model.eval()

def load_image(path):
    """Load an image from the given path."""
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def preprocess_image(image, transform):
    """Preprocess the image for the model."""
    image = transform(image)
    return image

def visualize(pre_image, post_image, overlayed, heatmap):
    """Visualize the images and masks."""
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    axes[0].imshow(pre_image)
    axes[0].set_title('Pre Image')
    axes[0].axis('off')
    
    axes[1].imshow(post_image)
    axes[1].set_title('Post Image')
    axes[1].axis('off')
    
    axes[2].imshow(overlayed)
    axes[2].set_title('Overlayed Mask')
    axes[2].axis('off')
    
    axes[3].imshow(heatmap)
    axes[3].set_title('Heatmap')
    axes[3].axis('off')
    
    plt.show()

# Define image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((512, 512))  # Resize to match model input size
])

# Load and preprocess the images
pre_image_path = 'pre_image.png'
post_image_path = 'post_image.png'
pre_image = load_image(pre_image_path)
post_image = load_image(post_image_path)
pre_image_tensor = preprocess_image(pre_image, transform)
post_image_tensor = preprocess_image(post_image, transform)

# Concatenate the images to have 6 input channels
input_tensor = torch.cat([pre_image_tensor, post_image_tensor], dim=0).unsqueeze(0).to(device)

# Make an inference
with torch.no_grad():
    logits = model(input_tensor).squeeze().cpu().numpy()

# Combine the heatmaps into one
combined_heatmap = sum(logits[i] for i in range(1, 5))

# Convert logits to class indices
pred_mask = np.argmax(logits, axis=0)

overlayed_image = np.zeros((pred_mask.shape[0], pred_mask.shape[1], 3), dtype=np.uint8)

# Define colors for each class
colors = {
    0: [0, 0, 0],       # Black for background
    1: [0, 255, 0],     # Green for level 1 damage
    2: [255, 255, 0],   # Yellow for level 2 damage
    3: [255, 69, 0],    # Orange for level 3 damage
    4: [255, 0, 0]      # Red for level 4 damage
}

for cls in range(5):
    overlayed_image[pred_mask == cls] = colors[cls]

# Visualize the images and masks
visualize(pre_image, post_image, overlayed_image, combined_heatmap)