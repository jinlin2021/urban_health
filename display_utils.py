import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def display_residential_info(residential_df, image_df, selected_residential):
    """展示社区详细信息及图片"""
    selected_row = residential_df[residential_df['名称'] == selected_residential].iloc[0]
    
    st.write(f"### {selected_row['名称']}")
    st.write(f"描述: {selected_row['describe']}")

    # 显示图片
    images_row = image_df[image_df['ID'] == selected_row['ID']]
    
    if not images_row.empty:
        image_urls = images_row['image_urls'].tolist()
        num_images = len(image_urls)
        st.write(f"展示 {min(num_images, 9)} 张图片")
        
        # 只展示前8张图片（如果不足8张则展示全部）
        cols = st.columns(3)  # 每行展示3张图片
        for i, url in enumerate(image_urls[:9]):  # 最多展示8张
            try:
                response = requests.get(url.strip())
                img = Image.open(BytesIO(response.content))
                with cols[i % 3]:  # 循环显示在3列中
                    st.image(img, use_column_width=True)  # 设置图片宽度适应列
            except Exception as e:
                st.error(f"无法加载图片: {url}, 错误: {e}")



# 展示社区对比信息（用于社区对比，包括房价）
# 展示社区对比信息（用于社区对比，包括房价）
def display_comparison_info(residential_df, image_df, selected_residential,most_similar,least_similar):
    """展示社区对比中的详细信息，包括房价"""
    selected_row = residential_df[residential_df['名称'] == selected_residential].iloc[0]
    # 设置一个具有最小高度和最大高度的文本区域
    # 设置一个具有最小高度和最大高度的文本区域，并确保滚动条生效

    
    # Display description with increased font size for all elements and added spacing
   # Display description with increased font size for all elements and added spacing
    st.markdown(f"""
        <div style="font-size: 30px; min-height: 200px; max-height: 220px; overflow-y: auto; padding-right: 10px;">
            <p><span style='font-size: 30px;'><strong>Description:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'>{selected_row['describe']}</span></p>
            <p><span style='font-size: 30px;'><strong>House Price:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'><strong>{selected_row['房价']}</strong></span></p>
            <p><span style='font-size: 30px;'><strong>Construction Year:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'><strong>{selected_row['建筑年代']}</strong></span></p>
        </div>
    """, unsafe_allow_html=True)
    # 显示最相似和最不相似的社区信息

    # 显示最相似和最不相似的社区信息
    most_similar_row = residential_df[residential_df['ID'] == most_similar['id']].iloc[0]
    least_similar_row = residential_df[residential_df['ID'] == least_similar['id']].iloc[0]

    st.markdown(f"""
        <div style="font-size: 30px; margin-top: 20px;">
            <p><span style='font-size: 30px;'><strong>Most Similar Community:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'>{most_similar_row['名称']} ({most_similar_row['市']},{most_similar_row['县']},{most_similar_row['街道']})</span></p>
            <p><span style='font-size: 30px;'><strong>Similarity Score:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'>{most_similar['similarity']:.4f}</span></p>
            <p><span style='font-size: 30px;'><strong>Least Similar Community:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'>{least_similar_row['名称']} ({most_similar_row['市']},{most_similar_row['县']},{most_similar_row['街道']})</span></p>
            <p><span style='font-size: 30px;'><strong>Similarity Score:&nbsp;</strong></span> <span style='font-size: 24px; margin-left: 20px;'>{least_similar['similarity']:.4f}</span></p>
        </div>
    """, unsafe_allow_html=True)

    # 显示图片
    images_row = image_df[image_df['ID'] == selected_row['ID']]
    
    if not images_row.empty:
        image_urls = images_row['image_urls'].tolist()
        num_images = len(image_urls)
        
        st.write(f"<span style='font-size: 30px;'><strong>Display {num_images} images</strong></span>", unsafe_allow_html=True)

        cols = st.columns(3)  # 每行展示3张图片
        for i, url in enumerate(image_urls):  # 展示所有图片
            try:
                response = requests.get(url.strip())
                img = Image.open(BytesIO(response.content))
                with cols[i % 3]:  # 循环显示在3列中
                    st.image(img, use_column_width=True)  # 设置图片宽度适应列
            except Exception as e:
                st.error(f"无法加载图片: {url}, 错误: {e}")
