# ===========================================================
# storage_subway_busapi/02_bus/verify.py
#
#   버스노선 적재 검증
#       - 필수 컬럼 NULL 여부
#       - 대구 좌표 범위
#       - 위치구분 값 분포 점검
#
# ===========================================================================
from sqlalchemy import text
from database import engine
import geopandas as gpd
from shapely.geometry import Point

# verify() 함수 밖에서 폴리곤 준비
gdf_sido = gpd.read_file("./file/sido/bnd_sido_00_2025_2Q.shp")
gdf_daegu = gdf_sido[gdf_sido["SIDO_CD"] == "22"].to_crs(epsg=4326)
daegu_polygon = gdf_daegu.geometry.union_all()

# 대구 구,군 + '기타'(경계 밖 지역) 허용값 목록
GU_LIST = {
    "경산시",
    "고령군",
    "구미시",
    "군위군",
    "남구",
    "달서구",
    "달성군",
    "동구",
    "북구",
    "서구",
    "수성구",
    "영천시",
    "의성군",
    "중구",
    "칠곡군",
    "창녕군",
}

def verify():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM bus_stop")).scalar()

        # 위도/경도 NULL 개수를 한 번의 쿼리로 동시에 집계
        null_check = conn.execute(text("""
            SELECT COUNT(*) FILTER (WHERE 위도 IS NULL) AS null_lat,
                   COUNT(*) FILTER (WHERE 경도 IS NULL) AS null_lon
            FROM bus_stop
        """)).fetchone() # 딱 한 행만

        # 대구 대략적인 경계값을 벗어나는 좌표 건수 확인
        #   (위도,경도 중 하나라도 범위를 벗어나면 or 조건으로 카운트)
        coords = conn.execute(text(
            "SELECT 위도, 경도 FROM bus_stop WHERE 위도 IS NOT NULL AND 경도 IS NOT NULL"
        )).fetchall()        
        out_of_range = sum(1 for lat, lon in coords if not daegu_polygon.contains(Point(lon, lat)))

        # 시군구 컬럼에 들어있는 고유값들을 모두 가져와서 GU_LIST에 없는 값들만 걸러낸다
        gu_values = conn.execute(text(
            "SELECT DISTINCT 시군구 FROM bus_stop"
        )).fetchall()
        invalid_gu = []
        for g in gu_values:
            if g[0] not in GU_LIST:
                invalid_gu.append(g[0])

    print('==== 적재 검증 결과 ====')
    print(f'전체 건수 : {total:,}')
    print(f'위도 NULL 건수 : {null_check[0]}')
    print(f'경도 NULL 건수 : {null_check[1]}')
    print(f'좌표 범위 이탈 건수 : {out_of_range}')
    print(f'시군구 이상값 : {invalid_gu if invalid_gu else "없음"}')

    ok = (null_check[0] == 0 and null_check[1] == 0 and out_of_range == 0 
          and not invalid_gu)
    print(f'검증 결과 : {ok}')
    return ok

if __name__ == '__main__':
    verify()