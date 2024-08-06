# TORDA
- TOols for Repetitive Data Analysis
- 분석 업무 진행 시, 반복해서 수행하게 되는 작업들을 모듈화 하기 위한 패키지입니다.

## 현재 존재하는 함수
### visualization class
- Parameters:
    - dataset : list of pandas series or numpy ndarray
        - pandas series, 혹은 numpy ndarray를 원소로 가지는 리스트를 할당.
- 사용 예시:
```python
from torda.visualization import distribution as vd
vd = vd(dataset=[np.random.randn(1000), np.random.randn(1000)+2])
```

`plot_histogram_kde(names, title, height, width, kernel = 'gaussian', bandwidth = None, bins = 10, opacity = 0.75, colors = None, display_quantiles = {'n_list':False, 'line_dash':'dash'}, display_maxinum_peak_density = {'use':False, 'line_dash':'dot'}, display_mean = {'use':False, 'line_dash':'dot'})`
- Parameters:
    - names : list of string
        - dataset 리스트 내 각 데이터의 이름.
    - title : string
        - 플롯의 제목.
    - height : int
        - 플롯의 높이.
    - width : int
        - 플롯의 폭.
    - kernel : {'gaussian', 'epanechnikov'}, default = 'gaussian'
        - KDE 진행 시 어떤 kernel function을 사용할 지 선택.
    - bandwidth : float, default = None
        - KDE 진행 시 bandwidth를 수동으로 선택하고 싶을 경우 숫자를 할당
    - bins : int, default = 10
        - 히스토그램의 bin 숫자.
    - opacity : float, default = 0.75
        - 히스토그램의 투명도.
    - colors : list of string, default = None
        - 데이터별 색.
    - display_quantiles : dictionary, default = {'n_list':False, 'line_dash':'dash'}
        - n_list에 정수 리스트를 할당하면, 해당하는 백분위수를 horizontal line으로 출력한다.
        - line_dash에는 아래와 같은 문자열들이 할당될 수 있다.
            - ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
            - '5px 10px 2px 2px', '5, 10, 2, 2', '10% 20% 40%'...
                - 선분의 형태를 조절할 수 있다.
    - display_maxinum_peak_density : dictionary, default = {'use':False, 'line_dash':'dot'}
        - True일 경우, KDE 결과에서 가장 밀도가 높은 peak를 점선으로 표시.
        - line_dash에는 아래와 같은 문자열들이 할당될 수 있다.
            - ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
            - '5px 10px 2px 2px', '5, 10, 2, 2', '10% 20% 40%'...
                - 선분의 형태를 조절할 수 있다.
    - display_mean : dictionary, default = {'use':False, 'line_dash':'dot'}
        - True일 경우, 평균 값을 점선으로 표시.
        - line_dash에는 아래와 같은 문자열들이 할당될 수 있다.
            - ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
            - '5px 10px 2px 2px', '5, 10, 2, 2', '10% 20% 40%'...
                - 선분의 형태를 조절할 수 있다.

`plot_box(names, title, height, width, colors = None)`
- Parameters:
    - names : list of string
        - dataset 리스트 내 각 데이터의 이름.
    - title : string
        - 플롯의 제목.
    - height : int
        - 플롯의 높이.
    - width : int
        - 플롯의 폭.
    - colors : list of string, default = None
        - 데이터별 색.

## 사용 예시
```Python
import pandas as pd
import numpy as np
from torda.visualization import distribution as vd

vd = vd(dataset=[np.random.randn(1000), np.random.randn(1000)+2])
vd.plot_histogram_kde(
    names=['Sample A', 'Sample B']
  , title='test_title'
  , height=600, width=1200, bins=60, opacity=0.5
  , display_quantiles={'n_list':[50], 'line_dash':'dash'}
  , display_maxinum_peak_density={'use':True, 'line_dash':'solid'}
  , display_mean={'use':True, 'line_dash':'5px 10px 2px 2px'}
  , kernel = 'gaussian'
).show()
vd.plot_box(
    names=['Sample A', 'Sample B']
  , title='test_title'
  , height=600, width=1200
).show()
```