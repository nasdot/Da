import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("Backup.csv")

# Page layout
st.set_page_config(layout="wide")

# Split into two columns: 1/4 and 3/4
col1, col2 = st.columns([1, 3])

# --- Left side: Raw Data ---
with col1:
    st.subheader("Raw Data (first 10 rows)")
    st.dataframe(df, height=400)

# --- Right side: Interactive Dashboard ---
with col2:
    st.subheader("Choose Objective")
    objective = st.selectbox(
        "Select an objective:",
        [
            "Objective 1: Social Media & Mental Health",
            "Objective 2: Lifestyle & Academic Performance",
            "Objective 3: Demographics & Social Interaction"
        ]
    )

    # Objective 1
    if objective.startswith("Objective 1"):
        st.write("### Social Media & Mental Health")

        gender_filter = st.multiselect(
            "Filter by Gender",
            df["Gender"].unique(),
            default=df["Gender"].unique()
        )
        filtered_df = df[df["Gender"].isin(gender_filter)]

        metrics = ["Stress Level", "Anxiety Level", "Addiction Level", "Depression Label"]
        colA, colB = st.columns(2)

        for i, metric in enumerate(metrics):
            avg_metric = filtered_df.groupby("Platform Usage")[metric].mean().reset_index()
            fig = px.bar(
                avg_metric,
                x="Platform Usage",
                y=metric,
                title=f"{metric} by Platform",
                text=metric,
                color="Platform Usage"
            )
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            if i % 2 == 0:
                colA.plotly_chart(fig, use_container_width=True)
            else:
                colB.plotly_chart(fig, use_container_width=True)

    # Objective 2
    elif objective.startswith("Objective 2"):
        st.write("### Lifestyle & Academic Performance")

        df["Sleep Group"] = pd.cut(df["Sleep Hours"], bins=[0, 5, 7, 9],
                                   labels=["Low Sleep", "Medium Sleep", "High Sleep"])
        avg_sleep = df.groupby("Sleep Group")["Academic Performance"].mean().reset_index()
        fig1 = px.bar(avg_sleep, x="Sleep Group", y="Academic Performance",
                      title="Sleep vs Academic Performance", text="Academic Performance")
        fig1.update_traces(texttemplate="%{text:.2f}", textposition="outside")

        df["Screen Group"] = pd.cut(df["Screen Time Before Sleep"], bins=[0, 1, 2, 3],
                                    labels=["Low Screen", "Medium Screen", "High Screen"])
        avg_screen = df.groupby("Screen Group")["Academic Performance"].mean().reset_index()
        fig2 = px.bar(avg_screen, x="Screen Group", y="Academic Performance",
                      title="Screen Time vs Academic Performance", text="Academic Performance")
        fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")

        df["Activity Group"] = pd.cut(df["Physical Activity"], bins=[0, 1, 2, 3],
                                      labels=["Low Activity", "Medium Activity", "High Activity"])
        avg_activity = df.groupby("Activity Group")["Academic Performance"].mean().reset_index()
        fig3 = px.bar(avg_activity, x="Activity Group", y="Academic Performance",
                      title="Activity vs Academic Performance", text="Academic Performance")
        fig3.update_traces(texttemplate="%{text:.2f}", textposition="outside")

        for fig in [fig1, fig2, fig3]:
            st.plotly_chart(fig, use_container_width=True)

    # Objective 3
    elif objective.startswith("Objective 3"):
        st.write("### Demographics & Social Interaction")

        df["Age Group"] = pd.cut(df["Age"], bins=[12, 15, 17, 19],
                                 labels=["13-15", "16-17", "18-19"])
        interaction_map = {"low": 1, "medium": 2, "high": 3}
        df["Social Interaction Score"] = df["Social Interaction Level"].map(interaction_map)

        avg_media_usage = df.groupby("Age Group")["Daily Social Media Hours"].mean().reset_index()
        fig1 = px.bar(avg_media_usage, x="Age Group", y="Daily Social Media Hours",
                      title="Media Usage by Age Group", text="Daily Social Media Hours")
        fig1.update_traces(texttemplate="%{text:.2f}", textposition="outside")

        avg_age_interaction = df.groupby("Age Group")["Social Interaction Score"].mean().reset_index()
        fig2 = px.bar(avg_age_interaction, x="Age Group", y="Social Interaction Score",
                      title="Social Interaction by Age Group", text="Social Interaction Score")
        fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")

        avg_gender = df.groupby("Gender")["Social Interaction Score"].mean().reset_index()
        fig3 = px.bar(avg_gender, x="Gender", y="Social Interaction Score",
                      title="Social Interaction by Gender", text="Social Interaction Score")
        fig3.update_traces(texttemplate="%{text:.2f}", textposition="outside")

        for fig in [fig1, fig2, fig3]:
            st.plotly_chart(fig, use_container_width=True)
