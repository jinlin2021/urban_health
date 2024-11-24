import pandas as pd

def load_city_data(city, cities):
    """加载选定城市的 POI、小区和图片数据"""
    poi_file_path = f"data/{city}/{cities[city]['poi_file']}"
    residential_file_path = f"data/{city}/{cities[city]['residential_file']}"
    image_file_path = f"data/{city}/{cities[city]['image_file']}"

    try:
        poi_df = pd.read_csv(poi_file_path)
        residential_df = pd.read_csv(residential_file_path)
        image_df = pd.read_csv(image_file_path)
        return poi_df, residential_df, image_df
    except Exception as e:
        return None, None, None

# 加载社区数据 (ID和名称)
def load_residential_data(csv_file):
    """从CSV文件加载社区数据"""
    df = pd.read_csv(csv_file)
    return df



# """加载社区的嵌入数据"""
def load_similarity_data(city,cities):
    """从Parquet文件加载相似度数据"""
    parquet_file = f"data/{city}/{cities[city]['similarity_file']}"
    df = pd.read_csv(parquet_file)
    return df
