from importlib.metadata import version

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scipy.stats as stats
from sklearn.neighbors import KernelDensity


class distribution:
    
    def __init__(self, dataset):
        self.dataset = []
        for idx, each_dataset in enumerate(dataset):
            if isinstance(each_dataset, pd.Series): # series가 들어왔을 때에는 ndarray로 변환. dataframe[컬럼명]으로 넣으면 series가 들어오게 되기 때문.
                self.dataset.append(each_dataset.values)
            elif isinstance(each_dataset, np.ndarray): # ndarray라면 아무 조정도 하지 않는다.
                self.dataset.append(each_dataset)
            else:
                raise ValueError("Each dataset must be a pandas series or a numpy ndarray.")
    
    @staticmethod
    def scott_bandwidth(data): # sklearn 1.2버전부터 KernelDensity의 bandwidth에서 'scott', 'silverman'을 받을 수 있다. 그 이전 버전이라면, 직접 계산해서 bandwidth를 넣어야 한다.
        std_dev = np.std(data, ddof=1)
        n = len(data)
        iqr = np.percentile(data, 75) - np.percentile(data, 25)
        bandwidth = 1.06 * min(std_dev, iqr / 1.34) * n ** (-1 / 5)
        return bandwidth
    
    def plot_histogram_kde(self, names, title, height, width, kernel = 'gaussian', bandwidth = None, bins = 10, opacity = 0.75, colors = None, display_quantiles = {'n_list':False, 'line_dash':'dot'}, display_maxinum_peak_density = {'use':False, 'line_dash':'dot'}, display_mean = {'use':False, 'line_dash':'dot'}):
        if colors is None:
            colors = ['blue', 'green', 'red', 'purple', 'orange']
        
        hist_data = []
        kde_data = []
        quantile_lines = []
        
        for i, each_data in enumerate(self.dataset):
            # Histogram
            hist = go.Histogram(
                x = each_data
              , nbinsx = bins
              , opacity = opacity
              , name = f'Histogram of {names[i]}'
              , marker_color = colors[i % len(colors)]
              , legendgroup = f"{names[i]}"
              , legendgrouptitle_text = f"{names[i]}"
            )
            hist_data.append(hist)
            
            # KDE
            x_vals = np.linspace(each_data.min(), each_data.max(), 1000)
            
            if kernel == 'gaussian':
                bw_method = 'scott' if bandwidth is None else bandwidth
                kde = stats.gaussian_kde(each_data, bw_method=bw_method)
                kde_vals = kde(x_vals)
            elif kernel == 'epanechnikov':
                if bandwidth is None and version('scikit-learn') < '1.2.0':
                    bandwidth = distribution.scott_bandwidth(each_data)
                elif bandwidth is None:
                    bandwidth = 'scott'
                kde = KernelDensity(bandwidth=bandwidth, kernel='epanechnikov')
                kde.fit(each_data.reshape(-1, 1))
                kde_vals = np.exp(kde.score_samples(x_vals.reshape(-1, 1)))
            
            kde_line = go.Scatter(
                x = x_vals
              , y = kde_vals
              , mode = 'lines'
              , name = f'KDE of {names[i]}'
              , line = dict(color = colors[i % len(colors)])
              , yaxis = 'y2'
              , legendgroup = f"{names[i]}"
              , legendgrouptitle_text = f"{names[i]}"
            )
            kde_data.append(kde_line)

            if display_maxinum_peak_density['use']:
                mean_val = np.mean(each_data)
                quantile_lines.append(go.Scatter(
                    x = [mean_val, mean_val]
                  , y = [0, max(kde_vals)]
                  , mode = 'lines'
                  , name = f'{names[i]}의 최대밀도 지점'
                  , line = dict(color = colors[i % len(colors)], dash = 'dot')
                  , yaxis = 'y2'
                  , legendgroup = f"{names[i]}"
                  , legendgrouptitle_text = f"{names[i]}"
                ))
                
            if display_mean['use']:
                max_likelihood = x_vals[np.argmax(kde_vals)]
                quantile_lines.append(go.Scatter(
                    x = [max_likelihood, max_likelihood]
                  , y = [0, max(kde_vals)]
                  , mode = 'lines'
                  , name = f'{names[i]}의 평균'
                  , line = dict(color = colors[i % len(colors)], dash = 'dot')
                  , yaxis = 'y2'
                  , legendgroup = f"{names[i]}"
                  , legendgrouptitle_text = f"{names[i]}"
                ))
                
            if display_quantiles['n_list'] != False:
                qs = np.percentile(each_data, display_quantiles['n_list'])
                for idx, each in enumerate(display_quantiles['n_list']):
                    quantile_lines.append(go.Scatter(
                        x = [qs[idx], qs[idx]]
                      , y = [0, max(kde_vals)]
                      , mode = 'lines'
                      , name = f'{names[i]}의 {each}th Quantile'
                      , line = dict(color = colors[i % len(colors)], dash = display_quantiles['line_dash'])
                      , yaxis = 'y2'
                      , legendgroup = f"{names[i]}"
                      , legendgrouptitle_text = f"{names[i]}"
                    ))
        
        hist_kde_fig = go.Figure(
            data = hist_data + kde_data + quantile_lines
        )
        hist_kde_fig.update_layout(
            title = f'Histogram & KDE / {title}'
          , xaxis_title = 'Value'
          , yaxis = {
                'title' : 'Histogram count'
          }
          , yaxis2 = {
                'title' : 'KDE likelihood'
              , 'overlaying' : 'y'
              , 'side' : 'right'
              , 'showgrid': False
           }
          , legend = {
              'x' : 1.08
            , 'groupclick' : 'toggleitem'
          }
          , barmode = 'overlay'
          , height = height
          , width = width
        )
        return hist_kde_fig
        
    def plot_box(self, names, title, height, width, colors = None):
        if colors is None:
            colors = ['blue', 'green', 'red', 'purple', 'orange']
        
        box_data = []
        
        for i, each_data in enumerate(self.dataset):
            box = go.Box(
                y = each_data
              , name = f'Box plot of {names[i]}'
              , marker_color = colors[i % len(colors)]
            )
            box_data.append(box)
        
        box_fig = go.Figure(data = box_data)
        box_fig.update_layout(
            title = f'Box Plot / {title}'
          , yaxis_title = 'Value'
          , height = height
          , width = width
        )
        return box_fig