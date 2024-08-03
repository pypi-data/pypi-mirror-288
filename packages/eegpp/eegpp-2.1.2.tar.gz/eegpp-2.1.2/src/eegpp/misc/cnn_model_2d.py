import torch
from torch import nn
from torch.nn import MaxPool1d, MaxPool2d


class MNAPooling(nn.Module):
    def __init__(self, kernel_size=3, stride=2):
        super().__init__()
        self.max_pooling = nn.MaxPool1d(kernel_size=kernel_size, stride=stride)
        self.avg_pooling = nn.AvgPool1d(kernel_size=kernel_size, stride=stride)

    def forward(self, x):
        mx = self.max_pooling(x)
        avg = self.avg_pooling(x)
        return torch.concat([mx, avg], dim=1)


class BiMaxPooling(nn.Module):
    def __init__(self, kernel_size=3, stride=2):
        super().__init__()
        self.max_pooling = nn.MaxPool1d(kernel_size=kernel_size, stride=stride)

    def forward(self, x):
        mx1 = self.max_pooling(x)
        mx2 = self.max_pooling(-x)
        return torch.concat([mx1, mx2], dim=1)


class CNNModel2(nn.Module):
    def __init__(self, n_class, n_base=16, n_conv=8):
        super().__init__()
        self.n_class = n_class
        self.type = "CNN2"

        self.layer1 = nn.Sequential(nn.Dropout(0.1),
                                    nn.Conv2d(1, n_base * 3, kernel_size=(3,11), stride=4, padding=0),
                                    # nn.BatchNorm1d(n_base * 3),
                                    nn.ReLU(),
                                    # nn.MaxPool1d(kernel_size=3, stride=2)
                                    MaxPool2d(kernel_size=(1,5), stride=1)
                                    )

        self.layer2 = nn.Sequential(nn.Conv2d(n_base * 3, n_base * 8, kernel_size=(3,5), stride=1, padding=2),
                                    # nn.BatchNorm1d(n_base * 8),
                                    nn.ReLU(),
                                    MaxPool2d(kernel_size=(3,5), stride=2))

        self.layer3 = nn.Sequential(nn.Conv2d(n_base * 8 , n_base * 20, kernel_size=(3,5), stride=1, padding=2),
                                    # nn.BatchNorm1d(n_base * 10),
                                    nn.ReLU(),
                                    MaxPool2d(kernel_size=(3,5), stride=2)
                                    )

        self.layer4 = nn.Sequential(nn.Conv2d(n_base * 20 , n_base * 8, kernel_size=(3,5), stride=1, padding=2),
                                    # nn.BatchNorm1d(n_base * 8),
                                    nn.ReLU(),
                                    MaxPool2d(kernel_size=(3,5), stride=2)
                                    )

        self.layer5 = nn.Sequential(nn.Conv2d(n_base * 8 , n_base * 6, kernel_size=(3,5), stride=1, padding=2),
                                    # nn.BatchNorm1d(n_base * 6),
                                    nn.ReLU(),
                                    MaxPool2d(kernel_size=(3,5), stride=2)
                                    )
        # self.fc1 = nn.Sequential(nn.Dropout(0.1), nn.Linear(2304, 320), nn.ReLU())
        self.fc1 = nn.Sequential(nn.Dropout(0.1), nn.Linear(1152, 320), nn.ReLU())

        # self.fc1 = nn.Sequential(nn.Dropout(0.1), nn.Linear(768, 320), nn.ReLU())

        self.fc2 = nn.Sequential(nn.Linear(320, n_class))

    def forward(self, x):
        # print("X", x.shape)

        out = self.layer1(x)
        # print(out.shape)
        # exit(-1)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = out.reshape(out.size(0), -1)
        # print(out.shape)
        # exit(-1)
        out = self.fc1(out)
        out = self.fc2(out)
        return out
