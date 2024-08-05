import os

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

from pystocky.data_processor.processor import DataProcessor
from pystocky.models.LSTM import LSTMModel


class Trainer(object):
    models = {
        'LSTM': LSTMModel,
    }

    def __init__(self, config: dict, target='close', model='LSTM'):
        self.config = config
        self.device = torch.device(self.config['device'])
        self.target = target
        self.modelname = model

        if model not in self.models:
            # Unrecognized model type
            raise TypeError('Model type unrecognized: %s' % model)
        else:
            self.model = self.models[model]().to(self.device)

        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.config['lr'])
        self.scheduler = optim.lr_scheduler.LambdaLR(self.optimizer, self.adjust_lr)

        self.scaler, self.train_dataset, self.test_dataset = DataProcessor.get_dataset_for_lstm(
            config['data'],
            config['look_back'],
            config['train_set_ratio'],
            target
        )
        self.train_loader = DataLoader(self.train_dataset, batch_size=32, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=32, shuffle=False)
        self.epoch = -1
        self.best_loss = -1
        self.avg_val_loss = -1

    def adjust_lr(self, epoch):
        total_epochs = self.config['epochs']
        start_lr = self.config['lr']
        end_lr = start_lr * 0.01
        update_lr = ((total_epochs - epoch) / total_epochs) * (start_lr - end_lr) + end_lr
        return update_lr * (1 / self.config['lr'])

    def step(self):
        running_loss = 0

        # 训练
        for i, batch in enumerate(self.train_loader):
            x_batch, y_batch = batch[0].to(self.device), batch[1].to(self.device)

            out = self.model(x_batch)

            loss = self.criterion(out, y_batch)
            running_loss += loss.item()

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        self.scheduler.step()
        avg_loss_epoch = running_loss / len(self.train_loader)
        # print(f'Epoch: {self.epoch}, Avg. Loss: {avg_loss_epoch}')
        running_loss = 0

    def save_best_model(self):
        if not os.path.exists(self.config['output']):
            os.makedirs(self.config['output'])
        torch.save(self.model.state_dict(), os.path.join(self.config['output'], 'best_model.pth'))
        print(f'Val Epoch: {self.epoch} - Best model saved at {self.config['output']}')

    def validate(self):
        self.model.eval()
        val_loss = 0
        with torch.no_grad():
            for _, batch in enumerate(self.test_loader):
                x_batch, y_batch = batch[0].to(self.device), batch[1].to(self.device)
                y = self.model(x_batch)
                loss = self.criterion(y, y_batch)
                val_loss += loss.item()
            self.avg_val_loss = val_loss / len(self.test_loader)
            # print(f'Epoch: {self.epoch}, Validation Loss: {avg_val_loss}')

        if self.epoch == 1:
            self.best_loss = self.avg_val_loss

        # 保存最佳模型
        if self.avg_val_loss < self.best_loss:
            self.best_loss = self.avg_val_loss
            self.save_best_model()

    def train(self):
        t = tqdm(range(1, self.config['epochs'] + 1))
        for self.epoch in t:
            self.model.train()
            self.step()
            self.validate()
            t.set_description(f'Epoch {self.epoch}, ' + ('Avg loss=%.6f' % self.avg_val_loss))

    def show(self):
        with torch.no_grad():
            # load best model
            best_model_path = os.path.join(self.config['output'], 'best_model.pth')
            self.model.load_state_dict(torch.load(best_model_path, weights_only=True))
            self.model.eval()
            x_train, y_train = self.train_dataset.get()
            x_test, y_test = self.test_dataset.get()
            train_predictions = self.model(x_train.to(self.device)).to('cpu').numpy().flatten()
            val_predictions = self.model(x_test.to(self.device)).to('cpu').numpy().flatten()

        dummies = np.zeros((x_train.shape[0], self.config['look_back'] + 1))
        dummies[:, 0] = train_predictions
        dummies = self.scaler.inverse_transform(dummies)
        train_predictions = dummies[:, 0].copy()

        dummies = np.zeros((x_test.shape[0], self.config['look_back'] + 1))
        dummies[:, 0] = val_predictions
        dummies = self.scaler.inverse_transform(dummies)
        val_predictions = dummies[:, 0].copy()

        dummies = np.zeros((x_train.shape[0], self.config['look_back'] + 1))
        dummies[:, 0] = y_train.flatten()
        dummies = self.scaler.inverse_transform(dummies)
        new_y_train = dummies[:, 0].copy()

        dummies = np.zeros((x_test.shape[0], self.config['look_back'] + 1))
        dummies[:, 0] = y_test.flatten()
        dummies = self.scaler.inverse_transform(dummies)
        new_y_test = dummies[:, 0].copy()

        plt.figure(figsize=(10, 6))
        plt.subplot(1, 2, 1)

        plt.plot(new_y_train, color='red', label='Actual ')
        plt.plot(train_predictions, color='blue', label='Predicted', alpha=0.5)
        plt.xlabel('Date')
        plt.ylabel(self.target)
        plt.title(f'Stock Price Prediction with {self.modelname} by pystocky (train)')
        # plt.legend()

        plt.subplot(1, 2, 2)
        # plt.figure(figsize=(10, 6))
        plt.plot(new_y_test, color='red', label='Actual')
        plt.plot(val_predictions, color='blue', label='Predicted', alpha=0.5)
        plt.xlabel('Date')
        plt.ylabel(self.target)
        plt.title(f'Stock Price Prediction with {self.modelname} by pystocky (test)')
        # plt.legend()

        plt.show()
