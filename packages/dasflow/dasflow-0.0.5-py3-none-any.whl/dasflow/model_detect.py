from .preprocess import *
from .model import *
from matplotlib import pyplot as plt
class detector():
    def __init__(self, model, device='cuda'):
        self.model = model
        self.model.eval()
        if torch.cuda.is_available() and device == 'cuda':
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        self.model.to(device)

    def detect(
            self, 
            data, 
            fil='bandpass', # 滤波器类型，可选值为'bandpass'或'Gauss'，默认为'bandpass'
            S_L=True, # 是否应用sta/lta算法，可选值为True或False，默认为True
            bandpass=[2,8], # bandpass滤波器的频率范围，可选值为[low,high]，默认为[2,8]
            freq=200,  # 采样频率，默认为100
            sl=[0.1,1], # sta/lta算法的sta和lta时间窗口，可选值为[sta,lta]，默认为[0.5,1]
            beta=0, # 高斯滤波器的标准差，默认为0
            kernel=(3,3), # 高斯滤波器的核大小，默认为(3,3)
            hwin=512,  # 时间窗口大小，默认为512
            wwin=512,  # 道窗口大小，默认为512
            overlap=0.25, # 重叠率，默认为0.25
            figure=True # 是否显示检测结果，默认为False
            ):
        """
        Detects the seismic events in the input data.

        Args:
            data (numpy.ndarray): The input data to be detected.
            fil (int, optional): The type of filter to be applied. Defaults to 2.
            S_L (int, optional): Whether to apply a line detection algorithm. Defaults to 1.

        Returns:
            numpy.ndarray: The detected events.
        """
        data = preprocess(data, fil=fil, S_L=S_L, bandpass=bandpass,freq=freq, sl=sl,beta=beta,kernel=kernel)
        datas = auto_split(data,hwin=hwin,wwin=wwin,overlap=overlap)
        a,b,_,_ = datas.shape
        datas = torch.from_numpy(datas)
        datas = datas.float().to(self.device).view(-1, 1, hwin, wwin)
        with torch.no_grad():
            outputs = self.model(datas)
            outputs = outputs.cpu().numpy()
            outputs = outputs.reshape(a,b,2)
            output_class = np.argmax(outputs, axis=2)
        datas = datas.cpu().numpy().reshape(a,b,hwin,wwin)    
        if figure:
            plt.figure(figsize=(12, 6))
            for i in range(a):
                for j in range(b):
                    plt.subplot(a,b,i*b+j+1)
                    plt.imshow(datas[i,j],cmap='seismic',alpha = output_class[i,j] * 0.5 + 0.5,aspect='auto')   
                    plt.axis('off')
            plt.tight_layout()
            plt.show()
        return output_class
    
    def change_model(self, model):
        self.model = model
        self.model.eval()
        self.model.to(self.device)