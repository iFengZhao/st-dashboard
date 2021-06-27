import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import RendererAgg
import base64
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

# some configuration
st.set_page_config(layout="wide")

plt.style.use('seaborn-pastel')

matplotlib.use("agg")
_lock = RendererAgg.lock


# some functions
def download_your_file(object_to_download, download_filename, download_link_text):
    """
    Generate a download button
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">' \
           f'<input type="button" value="Download your list"></a>'


def get_month_format(year, month, length):
    """
    Generate the date variable to use prophet
    """
    var_list = []
    count = 0
    while month <= 12:
        count += 1
        month += 1
        if month > 12:
            year += 1
            month = 1
        var = str(year) + '-' + str(month).zfill(2) + '-01'
        var_list.append(var)
        if count == length:
            break
    return var_list


def draw_pie_chart(x, subheader, label):
    """
    Draw bar chart using matplotlib
    """
    st.subheader(subheader)
    fig, ax = plt.subplots()
    ax.pie(x, labels=label, autopct="%.1f%%")
    ax.axis('equal')
    st.pyplot(fig)


def draw_histogram(df, subheader, xlabel, ylabel):
    """
    Draw histogram using matplotlib
    """
    st.subheader(subheader)
    fig, ax = plt.subplots()
    ax.hist(df)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)


def draw_bar_chart(x, y, subheader, xlabel, ylabel):
    """
    Draw bar chart using matplotlib
    """
    st.subheader(subheader)
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)


# get the data
@st.cache
def load_data(url):
    df = pd.read_csv(url)
    # Replace empty strings and some text
    df.Payor_Receiving_Fed_Benefits.replace(r'^\s*$', 'None', regex=True, inplace=True)
    df.Levy_Active.replace('Y', 'Yes', inplace=True)
    df.Levy_Active.replace(r'^\s*$', 'No', regex=True, inplace=True)
    df.LISAN_Action.replace(r'^\s*$', 'None', regex=True, inplace=True)
    df.Contempt_Action.replace(r'^\s*$', 'None', regex=True, inplace=True)
    return df


df = load_data('example_list.csv')

title_spacer1, title_1, title_spacer2 = st.beta_columns((1.2, 3, .1))

with title_1:
    st.title("Welcome to Px4C2 Dashboard!")

row0_spacer1, row0_1, row0_spacer2 = st.beta_columns((.15, 3.2, .15))

with row0_1:
    st.markdown("**To begin, please first select your office number, then choose your worker ID.**")

sb_space1, sb_1, sb_space2, sb_2, sb_space3 = st.beta_columns((.1, 1, .1, 1, .1))

with sb_1:
    office_list = sorted(list(df.Off.value_counts().index))
    office = st.selectbox("Office", office_list)
    df_office = df.loc[df.Off == office]
with sb_2:
    worker_list = list(df_office.Wrkr_ID.value_counts().index)
    worker = st.selectbox("Worker ID", worker_list)
    df_worker = df.loc[df.Wrkr_ID == worker]

st.sidebar.subheader("Which Dashboard?")
option = st.sidebar.selectbox("", ('Working on cases', 'Cases overview'), 1)

if option == 'Working on cases':

    data_spacer1, data_1, data_spacer2 = st.beta_columns((.15, 3.2, .15))

    with data_1:
        st.subheader('Your Contact List')
        filter_cases = st.multiselect('Filter your cases', ['Female payor', 'Past prisoner',
                                                            'Payor is receiving federal benefits',
                                                            'With contempt action'])
        filter_dict = {'Female payor': df_worker.PayorGender == 0,
                       'Past prisoner': df_worker.PayorPrsnPast == 1,
                       'Payor is receiving federal benefits': df_worker.Payor_Receiving_Fed_Benefits != 'None',
                       'With contempt action': df_worker.Contempt_Action != 'None'}

        for flt in filter_cases:
            df_worker = df_worker.loc[filter_dict[flt]]

        st.write(df_worker)

        tmp_download_link = download_your_file(df_worker, f'{worker}_contact_list.csv',
                                               'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
        st.markdown("**Enter the case number to get the case summary and the predicted payments in the next 6 months.**")
        case = st.text_input("")
        case_button = st.button("Get case summary")

        if case_button:
            df_case = df_worker[df_worker['Case_Number'] == int(case)]
            # Generate case summary
            if df_case.iloc[0]['Self_Emp']:
                st.markdown("**This payor is self-employed.**")
            if df_case.iloc[0]['PayorPrsnPast']:
                st.markdown("**This payor was in prison.**")
            if df_case.iloc[0]['Payor_Receiving_Fed_Benefits'] != 'None':
                st.markdown(f"**Type of federal benefits:** {df_case.iloc[0]['Payor_Receiving_Fed_Benefits']}")
            if df_case.iloc[0]['Contempt_Action'] != 'None':
                st.markdown(f"**Type of Contempt Action:** {df_case.iloc[0]['Contempt_Action']}")
            st.markdown(f"**Payor's monthly child support due amount is** ${df_case.iloc[0]['Month35_CSMSDue']}.")
            st.markdown(f"**The payor has paid** {round(df_case.iloc[0]['Mean_Paid_Percent'], 2) * 100}% "
                        f"**of the due amount in the past 24 months.**")
            st.markdown(f"**Payor's Payment Record:** {df_case.iloc[0]['PaymentRecord']} (0: Not Paid; 1: Paid)")

            months = get_month_format(2016, 3, 35)
            months = pd.DataFrame(months, columns=['ds'])
            monthly_payment = df_case.iloc[0][-35:].to_frame(name="y")
            df_monthly_payment = months.assign(y=df_case.iloc[0][-35:].values)
            # Draw case payment record history
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_monthly_payment['ds'], y=df_monthly_payment['y']))
            fig.layout.update(title_text='Payment History', xaxis_rangeslider_visible=True)
            fig.update_xaxes(title_text="Month")
            fig.update_yaxes(title_text="Payment ($)")
            st.plotly_chart(fig)

            m = Prophet(seasonality_mode='multiplicative')
            m.fit(df_monthly_payment)
            future = m.make_future_dataframe(periods=6, freq='MS')  # freq='MS' because it's monthly data
            forecast = m.predict(future)

            # Show and plot forecast
            st.subheader('Forecast data by Prophet')
            st.write(forecast.tail(6))

            st.write(f'Forecast plot for 6 months')
            fig1 = plot_plotly(m, forecast)
            st.plotly_chart(fig1)

            # Show trend and seasonality
            st.write("Forecast components")
            fig2 = m.plot_components(forecast)
            st.write(fig2)

if option == 'Cases overview':

    db_spacer1, db_1, db_spacer2 = st.beta_columns((.15, 3.2, .15))
    with db_1:
        st.subheader('Case overview')
        st.markdown(f"**You have** {len(df_worker)} **cases on your contact list.**")
        st.markdown("To work on specific cases, please choose from the left sidebar.")

    row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.beta_columns((.1, 1, .1, 1, .1))

    with row1_1, _lock:
        draw_pie_chart(list(df_worker.PayorGender.value_counts()),
                       "Payor's Gender",
                       ["Male", "Female"])

    with row1_2, _lock:
        draw_pie_chart(list(df_worker.Self_Emp.value_counts()),
                       "Payor Is Self-Employed",
                       ["No", "Yes"])

    row2_space1, row2_1, row2_space2, row2_2, row2_space3 = st.beta_columns((.1, 1, .1, 1, .1))

    with row2_1, _lock:
        draw_pie_chart(list(df_worker.PayorPrsnPast.value_counts()),
                       "Payor Was In Prison",
                       ["No", "Yes"])

    with row2_2, _lock:
        if len(df_worker.Levy_Active.value_counts()) == 1:
            labels = ["No"]
        else:
            labels = ["No", "Yes"]
        draw_pie_chart(list(df_worker.Levy_Active.value_counts()),
                       "Levy Is Active",
                       labels)

    row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.beta_columns((.1, 1, .1, 1, .1))

    with row3_1, _lock:
        draw_histogram(pd.to_numeric(df_worker.Payor_Current_Age, errors='coerce'),
                       "Payor's Age",
                       "Age",
                       "Count")

    with row3_2, _lock:
        draw_histogram(pd.to_numeric(df_worker.Case_Years_Open, errors='coerce'),
                       "# of Years In The System",
                       "Years",
                       "Count")

    row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.beta_columns((.1, 1, .1, 1, .1))

    with row4_1, _lock:
        draw_bar_chart(list(df_worker.Payor_Receiving_Fed_Benefits.value_counts().index),
                       list(df_worker.Payor_Receiving_Fed_Benefits.value_counts()),
                       "Payor Is Receiving Federal Benefits",
                       "Federal Benefit",
                       "Count")

    with row4_2, _lock:
        draw_bar_chart(list(df_worker.Contempt_Action.value_counts().index),
                       list(df_worker.Contempt_Action.value_counts()),
                       "Contempt Actions",
                       "Contempt Action",
                       "Count")

    row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.beta_columns((.1, 1, .1, 1, .1))

    with row5_1, _lock:
        draw_bar_chart(list(df_worker.AcctType.value_counts().index),
                       list(df_worker.AcctType.value_counts()),
                       "Account Types",
                       "Account Type",
                       "Count")

    with row5_2, _lock:
        draw_bar_chart(list(df_worker.LISAN_Action.value_counts().index),
                       list(df_worker.LISAN_Action.value_counts()),
                       "Type Of LISAN Actions",
                       "LISAN Action",
                       "Count")
