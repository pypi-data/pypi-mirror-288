
from .preprocess import *
from .model import *
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader, Dataset
import os
class dataset(Dataset):
    def __init__(self, path):
        self.path = path
        self.data = os.listdir(path)
        # eq_ 开头 .npy 文件 为地震数据
        # noise_ 开头 .npy 文件 为噪声数据
        self.eq_data = [file for file in self.data if file.startswith('eq_')]
        self.noise_data = [file for file in self.data if file.startswith('noise_')]
        assert len(self.eq_data) != 0, 'No earthquake data found'
        assert len(self.noise_data) != 0, 'No noise data found'
        self.labels = np.zeros(len(self.data))
        self.labels[[i for i in range(len(self.data)) if self.data[i].split('_')[0] == 'eq']] = 1
        # one-hot编码，地震数据标签为1，噪声数据标签为0
        self.labels = torch.tensor(self.labels.astype(int))
        self.labels = np.eye(2)[self.labels]
    def __len__(self):
        return len(self.labels)
    def __getitem__(self, idx):
        data = np.load(self.path+'/'+self.data[idx]) / 5
        label = self.labels[idx]
        data = torch.from_numpy(data).unsqueeze(0)
        label = torch.from_numpy(label).float()
        return data, label
class trainer():
    def __init__(self, model,trainset_path, device='cpu',batch_size=32):
        self.model = model
        self.model.eval()
        if torch.cuda.is_available() and device == 'cuda':
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        self.model.to(device)
        self.trainset_path = trainset_path
        self.trainset = dataset(self.trainset_path)
        self.trainloader = DataLoader(self.trainset, batch_size=batch_size, shuffle=True)
    def train(self, epochs=10, lr=0.001):
        self.model.train()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.BCELoss()
        for epoch in range(epochs):
            running_loss = 0.0
            for i, data in enumerate(self.trainloader, 0):
                inputs, labels = data
                inputs, labels = inputs.float().to(self.device), labels.to(self.device)
                optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
            print(f'Epoch {epoch+1}, loss: {running_loss/len(self.trainloader)}')
