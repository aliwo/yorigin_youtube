# 카테고리 지역 타겟팅

* 홈 카테고리의 성능을 빠르게 할 방법을 고민했습니다.
* mongodb 와 mongodb 내부의 google s2 를 사용합니다. (2dsphere 인덱스 사용)
* 주어진 Point 에서 배달 가능한 매장이 1개라도 있는 모든 카테고리를 distinct 해서 가져옵니다.
* github action 에서 간단한 성능 테스트 (apache bench) 를 수행합니다.


## 테스트 방법

![random_seoul_area.png](assets%2Frandom_seoul_area.png)
1. leaflet 과 turf.js 를 사용해서 서울을 중심으로 랜덤한 폴리곤을 생성합니다.
2. 랜덤 카테고리, 랜덤 폴리곤을 mongodb 에 적재합니다.
3. 랜덤한 Point 를 잡고, 그 지역에서 배달 가능한 카테고리를 쿼리합니다.
