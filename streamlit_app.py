import math
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="GDP 데이터 스튜디오",
    page_icon=":earth_americas:",
    layout="wide",
)


@st.cache_data
def get_gdp_data():
    """Load and reshape the World Bank GDP dataset."""
    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    groups = ["그룹 A", "그룹 B", "그룹 C", "그룹 D"]
    rows = []
    for month, sample_date in enumerate(dates, start=1):
        for group_index, group in enumerate(groups):
            rows.append(
                {
                    "날짜": sample_date,
                    "그룹": group,
                    "측정값": 80 + month * 7 + group_index * 13 + (month * group_index * 5) % 17,
                    "수량": 20 + month * 3 + group_index * 8,
                    "만족도": round(3 + ((month + group_index) % 20) / 10, 1),
                }
            )
    return pd.DataFrame(rows)
    raw_gdp_df = pd.read_csv(data_filename)
    year_columns = [str(year) for year in range(1960, 2023)]
    gdp_df = raw_gdp_df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_columns,
        var_name="Year",
        value_name="GDP",
    )
    gdp_df["Year"] = pd.to_numeric(gdp_df["Year"])
    gdp_df["GDP"] = pd.to_numeric(gdp_df["GDP"], errors="coerce")
    return gdp_df


    sample_df = get_sample_data()
min_year = int(gdp_df["Year"].min())
max_year = int(gdp_df["Year"].max())
country_options = (
    sample_df["그룹"].unique().tolist()
    .drop_duplicates()
    .sort_values("Country Name")
)
country_labels = dict(zip(country_options["Country Code"], country_options["Country Name"]))
country_codes = country_options["Country Code"].tolist()
favorite_codes = ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"]
default_codes = [code for code in favorite_codes if code in country_codes]


st.title(":earth_americas: GDP 데이터 스튜디오")
st.title(":material/widgets: Streamlit 요소 갤러리")
st.caption("World Bank 공개 데이터로 살펴보는 경제 지표와 Streamlit 인터페이스 요소")
st.caption("입력 위젯, 레이아웃, 차트, 데이터 표시와 상호작용을 한 페이지에서 살펴봅니다.")
st.divider()

with st.sidebar:
    st.header("분석 조건")
        st.header("샘플 데이터 필터")
        selected_groups = st.multiselect("그룹", group_options, default=group_options)
        from datetime import date

        import pandas as pd
        import streamlit as st


        st.set_page_config(
            page_title="Streamlit 요소 갤러리",
            page_icon=":material/widgets:",
            layout="wide",
        )


        @st.cache_data
        def get_sample_data():
            dates = pd.date_range("2025-01-01", periods=12, freq="MS")
            groups = ["그룹 A", "그룹 B", "그룹 C", "그룹 D"]
            rows = []
            for month, sample_date in enumerate(dates, start=1):
                for group_index, group in enumerate(groups):
                    rows.append(
                        {
                            "날짜": sample_date,
                            "그룹": group,
                            "측정값": 80 + month * 7 + group_index * 13 + (month * group_index * 5) % 17,
                            "수량": 20 + month * 3 + group_index * 8,
                            "만족도": round(3 + ((month + group_index) % 20) / 10, 1),
                        }
                    )
            return pd.DataFrame(rows)


        sample_df = get_sample_data()
        group_options = sample_df["그룹"].unique().tolist()
        metric_options = ["측정값", "수량", "만족도"]

        st.title(":material/widgets: Streamlit 요소 갤러리")
        st.caption("입력 위젯, 레이아웃, 차트, 데이터 표시와 상호작용을 한 페이지에서 살펴봅니다.")
        st.divider()

        with st.sidebar:
            st.header("샘플 데이터 필터")
            selected_groups = st.multiselect("그룹", group_options, default=group_options)
            month_range = st.slider("월 범위", 1, 12, (1, 12))
            selected_metric = st.selectbox("표시할 지표", metric_options)
            st.caption("모든 차트와 표에는 페이지 안에서 생성한 예시 데이터가 사용됩니다.")

        filtered_df = sample_df[
            sample_df["그룹"].isin(selected_groups)
            & sample_df["날짜"].dt.month.between(month_range[0], month_range[1])
        ].copy()

        overview_tab, data_tab, widgets_tab, interaction_tab = st.tabs(
            ["요약", "데이터와 차트", "위젯", "상호작용"]
        )

        with overview_tab:
            st.subheader("요약 지표")
            if filtered_df.empty:
                st.warning("선택한 조건에 맞는 데이터가 없습니다. 필터를 조정해 보세요.")
            else:
                latest_date = filtered_df["날짜"].max()
                latest_rows = filtered_df[filtered_df["날짜"] == latest_date]
                metric_columns = st.columns(4)
                metric_columns[0].metric("선택 그룹", f"{filtered_df['그룹'].nunique()}개")
                metric_columns[1].metric("데이터 행", f"{len(filtered_df):,}개")
                metric_columns[2].metric("최근 측정값 합계", f"{latest_rows[selected_metric].sum():,.1f}")
                metric_columns[3].metric("만족도 평균", f"{filtered_df['만족도'].mean():.1f}점", delta="샘플")

                st.subheader(f"월별 {selected_metric} 변화")
                st.line_chart(filtered_df, x="날짜", y=selected_metric, color="그룹")

                with st.expander("요약 설명 보기"):
                    st.write(
                        f"현재 {len(selected_groups)}개 그룹과 "
                        f"{month_range[0]}~{month_range[1]}월 데이터가 선택되어 있습니다."
                    )
                    st.caption("사이드바 필터를 바꾸면 요약 지표와 차트가 함께 갱신됩니다.")

        with data_tab:
            st.subheader("표와 차트")
            if filtered_df.empty:
                st.info("표시할 데이터가 없습니다.")
            else:
                chart_column, table_column = st.columns([1, 1.5])
                with chart_column:
                    st.markdown("##### 그룹별 합계")
                    group_totals = filtered_df.groupby("그룹", as_index=False)[selected_metric].sum()
                    st.bar_chart(group_totals, x="그룹", y=selected_metric, color="#167D78")
                    st.markdown("##### 지표 관계")
                    st.scatter_chart(filtered_df, x="수량", y="만족도", color="그룹", size="측정값")
                with table_column:
                    st.markdown("##### 편집 가능한 데이터")
                    edited_df = st.data_editor(
                        filtered_df,
                        hide_index=True,
                        width="stretch",
                        num_rows="dynamic",
                    )
                    st.caption(f"편집기에서 현재 {len(edited_df)}개 행을 표시합니다.")

                st.markdown("##### 영역 차트")
                st.area_chart(filtered_df, x="날짜", y=selected_metric, color="그룹")
                csv_data = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "CSV 다운로드",
                    data=csv_data,
                    file_name="sample_data.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

        with widgets_tab:
            st.subheader("입력 위젯")
            st.caption("컨트롤을 바꾸면 아래 미리보기에 반영됩니다.")
            left_column, right_column = st.columns(2)
            with left_column:
                preview_group = st.selectbox("selectbox · 그룹", group_options)
                preview_style = st.radio("radio · 표시 방식", ["선", "막대", "영역"], horizontal=True)
                show_table = st.checkbox("checkbox · 값 표 표시", value=True)
                preview_month = st.select_slider("select_slider · 마지막 월", options=list(range(1, 13)), value=12)
                minimum_value = st.number_input("number_input · 최소 측정값", min_value=0, value=0, step=10)
                search_text = st.text_input("text_input · 그룹 검색", placeholder="그룹 이름")
            with right_column:
                accent_color = st.color_picker("color_picker · 강조 색상", "#167D78")
                selected_date = st.date_input("date_input · 날짜 선택", value=date.today())
                note = st.text_area("text_area · 메모", placeholder="메모를 입력하세요")
                show_details = st.toggle("toggle · 상세 정보 표시", value=True)
                progress_value = st.slider("slider · 진행률", 0, 100, 65)
                st.progress(progress_value, text=f"진행률 {progress_value}%")

            preview_df = sample_df[
                (sample_df["그룹"] == preview_group)
                & (sample_df["날짜"].dt.month <= preview_month)
                & (sample_df["측정값"] >= minimum_value)
            ]
            st.markdown(f"##### {preview_group} 미리보기")
            preview_chart = {"선": st.line_chart, "막대": st.bar_chart, "영역": st.area_chart}[preview_style]
            preview_chart(preview_df, x="날짜", y="측정값", color=accent_color)

            if show_details:
                st.caption(f"선택 날짜: {selected_date:%Y-%m-%d} · 메모 글자 수: {len(note)}")
            if search_text:
                matching_groups = [group for group in group_options if search_text.casefold() in group.casefold()]
                st.write("검색 결과:", matching_groups or "일치하는 그룹이 없습니다.")
            if show_table:
                st.dataframe(preview_df, hide_index=True, width="stretch")
            rating = st.feedback("stars", key="sample_rating")
            if rating is not None:
                st.success(f"별점 {rating + 1}점을 선택했습니다.")

        with interaction_tab:
            st.subheader("폼, 업로드와 대화")
            form_column, upload_column = st.columns(2)
            with form_column:
                with st.form("sample_form"):
                    st.markdown("##### form · 응답 남기기")
                    response_type = st.selectbox("응답 종류", ["의견", "질문", "요청"])
                    response_text = st.text_input("내용", placeholder="내용을 입력하세요")
                    importance = st.slider("중요도", 1, 5, 3)
                    submitted = st.form_submit_button("제출", type="primary")
                if submitted:
                    if response_text.strip():
                        st.success(f"{response_type}을 받았습니다. 중요도: {importance}/5")
                    else:
                        st.warning("제출 전에 내용을 입력해 주세요.")

                uploaded_file = st.file_uploader("file_uploader · CSV 미리보기", type=["csv"])
                if uploaded_file is not None:
                    try:
                        uploaded_df = pd.read_csv(uploaded_file)
                        st.dataframe(uploaded_df.head(20), hide_index=True, width="stretch")
                    except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
                        st.error(f"CSV 파일을 읽을 수 없습니다: {error}")

            with upload_column:
                st.markdown("##### 버튼과 링크")
                if st.button("toast 알림 보기", icon=":material/notifications:"):
                    st.toast("버튼 클릭 이벤트가 실행됐습니다.", icon=":material/check:")
                st.link_button("Streamlit 문서 열기", "https://docs.streamlit.io/", icon=":material/open_in_new:")
                with st.popover("popover · 추가 설정"):
                    st.checkbox("알림 받기", value=True)
                    st.selectbox("표시 밀도", ["편안하게", "간결하게"])

                with st.status("status · 예시 처리 완료", state="complete", expanded=False):
                    st.write("상태 컨테이너 안에 진행 상황이나 결과를 표시할 수 있습니다.")

                with st.expander("메시지, 코드와 JSON"):
                    st.success("success · 완료 메시지")
                    st.info("info · 안내 메시지")
                    st.warning("warning · 주의 메시지")
                    st.error("error · 오류 메시지 예시")
                    st.code('st.metric("측정값", "128", delta="8%")', language="python")
                    st.json({"상태": "완료", "항목": ["차트", "표", "위젯"]})

            st.markdown("##### chat · 대화형 입력")
            if "chat_messages" not in st.session_state:
                st.session_state.chat_messages = [
                    {"role": "assistant", "content": "안녕하세요. 메시지를 입력하면 이곳에 대화가 표시됩니다."}
                ]
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            prompt = st.chat_input("메시지를 입력하세요")
            if prompt:
                st.session_state.chat_messages.append({"role": "user", "content": prompt})
                reply = f"메시지를 받았습니다: {prompt}"
                st.session_state.chat_messages.append({"role": "assistant", "content": reply})
                with st.chat_message("user"):
                    st.write(prompt)
                with st.chat_message("assistant"):
                    st.write(reply)