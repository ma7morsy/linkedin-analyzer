import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="محلل شبكة LinkedIn", layout="wide")

st.title("📊 محلل شبكة علاقات LinkedIn")
st.write("قم برفع ملف `Connections.csv` المستخرج من حسابك لتحليل بيانات شبكتك بسهولة.")

uploaded_file = st.file_uploader("اختر ملف Connections.csv", type=["csv"])

if uploaded_file is not None:
    try:
        # تخطي أول سطرين لأن LinkedIn يضع تنبيهات في بداية الملف
        df = pd.read_csv(uploaded_file, skiprows=2)
        df.columns = df.columns.str.strip()

        # إحصائيات سريعة
        c1, c2, c3 = st.columns(3)
        c1.metric("إجمالي العلاقات", len(df))
        c2.metric("عدد الشركات", df['Company'].nunique() if 'Company' in df.columns else 0)
        c3.metric("المسميات الوظيفية", df['Position'].nunique() if 'Position' in df.columns else 0)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏢 أكثر 10 شركات تكراراً")
            if 'Company' in df.columns:
                top_comp = df['Company'].value_counts().head(10).reset_index()
                top_comp.columns = ['الشركة', 'العدد']
                fig1 = px.bar(top_comp, x='العدد', y='الشركة', orientation='h', color='العدد')
                fig1.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader("💼 أكثر 10 مسميات وظيفية")
            if 'Position' in df.columns:
                top_pos = df['Position'].value_counts().head(10).reset_index()
                top_pos.columns = ['المسمى الوظيفي', 'العدد']
                fig2 = px.bar(top_pos, x='العدد', y='المسمى الوظيفي', orientation='h', color='العدد')
                fig2.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig2, use_container_width=True)

        # رسم بياني لنمو العلاقات
        if 'Connected On' in df.columns:
            st.subheader("📈 نمو شبكة العلاقات عبر الزمن")
            df['Connected On'] = pd.to_datetime(df['Connected On'], errors='coerce')
            df_time = df.dropna(subset=['Connected On']).sort_values('Connected On')
            df_time['Cumulative'] = range(1, len(df_time) + 1)
            
            fig3 = px.line(df_time, x='Connected On', y='Cumulative', title="تراكم العلاقات")
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف، تأكد من رفع ملف Connections.csv الصحيح. التفاصيل: {e}")
