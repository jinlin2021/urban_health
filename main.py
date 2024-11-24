import streamlit as st
from data_loader import load_city_data, load_similarity_data
from map_visualization import display_map
from similarity_calculator import calculate_similarity
from display_utils import display_residential_info, display_comparison_info
import streamlit.components.v1 as components  # 用于加载 HTML

# 设置页面布局为宽屏模式
st.set_page_config(layout="wide")

# Step 1: 选择城市
cities = {
    "beijing": {"lat": 39.9042, "lon": 116.4074, "poi_file": "beijing_POI_sampled.csv", "residential_file": "sampled_residential.csv", "image_file": "selected_residential_image.csv", "similarity_file": "beijing_similarity_sampled.csv", "street_health_file1": "街道的kmeans聚类情况_小修.html","street_health_file2": "60岁以上老年分级图_小修.html"},
    "shanghai": {"lat": 31.2304, "lon": 121.4737, "poi_file": "shanghai_POI.csv", "residential_file": "shanghai_residential.csv", "image_file": "shanghai_image.csv", "similarity_file": "shanghai_similarity.parquet"},
    "other city":{},
}

# 疾病信息字典
disease_info = {
    "MCI": {
        "description": "MCI is a condition where a person experiences noticeable declines in cognitive abilities, such as memory or attention, that are greater than normal aging but do not significantly impact daily life. There are two main types: Amnestic MCI, which mainly affects memory and is linked to Alzheimer’s disease, and Non-Amnestic MCI, which affects other areas like language or problem-solving. While not everyone with MCI develops dementia, it increases the risk. Early detection and care can help slow progression and improve quality of life.",
        "beijing_html": "2020年北京街道患病人口分布_MCI.html",
        "shanghai_html": "2020年上海街道患病人口分布_MCI.html"
    },
    "Hypertension": {
        "description": "Hypertension is a condition where the force of blood against the artery walls is consistently too high. It is often called the silent killer because it may not present symptoms but significantly increases the risk of heart disease, stroke, and kidney problems. Hypertension is classified into two types: Primary hypertension, which develops gradually over years, and Secondary hypertension, caused by underlying conditions. Early detection, lifestyle changes, and medication can effectively manage this condition.",
        "beijing_html": "2020年北京街道患病人口分布_Hypertension.html",
        "shanghai_html": "2020年上海街道患病人口分布_Hypertension.html"
    },
    "Diabetes": {
        "description": "Diabetes is a chronic health condition that affects how your body turns food into energy. There are three main types: Type 1 diabetes, where the body does not produce insulin; Type 2 diabetes, where the body cannot use insulin effectively; and Gestational diabetes, which occurs during pregnancy. Uncontrolled diabetes can lead to complications such as heart disease, kidney damage, nerve damage, and vision problems. Management includes monitoring blood sugar levels, maintaining a healthy diet, exercising, and using medications or insulin therapy if needed.",
        "beijing_html": "2020年北京街道患病人口分布_Diabetes.html",
        "shanghai_html": "2020年上海街道患病人口分布_Diabetes.html"
    },
    "MDD": {
        "description": "MDD is a mental health condition characterized by persistent feelings of sadness, hopelessness, and a lack of interest in activities once enjoyed. Symptoms may include changes in appetite, sleep disturbances, fatigue, difficulty concentrating, and thoughts of self-harm. MDD can be triggered by genetic, biological, environmental, and psychological factors. Effective treatments include psychotherapy, medication, and lifestyle changes to improve overall mental health and quality of life.",
        "beijing_html": "2020年北京街道患病人口分布_MDD.html",
        "shanghai_html": "2020年上海街道患病人口分布_MDD.html"
    }
}





# 设置侧边栏导航的样式
st.sidebar.markdown("""
    <style>
.sidebar-title {
    font-size: 40px;
    font-weight: bold;
    color: #34495E;
    margin-bottom: 40px;
    text-align: center;
}
.sidebar-radio {
    font-size: 30px;
    color: #2C3E50;
    margin-top: 20px;
    padding: 30px;
    background-color: #F8F9FA;
    border-radius: 30px;
    font-family: 'Arial', sans-serif;
}
.sidebar-radio:hover {
    background-color: #E8E9EB;
}
.streamlit-expanderHeader {
    font-size: 30px;
}
.streamlit-radio {
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# Main navigation layout
st.sidebar.markdown("<div class='sidebar-title'>Explore</div>", unsafe_allow_html=True)
option = st.sidebar.radio("", ["Project Introduction", "Chronic Disease","Community Health Analysis", "Street Health Analysis"], key="nav_option", index=0, format_func=lambda x: f' {x}')


# Create a container to hold the page content
page_container = st.empty()
page_style = """
    <style>
        h1 {
            font-size: 60px;
            color: #2C3E50;
            text-align: center; /* 修改为居中对齐 */
            font-weight: bold;
        }
        h2 {
            font-size: 36px;
            color: #34495E;
            text-align: left; /* 修改为左对齐 */
            font-weight: bold;
            margin-top: 30px;
        }
        p {
            font-size: 24px;
            line-height: 1.8;
            color: #2C3E50;
            text-align: left; /* 左对齐 */
        }
        ul {
            font-size: 30px; /* 调整列表字体为 30px */
            line-height: 2;
            color: #2C3E50;
        }
        ul li {
            font-size: 30px; /* 列表字体 */
            margin-bottom: 10px;
            color: #2C3E50;
        }
    </style>
"""

# 应用全局样式
with page_container.container():
    st.markdown(page_style, unsafe_allow_html=True)

    if option == "Project Introduction":
        # 主标题
        st.markdown("<h1>❤️ Urban Community Health Analysis Platform</h1>", unsafe_allow_html=True)

        # 第一段内容
        st.markdown(
            """
            <p>
            Welcome to our <strong>Urban Community Health Analysis Platform</strong>! 👵 This platform aims to empower urban planners and public health policymakers by analyzing the connections  the connections between urban community living environments and health outcomes among the elderly, fostering health-oriented urban development and improved quality of life.
            </p>
            """,
            unsafe_allow_html=True,
        )

        # 第二段内容（关于慢性病预测）
        st.markdown(
            """
            <h2>🔍 Chronic Disease Prediction Focus</h2>
            <p>
            Our platform focuses on the early detection and prediction of chronic diseases, particularly common among the elderly, such as:
            </p>
            <ul>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Mild Cognitive Impairment (MCI)</strong></li>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Hypertension</strong></li>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Diabetes</strong></li>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Major Depressive Disorder (MDD)</strong></li>
            </ul>
            <p>
            These conditions are closely linked to community environmental factors, including green space coverage, healthcare facility distribution, transportation convenience, and residents’ socioeconomic conditions. 
            </p>
            <p>
            The project employs a <strong>graph-based multi-modal representation learning framework</strong>, leveraging rich multi-modal information such as community photos, textual reviews, and surrounding points of interest to create neighborhood embeddings for chronic disease prevalence prediction. By incorporating contrastive learning and cross-modal modeling techniques, our platform achieves enhanced accuracy, improving baseline performance by <strong>28%</strong>. 🚀
            </p>
            """,
            unsafe_allow_html=True,
        )

        # 愿景部分
        st.markdown(
            """
            <h2>🌟 Our Vision</h2>

            <ul>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Helping users understand the health-oriented characteristics of urban environments.</strong></li>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Providing insights to identify the stage-wise progression of chronic diseases among the elderly.</strong></li>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>Promoting sustainable urban community development and better public health outcomes.</strong></li>
                <li style="font-size: 28px; color: #2C3E50; margin-bottom: 10px;"><strong>By selecting Beijing or Shanghai, you can explore specific neighborhood-level details to support health management in an aging society.</strong></li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
        # 默认加载北京市的地图展示
        city = "beijing"
        latitude, longitude = cities[city]["lat"], cities[city]["lon"]
        poi_df, residential_df, image_df = load_city_data(city, cities)



        if poi_df is not None and residential_df is not None:
            # 显示地图
            display_map(poi_df, residential_df, latitude, longitude)


       

    elif option == "Chronic Disease":
         # Disease selection
        disease = st.selectbox("Select a disease to view details:", list(disease_info.keys()))
        # Display disease description
        if disease:
            st.subheader(f"About {disease}")
            st.write(disease_info[disease]["description"])

            # Display Beijing file (if available)
            if disease_info[disease]["beijing_html"]:
                st.subheader("Beijing")
                html_file =  f"data/慢性病展示/{disease_info[disease]['beijing_html']}"
                with open(html_file, 'r', encoding='utf-8') as html_file1:
                    html_content1 = html_file1.read()
                components.html(html_content1, height=600, scrolling=True)
            else:
                st.error("Beijing HTML file not found!")

            # Display Shanghai file (if available)
            if disease_info[disease]["shanghai_html"]:
                st.subheader("Shanghai")
                html_file2 =  f"data/慢性病展示/{disease_info[disease]['shanghai_html']}"
                with open(html_file2, 'r', encoding='utf-8') as html_file2:
                    html_content2 = html_file2.read()
                components.html(html_content2, height=600, scrolling=True)
            else:
                st.error("Shanghai HTML file not found!")


    elif option == "Community Health Analysis":
        st.markdown("<h1>Community Health Analysis</h1>", unsafe_allow_html=True)
    

        # Define styles
        page_style = """
            <style>
                h2 {
                    font-size: 36px;
                    color: #34495E;
                    text-align: left;
                    font-weight: bold;
                    margin-top: 20px;
                }
                p {
                    font-size: 24px;
                    line-height: 1.8;
                    color: #2C3E50;
                    text-align: left;
                }
                ul {
                    font-size: 24px;
                    line-height: 1.8;
                    color: #2C3E50;
                    padding-left: 20px;
                }
                ul li {
                    margin-bottom: 10px;
                }
            </style>
        """

        # Apply styles
        st.markdown(page_style, unsafe_allow_html=True)
        # First paragraph
        st.markdown(
            """
            <p>
            For a given living circle in a city, we can calculate the cosine similarity between its embedding vector and the embedding vectors of all other regions in the city. Based on the similarity scores, neighborhoods are ranked, allowing for insightful comparisons.
            </p>
            """,
            unsafe_allow_html=True,
        )

        # Second paragraph
        st.markdown(
            """
            <p>
            The <strong>Community Comparison</strong> feature provides a detailed analysis of health embeddings between any two selected communities. Additionally, users can identify the communities with the most similar and least similar health embeddings to the chosen community.
            </p>
            <p>
            This empowers users to gain a comprehensive understanding of urban health dynamics, regional disparities, and environmental influences on community well-being, enabling them to make more informed decisions to foster healthier and more sustainable urban development.
            </p>
            """,
            unsafe_allow_html=True,
        )


        
        
        # 选择城市并加载对应的数据
        st.markdown("<p style='font-size: 24px;'>Select a city:</p>", unsafe_allow_html=True)
        city = st.selectbox("", list(cities.keys()), key="comparison_city")

        if city == "beijing":
            # 加载社区数据和相似度数据
            _, residential_df, image_df = load_city_data(city, cities)
            similarity_df = load_similarity_data(city, cities)

            if residential_df is not None and similarity_df is not None:
                st.markdown("<p style='font-size: 30px;'>Select one community:</p>", unsafe_allow_html=True)
                selected_residential_1 = st.selectbox("", options=residential_df['名称'].unique(), key="select_residential_1")
                st.markdown("<p style='font-size: 30px;'>Select other community:</p>", unsafe_allow_html=True)
                selected_residential_2 = st.selectbox("", options=residential_df['名称'].unique(), key="select_residential_2")

                if selected_residential_1 and selected_residential_2:
                    # 查找社区对应的ID
                    community_id_1 = residential_df[residential_df['名称'] == selected_residential_1].iloc[0]['ID']
                    community_id_2 = residential_df[residential_df['名称'] == selected_residential_2].iloc[0]['ID']

                    # 查找并展示相似度
                    comparison_results = calculate_similarity(similarity_df, community_id_1, community_id_2)
                    if comparison_results['similarity_value'] is not None:
                        st.markdown(f"""
                            <div style='margin-top: 30px;'>
                                <h3 style="color: #2C3E50; text-align: left; font-size: 30px; font-weight: bold;"><strong>Community Health Embedding Cosine Similarity:</strong></h3>
                                <h1 style="color: #4CAF50; text-align: left; font-size: 48px; margin: 0; font-weight: bold;"><strong>{comparison_results['similarity_value']:.4f}</strong></h1>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write("未找到选定社区对的相似度信息")

                    # 分两列展示两个社区的详细信息
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"#### {selected_residential_1}")
                        display_comparison_info(residential_df, image_df, selected_residential_1,comparison_results['most_similar_1'], comparison_results['least_similar_1'])

                    with col2:
                        st.write(f"#### {selected_residential_2}")
                        display_comparison_info(residential_df, image_df, selected_residential_2,comparison_results['most_similar_2'], comparison_results['least_similar_2'])
        else:
            # 检查是否有输入
            # 用户手动输入城市名称
            city = st.text_input("Please enter a city:")

            if city:
                st.write(f"Please upload your data for '{city}'.")

                # 提供文件上传窗口
                uploaded_file = st.file_uploader(f"", type=["csv", "xlsx", "txt"])

                # 检查是否有文件上传
                if uploaded_file:
                    st.write(f"File '{uploaded_file.name}' has been uploaded successfully.")
                else:
                    st.write("No file uploaded yet. Please upload your data file.")
            else:
                st.write("Awaiting input... Please enter a city above.")

        st.markdown(
                    """
                    <p style="font-size: 28px;">
                    The data used in this analysis is sourced from publicly available online platforms.
                    </p>
                    <div class="note-text" style="font-size: 25px; margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                        <strong>Data Sources:</strong>
                        <ol style="margin-top: 10px; font-size: 22px;">
                            <li><a href="https://bj.lianjia.com/" target="_blank">https://bj.lianjia.com/</a></li>
                            <li><a href="https://www.dianping.com/" target="_blank">https://www.dianping.com/</a></li>
                            <li><a href="https://www.meituan.com/" target="_blank">https://www.meituan.com/</a></li>
                            <li><a href="https://map.baidu.com/" target="_blank">https://map.baidu.com/</a></li>
                            <li><a href="https://hotels.ctrip.com/" target="_blank">https://hotels.ctrip.com/</a></li>
                            <li><a href="https://m.tujia.com/" target="_blank">https://m.tujia.com/</a></li>
                            <li><a href="https://www.elong.com/" target="_blank">https://www.elong.com/</a></li>
                        </ol>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    elif option == "Street Health Analysis":
        st.markdown("<h1>Street Health Analysis</h1>", unsafe_allow_html=True)

        # 选择城市并加载对应的数据
        st.markdown("<p style='font-size: 24px;'>Select a city:</p>", unsafe_allow_html=True)
        city = st.selectbox("", list(cities.keys()), key="comparison_city")

        # 当选择了北京市时，加载街道健康分析的地图 HTML
        if city == "beijing":
            html_file_path1 = f"data/{city}/{cities[city]['street_health_file1']}"
            html_file_path2 = f"data/{city}/{cities[city]['street_health_file2']}"

            st.markdown(f"## K-means clustering on the street embeddings in {city.capitalize()}(k=3)")
            with open(html_file_path1, 'r', encoding='utf-8') as html_file1:
                html_content1 = html_file1.read()
            components.html(html_content1, height=600, scrolling=True)

            st.markdown(f"## Distribution of the population aged 60 and above in {city.capitalize()}")
            with open(html_file_path2, 'r', encoding='utf-8') as html_file2:
                html_content2 = html_file2.read()
            components.html(html_content2, height=600, scrolling=True)



            st.markdown(
                """
                <p style="font-size: 28px;">
                We applied K-means clustering on the embeddings obtained from the proposed model and presented the distribution of the population aged 60 and above in Beijing. We observed certain similarities in the health representations and elderly population distributions between suburban and central urban areas at the spatial street level. However, through an analysis of Beijing’s municipal census data, we found that the aging problem is particularly severe in the city center. For example, in Dongcheng and Xicheng districts, the proportion of the population aged 60 and above has reached approximately 26%. These central urban communities urgently require the implementation of elderly-friendly facilities and supportive welfare policies for aging residents.
                </p>
                <div class="note-text" style="font-size: 25px; margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    <strong>Note:</strong> The red-bordered boundary highlights the Dongcheng and Xicheng districts, where a noticeable clustering pattern has emerged within the city's second ring road. These areas face significant challenges related to population aging, reflected in the high concentration of elderly residents.
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            # 检查是否有输入
            # 用户手动输入城市名称
            city = st.text_input("Please enter a city:")

            if city:
                st.write(f"Please upload your data for '{city}'.")

                # 提供文件上传窗口
                uploaded_file = st.file_uploader(f"", type=["csv", "xlsx", "txt"])

                # 检查是否有文件上传
                if uploaded_file:
                    st.write(f"File '{uploaded_file.name}' has been uploaded successfully.")
                else:
                    st.write("No file uploaded yet. Please upload your data file.")
            else:
                st.write("Awaiting input... Please enter a city above.")

          
