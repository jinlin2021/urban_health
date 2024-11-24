import pydeck as pdk
import streamlit as st

def display_map(poi_df, residential_df, latitude, longitude):
    """使用 pydeck 显示 POI 和小区地图"""
    poi_layer = pdk.Layer(
        'ScatterplotLayer',
        data=poi_df,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 160]',  # 红色标记表示 POI
        get_radius=100,  # POI 半径
    )

    residential_layer = pdk.Layer(
        'ScatterplotLayer',
        data=residential_df,
        get_position='[lon, lat]',
        get_color='[0, 128, 255, 200]',  # 蓝色标记表示小区
        get_radius=400,  # 半径设置
        pickable=True,  # 设置可点击
    )

    # 配置 pydeck 地图
    deck = pdk.Deck(
        # map_style='mapbox://styles/mapbox/dark-v9',
        map_style= 'mapbox://styles/mapbox/streets-v11',
        initial_view_state=pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=12,
            pitch=10,
        ),
        layers=[poi_layer, residential_layer],
        tooltip={"text": "{名称}"}
    )

    # 显示地图
    st.pydeck_chart(deck, use_container_width=True,height=800)
    st.markdown(
    """
    <div class="note-text" style="margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 22px;">
        <strong>Note:</strong> The blue markers on the map indicate residential communities, representing various neighborhoods within a 15-minute living circle across the city. The red markers represent Points of Interest (POIs) categorized into 10 different types, including food, shopping, sports and fitness, tourist attractions, leisure and entertainment, life services, education and training, culture and media, transportation facilities, and stores.
    </div>
    """, 
    unsafe_allow_html=True
    )
