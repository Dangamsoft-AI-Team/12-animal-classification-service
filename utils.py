from PIL import Image
from torchvision import transforms
from torch.autograd import Variable
import io
from PIL import Image

def inference(model, img_bytes):
    model.eval()

    encoder = {0: 'chicken', 1: 'cow', 2: 'dog', 3: 'dragon', 4: 'horse', 5: 'monkey', 6: 'mouse', 7: 'pig', 8: 'rabbit', 9: 'sheep', 10: 'snake', 11: 'tiger'}

    imsize=300
    mean, std = [0.49787724, 0.46538547, 0.458713], [0.27272928, 0.26059055, 0.25504208]
    
    test_transforms = transforms.Compose([transforms.Resize(size=(imsize, imsize)),
                                                                      transforms.ToTensor(),
                                                                      transforms.Normalize(mean, std)])

    image =  Image.open(io.BytesIO(img_bytes)).convert('RGB')

    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)

    input = Variable(image_tensor)

    output = model(input)[0].detach().numpy()

    return output