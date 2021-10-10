"""
This code is used to batch detect images in a folder.
"""
import argparse
import os
import sys
import time
import cv2

from vision.ssd.config.fd_config import define_img_size

parser = argparse.ArgumentParser(
    description='detect_imgs')

parser.add_argument('--net_type', default="RFB", type=str,
                    help='The network architecture ,optional: RFB (higher precision) or slim (faster)')
parser.add_argument('--input_size', default=320, type=int,
                    help='define network input size,default optional value 128/160/320/480/640/1280')
parser.add_argument('--threshold', default=0.85, type=float,
                    help='score threshold')
parser.add_argument('--candidate_size', default=1500, type=int,  # 只保留前 candidate_size 个 boxes 其余的不考虑了
                    help='nms candidate size')
parser.add_argument('--path', default="./fire", type=str,
                    help='imgs dir')
parser.add_argument('--test_device', default="cpu", type=str,
                    help='cuda:0 or cpu')
args = parser.parse_args()
define_img_size(
    args.input_size)  # must put define_img_size() before 'import create_mb_tiny_fd, create_mb_tiny_fd_predictor'

from vision.ssd.mb_tiny_fd import create_mb_tiny_fd, create_mb_tiny_fd_predictor
from vision.ssd.mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd, create_Mb_Tiny_RFB_fd_predictor

result_path = "./detect_imgs_results"
label_path = "./voc-model-labels.txt"
test_device = args.test_device

class_names = [name.strip() for name in open(label_path).readlines()]
if args.net_type == 'slim':
    model_path = "models/pretrained/version-slim-320.pth"
    # model_path = "models/pretrained/version-slim-640.pth"
    net = create_mb_tiny_fd(len(class_names), is_test=True, device=test_device)
    predictor = create_mb_tiny_fd_predictor(net, candidate_size=args.candidate_size, device=test_device)
elif args.net_type == 'RFB':
    # model_path = "models/train-version-RFB/RFB-Epoch-215-Loss-2.787177402491963.pth"
    model_path = "./RFB-220.pth"
    model_path2 = "./RFB-Epoch-100-Loss-2.7303400649580847.pth"
    #  model_path = "models/pretrained/version-RFB-320.pth"
    net = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True, device=test_device)
    net2 = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True, device=test_device)
    predictor = create_Mb_Tiny_RFB_fd_predictor(net, candidate_size=args.candidate_size, device=test_device)
    predictor2 = create_Mb_Tiny_RFB_fd_predictor(net2, candidate_size=args.candidate_size, device=test_device)
else:
    print("The net type is wrong!")
    sys.exit(1)
net.load(model_path)
net2.load(model_path2)

if not os.path.exists(result_path):
    os.makedirs(result_path)
listdir = os.listdir(args.path)

With = 1280
high = 720
# camera = cv2.VideoCapture(0)  ## get camera handle
# camera.set(With, high)
success = True
# print(frame.shape)



def detect(frame):
    ok = False
    sum = 0
    Tstart = time.time()
    print(frame.shape)

    if success == True:
        orig_image = cv2.resize(frame, (With, high))
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        boxes, labels, probs = predictor.predict(image, args.candidate_size / 2, args.threshold)
        boxes2, labels2, probs2 = predictor2.predict(image, args.candidate_size / 2, args.threshold)
        print(boxes)
        sum += boxes.size(0)
        print("labels is:" + str(labels))
        print("probs is:" + str(probs))
        for i in range(boxes.size(0)):
            ok = True
            box = boxes[i, :]

            x_1 = box[0].item()
            rectimg = orig_image[int(box[1].item()):int(box[3].item()), int(box[0].item()):int(box[2].item())]
            newImgName = img_name = str(time.time()).replace('.', '') + '.jpg'
            print(newImgName)
            print(rectimg)

            if (rectimg.any()):
                lenshi = rectimg
                print(rectimg)
                rectimg = cv2.resize(rectimg, (500, 500))
                cv2.imwrite("./人脸抓拍/" + newImgName, rectimg)
            cv2.rectangle(orig_image, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
            # label = f"""{voc_dataset.class_names[labels[i]]}: {probs[i]:.2f}"""
            # label = f"{probs[i]:.2f}"
            label = labels[i];
        # cv2.putText(orig_image, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # cv2.putText(orig_image, str(labels), (box[0], box[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        Tend = time.time()  # %2.2f  ms'%(t)
        cv2.putText(orig_image, str(boxes.size(0)) + "  time:" + str(Tend - Tstart), (30, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2)

        # t = (Tend - Tstart) * 1000.0
        # timestr = 'time: %2.2f  ms' % (t)
        # cv2.putText(orig_image, "time: "+str(int(Tend - Tstart)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow('fire', orig_image)
        cv2.waitKey(1)

    return ok
